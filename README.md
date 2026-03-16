# Mini Telugu Voice Assistant

A conversational AI assistant that understands Telugu speech and responds in Telugu.

## Features
- **Intelligent Voice Input**: Captures audio using `sounddevice` with dynamic silence detection, a grace period to wait for speech, and a minimum recording duration for reliability.
- **Robust Speech-to-Text**: High-accuracy transcription using Google Web Speech API, with 16-bit PCM audio encoding for maximum compatibility.
- **Conversational AI**: Context-aware natural language processing via Google Gemini 1.5 Flash. It remembers previous turns for a fluid experience.
- **Natural Text-to-Speech**: Professional sounding Telugu voices using Microsoft Edge TTS (Shruti Neural).
- **Auto Audio Playback**: Instant playback of generated responses using Pygame.

## Setup

1. **Clone the repository**:
   ```bash
   git clone "https://github.com/PrabhakarMaddi/telugu_voice_assistant.git"
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
- `src/`: Core Python modules (`recorder.py`, `stt_engine.py`, `llm_engine.py`, etc.).
- `audio/`: Temporary audio storage for input and output.
- `main.py`: Main entry point with interactive CLI.
- `requirements.txt`: Python dependencies.

## Technical Details
- **STT**: Google Web Speech API (via `SpeechRecognition`)
- **LLM**: Google Gemini 1.5 Flash (`gemini-flash-latest`)
- **TTS**: Microsoft Edge TTS (`edge-tts`)
- **Playback**: Pygame
- **Audio Processing**: 16-bit PCM conversion via `numpy` and `scipy`.
