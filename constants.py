AUTHENTICATION_HELP = """
Your credentials are only stored in your session state.\n
The keys are neither exposed nor made visible or stored permanently in any way.\n
Feel free to check out [the code base]("https://github.com/pnkvalavala/Multivoice") to validate how things work.
"""

OPENAI_HELP="""
To generate user dialogues in different language, we need OpenAI API. If you come across any reliable open-source models for translation, please feel free to share them with us.\n
You can sign up for OpenAI API and manage your API usage by visiting [here](https://platform.openai.com/account/api-keys)
"""

EL_TOKEN = """
To voice clone the characters and generate Text-to-Speech we need ElevenLabs API. You can sign up for ElevenLabs API and manage your API usage by visiting [here](https://elevenlabs.io/sign-up)
"""

SIXTYDB_TOKEN = """
60db is an alternative voice cloning + Text-to-Speech backend. Cloning on 60db is asynchronous (it needs several short samples per character and can take ~10-15 min). You can sign up and get an API key at [60db](https://60db.ai).
"""

PROVIDER_HELP = """
Choose which backend clones the character voices and generates speech.\n
A single provider is used for the whole run, because a cloned voice from one backend cannot be used by the other.
"""

PROVIDER_TOKEN_HELP = {
    "ElevenLabs": EL_TOKEN,
    "60db": SIXTYDB_TOKEN,
}