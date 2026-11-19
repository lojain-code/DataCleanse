import pandas as pd
def clean_data(df):
    df = df.copy()
    df = df.drop_duplicates()
    df["city"] = df["city"].str.strip().str.title()
    df["score"] = df["score"].fillna(df["score"].median())
    df = df[(df["age"] >= 15) & (df["age"] <= 70)]
    return df.reset_index(drop=True)
