import speech_recognition as sr
import openai
from gtts import gTTS
import requests
import os
import streamlit as st
import pyaudio
import wave
from apikey import apikey

# Define your OpenAI API key
openai.api_key = apikey
 

 
def capture_live_audio():
    # Define audio parameters
    format = pyaudio.paInt16
    channels = 1
    sample_rate = 44100  # You can adjust this as needed
    chunk = 1024  # Adjust the chunk size as needed

    audio = pyaudio.PyAudio()

    # Open a stream
    stream = audio.open(format=format,
                        channels=channels,
                        rate=sample_rate,
                        input=True,
                        frames_per_buffer=chunk)

    print("Capturing audio... Press Ctrl+c to stop recording.")

    frames = []

    try:
        while True:
            data = stream.read(chunk)
            frames.append(data)
    except KeyboardInterrupt:
        print("Recording stopped.")

    stream.stop_stream()
    stream.close()
    audio.terminate()

    # Save the captured audio to a WAV file for later use, if needed
    with wave.open("live_audio.wav", 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(audio.get_sample_size(format))
        wf.setframerate(sample_rate)
        wf.writeframes(b''.join(frames))

    return b''.join(frames)

# Add this code to your main() function
live_audio = capture_live_audio()

def audio_to_text(audio_path):
    # Initialize the recognizer
    recognizer = sr.Recognizer()
    
    with sr.AudioFile(audio_path) as source:
        audio = recognizer.record(source)
    
    # Convert audio to text
    text = recognizer.recognize_google(audio)
    
    return text

def chat_with_gpt(text):
    # Send text to ChatGPT
    response = openai.Completion.create(
        engine = "text-davinci-002",
        prompt = text,
        max_tokens = 100,
    )
    
    return response.choices[0].text

def text_to_audio(text, audio_path):
    tts = gTTS(text)
    audio_path = os.path.expanduser("C:\Coding\Python VS")  # Get the user's home directory
    audio_path = os.path.join(audio_path, "output.mp3")  # Set the output file name
    tts.save(audio_path)



def main(input_type, input_data, output_type, output_path):
    if input_type == 'audio':
        # Convert audio to text
        text = audio_to_text(input_data)
    elif input_type == 'text':
        text = input_data
    else:
        print("Invalid input type")
        return

    # Chat with GPT
    gpt_response = chat_with_gpt(text)

    if output_type == 'text':
        # Save GPT response as a text file
        with open(output_path, 'w') as file:
            file.write(gpt_response)
    elif output_type == 'audio':
        # Convert GPT response to audio
        text_to_audio(gpt_response, output_path)
    else:
        print("Invalid output type")

if __name__ == "__main__":
    
    input_type = input("Enter input type (audio or text): ").lower()
    input_data = input("Enter audio file path or text: ")
    output_type = input("Enter output type (text or audio): ").lower()
    output_path = input("Enter output file path: ")

    main(input_type, input_data, output_type, output_path)





