#############
# TOPIC 14 : Table Formats and the Lakehouse
#
# iceberg/writer.py
#
# 302.2-Data infrastructure
# @ Gaetan Veuillet
#
# Appends one new day, one file at a time.
# Last step -> once all files are written -> one commit adds them 
# to the table at once.
#############

import glob
import os
import time
from common import FOLDER, TABLE_NAME, FILES_PER_DAY, DELAY, write_file, get_catalog

table = get_catalog().load_table(TABLE_NAME)

#In this case, new day is the one after the last day already in the table
existing_d = table.scan(selected_fields=("day",)).to_pandas()["day"]
new_d = int(existing_d.max()) + 1 if len(existing_d) else 1

print(f"[writer] Starts append of day {new_d} (nbr files : {FILES_PER_DAY}, delay : {DELAY}s)")

files = []
for part in range(1, FILES_PER_DAY + 1):
    files.append(write_file(new_d, part=part))
    print(f"[writer] day {new_d}: file {part}/{FILES_PER_DAY} written (on disk, NOT in the table yet)")
    time.sleep(DELAY)

print(f"[writer] day {new_d} complete")

#The commit : writes the new metadata (manifest, manifest list, metadata file)
#and then switch the catalog pointer to it, in one anotmic step
table.add_files(files)
print(f"[writer] COMMIT: day {new_d} added to the table in one step")
print(f"(new snapshot {table.current_snapshot().snapshot_id})")


files_now = glob.glob(f"{FOLDER}/*.parquet")
files_in_table = len(table.inspect.files())
print(f"\n[writer] folder when writer.py finished: {len(files_now)} files ON DISK\n{files_in_table} files in the table")