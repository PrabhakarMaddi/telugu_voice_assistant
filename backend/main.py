import sys
import os
from contextlib import asynccontextmanager
from typing import List, Optional
from pydantic import BaseModel, ConfigDict
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone

# Add current and src to path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(current_dir)
sys.path.append(os.path.join(parent_dir, "src"))

from database import engine, get_db, init_db, User, Conversation
from auth import get_current_user, create_access_token, verify_password, get_password_hash
from llm_engine import generate_response
from text_to_speech import text_to_speech

# Pydantic Models
class UserCreate(BaseModel):
    username: str
    password: str

class VoiceUpdate(BaseModel):
    voice: str

class ChatPayload(BaseModel):
    text: str

class ConversationResponse(BaseModel):
    id: int
    user_text: str
    assistant_text: str
    audio_url: Optional[str] = None
    timestamp: datetime

    model_config = ConfigDict(from_attributes=True)

class ReplayPayload(BaseModel):
    text: str

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    os.makedirs(os.path.join(parent_dir, "audio", "input"), exist_ok=True)
    os.makedirs(os.path.join(parent_dir, "audio", "output"), exist_ok=True)
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    return {"status": "ok", "version": "1.1", "features": ["history_replay"]}

@app.post("/register")
async def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    hashed_password = get_password_hash(user.password)
    new_user = User(username=user.username, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    return {"message": "User created successfully"}

@app.post("/token")
async def login(user_data: UserCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == user_data.username).first()
    if not user or not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/me")
async def read_users_me(current_user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == current_user).first()
    return {"username": user.username, "preferred_voice": user.preferred_voice}

@app.post("/settings/voice")
async def update_voice(voice_data: VoiceUpdate, current_user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == current_user).first()
    user.preferred_voice = voice_data.voice
    db.commit()
    return {"message": "Voice updated"}

@app.post("/chat")
async def chat(payload: ChatPayload, current_user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == current_user).first()
    
    recent_db_history = db.query(Conversation).filter(
        Conversation.user_id == user.id
    ).order_by(Conversation.timestamp.desc()).limit(5).all()
    
    gemini_history = []
    for conv in reversed(recent_db_history):
        gemini_history.append({"role": "user", "parts": [conv.user_text]})
        gemini_history.append({"role": "model", "parts": [conv.assistant_text]})
    
    assistant_text = generate_response(payload.text, history=gemini_history)
    
    output_filename = f"resp_{user.username}_{int(datetime.now(timezone.utc).timestamp())}.mp3"
    # Use absolute path for output to ensure it saves in the project root's audio folder
    output_path = os.path.join(parent_dir, "audio", "output", output_filename)
    audio_url = f"/audio/{output_filename}"
    
    # Properly await the async TTS function
    await text_to_speech(assistant_text, output_path, voice=user.preferred_voice)
    
    conversation = Conversation(
        user_id=user.id,
        user_text=payload.text,
        assistant_text=assistant_text,
        audio_url=audio_url,
        timestamp=datetime.now(timezone.utc)
    )
    db.add(conversation)
    db.commit()
    
    return {
        "user_text": payload.text,
        "assistant_text": assistant_text,
        "audio_url": audio_url
    }

@app.get("/history", response_model=List[ConversationResponse])
async def get_history(current_user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == current_user).first()
    
    ten_days_ago = datetime.now(timezone.utc) - timedelta(days=10)
    db.query(Conversation).filter(Conversation.timestamp < ten_days_ago).delete()
    db.commit()
    
    # Cleanup old audio files on disk
    try:
        audio_dir = os.path.join(parent_dir, "audio", "output")
        if os.path.exists(audio_dir):
            for f in os.listdir(audio_dir):
                if f.endswith(".mp3"):
                    file_path = os.path.join(audio_dir, f)
                    if os.path.getmtime(file_path) < ten_days_ago.timestamp():
                        os.remove(file_path)
    except Exception as e:
        print(f"Disk cleanup error: {e}")
    
    history = db.query(Conversation).filter(
        Conversation.user_id == user.id,
        Conversation.timestamp >= ten_days_ago
    ).order_by(Conversation.timestamp.desc()).all()
    
    return history

@app.post("/chat/replay")
async def replay_audio(payload: ReplayPayload, current_user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == current_user).first()
    output_filename = f"replay_{user.username}_{int(datetime.now(timezone.utc).timestamp())}.mp3"
    output_path = os.path.join(parent_dir, "audio", "output", output_filename)
    await text_to_speech(payload.text, output_path, voice=user.preferred_voice)
    return {"audio_url": f"/audio/{output_filename}"}

# Use absolute path for mounting static files
audio_output_dir = os.path.join(parent_dir, "audio", "output")
os.makedirs(audio_output_dir, exist_ok=True)
app.mount("/audio", StaticFiles(directory=audio_output_dir), name="audio")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
