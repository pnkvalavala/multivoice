import os
import json
import tempfile
import streamlit as st

from pydub import AudioSegment
from tts import tts

def extract_audio(segments_data, output_dir):
    audio = AudioSegment.from_file(st.session_state['audio_file'])
    user_audio_map = {}  # To store user-wise audio segments

    for segment in segments_data:
        username = segment["user"]
        start = segment["start_time"]
        end = segment["end_time"]

        segment_audio = audio[start:end]

        if username not in user_audio_map:
            user_audio_map[username] = segment_audio
        else:
            user_audio_map[username] += segment_audio

    for username, user_audio in user_audio_map.items():
        out_path = os.path.join(output_dir, f"{username}.mp3")
        user_audio.export(out_path, format="mp3")

def generate_audio():
    audio_file = st.session_state['audio_file']
    with tempfile.NamedTemporaryFile(delete=False) as f:
        f.write(audio_file.getvalue())
        audio_path = f.name

    audio = AudioSegment.from_file(audio_path)
    if st.session_state["dialogue_translated"] is not None:
        dialog_json = st.session_state["dialogue_translated"]
        dialogs = json.loads(dialog_json)

        output_audio = AudioSegment.empty()
        prev_end = 0
        
        for dialog in dialogs:
            start = dialog["start_time"]
            end = dialog["end_time"]

            user = dialog["user"]
            text = dialog["text"]
            id = st.session_state["voice_id"].get(user)

            new_audio = tts(id, text)

            new_audio = new_audio.set_frame_rate(audio.frame_rate)
            new_audio = new_audio.set_channels(audio.channels)

            output_audio = output_audio + audio[prev_end:start] + new_audio
            prev_end = end

        output_audio = output_audio + audio[prev_end:]
        output_audio.export("output.mp3", format="mp3")