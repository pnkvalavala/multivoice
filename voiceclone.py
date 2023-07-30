import os
import requests
import streamlit as st

def clone():
    audio_files = os.listdir('voice_clones/')
    st.session_state["voice_id"] = {}
    num_files = len(audio_files)
        
    for f in audio_files:
        st.session_state["count"] += 1
        filepath = os.path.join('voice_clones/', f)

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
        
            st.session_state["voice_id"][f.rsplit(".", 1)[0]] = cloned_voice_id
    if st.session_state["count"] == num_files != 0:
        st.session_state["clone"] = True
        st.session_state["auth_ok"] = False
        st.success("Cloned all the voices.")