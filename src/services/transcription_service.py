"""
Service de transcription audio → texte.
Utilise faster-whisper (Whisper optimisé).
"""
from pathlib import Path
from typing import Optional, Union
import tempfile

from faster_whisper import WhisperModel


class TranscriptionService:
    """Service de transcription audio avec faster-whisper."""

    def __init__(self, model_size: str = "base", device: str = "cpu"):
        self.model_size = model_size
        self.device = device
        self.model = WhisperModel(
            model_size,
            device=device,
            compute_type="int8",
        )

    def transcrire(
        self,
        audio_path: Union[str, Path],
        language: Optional[str] = "fr",
    ) -> dict:
        """Transcrit un fichier audio en texte."""
        segments_gen, info = self.model.transcribe(
            str(audio_path),
            language=language,
            beam_size=5,
            vad_filter=True,
        )

        segments = []
        textes = []
        for seg in segments_gen:
            segments.append({
                "start": round(seg.start, 2),
                "end": round(seg.end, 2),
                "text": seg.text.strip(),
            })
            textes.append(seg.text.strip())

        return {
            "texte": " ".join(textes).strip(),
            "langue": info.language,
            "duree": round(info.duration, 2),
            "segments": segments,
        }

    def transcrire_bytes(
        self,
        audio_bytes: bytes,
        suffix: str = ".wav",
        language: Optional[str] = "fr",
    ) -> dict:
        """Transcrit des bytes audio (pour l'API)."""
        with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
            tmp.write(audio_bytes)
            tmp_path = tmp.name

        try:
            return self.transcrire(tmp_path, language=language)
        finally:
            Path(tmp_path).unlink(missing_ok=True)


_instance: Optional[TranscriptionService] = None


def get_transcription_service(
    model_size: str = "base",
) -> TranscriptionService:
    global _instance
    if _instance is None:
        _instance = TranscriptionService(model_size=model_size)
    return _instance
