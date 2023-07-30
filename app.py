import json
import streamlit as st

from utils import init_session_state, voice_folder
from credentials import credentials
from audio_handler import extract_audio
from voiceclone import clone
from translate import translation

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
    input_json = st.file_uploader("Only JSON format of [this](https://github.com/pnkvalavala/Multivoice/blob/main/data/dialogues.json) structure is supported for now", type=["json"])

    if input_json:
        st.session_state['json_file'] = json.load(input_json)

    st.session_state['audio_file'] = st.file_uploader("Upload audio file for voice cloning", type=["mp3", "wav"])

    with st.spinner('Generating individual voice clones'):
        voice_folder()
        if st.session_state['audio_file'] and st.session_state['json_file']:
            extract_audio(
                st.session_state['audio_file'], 
                st.session_state['json_file'], 
                st.session_state['voice_clone_dir']
            )

    clone()

if st.session_state["clone"]==True:
    # Translating json file
    languages = ['English', 'German', 'Polish', 'Spanish', 'Italian', 'French', 'Portuguese', 'Hindi']
    selected_lang = st.selectbox('Select language', languages)

    if st.button('Submit'):
        translations = translation(
            st.session_state['json_file'], 
            selected_lang, 
            st.session_state['openai_token']
        )

        translations_json = json.dumps(translations, ensure_ascii=False)
        st.session_state["dialogue_translated"] = translations_json        
        st.success(f'Dialogues translated to {selected_lang}!')