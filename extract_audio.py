import os

from pydub import AudioSegment

def extract_audio(input_audio_path, output_audio_folder, dialogue_segments):
    audio = AudioSegment.from_file(input_audio_path)

    user_audio_map = {}  # To store user-wise audio segments

    for segment in dialogue_segments:
        username = segment["user"]
        start_time = segment["start_time"]
        end_time = segment["end_time"]

        extracted_audio = audio[start_time:end_time]

        if username not in user_audio_map:
            user_audio_map[username] = extracted_audio
        else:
            user_audio_map[username] += extracted_audio

    for username, user_audio in user_audio_map.items():
        output_file_path = os.path.join(output_audio_folder, f"{username}.mp3")
        user_audio.export(output_file_path, format="mp3")