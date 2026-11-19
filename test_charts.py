# DataCleanse - check that every chart file exists (Lecture 4)
# Run AFTER run_charts.py:  python test_charts.py
import os

EXPECTED = [
    "output/charts/datacleanse_city_counts.png",
    "output/charts/datacleanse_age_hist.png",
    "output/charts/datacleanse_age_vs_score.png",
    "output/charts/datacleanse_score_hist.png",
]

ok = 0
for path in EXPECTED:
    if os.path.exists(path) and os.path.getsize(path) > 2000:
        print("PASS -", path)
        ok = ok + 1
    else:
        print("FAIL -", path)
print(ok, "of", len(EXPECTED), "charts created")
