#############
# TOPIC 14 : Table Formats and the Lakehouse
#
# run_demo.py
#
# 302.2-Data infrastructure
# @ Gaetan Veuillet
#
# One command file demo : python run_demo.py
#############

import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
READER_START = 2.5  #seconds after the writer starts, so it lands mid append


def run(script):
    subprocess.run([sys.executable, str(ROOT / script)], check=True)


def title(text):
    print(f"\n||\n\t{text}\n{'-'*80}")


def writer_and_reader(part):
    writer = subprocess.Popen([sys.executable, str(ROOT / part / "writer.py")],
                              stdout=subprocess.PIPE, text=True)
    print(f"[demo] writer.py started, reader.py starts {READER_START}s later...\n")
    time.sleep(READER_START)
    run(f"{part}/reader.py")
    out, _ = writer.communicate()
    print("\n[demo] meanwhile, the writer printed:")
    print("\n".join("   " + line for line in out.strip().splitlines()))

title("1 -> PLAIN FOLDER, written then read")
run("plain/setup.py")
run("plain/writer.py")
run("plain/reader.py")

title("1a -> PLAIN FOLDER, append while a reader is running")
run("plain/setup.py")
writer_and_reader("plain")

title("2 -> ICEBERG TABLE, same append, same reader")
run("iceberg/setup.py")
writer_and_reader("iceberg")

title("2 -> ICEBERG TABLE, reader try to get the new data")
run("iceberg/reader.py")

title("2b -> WHAT THE COMMIT CHANGED IN THE METADATA")
run("iceberg/inspect_table.py")

title("3 -> SCHEMA CHANGE, then the old query again")
run("iceberg/evolve.py")
print()
run("iceberg/reader.py")