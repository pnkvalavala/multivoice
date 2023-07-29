import streamlit as st
import requests

from constants import *

def credentials():
    with st.sidebar:
        st.title("Authentication", help=AUTHENTICATION_HELP)
        with st.form("tokens"):
            openai_token = st.text_input(
                "OpenAI API",
                type="password",
                help=OPENAI_HELP,
                placeholder="This field is mandatory"
            )
            el_token = st.text_input(
                "ElevenLabs Token",
                type="password",
                help=EL_TOKEN,
                placeholder="This field is mandatory"
            )
            submit_tokens = st.form_submit_button("Submit")
    
    if submit_tokens:
        with st.spinner("Hang tight, validating the tokens..."):
            if not(openai_token and el_token):
                st.error("Enter all credentials")
                st.stop()
            if check_openai(openai_token) and check_el(el_token):
                st.session_state["auth_ok"] = True
                st.session_state["openai_token"] = openai_token
                st.session_state["el_token"] = el_token
                st.success("API Keys are valid")

def check_openai(openai_token):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {openai_token}',
    }
    response = requests.get("https://api.openai.com/v1/engines", headers=headers)
    if response.status_code == 200:
        return True
    st.error("Enter valid OpenAI token")
    st.stop()

def check_el(el_token):
    url = "https://api.elevenlabs.io/v1/models"
    headers = {
        "Accept": "application/json",
        "xi-api-key": el_token
    }
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return True
    st.error("Enter valid ElevenLabs token")
    st.stop()