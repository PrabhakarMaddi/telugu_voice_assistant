from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize Gemini Client
api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    try:
        client = genai.Client(api_key=api_key)
        # Create a chat session
        chat_session = client.chats.create(model="gemini-1.5-flash")
    except Exception as e:
        print(f"Error initializing Gemini: {e}")
        chat_session = None
else:
    chat_session = None

def generate_response(user_text):
    """
    Generates a Telugu response using Google Gemini 1.5 Flash (Free Tier)
    with conversation history support using the new google-genai SDK.
    """
    if not chat_session:
        return "Error: Gemini API key not found or client initialization failed."

    try:
        system_instruction = (
            "You are a helpful assistant that speaks Telugu. "
            "Always respond in clear, natural Telugu. Keep responses concise. "
            "If the user asks who you are, say you are a Telugu Voice Assistant."
        )
        
        # In the new SDK, we can't easily prepend the first message to a chat object
        # but we can set config or just ensure the context is clear.
        # For simplicity, if history is empty, we'll prefix.
        
        prompt = user_text
        # Access history via chat_session.list_messages() or check internal state
        # For this SDK, the history is maintained by the chat object.
        
        # If it's the first message, add system context
        if not chat_session._curated_history: # Internal hint or just use a flag
             prompt = f"{system_instruction}\n\nUser: {user_text}"

        response = chat_session.send_message(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Gemini error: {str(e)}"

if __name__ == "__main__":
    # Test
    # print(generate_response("నమస్కారం! నువ్వు ఎవరు?"))
    pass
