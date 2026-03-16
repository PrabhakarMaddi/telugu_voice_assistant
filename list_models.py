from google import genai
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("Error: GEMINI_API_KEY not found.")
else:
    try:
        client = genai.Client(api_key=api_key)
        print("Available Flash Models:")
        for m in client.models.list():
            if 'flash' in m.name.lower():
                print(f"- {m.name} ({m.display_name})")
    except Exception as e:
        print(f"Error listing models: {e}")
