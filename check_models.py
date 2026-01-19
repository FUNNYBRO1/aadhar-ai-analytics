from google import genai
import streamlit as st

# Secrets se key uthayein
api_key = st.secrets["GEMINI_API_KEY"]
client = genai.Client(api_key=api_key)

# Saare available models print karein
print("Available Gemini Models:")
for model in client.models.list():
    print(f"- {model.name}")