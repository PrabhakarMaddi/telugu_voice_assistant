import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import os
import time

def record_audio(filename, max_duration=10, silence_threshold=0.005, silence_duration=1.5, fs=44100, min_duration=2.0, grace_period=1.5):
    """
    Records audio until silence is detected or max_duration is reached.
    Includes a grace period where silence is ignored and a minimum recording duration.
    Saves as 16-bit PCM WAV for compatibility.
    """
    print(f"Recording... (Min: {min_duration}s, Max: {max_duration}s, Grace: {grace_period}s)")
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    recording = []
    silent_chunks = 0
    max_silent_chunks = int(silence_duration / 0.1)
    
    def callback(indata, frames, time, status):
        # Calculate volume
        volume_norm = np.linalg.norm(indata) / np.sqrt(len(indata))
        recording.append(indata.copy())
        
        nonlocal silent_chunks
        if volume_norm < silence_threshold:
            silent_chunks += 1
        else:
            silent_chunks = 0

    with sd.InputStream(samplerate=fs, channels=1, callback=callback):
        start_time = time.time()
        while True:
            elapsed_time = time.time() - start_time
            
            # Reset silent chunks if within grace period
            if elapsed_time < grace_period:
                silent_chunks = 0
                
            # Only stop if past min_duration AND silence detected OR max_duration reached
            if elapsed_time > min_duration and silent_chunks > max_silent_chunks:
                print("Silence detected, stopping...")
                break
            if elapsed_time > max_duration:
                print("Max duration reached, stopping...")
                break
                
            time.sleep(0.1)
            
    # Concatenate all chunks
    audio_data = np.concatenate(recording, axis=0)
    
    # Convert to 16-bit PCM (CRITICAL for SpeechRecognition)
    audio_int16 = (audio_data * 32767).astype(np.int16)
    
    # Save as WAV file
    wav.write(filename, fs, audio_int16)
    print(f"Recording saved to {filename}")

if __name__ == "__main__":
    # Test recording
    test_file = os.path.join("audio", "input", "test_refined.wav")
    record_audio(test_file)
