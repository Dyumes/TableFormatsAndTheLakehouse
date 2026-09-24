#############
# TOPIC 14 : Table Formats and the Lakehouse
#
# iceberg/setup.py
#
# 302.2-Data infrastructure
# @ Gaetan Veuillet
#
# Deletes data/ and writes day 1 (FILES_PER_DAY nbr of files).
#############

import os
import shutil
from common import TABLE_NAME, SCHEMA, TABLE_DIR, WAREHOUSE, DAYS, FOLDER, FILES_PER_DAY, ROWS_PER_FILE, DELAY, write_file, get_catalog

#Clean up the folder
shutil.rmtree(WAREHOUSE, ignore_errors=True)
os.makedirs(FOLDER)

#Create table -> write first metadata file and registers it in the catalog
catalog = get_catalog()
catalog.create_namespace("demo")
table = catalog.create_table(TABLE_NAME, SCHEMA, str(TABLE_DIR))


for day in range(1, DAYS + 1):
    files = [write_file(day=day, part=part) for part in range(1, FILES_PER_DAY + 1)]
    table.add_files(files)

print(f"[setup] data/iceberg cleaned, table {TABLE_NAME} created\n[setup] day 1 written ({FILES_PER_DAY} files, 1 commit)")