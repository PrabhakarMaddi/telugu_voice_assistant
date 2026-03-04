import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import time

def play_audio(file_path):
    """
    Plays an MP3 or WAV file using pygame.
    """
    if not os.path.exists(file_path):
        print(f"Error: Playback file not found: {file_path}")
        return

    try:
        pygame.mixer.init()
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()
        
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)
        
        pygame.mixer.quit()
    except Exception as e:
        print(f"Playback error: {str(e)}")

if __name__ == "__main__":
    # Test (requires an actual file)
    # play_audio("audio/output/test.mp3")
    pass
