# DataCleanse - draw and save all charts (Lecture 4)
# Run from the project folder:  python run_charts.py
import os
import pandas as pd
from core.charts import plot_city_counts, plot_age_hist, plot_age_vs_score, plot_score_hist

df = pd.read_csv("output/records_raw_cleaned.csv")
os.makedirs("output/charts", exist_ok=True)

results = [
    ("plot_city_counts", plot_city_counts(df)),
    ("plot_age_hist", plot_age_hist(df)),
    ("plot_age_vs_score", plot_age_vs_score(df)),
    ("plot_score_hist", plot_score_hist(df)),
]
for name, path in results:
    if path is None:
        print("Not created yet:", name)
    else:
        print("Saved:", path)
