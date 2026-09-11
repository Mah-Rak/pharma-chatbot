"""
Routes API pour les fournisseurs.
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from src.db.database import get_db
from src.schemas.fournisseur import (
    FournisseurCreate,
    FournisseurUpdate,
    FournisseurResponse,
)
from src.services.fournisseur_service import FournisseurService

router = APIRouter(prefix="/fournisseurs", tags=["Fournisseurs"])


@router.get("/", response_model=List[FournisseurResponse])
def list_fournisseurs(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
):
    """Liste tous les fournisseurs."""
    return FournisseurService.get_all(db, skip=skip, limit=limit)


@router.get("/search/", response_model=List[FournisseurResponse])
def search_fournisseurs(
    q: str = Query(..., min_length=1),
    db: Session = Depends(get_db),
):
    """Recherche des fournisseurs par nom."""
    return FournisseurService.get_by_nom(db, q)


@router.get("/{fournisseur_id}", response_model=FournisseurResponse)
def get_fournisseur(fournisseur_id: int, db: Session = Depends(get_db)):
    """Récupère un fournisseur par son ID."""
    fournisseur = FournisseurService.get_by_id(db, fournisseur_id)
    if not fournisseur:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Fournisseur {fournisseur_id} non trouvé",
        )
    return fournisseur


@router.post("/", response_model=FournisseurResponse, status_code=status.HTTP_201_CREATED)
def create_fournisseur(data: FournisseurCreate, db: Session = Depends(get_db)):
    """Crée un nouveau fournisseur."""
    return FournisseurService.create(db, data)


@router.put("/{fournisseur_id}", response_model=FournisseurResponse)
def update_fournisseur(
    fournisseur_id: int,
    data: FournisseurUpdate,
    db: Session = Depends(get_db),
):
    """Met à jour un fournisseur existant."""
    fournisseur = FournisseurService.update(db, fournisseur_id, data)
    if not fournisseur:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Fournisseur {fournisseur_id} non trouvé",
        )
    return fournisseur


@router.delete("/{fournisseur_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_fournisseur(fournisseur_id: int, db: Session = Depends(get_db)):
    """Supprime un fournisseur."""
    if not FournisseurService.delete(db, fournisseur_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Fournisseur {fournisseur_id} non trouvé",
        )
    return None
