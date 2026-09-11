"""Tests du service FournisseurService."""
from src.schemas.fournisseur import FournisseurCreate, FournisseurUpdate
from src.services.fournisseur_service import FournisseurService


class TestFournisseurService:
    def test_create(self, db_session):
        f = FournisseurService.create(db_session, FournisseurCreate(nom="PharmaDistrib"))
        assert f.id is not None
        assert f.nom == "PharmaDistrib"

    def test_get_by_id(self, db_session):
        f = FournisseurService.create(db_session, FournisseurCreate(nom="Test"))
        lu = FournisseurService.get_by_id(db_session, f.id)
        assert lu.nom == "Test"

    def test_get_all(self, db_session):
        FournisseurService.create(db_session, FournisseurCreate(nom="A"))
        FournisseurService.create(db_session, FournisseurCreate(nom="B"))
        assert len(FournisseurService.get_all(db_session)) == 2

    def test_search(self, db_session):
        FournisseurService.create(db_session, FournisseurCreate(nom="PharmaDistrib"))
        FournisseurService.create(db_session, FournisseurCreate(nom="MediPlus"))
        resultats = FournisseurService.get_by_nom(db_session, "pharma")
        assert len(resultats) == 1

    def test_update(self, db_session):
        f = FournisseurService.create(db_session, FournisseurCreate(nom="Test"))
        modifie = FournisseurService.update(db_session, f.id, FournisseurUpdate(nom="Test2"))
        assert modifie.nom == "Test2"

    def test_delete(self, db_session):
        f = FournisseurService.create(db_session, FournisseurCreate(nom="Test"))
        assert FournisseurService.delete(db_session, f.id) is True
        assert FournisseurService.get_by_id(db_session, f.id) is None
