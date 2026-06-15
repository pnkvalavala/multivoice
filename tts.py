from providers import get_provider

def tts(voice_id, text):
    """Synthesize one line of text in the given voice using the active
    provider. Returns a pydub AudioSegment (or None on failure)."""
    return get_provider().synthesize(voice_id, text)
