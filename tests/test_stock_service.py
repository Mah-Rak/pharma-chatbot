"""Tests du service StockService."""
from decimal import Decimal
import pytest

from src.schemas.produit import ProduitCreate
from src.schemas.fournisseur import FournisseurCreate
from src.schemas.stock import StockCreate, StockUpdate
from src.services.produit_service import ProduitService
from src.services.fournisseur_service import FournisseurService
from src.services.stock_service import StockService


@pytest.fixture
def produit(db_session):
    return ProduitService.create(db_session, ProduitCreate(nom="Test Produit", prix=Decimal("2.50")))


@pytest.fixture
def fournisseur(db_session):
    return FournisseurService.create(db_session, FournisseurCreate(nom="Test Fournisseur"))


class TestStockServiceCreate:
    def test_create(self, db_session, produit):
        stock = StockService.create(db_session, StockCreate(produit_id=produit.id, quantite=50))
        assert stock.id is not None
        assert stock.quantite == 50

    def test_create_avec_fournisseur(self, db_session, produit, fournisseur):
        stock = StockService.create(db_session, StockCreate(
            produit_id=produit.id, fournisseur_id=fournisseur.id, quantite=30
        ))
        assert stock.fournisseur_id == fournisseur.id

    def test_create_produit_inexistant(self, db_session):
        with pytest.raises(ValueError, match="introuvable"):
            StockService.create(db_session, StockCreate(produit_id=99999, quantite=10))

    def test_create_fournisseur_inexistant(self, db_session, produit):
        with pytest.raises(ValueError, match="introuvable"):
            StockService.create(db_session, StockCreate(
                produit_id=produit.id, fournisseur_id=99999, quantite=10
            ))


class TestStockServiceRead:
    def test_get_by_id(self, db_session, produit):
        stock = StockService.create(db_session, StockCreate(produit_id=produit.id, quantite=50))
        lu = StockService.get_by_id(db_session, stock.id)
        assert lu is not None
        assert lu.quantite == 50
        assert lu.produit is not None

    def test_get_all(self, db_session, produit):
        StockService.create(db_session, StockCreate(produit_id=produit.id, quantite=10))
        StockService.create(db_session, StockCreate(produit_id=produit.id, quantite=20))
        assert len(StockService.get_all(db_session)) == 2

    def test_get_by_produit(self, db_session, produit):
        StockService.create(db_session, StockCreate(produit_id=produit.id, quantite=10))
        resultats = StockService.get_by_produit(db_session, produit.id)
        assert len(resultats) == 1

    def test_get_alertes(self, db_session, produit):
        StockService.create(db_session, StockCreate(produit_id=produit.id, quantite=5, seuil_alerte=10))
        StockService.create(db_session, StockCreate(produit_id=produit.id, quantite=100, seuil_alerte=10))
        alertes = StockService.get_alertes(db_session)
        assert len(alertes) == 1
        assert alertes[0].quantite == 5


class TestStockServiceUpdate:
    def test_update(self, db_session, produit):
        stock = StockService.create(db_session, StockCreate(produit_id=produit.id, quantite=50))
        modifie = StockService.update(db_session, stock.id, StockUpdate(quantite=30))
        assert modifie.quantite == 30

    def test_update_fournisseur_inexistant(self, db_session, produit):
        stock = StockService.create(db_session, StockCreate(produit_id=produit.id, quantite=50))
        with pytest.raises(ValueError, match="introuvable"):
            StockService.update(db_session, stock.id, StockUpdate(fournisseur_id=99999))


class TestStockServiceDelete:
    def test_delete(self, db_session, produit):
        stock = StockService.create(db_session, StockCreate(produit_id=produit.id, quantite=50))
        assert StockService.delete(db_session, stock.id) is True
        assert StockService.get_by_id(db_session, stock.id) is None

    def test_delete_inexistant(self, db_session):
        assert StockService.delete(db_session, 99999) is False
