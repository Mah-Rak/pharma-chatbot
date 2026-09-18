"""
Routes API pour le chatbot.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.db.database import get_db
from src.schemas.chatbot import ChatRequest, ChatResponse
from src.nlp.chatbot import get_chatbot_service

router = APIRouter(prefix="/chatbot", tags=["Chatbot"])


@router.post(
    "/",
    response_model=ChatResponse,
    status_code=status.HTTP_200_OK,
    summary="Interroger le chatbot",
    description=(
        "Envoie un message decrivant des symptomes. "
        "Le chatbot detecte les symptomes, identifie les maladies probables "
        "et recommande des medicaments disponibles en stock."
    ),
)
def chat(request: ChatRequest, db: Session = Depends(get_db)):
    """Endpoint principal du chatbot."""
    try:
        chatbot = get_chatbot_service()
        return chatbot.traiter(request, db)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur du chatbot : {str(e)}",
        )


@router.get(
    "/historique/{session_id}",
    summary="Historique d'une session",
)
def get_historique(session_id: str, limit: int = 50):
    """Recupere l'historique des conversations d'une session."""
    try:
        from src.services.chat_service import get_chat_log_service
        service = get_chat_log_service()
        return service.get_conversations(session_id, limit=limit)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur : {str(e)}",
        )


@router.get(
    "/stats",
    summary="Statistiques des conversations",
)
def get_stats():
    """Retourne le nombre total de conversations enregistrees."""
    try:
        from src.services.chat_service import get_chat_log_service
        service = get_chat_log_service()
        return {"total_conversations": service.count()}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur : {str(e)}",
        )

# ============ AUDIO ============

from fastapi import File, UploadFile


@router.post(
    "/audio",
    response_model=ChatResponse,
    summary="Interroger le chatbot via un fichier audio",
)
async def chat_audio(
    file: UploadFile = File(..., description="Fichier audio (WAV, MP3...)"),
    db: Session = Depends(get_db),
):
    """Recoit un audio, le transcrit, puis traite le texte comme un message."""
    from src.services.vocal_client import get_vocal_client

    # Verifier l'extension
    extensions_ok = (".wav", ".mp3", ".ogg", ".m4a", ".webm")
    if not file.filename or not file.filename.lower().endswith(extensions_ok):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Format audio non supporte",
        )

    # Lire l'audio
    audio_bytes = await file.read()
    if not audio_bytes:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Fichier audio vide",
        )

    # Verifier le microservice vocal
    vocal = get_vocal_client()
    if not vocal.health():
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Service vocal indisponible. Lancez : uvicorn src.vocal_api:app --port 8001",
        )

    # Transcrire
    result = vocal.transcrire(audio_bytes, filename=file.filename)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur lors de la transcription",
        )

    texte = result["texte"]
    if not texte.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Aucun texte detecte dans l'audio",
        )

    # Traiter comme un message texte
    request = ChatRequest(message=texte)
    chatbot = get_chatbot_service()
    response = chatbot.traiter(request, db)

    # Enrichir avec les infos audio
    response_dict = response.model_dump()
    response_dict["transcription"] = {
        "texte": texte,
        "langue": result["langue"],
        "duree": result["duree"],
    }

    return response_dict
