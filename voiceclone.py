import os
import streamlit as st

from pydub import AudioSegment

from providers import get_provider

def clone():
    provider = get_provider()
    audio_files = os.listdir('voice_clones/')
    st.session_state["voice_id"] = {}
    num_files = len(audio_files)

    for f in audio_files:
        st.session_state["count"] += 1
        filepath = os.path.join('voice_clones/', f)
        name = f.rsplit(".", 1)[0]

        with st.spinner(f'Cloning {name} voice with {provider.label}'):
            audio = AudioSegment.from_file(filepath)
            voice_id = provider.clone_voice(name, audio)

            if voice_id:
                st.session_state["voice_id"][name] = voice_id

    if st.session_state["count"] == num_files != 0:
        st.session_state["clone"] = True
        st.session_state["auth_ok"] = False
        st.success("Cloned all the voices.")
