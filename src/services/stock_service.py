"""
Service métier pour le stock.
Gère les vérifications de clés étrangères et les relations.
"""
from typing import List, Optional

from sqlalchemy.orm import Session, joinedload

from src.db.models import Stock, Produit, Fournisseur
from src.schemas.stock import StockCreate, StockUpdate


class StockService:
    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100) -> List[Stock]:
        """Récupère tout le stock avec les relations pré-chargées."""
        return (
            db.query(Stock)
            .options(joinedload(Stock.produit), joinedload(Stock.fournisseur))
            .offset(skip)
            .limit(limit)
            .all()
        )

    @staticmethod
    def get_by_id(db: Session, stock_id: int) -> Optional[Stock]:
        """Récupère une entrée de stock par ID avec relations."""
        return (
            db.query(Stock)
            .options(joinedload(Stock.produit), joinedload(Stock.fournisseur))
            .filter(Stock.id == stock_id)
            .first()
        )

    @staticmethod
    def get_by_produit(db: Session, produit_id: int) -> List[Stock]:
        """Récupère tout le stock d'un produit donné."""
        return (
            db.query(Stock)
            .options(joinedload(Stock.produit), joinedload(Stock.fournisseur))
            .filter(Stock.produit_id == produit_id)
            .all()
        )

    @staticmethod
    def get_alertes(db: Session) -> List[Stock]:
        """Récupère les stocks sous le seuil d'alerte."""
        return (
            db.query(Stock)
            .options(joinedload(Stock.produit), joinedload(Stock.fournisseur))
            .filter(Stock.quantite <= Stock.seuil_alerte)
            .all()
        )

    @staticmethod
    def create(db: Session, data: StockCreate) -> Stock:
        """
        Crée une entrée de stock.
        Vérifie que le produit et le fournisseur existent.
        Déclenche automatiquement une alerte si le stock est bas.
        """
        # Vérifier que le produit existe
        produit = db.query(Produit).filter(Produit.id == data.produit_id).first()
        if not produit:
            raise ValueError(f"Produit {data.produit_id} introuvable")

        # Vérifier que le fournisseur existe (si fourni)
        if data.fournisseur_id is not None:
            fournisseur = db.query(Fournisseur).filter(
                Fournisseur.id == data.fournisseur_id
            ).first()
            if not fournisseur:
                raise ValueError(f"Fournisseur {data.fournisseur_id} introuvable")

        stock = Stock(**data.model_dump())
        db.add(stock)
        db.commit()
        db.refresh(stock)

        # Hook : vérifier et créer une alerte si nécessaire
        from src.services.alerte_service import AlerteService
        AlerteService.verifier_et_creer_alerte(db, stock)

        return stock

    @staticmethod
    def update(db: Session, stock_id: int, data: StockUpdate) -> Optional[Stock]:
        """
        Met à jour une entrée de stock.
        Déclenche automatiquement la gestion des alertes.
        """
        stock = StockService.get_by_id(db, stock_id)
        if not stock:
            return None

        # Vérifier le fournisseur si modifié
        if data.fournisseur_id is not None:
            fournisseur = db.query(Fournisseur).filter(
                Fournisseur.id == data.fournisseur_id
            ).first()
            if not fournisseur:
                raise ValueError(f"Fournisseur {data.fournisseur_id} introuvable")

        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(stock, key, value)

        db.commit()
        db.refresh(stock)

        # Hook : vérifier et gérer les alertes
        from src.services.alerte_service import AlerteService
        AlerteService.verifier_et_creer_alerte(db, stock)

        return stock

    @staticmethod
    def delete(db: Session, stock_id: int) -> bool:
        """Supprime une entrée de stock."""
        stock = StockService.get_by_id(db, stock_id)
        if not stock:
            return False
        db.delete(stock)
        db.commit()
        return True
