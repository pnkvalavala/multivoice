import os
import json
import librosa
import requests
import streamlit as st

from utils import init_session_state, voice_clone
from credentials import credentials
from audio_handler import extract_audio

init_session_state()

st.set_page_config(
    page_title="Multivoice",
    page_icon="🎬",
    initial_sidebar_state="expanded",
    menu_items={
        'Report a bug': "https://github.com/pnkvalavala/Multivoice/issues",
        'About': "Multivoice is an innovative project designed to enhance the viewing experience of foreign-language movies and TV shows. We understand that language barriers can sometimes hinder the enjoyment of captivating content. That's why Multivoice offers a unique solution: personalized dubbed versions for each user."
    }
)

st.markdown(
    "<h1 style='text-align: center;'>Multivoice</h1>",
    unsafe_allow_html=True
)


credentials()

if st.session_state["auth_ok"]:

    st.session_state['json_file'] = st.file_uploader("Only JSON format of [this](https://github.com/pnkvalavala/Multivoice/blob/main/data/dialogues.json) structure is supported for now", type=["json"])

    st.session_state['audio_file'] = st.file_uploader("Upload audio file for voice cloning", type=["mp3", "wav"])

    with st.spinner('Generating individual voice clones'):
        voice_clone()
        if st.session_state['audio_file'] and st.session_state['json_file']:
            extract_audio(
                st.session_state['audio_file'], 
                json.load(st.session_state['json_file']), 
                st.session_state['voice_clone_dir']
            )

    audio_files = os.listdir('voice_clones/')

    voices = {}

    # Cloning voice
    for f in audio_files:
        filepath = os.path.join('voice_clones/', f)
        duration = librosa.get_duration(filename=filepath)

        with st.spinner(f'Cloning {f.rsplit(".", 1)[0]} Voice'):
            add_url = "https://api.elevenlabs.io/v1/voices/add"
            headers = {
                "Accept": "application/json",
                "xi-api-key": st.session_state['el_token']
            }

            data = {
                'name': f,
                'labels': '{"accent": "American"}',
                'description': f'Cloned from {f}'
            }

            files = [
                ('files', (f, open(filepath, 'rb'), 'audio/mpeg'))
            ]

            response = requests.post(add_url, headers=headers, data=data, files=files)
            cloned_voice_id = response.json()['voice_id']
        
            voices[f.rsplit(".", 1)[0]] = cloned_voice_id
    st.write(voices)