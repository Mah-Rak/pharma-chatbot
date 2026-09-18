"""
Schémas Pydantic pour le chatbot.
"""
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """Requête du client vers le chatbot."""
    message: str = Field(..., min_length=1, max_length=1000, description="Texte du client")
    session_id: Optional[str] = Field(None, description="ID de session (optionnel)")


class MaladieProposee(BaseModel):
    """Maladie proposée avec son score."""
    nom: str
    nb_symptomes: int
    total_symptomes: int
    score: float


class MedicamentPropose(BaseModel):
    """Médicament proposé."""
    nom: str
    dci: Optional[str] = None
    description: Optional[str] = None
    categorie: Optional[str] = None
    ordonnance_requise: bool = False
    maladie_associee: Optional[str] = None
    stock_disponible: Optional[int] = None


class ChatResponse(BaseModel):
    """Réponse du chatbot."""
    message_original: str
    symptomes_detectes: List[str]
    maladies_probables: List[MaladieProposee]
    medicaments_recommandes: List[MedicamentPropose]
    reponse: str = Field(..., description="Message texte à afficher au client")
    est_urgent: bool = False
    avertissement: Optional[str] = None
    transcription: Optional[dict] = None
    timestamp: datetime = Field(default_factory=datetime.now)
