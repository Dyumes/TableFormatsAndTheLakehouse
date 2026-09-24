#############
# TOPIC 14 : Table Formats and the Lakehouse
#
# setup.py
#
# 302.2-Data infrastructure
# @ Gaetan Veuillet
#
# Deletes data/ and writes day 1 (10 files).
#############

import os
import shutil
from common import FOLDER, FILES_PER_DAY, write_file

#Clean up the folder and write day 1 (10 files)
shutil.rmtree("data", ignore_errors=True)
os.makedirs(FOLDER)

for part in range(1, FILES_PER_DAY + 1):
    write_file(day=1, part=part)

print(f"[setup] day 1 written ({FILES_PER_DAY} files)")