import io
import requests
import streamlit as st

from pydub import AudioSegment

CHUNK_SIZE = 1024

def tts(id, text):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{id}"

    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": st.session_state['el_token']
    }

    data = {
        "text": text,
        "model_id": "eleven_multilingual_v1",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.5
        }
    }

    response = requests.post(url, json=data, headers=headers)

    if response.ok:
        audio_content = io.BytesIO(response.content)
        return AudioSegment.from_file(audio_content)