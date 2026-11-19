"""Charts module of DataCleanse (Lecture 4).
Every function: draws ONE chart, saves a PNG file, and returns the saved path.
Streamlit will call these functions later (Lecture 5) without any change.
"""
import os
import matplotlib
matplotlib.use("Agg")          # draw to files only (no pop-up window in WSL)
import matplotlib.pyplot as plt

os.makedirs("output/charts", exist_ok=True)


def plot_city_counts(df, path="output/charts/datacleanse_city_counts.png"):
    """Bar chart: number of records in each city."""
    counts = df["city"].value_counts()
    plt.figure(figsize=(8, 4.5))
    plt.bar(counts.index, counts.values)
    plt.title("Records per City")
    plt.xlabel("City")
    plt.ylabel("Number of records")
    plt.tight_layout()
    plt.savefig(path)
    plt.close()
    return path


def plot_age_hist(df, path="output/charts/datacleanse_age_hist.png", bins=8):
    """Histogram: distribution of ages."""
    plt.figure(figsize=(8, 4.5))
    plt.hist(df["age"], bins=bins)
    plt.title("Distribution of Ages")
    plt.xlabel("Age")
    plt.ylabel("Number of records")
    plt.tight_layout()
    plt.savefig(path)
    plt.close()
    return path


def plot_age_vs_score(df, path="output/charts/datacleanse_age_vs_score.png"):
    """Scatter plot: is there a relation between age and score?"""
    plt.figure(figsize=(8, 4.5))
    plt.scatter(df["age"], df["score"])
    plt.title("Age vs Score")
    plt.xlabel("Age")
    plt.ylabel("Score")
    plt.tight_layout()
    plt.savefig(path)
    plt.close()
    return path


def plot_score_hist(df, path="output/charts/datacleanse_score_hist.png", bins=8):
    """Histogram: distribution of scores."""
    plt.figure(figsize=(8, 4.5))
    plt.hist(df["score"], bins=bins)
    plt.title("Distribution of Scores")
    plt.xlabel("Score")
    plt.ylabel("Number of records")
    plt.tight_layout()
    plt.savefig(path)
    plt.close()
    return path
