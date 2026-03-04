import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import os
import time

def record_audio(filename, duration=5, fs=44100):
    """
    Simple audio recorder. 
    Eventually we can add silence detection.
    """
    print(f"Recording for {duration} seconds...")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()  # Wait until recording is finished
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    # Save as WAV file
    wav.write(filename, fs, recording)
    print(f"Recording saved to {filename}")

if __name__ == "__main__":
    # Test recording
    test_file = os.path.join("audio", "input", "test.wav")
    record_audio(test_file)
