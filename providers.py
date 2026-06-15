"""Voice/TTS provider abstraction.

The dubbing pipeline (cloning + per-line synthesis) is written against the
`TTSProvider` interface so the rest of the app never has to know which backend
is in use. Two concrete providers are implemented:

  * ElevenLabsProvider - instant single-file cloning, raw-MP3 TTS.
  * SixtyDBProvider     - async multi-sample cloning (polled), base64-JSON TTS.

A single provider drives BOTH cloning and synthesis for a run, because a
voice_id minted by one backend cannot be used by the other.
"""

import io
import time
import base64

import requests
import streamlit as st

from pydub import AudioSegment


class TTSProvider:
    """Common interface every backend implements."""

    label = "provider"

    def __init__(self, token):
        self.token = token

    def validate_token(self, token):
        """Return True if the token is accepted by the backend."""
        raise NotImplementedError

    def clone_voice(self, name, audio):
        """Clone a voice from a character's `AudioSegment`.

        Returns a ready-to-use voice_id (str), or None if cloning could not be
        completed (e.g. not enough source audio / backend failure).
        """
        raise NotImplementedError

    def synthesize(self, voice_id, text):
        """Synthesize one line of `text` in `voice_id`. Returns an
        `AudioSegment`, or None on failure."""
        raise NotImplementedError


class ElevenLabsProvider(TTSProvider):
    label = "ElevenLabs"
    BASE = "https://api.elevenlabs.io/v1"

    def validate_token(self, token):
        response = requests.get(
            f"{self.BASE}/models",
            headers={"Accept": "application/json", "xi-api-key": token},
        )
        return response.status_code == 200

    def clone_voice(self, name, audio):
        buf = io.BytesIO()
        audio.export(buf, format="mp3")
        buf.seek(0)

        headers = {"Accept": "application/json", "xi-api-key": self.token}
        data = {
            "name": name,
            "labels": '{"accent": "American"}',
            "description": f"Cloned from {name}",
        }
        files = [("files", (f"{name}.mp3", buf, "audio/mpeg"))]

        response = requests.post(
            f"{self.BASE}/voices/add", headers=headers, data=data, files=files
        )
        if not response.ok:
            st.error(f"ElevenLabs cloning failed for '{name}': {response.text}")
            return None
        return response.json().get("voice_id")

    def synthesize(self, voice_id, text):
        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": self.token,
        }
        data = {
            "text": text,
            "model_id": "eleven_multilingual_v1",
            "voice_settings": {"stability": 0.5, "similarity_boost": 0.5},
        }
        response = requests.post(
            f"{self.BASE}/text-to-speech/{voice_id}", json=data, headers=headers
        )
        if response.ok:
            return AudioSegment.from_file(io.BytesIO(response.content))
        return None


