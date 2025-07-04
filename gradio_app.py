import os
import uuid
import gradio as gr
from brain_of_the_doctor import encode_image, analyze_image_with_query
from voice_of_patient import transcribe_with_groq
from voice_of_the_doctor import text_to_speech_with_gtts, text_to_speech_with_pyttsx3

# Check if API Key is set
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("❌ GROQ_API_KEY is missing. Please set it in your environment.")

# Doctor prompt
system_prompt = """You have to act as a professional doctor, I know you are not, but this is for learning purposes.
            What's in this image? Do you find anything wrong with it medically? 
            If you make a differential, suggest some remedies for them. Do not add any numbers or special characters in 
            your response. Your response should be in one long paragraph. Also, always answer as if you are answering a real person.
            Do not say 'In the image I see' but say 'With what I see, I think you have ....'
            Don't respond as an AI model in markdown, your answer should mimic that of an actual doctor, not an AI bot. 
            Keep your answer concise (max 2 sentences). No preamble, start your answer right away, please."""

# Main logic
def process_inputs(audio_filepath, image_filepath):
    try:
        # Step 1: Convert Speech to Text
        transcription = transcribe_with_groq(
            GROQ_API_KEY=GROQ_API_KEY,
            audio_filepath=audio_filepath,
            stt_model="whisper-large-v3"
        )

        # Step 2: Analyze image (optional)
        if image_filepath:
            encoded_image = encode_image(image_filepath)
            doctor_response = analyze_image_with_query(
                query=system_prompt + transcription,
                encoded_image=encoded_image,
                model="meta-llama/llama-4-scout-17b-16e-instruct"
            )
        else:
            doctor_response = "No image provided for me to analyze."

        # Step 3: Convert doctor's response to speech
        audio_output_path = f"doctor_response_{uuid.uuid4().hex}.mp3"
        text_to_speech_with_gtts(input_text=doctor_response, output_filepath=audio_output_path)

        # Step 4: Also speak out loud using pyttsx3 (offline)
        text_to_speech_with_pyttsx3(doctor_response)

        # Final Output
        return transcription, doctor_response, audio_output_path

    except Exception as e:
        return f"❌ Error: {e}", "Something went wrong.", None

# Gradio Interface
iface = gr.Interface(
    fn=process_inputs,
    inputs=[
        gr.Audio(sources=["microphone"], type="filepath", label="Speak your symptoms"),
        gr.Image(type="filepath", label="Upload medical image (optional)")
    ],
    outputs=[
        gr.Textbox(label="Speech to Text"),
        gr.Textbox(label="Doctor's Response"),
        gr.Audio(label="Doctor's Voice Reply")
    ],
    title="AI Doctor 2.0: Vision + Voice"
)

iface.launch(debug=True)

