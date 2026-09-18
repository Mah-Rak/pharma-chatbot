"""
Microservice de transcription vocale.
Tourne dans venv_vocal (Python 3.12) sur le port 8001.

Lance avec :
    uvicorn src.vocal_api:app --port 8001
"""
from fastapi import FastAPI, File, UploadFile, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

from src.services.transcription_service import get_transcription_service


app = FastAPI(
    title="Pharma Vocal API",
    description="Microservice de transcription audio (Whisper)",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    """Verifie que le service est en ligne."""
    return {"status": "ok", "service": "vocal"}


@app.post("/transcribe")
async def transcribe(
    file: UploadFile = File(..., description="Fichier audio (WAV, MP3, OGG...)"),
    language: str = "fr",
):
    """
    Transcrit un fichier audio en texte.
    Retourne : texte, langue, duree, segments.
    """
    # Verifier l'extension
    extensions_ok = (".wav", ".mp3", ".ogg", ".m4a", ".webm")
    if not file.filename or not file.filename.lower().endswith(extensions_ok):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Format audio non supporte",
        )

    # Lire les bytes
    audio_bytes = await file.read()
    if not audio_bytes:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Fichier audio vide",
        )

    # Determiner le suffixe
    suffix = ".wav"
    for ext in extensions_ok:
        if file.filename.lower().endswith(ext):
            suffix = ext
            break

    # Transcrire
    try:
        service = get_transcription_service(model_size="base")
        result = service.transcrire_bytes(
            audio_bytes,
            suffix=suffix,
            language=language,
        )
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur de transcription : {str(e)}",
        )
