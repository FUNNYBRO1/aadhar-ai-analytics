# app.py
import os
import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
from src.prompt_router import route_prompt
from src.analyzer import adult_analysis, youth_analysis, total_analysis
from src.visualizer import generate_graph
# 🔥 GEMINI (NEW SDK)
from src.ai.gemini_parser import gemini_parse_prompt
from src.ai.gemini_insight import generate_ai_insight


# ======================================================
# STATE NAME STANDARDIZATION
# ======================================================
STATE_FIX_MAP = {
    "west bengal": "West Bengal",
    "west bangal": "West Bengal",
    "west bengli": "West Bengal",
    "westbengal": "West Bengal",
    "west bengal ": "West Bengal",
    
    "andhra pradesh": "Andhra Pradesh",
    "andhrapradesh": "Andhra Pradesh",

    "odisha": "Odisha",
    "orissa": "Odisha",

    "chhattisgarh": "Chhattisgarh",
    "chattisgarh": "Chhattisgarh",
    "chhatishgarh": "Chhattisgarh",
    "chhatisgarh": "Chhattisgarh",
    "chatisgarh": "Chhattisgarh"
}

def clean_state_name(state):
    if not isinstance(state, str):
        return state
    key = state.strip().lower()
    return STATE_FIX_MAP.get(key, state.strip().title())





# ======================================================
# PAGE CONFIG
# ======================================================
st.set_page_config(
    page_title="Aadhaar AI Analytics",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ======================================================
# THEME CSS
# ======================================================
with open("styles/theme.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ======================================================
# HEADER
# ======================================================
h1, h2 = st.columns([1, 6])

with h1:
    logo_path = "assets/logos/logo_main.png"
    if os.path.exists(logo_path):
        st.image(logo_path, width=80)

with h2:
    st.markdown(
        """
        <h1 class="gradient-text" style="margin-bottom:0;">
            Aadhaar AI Analytics
        </h1>
        <p style="color:#9ca3af;margin-top:4px">
            Smart insights for Aadhaar enrolment & demographics
        </p>
        """,
        unsafe_allow_html=True
    )

st.divider()

# ======================================================
# DATA LOAD
# ======================================================
DATA_PATH = "data/input/aadhar_clean.csv"

@st.cache_data
def load_data(path):
    df = pd.read_csv(path)
    df.columns = df.columns.str.strip()

    # 🔥 FIX STATE NAMES HERE
    df["state"] = df["state"].apply(clean_state_name)

    df["Total_Aadhaar"] = df["demo_age_5_17"] + df["demo_age_17_"]

    return df

df = load_data(DATA_PATH)

# ======================================================
# FILTERS
# ======================================================
st.markdown("### 🔍 Search & Filters")

f1, f2, f3, f4 = st.columns(4)

with f1:
    selected_states = st.multiselect(
        "State",
        sorted(df["state"].unique()),
        placeholder="Search state"
    )

district_df = df[df["state"].isin(selected_states)] if selected_states else df

with f2:
    selected_districts = st.multiselect(
        "District",
        sorted(district_df["district"].unique()),
        placeholder="Search district"
    )

pin_df = district_df[district_df["district"].isin(selected_districts)] if selected_districts else district_df

with f3:
    selected_pincodes = st.multiselect(
        "Pincode",
        sorted(pin_df["pincode"].astype(str).unique()),
        placeholder="Search pincode"
    )

with f4:
    age_type_ui = st.radio(
        "Age Group",
        ["Total", "Adults (17+)", "Youth (5–17)"],
        horizontal=True
    )

st.divider()

# ======================================================
# AI QUERY
# ======================================================
st.markdown(
    "<h3 class='gradient-text'>🤖 Ask Ekta AI</h3>",
    unsafe_allow_html=True
)

user_query = st.text_input(
    "Ask your query",
    placeholder="eg. Top 5 adult Aadhaar saturation districts in Uttar Pradesh",
    label_visibility="collapsed"
)

# ======================================================
# PROCESS
# ======================================================
if user_query:

    # ---------------- GEMINI PARSER ----------------
    try:
        parsed = gemini_parse_prompt(user_query)
        parser_used = "gemini"
    except Exception:
        parsed = route_prompt(user_query)
        parser_used = "fallback"

    top_n = parsed.get("top_n", 5)
    level = parsed.get("level", "state")
    age_group = parsed.get("age_group", "total")
    graph_title = parsed.get("graph_title", "Aadhaar Analytics Overview")

    # ---------------- APPLY FILTERS ----------------
    filtered_df = df

    if selected_states:
        filtered_df = filtered_df[filtered_df["state"].isin(selected_states)]

    if selected_districts:
        filtered_df = filtered_df[filtered_df["district"].isin(selected_districts)]

    if selected_pincodes:
        filtered_df = filtered_df[
            filtered_df["pincode"].astype(str).isin(selected_pincodes)
        ]

    # ---------------- SUMMARY CARDS ----------------
    c1, c2, c3, c4 = st.columns(4)

    c1.metric("📄 Records", f"{len(filtered_df):,}")
    c2.metric("🆔 Total Aadhaar", f"{int(filtered_df['Total_Aadhaar'].sum()):,}")
    c3.metric("🏙️ States", filtered_df["state"].nunique())
    c4.metric("📍 Districts", filtered_df["district"].nunique())

    st.divider()

    # ---------------- ANALYSIS ----------------
    analysis_level = "district" if level == "district" else "state"

    if age_group == "adult":
        result_df = adult_analysis(filtered_df, analysis_level, top_n)
    elif age_group == "youth":
        result_df = youth_analysis(filtered_df, analysis_level, top_n)
    else:
        result_df = total_analysis(filtered_df, analysis_level, top_n)

    # ---------------- OUTPUT ----------------
    left, right = st.columns([3, 1])

    with left:
        st.markdown(f"### {graph_title}")
        generate_graph(result_df, "bar", graph_title)

    with right:
        st.markdown("### 🧠 AI-Generated Insight")

        ai_insight = generate_ai_insight(
            result_df,
            context={
                "level": analysis_level,
                "age_group": age_group,
                "state": parsed.get("state"),
                "parser": parser_used
            }
        )

        st.info(ai_insight)

    st.divider()

    st.markdown("### 📋 Detailed Data")
    st.dataframe(result_df, use_container_width=True)

# ======================================================
# ABOUT SECTION
# ======================================================
about_path = "assets/html/about.html"

st.divider()

if os.path.exists(about_path):
    with open(about_path, "r", encoding="utf-8") as f:
        about_html = f.read()

    components.html(
        about_html,
        height=650,
        scrolling=False
    )
