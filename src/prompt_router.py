import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

# SDK Configure karein
genai.configure(api_key=API_KEY)

PROBLEMS = [
    "Age-wise Aadhaar Coverage Imbalance",
    "Regional Youth Population Pressure",
    "Adult Enrollment Saturation Mapping",
    "Temporal Growth Pattern Analysis",
    "District-Level Demographic Disparity",
    "Pincode-Level Coverage Gaps",
    "Youth-to-Adult Ratio Risk Zones",
    "State-wise Demographic Concentration",
    "Longitudinal Stability Assessment",
    "Resource Allocation Optimization"
]

def route_prompt(user_prompt: str):
    try:
        # Aapki list ke mutabik exact model name
        model = genai.GenerativeModel('models/gemini-2.5-flash')
        
        system_instruction = f"""
        Instructions: You are a data classifier. 
        List of Categories: {', '.join(PROBLEMS)}
        
        Task: Map the user query to one or more categories from the list above.
        Rule: Return ONLY the exact category names separated by commas.
        """
        
        response = model.generate_content(f"{system_instruction}\nUser Query: {user_prompt}")
        
        if not response.text:
            return []
            
        text = response.text.strip()
        
        # Valid labels ko extract karein
        mapped = [p.strip() for p in text.split(",") if p.strip() in PROBLEMS]
        return mapped

    except Exception as e:
        print(f"Gemini API Error: {e}")
        return []