#############
# TOPIC 14 : Table Formats and the Lakehouse
#
# iceberg/inspect_table
#
# 302.2-Data infrastructure
# @ Gaetan Veuillet
#
# Follow the same path a reader follows, and prints each level :
# catalog -> metadata file -> snapshot -> manifest list -> manifests -> data files
# Run it after setup.py, and again after writer.py, to see what a commit adds
#############

import json
import os
import sqlite3
from common import WAREHOUSE, TABLE_NAME, get_catalog

name = lambda path: os.path.basename(path)

#The catalog -> one row per table, holding a pointer to the current metadata file
con = sqlite3.connect(WAREHOUSE/"catalog.db")
pointer = con.execute(
    "SELECT metadata_location FROM iceberg_tables WHERE table_name = 'sales'"
).fetchone()[0]
con.close
print(f"CATALOG (catalog.db)\n\t{TABLE_NAME} -> {name(pointer)}")

#The metadata file -> schema, and the list of every snapshot
table = get_catalog().load_table(TABLE_NAME)
with open(pointer.replace("file://", "")) as f:
    meta = json.load(f)
print(f"METADATA FILE ({name(pointer)})")
print(f"\tschema: " + ", ".join(
    f"{c['name']} (id {c['id']})" for c in meta["schemas"][-1]["fields"]))
print(f"\tsnapshots: {len(meta['snapshots'])}, current = {meta['current-snapshot-id']}")

#Each snapshot points to its own manifest list
print("SNAPSHOTS -> MANIFEST LISTS")
for snap in meta["snapshots"]:
    mark = "<- current" if snap["snapshot-id"] == meta["current-snapshot-id"] else ""
    print(f"\tsnapshot {snap['snapshot-id']} -> {name(snap["manifest-list"])}{mark}")

#Current manifest list points to manifests, each listing data files
print("CURRENT SNAPSHOT: MANIFESTS -> DATA FILES")
manifests = table.inspect.manifests()
files = table.inspect.files()["file_path"].to_pylist()
for m in manifests.to_pylist():
    print(f"\tmanifest {name(m['path'])}: {m['added_data_files_count']} data files")
print(f"\tdata files in the table : {len(files)}")
for day in sorted({name(f).split("_")[0] for f in files}):
    n = sum(1 for f in files if name(f).startswith(day + "_"))
    print(f"\t\t{day}:{n} files ({day}_part1.parquet ... {day}_part{n}.parquet)")

pretty_dir = WAREHOUSE / "pretty"
pretty_dir.mkdir(exist_ok=True)
pretty_path = pretty_dir / name(pointer)
with open(pretty_path, "w") as f:
    json.dump(meta, f, indent=2)
print(f"\n5. Readable copy of the current metadata file: {pretty_path}")