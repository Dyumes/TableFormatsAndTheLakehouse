#############
# TOPIC 14 : Table Formats and the Lakehouse
#
# setup.py
#
# 302.2-Data infrastructure
# @ Gaetan Veuillet
#
# Deletes data/ and writes day 1 (FILES_PER_DAY nbr of files).
#############

import os
import shutil
from common import DAYS, FOLDER, FILES_PER_DAY, ROWS_PER_FILE, DELAY, write_file

#Clean up the folder
shutil.rmtree("data", ignore_errors=True)
os.makedirs(FOLDER)

for day in range(1, DAYS + 1):
    for part in range(1, FILES_PER_DAY + 1):
        write_file(day=1, part=part)

print(f"[setup] data cleaned\n[setup] day 1 written ({FILES_PER_DAY} files)")