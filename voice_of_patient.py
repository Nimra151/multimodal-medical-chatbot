import logging
import speech_recognition as sr
from pydub import AudioSegment
from io import BytesIO
import time
import os
from groq import Groq

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def record_audio(file_path, timeout=20, phrase_time_limit=None, max_retries=3):
    """
    Function to record audio from the microphone and save it as an MP3 file, with retry attempts on failure.
    """
    recognizer = sr.Recognizer()
    retries = 0
    
    while retries < max_retries:
        try:
            with sr.Microphone() as source:
                logging.info("Adjusting for ambient noise...")
                recognizer.adjust_for_ambient_noise(source, duration=1)
                logging.info("Start speaking now...")

                # Record the audio
                audio_data = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
                logging.info("Recording complete.")

                # Convert the recorded audio to an MP3 file
                wav_data = audio_data.get_wav_data()
                audio_segment = AudioSegment.from_wav(BytesIO(wav_data))
                audio_segment.export(file_path, format="mp3", bitrate="128k")

                logging.info(f"Audio saved to {file_path}")
                return  # Exit function successfully after recording

        except sr.WaitTimeoutError:
            logging.error("No speech detected within the timeout period. Retrying...")
        
        except sr.RequestError:
            logging.error("Could not connect to the recognition service. Retrying...")
        
        except sr.UnknownValueError:
            logging.error("Speech recognition could not understand the audio. Retrying...")

        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}. Retrying...")

        retries += 1
        time.sleep(2)  # Wait before retrying

    logging.error("Max retries reached. Could not record audio.")

if __name__ == "__main__":
    file_path = "patient_voice_test_for_patient.mp3"
    record_audio(file_path)

# ✅ Check if the audio file exists before proceeding
audio_filepath = "patient_voice_test_for_patient.mp3"
if not os.path.exists(audio_filepath):
    raise FileNotFoundError(f"Error: The file '{audio_filepath}' was not found. Ensure Step 1 completed successfully.")

# ✅ Load API Key safely
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("Error: GROQ_API_KEY is not set. Please configure your environment variables.")

def transcribe_with_groq(stt_model, audio_filepath, GROQ_API_KEY):
    """
    Function to transcribe audio using Groq API.
    """
    client = Groq(api_key=GROQ_API_KEY)

    with open(audio_filepath, "rb") as audio_file:
        transcription = client.audio.transcriptions.create(
            model=stt_model,
            file=audio_file,
            language="en"
        )

    return transcription.text

# ✅ Define the model name
stt_model = "whisper-large-v3"

# ✅ Call the transcription function
transcribed_text = transcribe_with_groq(stt_model, audio_filepath, GROQ_API_KEY)

# ✅ Print the transcribed text
print("Transcription:", transcribed_text)
