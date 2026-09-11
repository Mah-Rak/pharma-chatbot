"""
Routes API pour les alertes.
"""
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from src.db.database import get_db
from src.schemas.alerte import AlerteCreate, AlerteUpdate, AlerteResponse
from src.services.alerte_service import AlerteService

router = APIRouter(prefix="/alertes", tags=["Alertes"])


@router.get("/", response_model=List[AlerteResponse])
def list_alertes(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    resolue: Optional[bool] = Query(None, description="Filtrer par statut"),
    db: Session = Depends(get_db),
):
    """Liste les alertes, avec filtre optionnel sur le statut."""
    return AlerteService.get_all(db, skip=skip, limit=limit, resolue=resolue)


@router.get("/non-resolues/", response_model=List[AlerteResponse])
def list_non_resolues(db: Session = Depends(get_db)):
    """Liste toutes les alertes non résolues."""
    return AlerteService.get_non_resolues(db)


@router.get("/produit/{produit_id}", response_model=List[AlerteResponse])
def list_alertes_produit(
    produit_id: int,
    resolue: Optional[bool] = Query(None),
    db: Session = Depends(get_db),
):
    """Liste les alertes d'un produit donné."""
    return AlerteService.get_by_produit(db, produit_id, resolue=resolue)


@router.get("/{alerte_id}", response_model=AlerteResponse)
def get_alerte(alerte_id: int, db: Session = Depends(get_db)):
    """Récupère une alerte par ID."""
    alerte = AlerteService.get_by_id(db, alerte_id)
    if not alerte:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Alerte {alerte_id} non trouvée",
        )
    return alerte


@router.post("/", response_model=AlerteResponse, status_code=status.HTTP_201_CREATED)
def create_alerte(data: AlerteCreate, db: Session = Depends(get_db)):
    """Crée manuellement une alerte (usage administrateur)."""
    return AlerteService.create(db, data)


@router.put("/{alerte_id}", response_model=AlerteResponse)
def update_alerte(
    alerte_id: int,
    data: AlerteUpdate,
    db: Session = Depends(get_db),
):
    """Met à jour une alerte (ex : la marquer comme résolue)."""
    alerte = AlerteService.update(db, alerte_id, data)
    if not alerte:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Alerte {alerte_id} non trouvée",
        )
    return alerte


@router.delete("/{alerte_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_alerte(alerte_id: int, db: Session = Depends(get_db)):
    """Supprime une alerte."""
    if not AlerteService.delete(db, alerte_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Alerte {alerte_id} non trouvée",
        )
    return None
