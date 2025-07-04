import os
import pygame
from gtts import gTTS
import pyttsx3

# ✅ Create output folder if it doesn't exist
OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ✅ Audio Player for gTTS files
def play_audio(filepath):
    try:
        pygame.mixer.init()
        pygame.mixer.music.load(filepath)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            continue
    except Exception as e:
        print(f"⚠️ Error playing audio: {e}")

# ✅ Google TTS (Online)
def text_to_speech_with_gtts(input_text, output_filename):
    output_filepath = os.path.join(OUTPUT_DIR, output_filename)

    # Remove old file if it exists
    if os.path.exists(output_filepath):
        os.remove(output_filepath)

    try:
        audio = gTTS(text=input_text, lang="en", slow=False)
        audio.save(output_filepath)
        print(f"🎤 gTTS Audio saved as {output_filepath}")
        play_audio(output_filepath)
    except Exception as e:
        print(f"❌ gTTS error: {e}")

# ✅ pyttsx3 TTS (Offline)
def text_to_speech_with_pyttsx3(input_text):
    try:
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)     # Speaking speed
        engine.setProperty('volume', 1.0)   # Volume (0.0 to 1.0)
        print("🎤 pyttsx3 is now speaking...")
        engine.say(input_text)
        engine.runAndWait()
    except Exception as e:
        print(f"❌ pyttsx3 error: {e}")

        import os
import pyttsx3
import pygame
from gtts import gTTS

def text_to_speech_with_gtts(input_text, output_filepath):
    try:
        tts = gTTS(text=input_text, lang="en", slow=False)
        tts.save(output_filepath)
        print(f"🎤 gTTS Audio saved as {output_filepath}")
    except Exception as e:
        print(f"⚠️ gTTS Error: {e}")

def text_to_speech_with_pyttsx3(input_text):
    try:
        engine = pyttsx3.init()
        # 🐢 Slow down the speech rate (default is ~200 words per minute)
        current_rate = engine.getProperty('rate')
        engine.setProperty('rate', 140)  # You can adjust this to 120–160 as needed

        # 🔊 Optionally, set voice (male/female)
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[1].id)  # voices[0] = male, voices[1] = female (depends on system)
        engine.say(input_text)
        engine.runAndWait()
        print("🎤 pyttsx3 is now speaking...")
    except Exception as e:
        print(f"⚠️ pyttsx3 Error: {e}")


# ✅ Main Program
if __name__ == "__main__":
    input_text_gtts = "Hello! This is the AI voice using Google TTS."
    input_text_pyttsx3 = "Hello! This is the AI voice using pyttsx3 offline."

    # Run both
    text_to_speech_with_gtts(input_text_gtts, "gtts_output.mp3")
    text_to_speech_with_pyttsx3(input_text_pyttsx3)
