import sys
import os
from fastapi import FastAPI, Depends, HTTPException, status, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import shutil

# Add current and src to path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(current_dir)
sys.path.append(os.path.join(parent_dir, "src"))

from database import engine, get_db, init_db, User, Conversation
from auth import get_current_user, create_access_token, verify_password, get_password_hash
from llm_engine import generate_response
from text_to_speech import text_to_speech
from stt_engine import transcribe_audio

app = FastAPI()

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event():
    init_db()
    # Ensure audio directories exist
    os.makedirs("audio/input", exist_ok=True)
    os.makedirs("audio/output", exist_ok=True)

@app.post("/register")
def register(user: dict, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user["username"]).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    hashed_password = get_password_hash(user["password"])
    new_user = User(username=user["username"], hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    return {"message": "User created successfully"}

@app.post("/token")
def login(form_data: dict, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data["username"]).first()
    if not user or not verify_password(form_data["password"], user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/me")
def read_users_me(current_user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == current_user).first()
    return {"username": user.username, "preferred_voice": user.preferred_voice}

@app.post("/settings/voice")
def update_voice(voice_data: dict, current_user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == current_user).first()
    user.preferred_voice = voice_data["voice"]
    db.commit()
    return {"message": "Voice updated"}

@app.post("/chat")
async def chat(payload: dict, current_user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    user_text = payload.get("text")
    user = db.query(User).filter(User.username == current_user).first()
    
    # Fetch recent history for context (last 5 exchanges)
    recent_db_history = db.query(Conversation).filter(
        Conversation.user_id == user.id
    ).order_by(Conversation.timestamp.desc()).limit(5).all()
    
    # Format history for Gemini: [{'role': 'user', 'parts': ['...']}, {'role': 'model', 'parts': ['...']}]
    # We reverse it to be in chronological order
    gemini_history = []
    for conv in reversed(recent_db_history):
        gemini_history.append({"role": "user", "parts": [conv.user_text]})
        gemini_history.append({"role": "model", "parts": [conv.assistant_text]})
    
    # 1. Generate LLM response
    assistant_text = generate_response(user_text, history=gemini_history)
    
    # 2. Save to history
    conversation = Conversation(
        user_id=user.id,
        user_text=user_text,
        assistant_text=assistant_text
    )
    db.add(conversation)
    db.commit()
    
    # 3. Generate Audio
    output_audio = f"audio/output/resp_{user.username}_{datetime.now().timestamp()}.mp3"
    text_to_speech(assistant_text, output_audio, voice=user.preferred_voice)
    
    return {
        "user_text": user_text,
        "assistant_text": assistant_text,
        "audio_url": f"/audio/{os.path.basename(output_audio)}"
    }

@app.get("/history")
def get_history(current_user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == current_user).first()
    
    # Task: Store only last 10 days
    ten_days_ago = datetime.utcnow() - timedelta(days=10)
    
    # Cleanup old conversations
    db.query(Conversation).filter(Conversation.timestamp < ten_days_ago).delete()
    db.commit()
    
    history = db.query(Conversation).filter(
        Conversation.user_id == user.id,
        Conversation.timestamp >= ten_days_ago
    ).order_by(Conversation.timestamp.desc()).all()
    
    return history

# To serve audio files
from fastapi.staticfiles import StaticFiles
app.mount("/audio", StaticFiles(directory="audio/output"), name="audio")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
