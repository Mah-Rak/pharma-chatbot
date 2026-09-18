"""
Client HTTP pour le microservice vocal (port 8001).
"""
import os
from typing import Optional

import requests


VOCAL_API_URL = os.getenv("VOCAL_API_URL", "http://localhost:8001")


class VocalClient:
    """Client pour le microservice de transcription."""

    def __init__(self, base_url: str = VOCAL_API_URL):
        self.base_url = base_url
        self.timeout = 60

    def health(self) -> bool:
        """Verifie que le service vocal est en ligne."""
        try:
            r = requests.get(f"{self.base_url}/health", timeout=5)
            return r.status_code == 200
        except requests.RequestException:
            return False

    def transcrire(
        self,
        audio_bytes: bytes,
        filename: str = "audio.wav",
        language: str = "fr",
    ) -> Optional[dict]:
        """Transcrit un audio via le microservice vocal."""
        try:
            files = {"file": (filename, audio_bytes, "audio/wav")}
            data = {"language": language}
            r = requests.post(
                f"{self.base_url}/transcribe",
                files=files,
                data=data,
                timeout=self.timeout,
            )
            r.raise_for_status()
            return r.json()
        except requests.RequestException as e:
            print(f"[WARN] Erreur transcription : {e}")
            return None


_instance: Optional[VocalClient] = None


def get_vocal_client() -> VocalClient:
    global _instance
    if _instance is None:
        _instance = VocalClient()
    return _instance
