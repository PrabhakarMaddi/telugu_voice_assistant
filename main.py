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
    
    if not os.getenv("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY not found in .env file.")
        print("Please copy .env.example to .env and add your API key.")
        return

    # Paths
    input_audio = os.path.join("audio", "input", "user_query.wav")
    output_audio = os.path.join("audio", "output", "assistant_response.mp3")

    print("--- Mini Telugu Voice Assistant ---")
    print("Type 'exit' to quit or press Enter to start speaking.")

    while True:
        cmd = input("\nPress Enter to record (or 'exit' to quit): ").strip().lower()
        if cmd == 'exit':
            break

        try:
            # 1. Record
            print("\nListening...")
            record_audio(input_audio, duration=5)

            # 2. STT
            print("Processing speech...")
            user_text = transcribe_audio(input_audio)
            print(f"You said: {user_text}")

            if "Error" in user_text:
                print(user_text)
                continue

            # 3. LLM
            print("Thinking...")
            assistant_text = generate_response(user_text)
            print(f"Assistant: {assistant_text}")

            # 4. TTS
            print("Generating speech...")
            text_to_speech(assistant_text, output_audio)

            # 5. Playback
            print("Playing response...")
            play_audio(output_audio)

        except KeyboardInterrupt:
            print("\nStopped.")
            break
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
