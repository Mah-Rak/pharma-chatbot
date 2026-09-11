"""Tests du service métier ProduitService."""
from decimal import Decimal

from src.schemas.produit import ProduitCreate, ProduitUpdate
from src.services.produit_service import ProduitService


class TestProduitServiceCreate:
    def test_create(self, db_session):
        data = ProduitCreate(nom="Ibuprofène", prix=Decimal("3.20"))
        produit = ProduitService.create(db_session, data)

        assert produit.id is not None
        assert produit.nom == "Ibuprofène"
        assert produit.prix == Decimal("3.20")


class TestProduitServiceRead:
    def test_get_by_id(self, db_session):
        data = ProduitCreate(nom="Aspirine", prix=Decimal("1.80"))
        produit = ProduitService.create(db_session, data)

        lu = ProduitService.get_by_id(db_session, produit.id)
        assert lu is not None
        assert lu.nom == "Aspirine"

    def test_get_by_id_inexistant(self, db_session):
        assert ProduitService.get_by_id(db_session, 99999) is None

    def test_get_all(self, db_session):
        ProduitService.create(db_session, ProduitCreate(nom="A", prix=Decimal("1")))
        ProduitService.create(db_session, ProduitCreate(nom="B", prix=Decimal("2")))

        produits = ProduitService.get_all(db_session)
        assert len(produits) == 2

    def test_get_by_nom(self, db_session):
        ProduitService.create(db_session, ProduitCreate(nom="Paracétamol", prix=Decimal("2")))
        ProduitService.create(db_session, ProduitCreate(nom="Ibuprofène", prix=Decimal("3")))

        resultats = ProduitService.get_by_nom(db_session, "para")
        assert len(resultats) == 1
        assert resultats[0].nom == "Paracétamol"


class TestProduitServiceUpdate:
    def test_update(self, db_session):
        produit = ProduitService.create(
            db_session, ProduitCreate(nom="Test", prix=Decimal("1.00"))
        )
        modifie = ProduitService.update(
            db_session, produit.id, ProduitUpdate(prix=Decimal("2.00"))
        )

        assert modifie.prix == Decimal("2.00")
        assert modifie.nom == "Test"  # inchangé

    def test_update_inexistant(self, db_session):
        resultat = ProduitService.update(
            db_session, 99999, ProduitUpdate(prix=Decimal("2.00"))
        )
        assert resultat is None


class TestProduitServiceDelete:
    def test_delete(self, db_session):
        produit = ProduitService.create(
            db_session, ProduitCreate(nom="Test", prix=Decimal("1"))
        )
        assert ProduitService.delete(db_session, produit.id) is True
        assert ProduitService.get_by_id(db_session, produit.id) is None

    def test_delete_inexistant(self, db_session):
        assert ProduitService.delete(db_session, 99999) is False
