# src/analyzer.py

import pandas as pd

def get_top_n(df, group_col, value_col, n):
    return (
        df.groupby(group_col)[[value_col]]
        .sum()
        .reset_index()
        .sort_values(value_col, ascending=False)
        .head(n)
    )

def get_total_by_state(df, state_name):
    return (
        df[df["state"].str.lower() == state_name.lower()]
        ["Total_Aadhaar"]
        .sum()
    )

def adult_analysis(df, level, top_n):
    group_col = "district" if level == "district" else "state"
    return get_top_n(df, group_col, "demo_age_17_", top_n)

def youth_analysis(df, level, top_n):
    group_col = "district" if level == "district" else "state"
    return get_top_n(df, group_col, "demo_age_5_17", top_n)

def total_analysis(df, level, top_n):
    group_col = "district" if level == "district" else "state"
    return get_top_n(df, group_col, "Total_Aadhaar", top_n)
