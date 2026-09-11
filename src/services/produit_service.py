"""
Service métier pour les produits.
Contient toutes les opérations CRUD sur les produits.
"""
from typing import List, Optional

from sqlalchemy.orm import Session

from src.db.models import Produit
from src.schemas.produit import ProduitCreate, ProduitUpdate


class ProduitService:
    """Service CRUD pour les produits."""

    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100) -> List[Produit]:
        """Récupère la liste des produits avec pagination."""
        return db.query(Produit).offset(skip).limit(limit).all()

    @staticmethod
    def get_by_id(db: Session, produit_id: int) -> Optional[Produit]:
        """Récupère un produit par son ID."""
        return db.query(Produit).filter(Produit.id == produit_id).first()

    @staticmethod
    def get_by_nom(db: Session, nom: str) -> List[Produit]:
        """Recherche les produits par nom (recherche partielle)."""
        return db.query(Produit).filter(Produit.nom.ilike(f"%{nom}%")).all()

    @staticmethod
    def create(db: Session, data: ProduitCreate) -> Produit:
        """Crée un nouveau produit."""
        produit = Produit(**data.model_dump())
        db.add(produit)
        db.commit()
        db.refresh(produit)
        return produit

    @staticmethod
    def update(db: Session, produit_id: int, data: ProduitUpdate) -> Optional[Produit]:
        """Met à jour un produit existant."""
        produit = ProduitService.get_by_id(db, produit_id)
        if not produit:
            return None

        # Met à jour uniquement les champs fournis
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(produit, key, value)

        db.commit()
        db.refresh(produit)
        return produit

    @staticmethod
    def delete(db: Session, produit_id: int) -> bool:
        """Supprime un produit. Retourne True si supprimé, False sinon."""
        produit = ProduitService.get_by_id(db, produit_id)
        if not produit:
            return False

        db.delete(produit)
        db.commit()
        return True
