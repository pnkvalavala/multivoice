# About

Multivoice is a powerful tool that aims to enhance the viewing experience of foreign-language movies and TV shows. It allows users to enjoy personalized dubbed versions in character voices, making entertainment accessible, delightful, and enjoyable, even if they don't understand the original language. With the option to translate dialogues into their chosen language, users can fully immerse themselves in the content and have a truly engaging experience.

## Getting Started

To run this app on your local machine,

* Clone the repository

  ```
  git clone https://github.com/pnkvalavala/Multivoice
  ```
* Install required packages

  ```
  pip install -r requirements.txt
  ```
* Run the app

  ```
  streamlit run app.py
  ```
## How Multivoice Works

1. **Prerequisites**: Before using Multivoice, users need to obtain the following:

   - **OpenAI API Token**: Users should sign up for the OpenAI API to enable translation services. API keys can be managed at [OpenAI API](https://platform.openai.com/account/api-keys).
   - **ElevenLabs API Key**: Users must obtain an API key from ElevenLabs to access their Text-to-Speech (TTS) and voice cloning services. Sign up and API key management are available at [ElevenLabs](https://elevenlabs.io/sign-up).

   Rest assured, the credentials provided by users are securely handled within the session state and are not permanently stored.

2. **Web Application Usage**:

   - The application leverages Streamlit for user interaction and seamless integration with other modules.

   - The user-friendly interface allows users to upload a JSON file and an MP3 audio file. The JSON file follows a [specific structure](https://github.com/pnkvalavala/Multivoice/blob/main/sample_data/dialogues.json)  containing user information and dialogues with timestamps.

3. **Dialogues Preprocessing**:

   - The uploaded JSON file is preprocessed to extract user dialogues and convert them into a structured format. The JSON format is optimized to specify user names, dialogue text, and corresponding timestamps.                                
  
4. **Audio Extraction**:

   - Multivoice automatically analyzes the uploaded MP3 audio file and identifies occurrences of each user's dialogues based on the JSON file structure.

   - Individual user audio segments are then extracted and merged into separate audio files. For example, if there are five users in the conversation, five separate audio files will be generated—one for each user.

5. **Voice Cloning**:

   - Multivoice leverages ElevenLabs' voice cloning technology to create personalized voice models for each user.

   - The extracted user audio files are sent to ElevenLabs to clone the corresponding user's voice. This step results in high-quality voice models that mimic the users' unique speech characteristics.

6. **Translation**:

   - Users can then choose to translate the dialogues into their preferred language using the OpenAI API.

   - The application sends the dialogues from the uploaded JSON file to OpenAI, which returns the translated dialogues in the user's chosen language.

7. **Audio Replacement**:

   - Once the voice cloning and translation processes are complete, Multivoice combines the original audio with the dubbed dialogues for each user.

   - The application replaces the original audio of the corresponding timestamps with the cloned user voice obtained from ElevenLabs. All other parts of the audio remain unaltered.

8. **Enjoy the Multivoice Experience**:

   - With the process complete, users can now enjoy foreign-language movies or TV shows with personalized dubbed versions in character voices, making the entertainment experience more immersive and enjoyable.


Please note that the project includes sample data, including an MP3 audio file (`BigBangS01E03.mp3`), a `dialogues.json` file, and `subtitles.srt`, which are used for demonstrations.

With Multivoice, immerse yourself in a world of diverse entertainment and enjoy foreign-language content like never before! 🌍🎉🎬😄

## Disclaimer

Please ensure that you have the appropriate permissions to use the audio and subtitle files for voice cloning and translation purposes.