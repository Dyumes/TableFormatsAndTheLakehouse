#############
# TOPIC 14 : Table Formats and the Lakehouse
#
# writer.py
#
# 302.2-Data infrastructure
# @ Gaetan Veuillet
#
# Appends one new day, one file at a time.
#############

import glob
import os
import time
from common import FOLDER, FILES_PER_DAY, DELAY, write_file


filter = glob.glob(f"{FOLDER}/day*_part*.parquet")
existing_d = {int(os.path.basename(f).split("_")[0][3:]) for f in filter}

new_d = max(existing_d) + 1 if existing_d else 1

print(f"[writer] Starts append of day {new_d} (nbr files : {FILES_PER_DAY}, delay : {DELAY}s)")

for part in range(1, FILES_PER_DAY + 1):
    write_file(day=2, part=part)
    print(f"[writer] day 2: file {part}/{FILES_PER_DAY} written")
    time.sleep(DELAY)

print(f"[writer] day {new_d} complete")