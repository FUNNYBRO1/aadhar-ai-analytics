from dotenv import load_dotenv
import os
from google import genai

load_dotenv()

key = os.getenv("GEMINI_API_KEY")
print("API KEY FOUND:", bool(key))

if not key:
    print("❌ GEMINI_API_KEY missing")
    exit()

client = genai.Client(
    api_key=key,
    http_options={"api_version": "v1"}
)

print("🚀 Calling Gemini API (REAL MODEL)...")

response = client.models.generate_content(
    model="models/gemini-2.5-flash",
    contents="Explain Aadhaar enrolment challenges in India in 4 lines"
)

print("\n✅ GEMINI RESPONSE:\n")
print(response.text)
