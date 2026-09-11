"""Tests des schémas Alerte."""
import pytest
from pydantic import ValidationError

from src.schemas.alerte import AlerteCreate, AlerteUpdate


class TestAlerteCreate:
    def test_valide(self):
        a = AlerteCreate(produit_id=1, type="epuisement")
        assert a.produit_id == 1
        assert a.type == "epuisement"
        assert a.resolue is False

    def test_produit_id_obligatoire(self):
        with pytest.raises(ValidationError):
            AlerteCreate(type="epuisement")

    def test_type_obligatoire(self):
        with pytest.raises(ValidationError):
            AlerteCreate(produit_id=1)

    def test_type_vide_rejete(self):
        with pytest.raises(ValidationError):
            AlerteCreate(produit_id=1, type="")


class TestAlerteUpdate:
    def test_tous_optionnels(self):
        a = AlerteUpdate()
        assert a.message is None
        assert a.resolue is None

    def test_resoudre(self):
        a = AlerteUpdate(resolue=True)
        assert a.resolue is True
