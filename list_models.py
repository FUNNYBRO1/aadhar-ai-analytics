from dotenv import load_dotenv
import os
from google import genai

load_dotenv()

key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=key, http_options={"api_version": "v1"})

print("Listing available models...\n")

models = client.models.list()

for m in models:
    print(m.name)
