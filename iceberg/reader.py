#############
# TOPIC 14 : Table Formats and the Lakehouse
#
# iceberg/reader.py
#
# 302.2-Data infrastructure
# @ Gaetan Veuillet
#
# Lists the folder, reads every file found, prints revenue per day.
#############

import glob
import pandas as pd
import os
from common import TABLE_NAME, FOLDER, FILES_PER_DAY, get_catalog

#For now, no table format: listing the folder is the only way 
#to find the data
print(f"--STEP 1: ICEBERG -> ASKING THE CATALOG FOR THE CURRENT SNAPSHOT")
table = get_catalog().load_table(TABLE_NAME)
snapshot = table.current_snapshot()
files = table.inspect.files(snapshot.snapshot_id)["file_path"].to_pylist()
files_on_disk = glob.glob(f"{FOLDER}/*.parquet")
print(f"[reader] snapshot {snapshot.snapshot_id}: {len(files)} files")
print(f"({len(files_on_disk)} files on disk right now)")


print(f"--STEP 2: READING THE FILES AND AGGREGATING REVENUE PER DAY")
df = table.scan(snapshot_id=snapshot.snapshot_id).to_pandas()

revenue = df.groupby("day")["amount"].sum()

for day, total in revenue.items():
      nbr_files = sum(1 for f in files if os.path.basename(f).startswith(f"day{day}_"))
      status = "COMPLETE" if nbr_files == FILES_PER_DAY else "INCOMPLETE"
      print(f"[reader] day {day}: {total} CHF ", f"({nbr_files}/{FILES_PER_DAY} files) -> {status}")

latest = get_catalog().load_table(TABLE_NAME).current_snapshot()

print(f"[reader] snapshot read by reader.py : {snapshot.snapshot_id}")
print(f"[reader] current snapshot now : {latest.snapshot_id}")

if len(files_on_disk) > len(files):
      print(f"[reader] {len(files_on_disk) - len(files)} files on disk were ignored: not in any committed snapshot yet")


