# Table formats and the lakehouse

**A lake is a directory of files. What does it take to call it a table?**

Gaëtan Veuillet

Flipped class, 302.1 Data Infrastructured, Topic 14

## Run the demo
```
pip install -r requirements.txt
python run_demo.py
```

Run from the root of the repository.The demo takes about 20 secondand writes everything in `data/`.

## What it shows

**Part 1, plain folder**

Day 1 is 10 Parquet files. A writer appends day 2 as 10 more files, one at a time. Then a reader starts in the middle (with no table fomrat), it can only list the folder so itreads day 1 plus part of day 2. The result for day 2 is then wrong, and nothing tells it so.

**Part2, Iceberg table
 (`iceberg/`)**

 Same data, same append. The writer writes its files the same way, then commits them in one step. The reader asks the catalog for the current snapshot instead of listing the folder : it sees day 1 complete and ignore the day 2 files that are on disk but not commited yet.

 `inspect_table.py` then follows the path a reader takes: cataog -> metadata file -> snapshots -> manifest lists -> manifests -> data files. It also writes a copy of the current metadata file in `data/iceberg/pretty` (indented version).

 **Part 3, schema change (`iceberg/evolve.py`)



