import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("Error: GEMINI_API_KEY not found.")
else:
    genai.configure(api_key=api_key)
    print("Available Flash Models:")
    try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods and 'flash' in m.name.lower():
                print(f"- {m.name} ({m.display_name})")
    except Exception as e:
        print(f"Error listing models: {e}")
