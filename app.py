import streamlit as st
import os
from src.loader import load_csv
from src.prompt_router import route_prompt
from src.analyzer import (
    age_wise_coverage, youth_pressure, adult_saturation, 
    temporal_growth, district_disparity, pincode_coverage, 
    youth_adult_ratio, state_concentration, longitudinal_stability,
    resource_allocation, adult_enrollment_mapping
)

# Website ki Page Configuration
st.set_page_config(page_title="Aadhaar AI Analytics", layout="wide")

st.title("📊 Aadhaar AI Demographic Analytics Dashboard")
st.markdown("Gemini 2.5 Flash ke saath natural language mein data analysis karein.")

# Sidebar for Status
st.sidebar.header("System Status")

# Analysis Map (Same as main.py)
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

# Data Loading (Caching use kar rahe hain taaki baar-baar load na ho)
@st.cache_data
def get_data():
    csv_path = os.path.join("data", "input", "aadhar_clean.csv")
    return load_csv(csv_path)

data_df = get_data()

if data_df is not None:
    st.sidebar.success("✅ Aadhaar Data Loaded")
else:
    st.sidebar.error("❌ Data Load Nahi Hua")

# User Query Input
user_query = st.text_input("Aapka query kya hai?", placeholder="e.g. Bihar ka youth pressure dikhao")

import matplotlib.pyplot as plt # Top par ye import add karein

# ... (baaki code same rahega) ...

if st.button("Generate Analysis"):
    if user_query:
        with st.spinner("Gemini AI analysis kar raha hai..."):
            problem_labels = route_prompt(user_query)
            
            if problem_labels:
                for problem in problem_labels:
                    if problem in ANALYSIS_MAP:
                        result_df = ANALYSIS_MAP[problem](data_df)
                        
                        if result_df is not None and not result_df.empty:
                            st.subheader(f"Analysis: {problem}")
                            
                            # --- FIX START: Matplotlib Graph Plotting ---
                            fig, ax = plt.subplots(figsize=(10, 6))
                            
                            if "Temporal" in problem or "Longitudinal" in problem:
                                result_df.plot(kind='line', ax=ax, marker='o')
                            else:
                                result_df.plot(kind='bar', ax=ax)
                            
                            plt.title(problem)
                            plt.xticks(rotation=45)
                            plt.tight_layout()
                            
                            # Graph ko website pe dikhane ke liye
                            st.pyplot(fig)
                            # --- FIX END ---

                            with st.expander("View Raw Data Table"):
                                st.dataframe(result_df)