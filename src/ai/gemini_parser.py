# src/ai/gemini_parser.py

from dotenv import load_dotenv
import os
import json
import re
from typing import Dict
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
You are an expert data analytics assistant for Aadhaar demographic analysis.

Your job:
- Understand the user query
- Convert it into structured analytics instructions

Return ONLY valid JSON. No explanation. No markdown.

JSON format:
{
  "dataset": "default | biometric | enrolment",
  "level": "state | district",
  "state": "state name or null",
  "age_group": "adult | youth | total",
  "top_n": number,
  "analysis_type": "enrolment | biometric | saturation",
  "graph_title": "clear human readable title"
}


Rules:
- If districts are mentioned → level = district
- If a state name is mentioned → include it
- If number missing → top_n = 5
- If age unclear → total
- Graph title must be meaningful
- If query mentions biometric → dataset = biometric
- If query mentions enrolment or enrollment → dataset = enrolment
- Otherwise → dataset = default

"""


# ------------------------------------------------------
# MAIN FUNCTION
# ------------------------------------------------------
def gemini_parse_prompt(user_prompt: str) -> Dict:
    """
    Parses a natural language prompt using Gemini
    and returns structured analytics instructions.
    """

    print("🔥 GEMINI PARSER (NEW SDK) CALLED 🔥")

    prompt = f"""
System instruction:
{SYSTEM_PROMPT}

User query:
{user_prompt}
"""

    # -------- Gemini Call --------
    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )
        raw_text = response.text.strip()
    except Exception as e:
        raise RuntimeError(f"Gemini API call failed: {e}")

    # -------- JSON Extraction --------
    try:
        json_text = _extract_json(raw_text)
        parsed = json.loads(json_text)
    except Exception as e:
        raise ValueError(f"Gemini JSON parsing failed: {e}")

    return _normalize(parsed)


# ------------------------------------------------------
# HELPERS
# ------------------------------------------------------
def _extract_json(text: str) -> str:
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        raise ValueError("No JSON found in Gemini response")
    return match.group(0)


def _normalize(parsed: Dict) -> Dict:
    parsed.setdefault("level", "state")
    parsed.setdefault("state", None)
    parsed.setdefault("age_group", "total")
    parsed.setdefault("analysis_type", "enrolment")
    parsed.setdefault("dataset", "default")

    if parsed["dataset"] not in ["default", "biometric", "enrolment"]:
        parsed["dataset"] = "default"

    # top_n
    try:
        parsed["top_n"] = int(parsed.get("top_n", 5))
    except Exception:
        parsed["top_n"] = 5

    if parsed["top_n"] <= 0 or parsed["top_n"] > 20:
        parsed["top_n"] = 5

    # validations
    if parsed["age_group"] not in ["adult", "youth", "total"]:
        parsed["age_group"] = "total"

    if parsed["level"] not in ["state", "district"]:
        parsed["level"] = "state"

    if not parsed.get("graph_title"):
        parsed["graph_title"] = "Aadhaar Analytics Overview"

    return parsed
