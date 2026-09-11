"""Tests des schémas Pydantic."""
import pytest
from decimal import Decimal
from pydantic import ValidationError

from src.schemas.produit import ProduitCreate, ProduitUpdate, ProduitResponse


class TestProduitCreate:
    def test_valide(self):
        p = ProduitCreate(nom="Test", prix=Decimal("2.50"))
        assert p.nom == "Test"
        assert p.prix == Decimal("2.50")
        assert p.ordonnance_requise is False

    def test_nom_vide_rejete(self):
        with pytest.raises(ValidationError):
            ProduitCreate(nom="", prix=Decimal("2.50"))

    def test_prix_negatif_rejete(self):
        with pytest.raises(ValidationError):
            ProduitCreate(nom="Test", prix=Decimal("-5"))

    def test_prix_zero_rejete(self):
        with pytest.raises(ValidationError):
            ProduitCreate(nom="Test", prix=Decimal("0"))


class TestProduitUpdate:
    def test_tous_champs_optionnels(self):
        p = ProduitUpdate()
        assert p.nom is None
        assert p.prix is None

    def test_mise_a_jour_partielle(self):
        p = ProduitUpdate(prix=Decimal("3.00"))
        assert p.prix == Decimal("3.00")
        assert p.nom is None
