# app.py

import streamlit as st
import pandas as pd

from src.prompt_router import route_prompt
from src.analyzer import adult_analysis, youth_analysis, total_analysis
from src.visualizer import generate_graph

# ---------------- UI CONFIG ----------------
st.set_page_config(page_title="Aadhaar AI Analytics", layout="wide")
st.title("📊 Aadhaar AI Analytics Dashboard")

# ---------------- DATA LOAD ----------------
DATA_PATH = "data/input/aadhar_clean.csv"

@st.cache_data
def load_data(path):
    df = pd.read_csv(path)
    df.columns = df.columns.str.strip()
    df["Total_Aadhaar"] = df["demo_age_5_17"] + df["demo_age_17_"]
    return df

df = load_data(DATA_PATH)

# ======================================================
# SIDEBAR FILTERS (SEARCH + SELECT IN SAME BOX)
# ======================================================
st.sidebar.header("🔎 Filters")

# -------- STATE MULTISELECT --------
selected_states = st.sidebar.multiselect(
    "Select State(s)",
    options=sorted(df["state"].unique()),
    placeholder="Type to search state"
)

# -------- DISTRICT MULTISELECT --------
district_df = df[df["state"].isin(selected_states)] if selected_states else df

selected_districts = st.sidebar.multiselect(
    "Select District(s)",
    options=sorted(district_df["district"].unique()),
    placeholder="Type to search district"
)

# -------- PINCODE MULTISELECT --------
pin_df = district_df[district_df["district"].isin(selected_districts)] if selected_districts else district_df

selected_pincodes = st.sidebar.multiselect(
    "Select Pincode(s)",
    options=sorted(pin_df["pincode"].astype(str).unique()),
    placeholder="Type to search pincode"
)

# -------- AGE GROUP --------
age_type = st.sidebar.radio(
    "Age Group",
    ["Total", "Adults (17+)", "Youth (5–17)"]
)

# ======================================================
# MAIN : AI PROMPT
# ======================================================
st.subheader("Ask Ekta AI for Aadhaar related Information")

user_query = st.text_input(
    "AI se kuch bhi poochho (Top 3, Top 5, solution etc.)",
    placeholder="eg. top 5 adult saturation"
)

# ======================================================
# PROCESS
# ======================================================
if user_query:
    parsed = route_prompt(user_query)
    top_n = parsed.get("top_n") or 5

    # -------- APPLY FILTERS --------
    filtered_df = df

    if selected_states:
        filtered_df = filtered_df[filtered_df["state"].isin(selected_states)]

    if selected_districts:
        filtered_df = filtered_df[filtered_df["district"].isin(selected_districts)]

    if selected_pincodes:
        filtered_df = filtered_df[
            filtered_df["pincode"].astype(str).isin(selected_pincodes)
        ]

    # -------- ANALYSIS --------
    if age_type == "Adults (17+)":
        result_df = adult_analysis(filtered_df, "state", top_n)
        title = f"Top {top_n} Adult Aadhaar Enrollment"
        insight = "Adult population high hai → extra Aadhaar centres required."

    elif age_type == "Youth (5–17)":
        result_df = youth_analysis(filtered_df, "state", top_n)
        title = f"Top {top_n} Youth Aadhaar Enrollment"
        insight = "Youth population zyada hai → school/camp based enrolment best rahega."

    else:
        result_df = total_analysis(filtered_df, "state", top_n)
        title = f"Top {top_n} Total Aadhaar Enrollment"
        insight = "High Aadhaar volume → resources scaling recommended."

    # -------- OUTPUT UI --------
    st.divider()
    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader(title)
        generate_graph(result_df, "bar", title)

    with col2:
        st.subheader("🧠 Insight & Solution")
        st.write(insight)

        st.markdown("**Applied Filters:**")
        if selected_states:
            st.write("State:", ", ".join(selected_states))
        if selected_districts:
            st.write("District:", ", ".join(selected_districts))
        if selected_pincodes:
            st.write("Pincode:", ", ".join(selected_pincodes))

    st.divider()
    st.subheader("📋 Detailed Data")
    st.dataframe(result_df, use_container_width=True)
