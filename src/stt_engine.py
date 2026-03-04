import speech_recognition as sr
import os

def transcribe_audio(audio_file_path):
    """
    Transcribes audio file to Telugu text using Google Web Speech API (Free).
    """
    recognizer = sr.Recognizer()
    
    if not os.path.exists(audio_file_path):
        return "Error: Audio file not found."

    try:
        with sr.AudioFile(audio_file_path) as source:
            audio_data = recognizer.record(source)
            # Use Google Web Speech API (no key required for limited use)
            text = recognizer.recognize_google(audio_data, language="te-IN")
            return text
    except sr.UnknownValueError:
        return "Error: Could not understand audio."
    except sr.RequestError as e:
        return f"Error: Could not request results from Google Speech Recognition service; {e}"
    except Exception as e:
        return f"Transcription error: {str(e)}"

if __name__ == "__main__":
    # Test
    # print(transcribe_audio("audio/input/test.wav"))
    pass
