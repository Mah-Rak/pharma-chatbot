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
