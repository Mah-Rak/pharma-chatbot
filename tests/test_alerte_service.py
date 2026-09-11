"""Tests du service AlerteService."""
from decimal import Decimal
import pytest

from src.schemas.produit import ProduitCreate
from src.schemas.stock import StockCreate
from src.schemas.alerte import AlerteCreate, AlerteUpdate
from src.services.produit_service import ProduitService
from src.services.stock_service import StockService
from src.services.alerte_service import AlerteService


@pytest.fixture
def produit(db_session):
    return ProduitService.create(
        db_session, ProduitCreate(nom="Test Alerte", prix=Decimal("2.50"))
    )


class TestAlerteServiceCRUD:
    def test_create(self, db_session, produit):
        alerte = AlerteService.create(
            db_session, AlerteCreate(produit_id=produit.id, type="epuisement")
        )
        assert alerte.id is not None
        assert alerte.type == "epuisement"

    def test_get_by_id(self, db_session, produit):
        alerte = AlerteService.create(
            db_session, AlerteCreate(produit_id=produit.id, type="epuisement")
        )
        lu = AlerteService.get_by_id(db_session, alerte.id)
        assert lu is not None
        assert lu.type == "epuisement"
        assert lu.produit is not None

    def test_get_all(self, db_session, produit):
        AlerteService.create(db_session, AlerteCreate(produit_id=produit.id, type="epuisement"))
        AlerteService.create(db_session, AlerteCreate(produit_id=produit.id, type="peremption"))
        assert len(AlerteService.get_all(db_session)) == 2

    def test_get_all_filtre_resolue(self, db_session, produit):
        a1 = AlerteService.create(db_session, AlerteCreate(produit_id=produit.id, type="epuisement"))
        AlerteService.create(db_session, AlerteCreate(produit_id=produit.id, type="peremption"))
        AlerteService.update(db_session, a1.id, AlerteUpdate(resolue=True))

        non_resolues = AlerteService.get_all(db_session, resolue=False)
        assert len(non_resolues) == 1

    def test_update(self, db_session, produit):
        alerte = AlerteService.create(
            db_session, AlerteCreate(produit_id=produit.id, type="epuisement")
        )
        modifiee = AlerteService.update(db_session, alerte.id, AlerteUpdate(resolue=True))
        assert modifiee.resolue is True

    def test_delete(self, db_session, produit):
        alerte = AlerteService.create(
            db_session, AlerteCreate(produit_id=produit.id, type="epuisement")
        )
        assert AlerteService.delete(db_session, alerte.id) is True
        assert AlerteService.get_by_id(db_session, alerte.id) is None


class TestAlerteAutomatique:
    def test_creation_stock_bas_genere_alerte(self, db_session, produit):
        """Un stock sous le seuil doit générer une alerte."""
        StockService.create(
            db_session,
            StockCreate(produit_id=produit.id, quantite=3, seuil_alerte=10),
        )
        alertes = AlerteService.get_non_resolues(db_session)
        assert len(alertes) == 1
        assert alertes[0].type == "epuisement"
        assert "Stock bas" in alertes[0].message

    def test_creation_stock_normal_pas_alerte(self, db_session, produit):
        """Un stock au-dessus du seuil ne doit pas générer d'alerte."""
        StockService.create(
            db_session,
            StockCreate(produit_id=produit.id, quantite=50, seuil_alerte=10),
        )
        assert len(AlerteService.get_non_resolues(db_session)) == 0

    def test_remonter_stock_resout_alerte(self, db_session, produit):
        """Remonter le stock doit résoudre l'alerte."""
        stock = StockService.create(
            db_session,
            StockCreate(produit_id=produit.id, quantite=3, seuil_alerte=10),
        )
        assert len(AlerteService.get_non_resolues(db_session)) == 1

        # Remonter le stock
        from src.schemas.stock import StockUpdate
        StockService.update(db_session, stock.id, StockUpdate(quantite=50))

        assert len(AlerteService.get_non_resolues(db_session)) == 0

    def test_pas_de_doublon_alerte(self, db_session, produit):
        """Deux créations de stock bas ne doivent pas créer 2 alertes."""
        StockService.create(
            db_session,
            StockCreate(produit_id=produit.id, quantite=3, seuil_alerte=10),
        )
        StockService.create(
            db_session,
            StockCreate(produit_id=produit.id, quantite=5, seuil_alerte=10),
        )
        assert len(AlerteService.get_non_resolues(db_session)) == 1
