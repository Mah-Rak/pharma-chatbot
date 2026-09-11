"""
Routes API pour les produits.
"""
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from src.db.database import get_db
from src.schemas.produit import ProduitCreate, ProduitUpdate, ProduitResponse
from src.services.produit_service import ProduitService

router = APIRouter(prefix="/produits", tags=["Produits"])


@router.get("/", response_model=List[ProduitResponse])
def list_produits(
    skip: int = Query(0, ge=0, description="Nombre d'éléments à sauter"),
    limit: int = Query(100, ge=1, le=500, description="Nombre max d'éléments"),
    db: Session = Depends(get_db),
):
    """Liste tous les produits avec pagination."""
    return ProduitService.get_all(db, skip=skip, limit=limit)


@router.get("/search/", response_model=List[ProduitResponse])
def search_produits(
    q: str = Query(..., min_length=1, description="Terme de recherche"),
    db: Session = Depends(get_db),
):
    """Recherche des produits par nom."""
    return ProduitService.get_by_nom(db, q)


@router.get("/{produit_id}", response_model=ProduitResponse)
def get_produit(produit_id: int, db: Session = Depends(get_db)):
    """Récupère un produit par son ID."""
    produit = ProduitService.get_by_id(db, produit_id)
    if not produit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Produit {produit_id} non trouvé",
        )
    return produit


@router.post(
    "/",
    response_model=ProduitResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_produit(data: ProduitCreate, db: Session = Depends(get_db)):
    """Crée un nouveau produit."""
    return ProduitService.create(db, data)


@router.put("/{produit_id}", response_model=ProduitResponse)
def update_produit(
    produit_id: int,
    data: ProduitUpdate,
    db: Session = Depends(get_db),
):
    """Met à jour un produit existant."""
    produit = ProduitService.update(db, produit_id, data)
    if not produit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Produit {produit_id} non trouvé",
        )
    return produit


@router.delete("/{produit_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_produit(produit_id: int, db: Session = Depends(get_db)):
    """Supprime un produit."""
    if not ProduitService.delete(db, produit_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Produit {produit_id} non trouvé",
        )
    return None
