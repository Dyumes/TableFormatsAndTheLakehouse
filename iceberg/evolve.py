#############
# TOPIC 14 : Table Formats and the Lakehouse
#
# iceberg/evolve.py
#
# 302.2-Data infrastructure
# @ Gaetan Veuillet
#
# Adds a column "currency" to the table, then appends one new days that has it
# Old files are not rewritten
# Re-run reader.py unchanged -> still works
#############

import pyarrow as pa
import pyarrow.parquet as pq
import pandas as pd
from pyiceberg.types import StringType
from common import FOLDER, TABLE_NAME, FILES_PER_DAY, ROWS_PER_FILE, AMOUNT, get_catalog

table = get_catalog().load_table(TABLE_NAME)
old_snapshot = table.current_snapshot().snapshot_id

def show_schema(title):
    columns = ", ".join(f"{f.name} (id {f.field_id})" for f in table.schema().fields)
    print(f"[evolve] schema {title}: {columns}")

print("--STEP 1: ADDING A COLUMN (metadata only, no data file is rewritten)")
show_schema("before")
with table.update_schema() as update:
    update.add_column("currency", StringType())
    
show_schema("after")
print("[evolve] existing columns keep their id, the new one gets a new id")

print("--STEP 2: APPENDING A NEW DAY THAT HAS THE NEW COLUMN")
existing_d = table.scan(selected_fields=("day",)).to_pandas()["day"]
new_d = int(existing_d.max()) + 1
files = []
for part in range(1, FILES_PER_DAY + 1):
    new_table = pa.table({
        "day": [new_d] * ROWS_PER_FILE,
        "amount": [AMOUNT] * ROWS_PER_FILE,
        "currency": ["CHF"] * ROWS_PER_FILE,
    })
    filename = f"{FOLDER}/day{new_d}_part{part}.parquet"
    pq.write_table(new_table, filename)
    files.append(filename)
table.add_files(files)
print(f"[evolve] day {new_d} committed ({FILES_PER_DAY} files with a currency column)")
 
print("--STEP 3: A NEW QUERY THAT USES THE NEW COLUMN")
df = table.scan(selected_fields=("day", "currency")).to_pandas()
per_day = df.groupby("day")["currency"].first()
for day, cur in per_day.items():
    shown = cur if pd.notna(cur) else "null (file written before the column existed)"
    print(f"[evolve] day {day}: currency = {shown}")
 
print("--STEP 4: AN OLD SNAPSHOT IS STILL READABLE WITH ITS OLD SCHEMA")
old = table.scan(snapshot_id=old_snapshot).to_pandas()
print(f"[evolve] snapshot {old_snapshot} (before the change): "
      f"columns {list(old.columns)}, {len(old):_} rows")
 