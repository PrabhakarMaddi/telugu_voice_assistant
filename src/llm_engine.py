import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

def generate_response(user_text):
    """
    Generates a Telugu response using Google Gemini 1.5 Flash (Free Tier).
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return "Error: Gemini API key not found."

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")
        
        system_prompt = (
            "You are a helpful assistant that speaks Telugu. "
            "Always respond in clear, natural Telugu. Keep responses concise."
        )
        
        response = model.generate_content(f"{system_prompt}\n\nUser: {user_text}")
        return response.text.strip()
    except Exception as e:
        return f"Gemini error: {str(e)}"

if __name__ == "__main__":
    # Test
    # print(generate_response("తెలంగాణ రాజధాని ఏది?"))
    pass
