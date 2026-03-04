# Mini Telugu Voice Assistant

A conversational AI assistant that understands Telugu speech and responds in Telugu.

## Features
- **Voice Input**: Captures audio from the microphone.
- **Speech-to-Text**: High-accuracy transcription using OpenAI Whisper.
- **AI Understanding**: Natural language processing via GPT-4o.
- **Text-to-Speech**: Natural sounding Telugu voices using OpenAI TTS.
- **Audio Playback**: Automatic playback of generated responses.

## Setup

1. **Clone the repository**:
   ```bash
   git clone <your-repo-url>
   cd telugu_voice_assistant
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment Variables**:
   - Copy `.env.example` to `.env`.
   - Add your `OPENAI_API_KEY`.

4. **Run the Assistant**:
   ```bash
   python main.py
   ```

## Folder Structure
- `src/`: Core Python modules.
- `audio/`: Temporary audio storage.
- `main.py`: Main entry point.
- `requirements.txt`: Python dependencies.

## Technical Details
- **STT**: OpenAI Whisper (`whisper-1`)
- **LLM**: OpenAI GPT-4o
- **TTS**: OpenAI TTS (`tts-1`)
- **Playback**: Pygame
