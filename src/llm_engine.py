import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize Gemini
api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
    # Use 'gemini-1.5-flash' (the SDK handles the models/ prefix usually)
    # If the user got a 404, it might be that the model ID changed or the v1beta endpoint is acting up.
    # We'll use 'gemini-1.5-flash-latest' to be safer.
    model_name = "gemini-1.5-flash"
    try:
        model = genai.GenerativeModel(model_name)
        chat_session = model.start_chat(history=[])
    except Exception as e:
        print(f"Error initializing Gemini: {e}")
        chat_session = None
else:
    chat_session = None

def generate_response(user_text):
    """
    Generates a Telugu response using Google Gemini 1.5 Flash (Free Tier)
    with conversation history support.
    """
    if not chat_session:
        return "Error: Gemini API key not found or model initialization failed."

    try:
        system_instruction = (
            "You are a helpful assistant that speaks Telugu. "
            "Always respond in clear, natural Telugu. Keep responses concise. "
            "If the user asks who you are, say you are a Telugu Voice Assistant."
        )
        
        full_prompt = user_text
        if not chat_session.history:
            full_prompt = f"{system_instruction}\n\nUser: {user_text}"

        response = chat_session.send_message(full_prompt)
        return response.text.strip()
    except Exception as e:
        return f"Gemini error: {str(e)}"

if __name__ == "__main__":
    # Test
    # print(generate_response("నమస్కారం! నువ్వు ఎవరు?"))
    pass
