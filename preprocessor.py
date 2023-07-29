import re
import json

def srt_to_json(srt_content):
    dialogue_segments = []

    pattern = r"(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})\n(.+?)\n\n"
    matches = re.findall(pattern, srt_content, re.DOTALL)

    for match in matches:
        start_time, end_time, text = match
        text = text.replace("\n", " ")

        if not re.search(r"<.*?>|<font.*?>|\(.*?\)", text):
            start_time_ms = time_to_milliseconds(start_time)
            end_time_ms = time_to_milliseconds(end_time)
            dialogue_segments.append({"user": None, "text": text, "start_time": start_time_ms, "end_time": end_time_ms})

    return dialogue_segments

def time_to_milliseconds(time_str):
    # Convert time in HH:MM:SS,mmm format to milliseconds
    h, m, s, ms = map(int, re.split(r"[:,]", time_str))
    return h * 3600000 + m * 60000 + s * 1000 + ms

with open("S01E03.srt", "r") as srt_file:
    srt_content = srt_file.read()

dialogues = srt_to_json(srt_content)

with open("dialogues.json", "w") as json_file:
    json.dump(dialogues, json_file)