import os
from pydub import AudioSegment

def extract_audio(audio_file, segments_data, output_dir):
    audio = AudioSegment.from_file(audio_file)
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