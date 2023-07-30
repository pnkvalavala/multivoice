import ast
import json
import openai

def translation(org_dialogues, lang, openai_token):
    prompt = f"""Translate the following conversations to "{lang}" while maintaining relevant context and ensuring that the output duration matches the start_time and end_time. Add special characters like .... or ---- where necessary based on the context. Provide the output in JSON code format for easy copying and pasting. My goal is to use this text for TTS (Text-to-Speech) purposes. Please make sure the translations are accurate and fluent.
    Input format : 
    [
    [dialogue, start_time, end_time],
    [dialogue, start_time, end_time],..
    ]
    Output format = 
    [
        dialogue,
        dialgoue,..
    ]
    Don't include time stamps in output"""

    preprocessed_dialogues = [
        (dialogue["text"], dialogue["start_time"], dialogue["end_time"])
        for dialogue in org_dialogues
    ]

    preprocessed_dialogues_str = json.dumps(preprocessed_dialogues)

    prompt += preprocessed_dialogues_str

    openai.api_key = openai_token

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=3500
    )

    translated_text = response["choices"][0]["text"]
    translated_list = ast.literal_eval(translated_text)

    translated_dialogues = org_dialogues.copy()
    
    for i in range(len(translated_dialogues)):
        translated_dialogues[i]["text"] = translated_list[i]

    return translated_dialogues