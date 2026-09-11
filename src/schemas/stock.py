"""
Schémas Pydantic pour le stock.
"""
from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict

from src.schemas.produit import ProduitResponse
from src.schemas.fournisseur import FournisseurResponse


class StockBase(BaseModel):
    produit_id: int = Field(..., gt=0, description="ID du produit")
    fournisseur_id: Optional[int] = Field(None, gt=0, description="ID du fournisseur (optionnel)")
    quantite: int = Field(0, ge=0, description="Quantité en stock")
    seuil_alerte: int = Field(10, ge=0, description="Seuil déclenchant une alerte")
    date_peremption: Optional[date] = Field(None, description="Date de péremption")


class StockCreate(StockBase):
    """Schéma pour créer une entrée de stock."""
    pass


class StockUpdate(BaseModel):
    """Schéma pour mettre à jour une entrée de stock."""
    fournisseur_id: Optional[int] = Field(None, gt=0)
    quantite: Optional[int] = Field(None, ge=0)
    seuil_alerte: Optional[int] = Field(None, ge=0)
    date_peremption: Optional[date] = None


class StockResponse(StockBase):
    """Schéma de réponse — inclut les relations."""
    id: int
    updated_at: datetime

    # Relations imbriquées (optionnelles pour éviter les requêtes lourdes)
    produit: Optional[ProduitResponse] = None
    fournisseur: Optional[FournisseurResponse] = None

    model_config = ConfigDict(from_attributes=True)


class StockSimple(BaseModel):
    """Version allégée sans relations (utile pour les listes)."""
    id: int
    produit_id: int
    fournisseur_id: Optional[int]
    quantite: int
    seuil_alerte: int
    date_peremption: Optional[date]
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
