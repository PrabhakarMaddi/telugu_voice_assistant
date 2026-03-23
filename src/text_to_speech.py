import edge_tts
import os

async def text_to_speech(text, output_file_path, voice="te-IN-ShrutiNeural"):
    """
    Converts Telugu text to speech using Microsoft Edge TTS (Free).
    Asynchronous version for FastAPI integration.
    """
    try:
        # Ensure directory exists
        os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
        
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(output_file_path)
        return output_file_path
    except Exception as e:
        print(f"TTS error: {str(e)}")
        return None
