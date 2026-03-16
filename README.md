# Mini Telugu Voice Assistant

A conversational AI assistant that understands Telugu speech and responds in Telugu.

## Features
- **Voice Input**: Captures audio from the microphone with silence detection.
- **Speech-to-Text**: Transcription using Google Web Speech API.
- **AI Understanding**: Natural language processing via Google Gemini 1.5 Flash.
- **Text-to-Speech**: Natural sounding Telugu voices using Microsoft Edge TTS.
- **Audio Playback**: Automatic playback of generated responses using Pygame.

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
   - Add your `GEMINI_API_KEY`.

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
- **STT**: Google Web Speech API (via `SpeechRecognition`)
- **LLM**: Google Gemini 1.5 Flash
- **TTS**: Microsoft Edge TTS (`edge-tts`)
- **Playback**: Pygame
