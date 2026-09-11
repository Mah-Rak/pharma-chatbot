"""
Schémas Pydantic pour les alertes.
"""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict

from src.schemas.produit import ProduitResponse


class AlerteBase(BaseModel):
    produit_id: int = Field(..., gt=0, description="ID du produit concerné")
    type: str = Field(..., min_length=1, max_length=50, description="Type d'alerte (epuisement, peremption)")
    message: Optional[str] = Field(None, description="Message détaillé")
    resolue: bool = Field(False, description="Alerte résolue ou non")


class AlerteCreate(AlerteBase):
    """Schéma pour créer une alerte (usage interne)."""
    pass


class AlerteUpdate(BaseModel):
    """Schéma pour mettre à jour une alerte."""
    message: Optional[str] = None
    resolue: Optional[bool] = None


class AlerteResponse(AlerteBase):
    """Schéma de réponse avec le produit imbriqué."""
    id: int
    created_at: datetime

    produit: Optional[ProduitResponse] = None

    model_config = ConfigDict(from_attributes=True)
