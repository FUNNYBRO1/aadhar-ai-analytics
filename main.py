import os
from dotenv import load_dotenv
import streamlit as st

# -----------------------------
# 1. ENV LOAD
# -----------------------------
load_dotenv()

# -----------------------------
# 2. IMPORTS
# -----------------------------
from src.loader import load_csv
from src.analyzer import (
    age_wise_coverage, youth_pressure, adult_saturation,
    temporal_growth, district_disparity, pincode_coverage,
    youth_adult_ratio, state_concentration, longitudinal_stability,
    resource_allocation, adult_enrollment_mapping
)
from src.visualizer import generate_graph
from src.prompt_router import route_prompt

# -----------------------------
# 3. STREAMLIT APP
# -----------------------------
def main():
    st.title("Aadhaar AI Analytics System")

    # -----------------------------
    # API KEY CHECK
    # -----------------------------
    api_key = os.getenv("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY")

    if not api_key:
        st.error("GEMINI_API_KEY missing hai. .env ya Streamlit secrets check karo.")
        st.stop()

    st.success("Gemini API Key Loaded")

    # -----------------------------
    # PATH CONFIG
    # -----------------------------
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(BASE_DIR, "data", "input", "aadhar_clean.csv")

    if not os.path.exists(csv_path):
        st.error(f"CSV file nahi mili: {csv_path}")
        st.stop()

    # -----------------------------
    # LOAD DATA
    # -----------------------------
    with st.spinner("CSV load ho rahi hai..."):
        df = load_csv(csv_path, use_chunks=True)

    if df is None or df.empty:
        st.error("CSV load nahi hui ya empty hai.")
        st.stop()

    st.success(f"Data Loaded | Rows: {len(df)}")

    # -----------------------------
    # USER INPUT
    # -----------------------------
    user_prompt = st.text_input(
        "Aapka Aadhaar related query likhiye:",
        placeholder="eg. youth aadhaar coverage district wise"
    )

    if not user_prompt:
        st.info("Query likhne ke baad Enter karo")
        return

    # -----------------------------
    # ROUTING
    # -----------------------------
    st.write("🔍 Gemini AI routing chal rahi hai...")
    problem_labels = route_prompt(user_prompt)

    if not problem_labels:
        st.warning("Koi matching analysis topic nahi mila.")
        return

    st.success(f"Mapped Topics: {problem_labels}")

    # -----------------------------
    # ANALYSIS MAP
    # -----------------------------
    ANALYSIS_MAP = {
        "Age-wise Aadhaar Coverage Imbalance": age_wise_coverage,
        "Regional Youth Population Pressure": youth_pressure,
        "Adult Enrollment Saturation Mapping": adult_enrollment_mapping,
        "Temporal Growth Pattern Analysis": temporal_growth,
        "District-Level Demographic Disparity": district_disparity,
        "Pincode-Level Coverage Gaps": pincode_coverage,
        "Youth-to-Adult Ratio Risk Zones": youth_adult_ratio,
        "State-wise Demographic Concentration": state_concentration,
        "Longitudinal Stability Assessment": longitudinal_stability,
        "Resource Allocation Optimization": resource_allocation
    }

    # -----------------------------
    # EXECUTION
    # -----------------------------
    for problem in problem_labels:
        if problem not in ANALYSIS_MAP:
            st.warning(f"Mapping missing for: {problem}")
            continue

        st.subheader(problem)

        try:
            result_df = ANALYSIS_MAP[problem](df)

            if result_df is None or result_df.empty:
                st.warning("Result empty hai")
                continue

            graph_type = "line" if (
                "Temporal" in problem or "Longitudinal" in problem
            ) else "bar"

            generate_graph(
                result_df,
                graph_type=graph_type,
                title=problem
            )

        except Exception as e:
            st.error(f"Error in {problem}: {e}")

    st.success("Process complete 🎉")

# -----------------------------
# ENTRY POINT
# -----------------------------
if __name__ == "__main__":
    main()
