import asyncio
import edge_tts
import os

async def _text_to_speech_async(text, output_file_path):
    """
    Internal async function for edge-tts.
    """
    # Professional Telugu female voice: te-IN-ShrutiNeural
    # Professional Telugu male voice: te-IN-MohanNeural
    voice = "te-IN-ShrutiNeural" 
    
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_file_path)

def text_to_speech(text, output_file_path):
    """
    Converts Telugu text to speech using Microsoft Edge TTS (Free).
    Synchronous wrapper for main.py integration.
    """
    try:
        # Ensure directory exists
        os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
        
        # Run the async function in a sync block
        asyncio.run(_text_to_speech_async(text, output_file_path))
        return output_file_path
    except Exception as e:
        return f"TTS error: {str(e)}"

if __name__ == "__main__":
    # Test
    # text_to_speech("నమస్కారం", "audio/output/test.mp3")
    pass
