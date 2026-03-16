import importlib
import sys

def check_dependencies():
    required = [
        "sounddevice", "numpy", "scipy", "edge_tts", 
        "google.generativeai", "speech_recognition", 
        "pygame", "dotenv"
    ]
    
    print(f"Python version: {sys.version}")
    print(f"Python executable: {sys.executable}")
    print("-" * 30)
    
    missing = []
    for lib in required:
        try:
            importlib.import_module(lib)
            print(f"✅ {lib} is installed.")
        except ImportError:
            print(f"❌ {lib} is MISSING!")
            missing.append(lib)
            
    if missing:
        print("-" * 30)
        print(f"Please install missing libraries using: pip install -r requirements.txt")
    else:
        print("-" * 30)
        print("All dependencies are correctly installed!")

if __name__ == "__main__":
    check_dependencies()
