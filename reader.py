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
from common import FOLDER

#For now, no table format: listing the folder is the only way 
#to find the data
files = glob.glob(f"{FOLDER}/*.parquet")
print(f"[reader] found {len(files)} files")



df = pd.concat([pd.read_parquet(f) for f in files])

revenue = df.groupby("day")["amount"].sum()
for day, total in revenue.items():
    print(f"[reader] day {day}: {total:_.0f} CHF")