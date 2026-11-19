"""DataCleanse - Streamlit website (Workshops 1-2).
Run from the project folder:   streamlit run app.py
Parts marked STUDENT PART are written by the group. Everything else is given."""
import os
import pandas as pd
import streamlit as st
from core.charts import plot_city_counts, plot_age_hist, plot_age_vs_score, plot_score_hist
from core.cleaning import clean_data
from core.analysis import quality_report


GROUP = """Lojain almayouf
Renad almutairi
Rahaf alazmi
Hessa alharbi"""
    # <- edit this line

st.set_page_config(page_title="DataCleanse", layout="wide")
st.title("DataCleanse - Data Quality Auditor")
st.caption("Training project with synthetic data. Not real data, not an official or professional system.")
st.sidebar.header("DataCleanse")
st.sidebar.write(GROUP)

for needed in ['output/records_raw_cleaned.csv', 'data/records_raw.csv']:
    if not os.path.exists(needed):
        st.error("File not found: " + needed + "  ->  run run_cleaning.py (Lecture 3) or copy it from datasets/DataCleanse/")
        st.stop()


# === STUDENT PART 1 START (Tuesday): read the cleaned CSV and show it ===
# HINT: df = pd.read_csv("output/records_raw_cleaned.csv"); metrics Rows, Cities, Average score; st.dataframe(df.head(10))

st.subheader("1. The cleaned records")
df = pd.read_csv("output/records_raw_cleaned.csv")

c1, c2, c3 = st.columns(3)
c1.metric("Rows", len(df))
c2.metric("Cities", df["city"].nunique())
c3.metric("Average score", round(float(df["score"].mean()), 1))

st.dataframe(df.head(10))
# === STUDENT PART 1 END ===
if df is None:
    st.stop()

# === STUDENT PART 2 START (Tuesday): show two charts from Lecture 4 ===
# HINT: plot_city_counts(df) and plot_age_vs_score(df); st.image(path)

st.subheader("2. Charts from Lecture 4")
left, right = st.columns(2)
left.image(plot_city_counts(df))
right.image(plot_age_vs_score(df))
# === STUDENT PART 2 END ===

# === STUDENT PART 3 START (Tuesday): interactive histograms ===
# HINT: st.slider("Age bins", 3, 15, 8) -> plot_age_hist(df, bins=age_bins); st.slider("Score bins", 3, 15, 8) -> plot_score_hist(df, bins=score_bins)

st.subheader("3. Interactive histograms")

age_bins = st.slider("Age bins", 3, 15, 8)
st.image(plot_age_hist(df, bins=age_bins))

score_bins = st.slider("Score bins", 3, 15, 8)
st.image(plot_score_hist(df, bins=score_bins))

# === STUDENT PART 3 END ===

# === STUDENT PART 4 START (Wednesday): upload, clean and report ===
# HINT: up = st.file_uploader("Upload a CSV file", type="csv"); raw = pd.read_csv(up) if up is not None else pd.read_csv("data/records_raw.csv")
# HINT: cleaned = clean_data(raw) inside try/except KeyError; report = quality_report(raw, cleaned); metrics Rows before, Rows after, Missing values, Duplicate rows; st.download_button

st.subheader("4. Upload, Clean and Report")

up = st.file_uploader("Upload a CSV file", type="csv")

try:
    raw = pd.read_csv(up) if up is not None else pd.read_csv("data/records_raw.csv")
    cleaned = clean_data(raw)
    report = quality_report(raw, cleaned)

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Rows before", len(raw))
    c2.metric("Rows after", len(cleaned))
    c3.metric("Missing values", int(raw.isna().sum().sum()))
    c4.metric("Duplicate rows", int(raw.duplicated().sum()))

    st.subheader("Data Quality Report")
    st.write(report)

    st.subheader("Cleaned Data")
    st.dataframe(cleaned)

    st.download_button(
        label="Download Cleaned CSV",
        data=cleaned.to_csv(index=False).encode("utf-8"),
        file_name="records_cleaned.csv",
        mime="text/csv"
    )

except KeyError as e:
    st.error(f"Missing required column: {e}")
# === STUDENT PART 4 END ===

st.divider()
st.caption("Project: DataCleanse | Advanced Programming DAI221 | Majmaah University - Applied College")
