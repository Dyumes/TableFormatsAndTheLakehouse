#############
# TOPIC 14 : Table Formats and the Lakehouse
#
# common.py
#
# 302.2-Data infrastructure
# @ Gaetan Veuillet
#
# Some settings and a helper function used by the other scripts.
#############

#Quick note on arrow: Arrow is just use for parquet reading/writing, 
#could have used pandas but Pyarrow is behind pandas too.
import pyarrow as pa
import pyarrow.parquet as pq

FOLDER = "data/plain"

#Some settings for the demo
FILES_PER_DAY = 10       
ROWS_PER_FILE = 100_000  #just to simulate a real dataset, 100k rows per file for now
DELAY = 0.6 #delay just so that reader.py can be run while writer.py is running


def write_file(day, part):
    table = pa.table({
        "day": [day] * ROWS_PER_FILE,
        "amount": [1.0] * ROWS_PER_FILE,
    })
    pq.write_table(table, f"{FOLDER}/day{day}_part{part}.parquet")