import os
import time
import streamlit as st

def init_session_state():
    SESSION_DEFAULTS = {
        "auth_ok": False,
        "openai_token": False,
        "el_token": None,
        "json_file": None,
        "audio_file" :None,
        "voice_clone_dir": 'voice_clones'
    }

    for keys, values in SESSION_DEFAULTS.items():
        if keys not in st.session_state:
            st.session_state[keys] = values

def voice_clone():
    if not os.path.exists(st.session_state["voice_clone_dir"]):
        os.mkdir(st.session_state["voice_clone_dir"])
    
    for f in os.listdir(st.session_state["voice_clone_dir"]):
        os.remove(os.path.join(st.session_state["voice_clone_dir"], f))

# def show_translation_progress(total_segments):
#     progress_bar = st.progress(0)
#     for i in range(total_segments):
#         time.sleep(0.1)
#         progress_bar.progress(i + 1)

# def show_voice_cloning_progress(total_users):
#     progress_bar = st.progress(0)
#     for i in range(total_users):
#         time.sleep(0.1)  
#         progress_bar.progress(i + 1)