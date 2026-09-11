"""Tests des schémas Stock."""
import pytest
from datetime import date
from pydantic import ValidationError

from src.schemas.stock import StockCreate, StockUpdate


class TestStockCreate:
    def test_valide(self):
        s = StockCreate(produit_id=1, quantite=50, seuil_alerte=10)
        assert s.produit_id == 1
        assert s.quantite == 50
        assert s.seuil_alerte == 10

    def test_avec_fournisseur(self):
        s = StockCreate(produit_id=1, fournisseur_id=2, quantite=50)
        assert s.fournisseur_id == 2

    def test_avec_date_peremption(self):
        s = StockCreate(produit_id=1, date_peremption=date(2027, 12, 31))
        assert s.date_peremption == date(2027, 12, 31)

    def test_produit_id_obligatoire(self):
        with pytest.raises(ValidationError):
            StockCreate(quantite=50)

    def test_quantite_negative_rejetee(self):
        with pytest.raises(ValidationError):
            StockCreate(produit_id=1, quantite=-5)

    def test_seuil_negative_rejete(self):
        with pytest.raises(ValidationError):
            StockCreate(produit_id=1, seuil_alerte=-1)


class TestStockUpdate:
    def test_tous_optionnels(self):
        s = StockUpdate()
        assert s.quantite is None
        assert s.seuil_alerte is None