class SixtyDBProvider(TTSProvider):
    label = "60db"
    BASE = "https://api.60db.ai"

    # Cloning sample constraints (per 60db create-voice docs).
    MIN_FILES = 3
    MAX_FILES = 10
    MIN_CHUNK_MS = 10_000
    MAX_CHUNK_MS = 60_000
    RECOMMENDED_TOTAL_MS = 120_000  # docs recommend >= 2 min combined

    # Async cloning poll settings.
    POLL_INTERVAL_S = 15
    POLL_TIMEOUT_S = 1_200  # 20 min
    PROCESSING_STATES = {"processing", "pending", "queued", "training", "in_progress"}
    FAILED_STATES = {"failed", "error", "rejected"}

    def _headers(self, json_body=False):
        headers = {"Authorization": f"Bearer {self.token}"}
        if json_body:
            headers["Content-Type"] = "application/json"
        return headers

    def validate_token(self, token):
        response = requests.get(
            f"{self.BASE}/myvoices",
            headers={"Authorization": f"Bearer {token}"},
        )
        return response.status_code == 200

    def _split_chunks(self, audio):
        """Split a character's audio into MIN_FILES..MAX_FILES clips of
        MIN_CHUNK_MS..MAX_CHUNK_MS each. Returns None if there isn't enough
        audio to satisfy the backend's minimum."""
        total = len(audio)
        if total < self.MIN_FILES * self.MIN_CHUNK_MS:
            return None

        # Aim for ~30s clips, clamped to the allowed file count and length.
        n = max(self.MIN_FILES, min(self.MAX_FILES, total // 30_000))
        step = max(self.MIN_CHUNK_MS, min(self.MAX_CHUNK_MS, total // n))

        chunks = []
        pos = 0
        while pos + self.MIN_CHUNK_MS <= total and len(chunks) < self.MAX_FILES:
            chunks.append(audio[pos:pos + step])
            pos += step

        if len(chunks) < self.MIN_FILES:
            return None
        return chunks

    def clone_voice(self, name, audio):
        chunks = self._split_chunks(audio)
        if not chunks:
            needed = (self.MIN_FILES * self.MIN_CHUNK_MS) // 1000
            st.warning(
                f"Not enough audio to clone '{name}' on 60db "
                f"(need ~{needed}s+, ideally 2 min). Skipping this voice."
            )
            return None

        if len(audio) < self.RECOMMENDED_TOTAL_MS:
            st.info(
                f"'{name}' has only {len(audio) // 1000}s of audio; 60db "
                "recommends >= 2 min for best cloning quality."
            )

        files = []
        for i, segment in enumerate(chunks):
            buf = io.BytesIO()
            segment.export(buf, format="mp3")
            buf.seek(0)
            files.append(("files", (f"{name}_{i}.mp3", buf, "audio/mpeg")))

        data = {"name": name, "description": f"Cloned from {name}"}
        response = requests.post(
            f"{self.BASE}/voices", headers=self._headers(), data=data, files=files
        )
        if not response.ok:
            st.error(f"60db cloning failed for '{name}': {response.text}")
            return None

        voice_id = response.json().get("id")
        return self._wait_until_ready(voice_id, name)

    def _wait_until_ready(self, voice_id, name):
        """Poll Get-Voice until the async clone leaves a processing state."""
        if not voice_id:
            return None

        waited = 0
        while waited < self.POLL_TIMEOUT_S:
            response = requests.get(
                f"{self.BASE}/voices/{voice_id}", headers=self._headers()
            )
            if response.ok:
                status = (response.json().get("status") or "").lower()
                if status in self.FAILED_STATES:
                    st.error(f"60db cloning failed for '{name}'.")
                    return None
                if status not in self.PROCESSING_STATES:
                    return voice_id  # ready / no status field -> assume usable
            time.sleep(self.POLL_INTERVAL_S)
            waited += self.POLL_INTERVAL_S

        st.warning(
            f"Timed out waiting for 60db voice '{name}' to finish cloning; "
            "using it anyway."
        )
        return voice_id

    def synthesize(self, voice_id, text):
        data = {
            "text": text,
            "voice_id": voice_id,
            "speed": 1,
            "stability": 50,
            "similarity": 75,
            "output_format": "mp3",
        }
        response = requests.post(
            f"{self.BASE}/tts-synthesize", json=data, headers=self._headers(json_body=True)
        )
        if not response.ok:
            return None

        payload = response.json()
        if not payload.get("success", True):
            return None

        audio_b64 = payload.get("audio_base64")
        if not audio_b64:
            return None
        return AudioSegment.from_file(io.BytesIO(base64.b64decode(audio_b64)))


PROVIDERS = {
    ElevenLabsProvider.label: ElevenLabsProvider,
    SixtyDBProvider.label: SixtyDBProvider,
}


def build_provider(name, token):
    return PROVIDERS[name](token)


def get_provider():
    """Construct the active provider from session state."""
    return build_provider(
        st.session_state["provider"], st.session_state["provider_token"]
    )
