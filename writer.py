#############
# TOPIC 14 : Table Formats and the Lakehouse
#
# writer.py
#
# 302.2-Data infrastructure
# @ Gaetan Veuillet
#
# Appends day 2, one file at a time.
#############

import time
from common import FILES_PER_DAY, DELAY, write_file

for part in range(1, FILES_PER_DAY + 1):
    write_file(day=2, part=part)
    print(f"[writer] day 2: file {part}/{FILES_PER_DAY} written")
    time.sleep(DELAY)

print("[writer] day 2 complete")