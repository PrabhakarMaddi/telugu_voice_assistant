import os
import warnings
from dotenv import load_dotenv

load_dotenv()

# Robustly suppress the deprecation warning from the old SDK
warnings.filterwarnings("ignore", category=FutureWarning)

try:
    import google.generativeai as genai
except ImportError:
    genai = None

# Initialize Gemini
api_key = os.getenv("GEMINI_API_KEY")
model = None
if api_key and genai:
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-flash-latest")
    except Exception as e:
        print(f"Error initializing Gemini: {e}")

def generate_response(user_text, history=None):
    """
    Generates a Telugu response using Google Gemini (Free Tier)
    with conversation history support.
    'history' should be a list of dicts: [{'role': 'user', 'parts': [...]}, ...]
    """
    if not model:
        return "Error: Gemini API key not found or initialization failed."

    try:
        system_instruction = (
            "You are a helpful assistant that speaks Telugu. "
            "Always respond in clear, natural Telugu. Keep responses concise. "
            "If the user asks who you are, say you are a Telugu Voice Assistant."
        )
        
        # Start a new chat session with the provided history
        # Gemini expects history format: [{'role': 'user', 'parts': ['...']}, ...]
        chat = model.start_chat(history=history or [])
        
        # If history is empty, prepend system instruction to first message
        full_user_text = user_text
        if not history:
            full_user_text = f"{system_instruction}\n\nUser: {user_text}"
            
        response = chat.send_message(full_user_text)
        return response.text.strip()
    except Exception as e:
        return f"Gemini error: {str(e)}"

if __name__ == "__main__":
    # Test
    # print(generate_response("నమస్కారం! నువ్వు ఎవరు?"))
    pass
