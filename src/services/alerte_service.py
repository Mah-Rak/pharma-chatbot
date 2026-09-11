"""
Service métier pour les alertes.
Gère la création, résolution et consultation des alertes.
"""
from typing import List, Optional

from sqlalchemy.orm import Session, joinedload

from src.db.models import Alerte, Stock
from src.schemas.alerte import AlerteCreate, AlerteUpdate


class AlerteService:
    @staticmethod
    def get_all(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        resolue: Optional[bool] = None,
    ) -> List[Alerte]:
        """Récupère les alertes, avec filtre optionnel sur 'resolue'."""
        query = db.query(Alerte).options(joinedload(Alerte.produit))

        if resolue is not None:
            query = query.filter(Alerte.resolue == resolue)

        return query.offset(skip).limit(limit).all()

    @staticmethod
    def get_by_id(db: Session, alerte_id: int) -> Optional[Alerte]:
        return (
            db.query(Alerte)
            .options(joinedload(Alerte.produit))
            .filter(Alerte.id == alerte_id)
            .first()
        )

    @staticmethod
    def get_non_resolues(db: Session) -> List[Alerte]:
        """Récupère toutes les alertes non résolues."""
        return (
            db.query(Alerte)
            .options(joinedload(Alerte.produit))
            .filter(Alerte.resolue == False)  # noqa: E712
            .all()
        )

    @staticmethod
    def get_by_produit(
        db: Session,
        produit_id: int,
        resolue: Optional[bool] = None,
    ) -> List[Alerte]:
        """Récupère les alertes d'un produit donné."""
        query = (
            db.query(Alerte)
            .options(joinedload(Alerte.produit))
            .filter(Alerte.produit_id == produit_id)
        )
        if resolue is not None:
            query = query.filter(Alerte.resolue == resolue)
        return query.all()

    @staticmethod
    def create(db: Session, data: AlerteCreate) -> Alerte:
        """Crée une nouvelle alerte."""
        alerte = Alerte(**data.model_dump())
        db.add(alerte)
        db.commit()
        db.refresh(alerte)
        return alerte

    @staticmethod
    def update(db: Session, alerte_id: int, data: AlerteUpdate) -> Optional[Alerte]:
        """Met à jour une alerte (ex : la marquer comme résolue)."""
        alerte = AlerteService.get_by_id(db, alerte_id)
        if not alerte:
            return None

        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(alerte, key, value)

        db.commit()
        db.refresh(alerte)
        return alerte

    @staticmethod
    def delete(db: Session, alerte_id: int) -> bool:
        """Supprime une alerte."""
        alerte = AlerteService.get_by_id(db, alerte_id)
        if not alerte:
            return False
        db.delete(alerte)
        db.commit()
        return True

    # ========== LOGIQUE MÉTIER AUTOMATIQUE ==========

    @staticmethod
    def verifier_et_creer_alerte(db: Session, stock: Stock) -> Optional[Alerte]:
        """
        Vérifie le stock et crée une alerte si la quantité est sous le seuil.
        Appelé automatiquement après create/update d'un stock.
        """
        if stock.quantite > stock.seuil_alerte:
            # Pas d'alerte nécessaire — résoudre les alertes existantes
            AlerteService._resoudre_alertes_produit(db, stock.produit_id, "epuisement")
            return None

        # Vérifier si une alerte non résolue existe déjà pour ce produit
        existante = (
            db.query(Alerte)
            .filter(
                Alerte.produit_id == stock.produit_id,
                Alerte.type == "epuisement",
                Alerte.resolue == False,  # noqa: E712
            )
            .first()
        )

        if existante:
            # Mettre à jour le message
            existante.message = (
                f"Stock bas : {stock.quantite} unités "
                f"(seuil : {stock.seuil_alerte})"
            )
            db.commit()
            db.refresh(existante)
            return existante

        # Créer une nouvelle alerte
        alerte = Alerte(
            produit_id=stock.produit_id,
            type="epuisement",
            message=f"Stock bas : {stock.quantite} unités (seuil : {stock.seuil_alerte})",
            resolue=False,
        )
        db.add(alerte)
        db.commit()
        db.refresh(alerte)
        return alerte

    @staticmethod
    def _resoudre_alertes_produit(db: Session, produit_id: int, type_alerte: str) -> int:
        """Résout toutes les alertes non résolues d'un produit pour un type donné."""
        count = (
            db.query(Alerte)
            .filter(
                Alerte.produit_id == produit_id,
                Alerte.type == type_alerte,
                Alerte.resolue == False,  # noqa: E712
            )
            .update({"resolue": True})
        )
        db.commit()
        return count
