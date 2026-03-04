from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

def transcribe_audio(audio_file_path):
    """
    Transcribes audio file to Telugu text using OpenAI Whisper.
    """
    client = OpenAI() # Assumes OPENAI_API_KEY is in environment or .env
    
    if not os.path.exists(audio_file_path):
        return "Error: Audio file not found."

    try:
        with open(audio_file_path, "rb") as audio_file:
            transcription = client.audio.transcriptions.create(
                model="whisper-1", 
                file=audio_file,
                language="te"  # Explicitly set to Telugu
            )
        return transcription.text
    except Exception as e:
        return f"Transcription error: {str(e)}"

if __name__ == "__main__":
    # Test (requires an actual file and API key)
    # print(transcribe_audio("audio/input/test.wav"))
    pass
