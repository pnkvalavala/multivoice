import os
import streamlit as st

def init_session_state():
    SESSION_DEFAULTS = {
        "auth_ok": False,
        "openai_token": False,
        "el_token": None,
        "json_file": None,
        "audio_file" :None,
        "voice_clone_dir": 'voice_clones',
        "clone": False,
        "voice_id": None,
        "count": 0,
        "dialogue_translated": None
    }

    for keys, values in SESSION_DEFAULTS.items():
        if keys not in st.session_state:
            st.session_state[keys] = values

def voice_folder():
    if not os.path.exists(st.session_state["voice_clone_dir"]):
        os.mkdir(st.session_state["voice_clone_dir"])
    
    for f in os.listdir(st.session_state["voice_clone_dir"]):
        os.remove(os.path.join(st.session_state["voice_clone_dir"], f))