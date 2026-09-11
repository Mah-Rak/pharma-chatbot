"""
Service métier pour les fournisseurs.
"""
from typing import List, Optional
from sqlalchemy.orm import Session

from src.db.models import Fournisseur
from src.schemas.fournisseur import FournisseurCreate, FournisseurUpdate


class FournisseurService:
    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100) -> List[Fournisseur]:
        return db.query(Fournisseur).offset(skip).limit(limit).all()

    @staticmethod
    def get_by_id(db: Session, fournisseur_id: int) -> Optional[Fournisseur]:
        return db.query(Fournisseur).filter(Fournisseur.id == fournisseur_id).first()

    @staticmethod
    def get_by_nom(db: Session, nom: str) -> List[Fournisseur]:
        return db.query(Fournisseur).filter(Fournisseur.nom.ilike(f"%{nom}%")).all()

    @staticmethod
    def create(db: Session, data: FournisseurCreate) -> Fournisseur:
        fournisseur = Fournisseur(**data.model_dump())
        db.add(fournisseur)
        db.commit()
        db.refresh(fournisseur)
        return fournisseur

    @staticmethod
    def update(db: Session, fournisseur_id: int, data: FournisseurUpdate) -> Optional[Fournisseur]:
        fournisseur = FournisseurService.get_by_id(db, fournisseur_id)
        if not fournisseur:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(fournisseur, key, value)
        db.commit()
        db.refresh(fournisseur)
        return fournisseur

    @staticmethod
    def delete(db: Session, fournisseur_id: int) -> bool:
        fournisseur = FournisseurService.get_by_id(db, fournisseur_id)
        if not fournisseur:
            return False
        db.delete(fournisseur)
        db.commit()
        return True
