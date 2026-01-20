# src/ai/gemini_insight.py

from dotenv import load_dotenv
import os
from typing import Dict
import pandas as pd
from google import genai


# ------------------------------------------------------
# ENV LOAD
# ------------------------------------------------------
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY not found in .env")

# ------------------------------------------------------
# GEMINI CLIENT (NEW SDK, v1)
# ------------------------------------------------------
client = genai.Client(
    api_key=GEMINI_API_KEY,
    http_options={"api_version": "v1"}
)

MODEL_NAME = "models/gemini-2.5-flash"

# ------------------------------------------------------
# SYSTEM PROMPT
# ------------------------------------------------------
SYSTEM_PROMPT = """
You are an AI data analyst for Aadhaar enrolment analytics.

Your task:
- Understand the user's question and the data summary
- Give a clear, short solution based strictly on the data

Response format (MANDATORY):
Solution:
<3–4 concise sentences explaining what should be done and why>

Rules:
- Always start with the heading word "Solution:"
- Keep it short and actionable
- Avoid generic statements
- Base suggestions on the user's prompt and the data
- No bullet points, no extra headings
"""


# ------------------------------------------------------
# PUBLIC FUNCTION
# ------------------------------------------------------
def generate_ai_insight(
    result_df: pd.DataFrame,
    context: Dict
) -> str:
    """
    Generates a detailed AI insight paragraph using Gemini,
    based on analyzed data and context.
    """

    if result_df is None or result_df.empty:
        return (
            "The selected filters did not return sufficient data for meaningful analysis. "
            "It is advisable to broaden the selection criteria or verify data availability "
            "before drawing conclusions."
        )

    summary_text = _build_data_summary(result_df, context)

    prompt = f"""
System instruction:
{SYSTEM_PROMPT}

Context:
{context}

Data summary:
{summary_text}
"""

    # -------- Gemini Call --------
    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )
        insight = response.text.strip()
    except Exception as e:
        return (
            "While the data indicates notable regional and demographic variation in Aadhaar "
            "enrolment, further operational review and targeted planning are recommended to "
            "address localized challenges."
        )

    return insight


# ------------------------------------------------------
# HELPERS
# ------------------------------------------------------
def _build_data_summary(df: pd.DataFrame, context: Dict) -> str:
    """
    Converts the result dataframe into a compact textual summary
    that Gemini can reason over.
    """

    col_x = df.columns[0]
    col_y = df.columns[1]

    top_rows = df.head(5)

    lines = []
    for _, row in top_rows.iterrows():
        lines.append(f"{row[col_x]}: {int(row[col_y]):,}")

    level = context.get("level", "state")
    age_group = context.get("age_group", "total")
    state = context.get("state")

    header = f"Top {len(top_rows)} {level}-level Aadhaar enrolment values"
    if state:
        header += f" in {state}"

    header += f" for {age_group} population"

    return header + ":\n" + "\n".join(lines)
