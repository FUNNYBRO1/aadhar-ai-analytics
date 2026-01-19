# src/prompt_router.py

import re

def route_prompt(user_prompt: str):
    p = user_prompt.lower()

    result = {
        "top_n": None,
        "topic": None
    }

    # -------- TOP N (top 1–10) --------
    match = re.search(r"top\s*(\d+)", p)
    if match:
        n = int(match.group(1))
        if 1 <= n <= 10:
            result["top_n"] = n

    # -------- TOPIC DETECTION --------
    if any(x in p for x in ["adult", "17", "above"]):
        result["topic"] = "adult"

    elif any(x in p for x in ["youth", "child", "5-17"]):
        result["topic"] = "youth"

    else:
        result["topic"] = "total"

    return result
