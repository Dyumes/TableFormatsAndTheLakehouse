#############
# TOPIC 14 : Table Formats and the Lakehouse
#
# tests/test_plain.py
#
# 302.2-Data infrastructure
# @ Gaetan Veuillet
#
# Tests for the plain table format demo.
#############

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PLAIN = ROOT / "plain"


def run(script):
    result = subprocess.run([sys.executable, script], cwd=PLAIN, capture_output=True, text=True)
    return result.stdout

def run_code(code):
    subprocess.run([sys.executable, "-c", code], cwd=PLAIN,check=True)

def test_stup_writes_day_1():
    run("setup.py")
    files = list((ROOT / "data/plain").glob("day1_part*.parquet"))
    assert len(files) == 10

def test_half_written_append():
    run("setup.py")
    run_code("from common import write_file\n"
             "for part in range(1,5): write_file(2,part)")
    out = run("reader.py")
    assert "(10/10 files) -> COMPLETE" in out
    assert "(4/10 files) -> INCOMPLETE" in out

def test_after_full_append():
    run("setup.py")
    run_code("from common import write_file\n"
             "for part in range(1,11): write_file(2,part)")
    out = run("reader.py")
    assert "INCOMPLETE" not in out


