# DataCleanse - test the helper functions in core/analysis.py (Workshop 2)
# Run from the project folder:   python test_analysis.py
import os
import sys
import pandas as pd

os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.getcwd())
from core.analysis import quality_report

results = []


def check(name, ok, why=""):
    results.append(ok)
    print(("PASS - " if ok else "FAIL - ") + name + ("" if ok else "   <- " + why))


raw = pd.read_csv("data/records_raw.csv")
cleaned = pd.read_csv("output/records_raw_cleaned.csv")
rep = quality_report(raw, cleaned)
check("rows_before is 125", rep["rows_before"] == 125, str(rep["rows_before"]))
check("duplicates_before is 5", rep["duplicates_before"] == 5, str(rep["duplicates_before"]))
check("missing_before is 22", rep["missing_before"] == 22, str(rep["missing_before"]))
check("rows_removed = rows_before - rows_after", rep["rows_removed"] == rep["rows_before"] - rep["rows_after"], str(rep))
check("cleaning does not add rows", rep["rows_after"] <= rep["rows_before"], str(rep))
toy = pd.DataFrame({"a": [1, 1, None], "b": [2, 2, 3]})
r2 = quality_report(toy, toy.drop_duplicates().dropna())
check("toy example: 3 rows -> 1 row, 1 missing, 1 duplicate", (r2["rows_after"], r2["missing_before"], r2["duplicates_before"]) == (1, 1, 1), str(r2))

print()
print(sum(results), "of", len(results), "checks passed")
