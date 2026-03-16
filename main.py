import os
import sys
from dotenv import load_dotenv

# Add src to path
sys.path.append(os.path.join(os.getcwd(), "src"))

from recorder import record_audio
from stt_engine import transcribe_audio
from llm_engine import generate_response
from text_to_speech import text_to_speech
from playback import play_audio

def main():
    load_dotenv()
    
    if not os.getenv("GEMINI_API_KEY"):
        print("\n[!] Error: GEMINI_API_KEY not found in .env file.")
        print("Please add your Google AI API key to .env.")
        return

    # Ensure audio directories exist
    base_dir = os.path.dirname(os.path.abspath(__file__))
    input_dir = os.path.join(base_dir, "audio", "input")
    output_dir = os.path.join(base_dir, "audio", "output")
    os.makedirs(input_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)
    

    input_audio = os.path.join(input_dir, "user_query.wav")
    output_audio = os.path.join(output_dir, "assistant_response.mp3")

    print("\n" + "="*40)
    print("   Mini Telugu Voice Assistant")
    print("="*40)
    print("Commands: 'exit' to quit, press Enter to record.")

    while True:
        try:
            cmd = input("\n> Press Enter to speak (or type 'exit'): ").strip().lower()
            if cmd == 'exit':
                print("Goodbye! సెలవు!")
                break

            # 1. Record
            print("\n[Listening...] Speaking now...")
            record_audio(input_audio, max_duration=10)

            # 2. STT
            print("[Processing speech...]")
            user_text = transcribe_audio(input_audio)
            
            if "Error" in user_text:
                print(f"STT Feedback: {user_text}")
                continue
            
            print(f"User: {user_text}")

            # 3. LLM
            print("[Assistant is thinking...]")
            assistant_text = generate_response(user_text)
            
            if "Error" in assistant_text:
                print(f"LLM Feedback: {assistant_text}")
                continue
            
            print(f"Assistant: {assistant_text}")

            # 4. TTS
            print("[Generating response audio...]")
            tts_result = text_to_speech(assistant_text, output_audio)
            
            if "Error" in tts_result:
                print(f"TTS Feedback: {tts_result}")
                continue

            # 5. Playback
            print("[Playing response...]")
            play_audio(output_audio)

        except KeyboardInterrupt:
            print("\n[Stopped by user]")
            break
        except Exception as e:
            print(f"\n[!] An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
