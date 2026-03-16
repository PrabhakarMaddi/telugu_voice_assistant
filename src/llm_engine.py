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
if api_key and genai:
    try:
        genai.configure(api_key=api_key)
        # Use a model that exists in the current environment
        # Based on list_models, gemini-flash-latest is available
        model = genai.GenerativeModel("gemini-flash-latest")
        # Start a chat session to maintain history
        chat_session = model.start_chat(history=[])
    except Exception as e:
        print(f"Error initializing Gemini: {e}")
        chat_session = None
else:
    chat_session = None

def generate_response(user_text):
    """
    Generates a Telugu response using Google Gemini (Free Tier)
    with conversation history support using the google-generativeai SDK.
    """
    if not chat_session:
        return "Error: Gemini API key not found or initialization failed."

    try:
        system_instruction = (
            "You are a helpful assistant that speaks Telugu. "
            "Always respond in clear, natural Telugu. Keep responses concise. "
            "If the user asks who you are, say you are a Telugu Voice Assistant."
        )
        
        full_prompt = user_text
        if len(chat_session.history) == 0:
            full_prompt = f"{system_instruction}\n\nUser: {user_text}"

        response = chat_session.send_message(full_prompt)
        return response.text.strip()
    except Exception as e:
        return f"Gemini error: {str(e)}"

if __name__ == "__main__":
    # Test
    # print(generate_response("నమస్కారం! నువ్వు ఎవరు?"))
    pass
