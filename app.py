import json

from extract_audio import extract_audio

with open("data/dialogues.json", "r") as file:
    dialogues = json.load(file)

input_audio_path = "audio/original/BigBangS01E03.mp3"
output_audio_folder = "audio/characters"

extract_audio(input_audio_path, output_audio_folder, dialogues)