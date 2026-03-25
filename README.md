# 🎙️ Mini Telugu Voice Assistant

A sophisticated, bilingual AI assistant that seamlessly interacts in Telugu. This project features both a direct **CLI-based Voice Assistant** and a modern **Web-based Dashboard** with persistent chat history.

---

## 🚀 Two Ways to Interact

### 1. 🖥️ CLI Voice Assistant (`main.py`)
A fast, lightweight interface for direct voice conversations.
- **Instant Response**: Captures audio, transcribes, processes via Gemini, and speaks back.
- **Silence Detection**: Automatically stops recording when you stop speaking.
- **Minimal Latency**: Optimized for real-time voice feedback.

### 2. 🌐 Web Assistant Dashboard (FastAPI + React)
A full-featured web application for managed conversations.
- **User Authentication**: Secure login and registration.
- **Voice Selection**: Choose between multiple professional Telugu voices (e.g., Shruti Neural).
- **Chat History**: Persistent storage of previous conversations using SQLite (SQLAlchemy).
- **History Replay**: Re-generate and play audio for any past message.
- **Modern UI**: Sleek, responsive design built with TailwindCSS.

---

## 🛠️ Tech Stack

| Component | Technology |
| :--- | :--- |
| **LLM (Brain)** | Google Gemini 1.5 Flash |
| **STT (Ear)** | Google Web Speech API (via SpeechRecognition) |
| **TTS (Voice)** | Microsoft Edge TTS (Shruti Neural) |
| **Backend** | Python, FastAPI, SQLAlchemy, Uvicorn |
| **Frontend** | React, Vite, TailwindCSS, Axios |
| **Database** | SQLite |
| **Audio** | Pygame (CLI), HTML5 Audio (Web) |

---

## ⚙️ Setup Instructions

### 1. Prerequisites
- Python 3.9+
- Node.js 18+
- [Google AI (Gemini) API Key](https://aistudio.google.com/)

### 2. General Setup
```bash
# Clone the repository
git clone "https://github.com/PrabhakarMaddi/telugu_voice_assistant.git"
cd telugu_voice_assistant

# Configure Environment
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY
```

### 3. CLI Assistant Setup
```bash
pip install -r requirements.txt
python main.py
```

### 4. Web Assistant Setup

**Backend:**
```bash
cd backend
pip install -r ../requirements.txt  # Shared dependencies
python main.py
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

---

## 📁 Project Structure
- `src/`: Core logic (recorder, STT, LLM, TTS).
- `backend/`: FastAPI server with auth and history management.
- `frontend/`: React components and dashboard UI.
- `audio/`: Local storage for generated voice responses.
- `main.py`: Entry point for the CLI assistant.

---

## 📝 License
MIT License. Feel free to use and contribute!
