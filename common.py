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

DATA_DIR = "data"
FOLDER = f"{DATA_DIR}/plain"



#Some settings for the demo
DAYS = 1
FILES_PER_DAY = 10       
ROWS_PER_FILE = 100_000  #just to simulate a real dataset, 100k rows per file for now
DELAY = 0.6 #delay just so that reader.py can be run while writer.py is running

#For this demo I choose that every row is a sale of 1 CHF
AMOUNT = 1.0 
EXPECTED_REVENUE_PER_DAY = FILES_PER_DAY * ROWS_PER_FILE * AMOUNT

def write_file(day, part):
    table = pa.table({
        "day": [day] * ROWS_PER_FILE,
        "amount": [1.0] * ROWS_PER_FILE,
    })
    filename = f"{FOLDER}/day{day}_part{part}.parquet"
    pq.write_table(table, filename)
    return filename