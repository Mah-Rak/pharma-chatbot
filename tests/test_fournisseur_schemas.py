"""Tests des schémas Fournisseur."""
import pytest
from pydantic import ValidationError

from src.schemas.fournisseur import FournisseurCreate, FournisseurUpdate


class TestFournisseurCreate:
    def test_valide(self):
        f = FournisseurCreate(nom="PharmaDistrib")
        assert f.nom == "PharmaDistrib"
        assert f.email is None

    def test_avec_email_valide(self):
        f = FournisseurCreate(nom="Test", email="contact@test.com")
        assert f.email == "contact@test.com"

    def test_email_invalide_rejete(self):
        with pytest.raises(ValidationError):
            FournisseurCreate(nom="Test", email="pas-un-email")

    def test_nom_vide_rejete(self):
        with pytest.raises(ValidationError):
            FournisseurCreate(nom="")


class TestFournisseurUpdate:
    def test_tous_optionnels(self):
        f = FournisseurUpdate()
        assert f.nom is None
        assert f.email is None
