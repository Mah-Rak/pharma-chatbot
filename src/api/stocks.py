"""
Routes API pour le stock.
"""
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from src.db.database import get_db
from src.schemas.stock import StockCreate, StockUpdate, StockResponse
from src.services.stock_service import StockService

router = APIRouter(prefix="/stocks", tags=["Stock"])


@router.get("/", response_model=List[StockResponse])
def list_stocks(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
):
    """Liste tout le stock (avec relations produit et fournisseur)."""
    return StockService.get_all(db, skip=skip, limit=limit)


@router.get("/alertes/", response_model=List[StockResponse])
def list_alertes(db: Session = Depends(get_db)):
    """Liste les stocks sous le seuil d'alerte."""
    return StockService.get_alertes(db)


@router.get("/produit/{produit_id}", response_model=List[StockResponse])
def list_stocks_par_produit(produit_id: int, db: Session = Depends(get_db)):
    """Liste le stock d'un produit donné."""
    return StockService.get_by_produit(db, produit_id)


@router.get("/{stock_id}", response_model=StockResponse)
def get_stock(stock_id: int, db: Session = Depends(get_db)):
    """Récupère une entrée de stock par ID."""
    stock = StockService.get_by_id(db, stock_id)
    if not stock:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Stock {stock_id} non trouvé",
        )
    return stock


@router.post("/", response_model=StockResponse, status_code=status.HTTP_201_CREATED)
def create_stock(data: StockCreate, db: Session = Depends(get_db)):
    """Crée une nouvelle entrée de stock."""
    try:
        return StockService.create(db, data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.put("/{stock_id}", response_model=StockResponse)
def update_stock(
    stock_id: int,
    data: StockUpdate,
    db: Session = Depends(get_db),
):
    """Met à jour une entrée de stock."""
    try:
        stock = StockService.update(db, stock_id, data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    if not stock:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Stock {stock_id} non trouvé",
        )
    return stock


@router.delete("/{stock_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_stock(stock_id: int, db: Session = Depends(get_db)):
    """Supprime une entrée de stock."""
    if not StockService.delete(db, stock_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Stock {stock_id} non trouvé",
        )
    return None
