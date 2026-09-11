"""
Schémas Pydantic pour les produits.
Séparent la validation API de la couche base de données.
"""
from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class ProduitBase(BaseModel):
    """Champs communs à tous les schémas produit."""
    nom: str = Field(..., min_length=1, max_length=255, description="Nom du médicament")
    description: Optional[str] = Field(None, description="Description du médicament")
    prix: Decimal = Field(..., gt=0, description="Prix unitaire en euros")
    categorie: Optional[str] = Field(None, max_length=100, description="Catégorie thérapeutique")
    ordonnance_requise: bool = Field(False, description="Vente sur ordonnance obligatoire")


class ProduitCreate(ProduitBase):
    """Schéma utilisé pour créer un produit (POST)."""
    pass


class ProduitUpdate(BaseModel):
    """Schéma utilisé pour mettre à jour un produit (PUT/PATCH). Tous les champs sont optionnels."""
    nom: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    prix: Optional[Decimal] = Field(None, gt=0)
    categorie: Optional[str] = Field(None, max_length=100)
    ordonnance_requise: Optional[bool] = None


class ProduitResponse(ProduitBase):
    """Schéma utilisé pour renvoyer un produit (GET)."""
    id: int
    created_at: datetime

    # Permet à Pydantic de lire depuis un objet SQLAlchemy
    model_config = ConfigDict(from_attributes=True)
