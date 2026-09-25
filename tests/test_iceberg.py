#############
# TOPIC 14 : Table Formats and the Lakehouse
#
# tests/test_iceberg.py
#
# 302.2-Data infrastructure
# @ Gaetan Veuillet
#
# Tests for the Iceberg part.
#############

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ICEBERG = ROOT / "iceberg"

def execute(arguments):
    result = subprocess.run([sys.executable, *arguments], cwd=ICEBERG, capture_output=True, text=True)
    assert result.returncode == 0, f"{arguments} failed:\n{result.stderr}"
    return result.stdout

def run(script):
    return execute([script])

def run_code(code):
    return execute(["-c", code])

def test_uncommited():
    run("setup.py")
    run_code("from common import write_file\n"
             "for part in range(1,5): write_file(2,part)")
    out = run("reader.py")
    assert "day 1:" in out
    assert "day 2:" not in out
    assert "4 files on disk were ignored" in out

def test_commit_whole_visible():
    run("setup.py")
    run_code("from common import write_file, get_catalog, TABLE_NAME\n"
             "files = [write_file(2, part) for part in range(1, 11)]\n"
             "get_catalog().load_table(TABLE_NAME).add_files(files)")
    out = run("reader.py")
    assert "INCOMPLETE" not in out
    assert out.count("(10/10 files) -> COMPLETE") == 2

def test_old_query_schema_change():
    run("setup.py")
    out = run("evolve.py")
    assert "currency (id 3)" in out
    assert "day (id 1), amount (id 2), currency" in out
    out = run("reader.py")
    assert out.count("-> COMPLETE") == 2
    assert "INCOMPLETE" not in out