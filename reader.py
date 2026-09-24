#############
# TOPIC 14 : Table Formats and the Lakehouse
#
# reader.py
#
# 302.2-Data infrastructure
# @ Gaetan Veuillet
#
# Lists the folder, reads every file found, prints revenue per day.
#############

import glob
import pandas as pd
import os
from common import FOLDER, FILES_PER_DAY

#For now, no table format: listing the folder is the only way 
#to find the data
print(f"--STEP 1: NO TABLE FORMAT -> LISTING THE FOLDER TO FIND DATA")
files = glob.glob(f"{FOLDER}/*.parquet")
print(f"[reader] found {len(files)} files")


print(f"--STEP 2: READING THE FILES AND AGGREGATING REVENUE PER DAY")
df = pd.concat([pd.read_parquet(f) for f in files])

revenue = df.groupby("day")["amount"].sum()
incomplete = []
for day, total in revenue.items():
      nbr_files = sum(1 for f in files if os.path.basename(f).startswith(f"day{day}_"))
      status = "COMPLETE" if nbr_files == FILES_PER_DAY else "INCOMPLETE"
      if nbr_files != FILES_PER_DAY:
            incomplete.append((day, nbr_files, total))
      print(f"[reader] day {day}: {total} CHF ", f"({nbr_files}/{FILES_PER_DAY} files) -> {status}")

files_now = glob.glob(f"{FOLDER}/*.parquet")
print(f"\n[reader] folder when reader.py finished: {len(files_now)} files")


