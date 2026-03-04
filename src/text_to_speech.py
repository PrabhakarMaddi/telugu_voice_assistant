from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

def text_to_speech(text, output_file_path):
    """
    Converts Telugu text to speech using OpenAI TTS.
    """
    client = OpenAI()
    
    try:
        # Ensure directory exists
        os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
        
        response = client.audio.speech.create(
            model="tts-1",
            voice="shimmer",  # Or 'alloy', 'fable', etc.
            input=text
        )
        response.stream_to_file(output_file_path)
        return output_file_path
    except Exception as e:
        return f"TTS error: {str(e)}"

if __name__ == "__main__":
    # Test (requires API key)
    # text_to_speech("నమస్కారం", "audio/output/test.mp3")
    pass
