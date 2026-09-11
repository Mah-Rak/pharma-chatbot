"""
Schémas Pydantic pour les fournisseurs.
"""
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict, EmailStr


class FournisseurBase(BaseModel):
    nom: str = Field(..., min_length=1, max_length=255, description="Nom du fournisseur")
    contact: Optional[str] = Field(None, max_length=255, description="Personne de contact")
    email: Optional[EmailStr] = Field(None, description="Email de contact")
    telephone: Optional[str] = Field(None, max_length=50, description="Numéro de téléphone")
    adresse: Optional[str] = Field(None, description="Adresse postale")


class FournisseurCreate(FournisseurBase):
    """Schéma pour créer un fournisseur."""
    pass


class FournisseurUpdate(BaseModel):
    """Schéma pour mettre à jour un fournisseur (tous optionnels)."""
    nom: Optional[str] = Field(None, min_length=1, max_length=255)
    contact: Optional[str] = Field(None, max_length=255)
    email: Optional[EmailStr] = None
    telephone: Optional[str] = Field(None, max_length=50)
    adresse: Optional[str] = None


class FournisseurResponse(FournisseurBase):
    """Schéma de réponse."""
    id: int

    model_config = ConfigDict(from_attributes=True)
