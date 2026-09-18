"""Tests du service de recommandation (Neo4j)."""
import pytest

from src.nlp.recommandation import get_recommandation_service


@pytest.fixture
def reco():
    service = get_recommandation_service()
    yield service
    # Ne pas fermer le driver entre les tests (singleton)


class TestTrouverMaladies:
    def test_symptomes_grippaux(self, reco):
        maladies = reco.trouver_maladies(["fievre", "mal_de_tete", "courbatures"])
        noms = [m["nom"] for m in maladies]
        assert "Grippe" in noms

    def test_grippe_en_tete(self, reco):
        """La Grippe doit être en tête (2 symptômes matchés)."""
        maladies = reco.trouver_maladies(["fievre", "mal_de_tete"])
        assert len(maladies) > 0
        # Le premier doit avoir 2 symptômes matchés
        assert maladies[0]["nb_symptomes"] >= 2

    def test_aucun_symptome(self, reco):
        maladies = reco.trouver_maladies([])
        assert maladies == []

    def test_symptome_inconnu(self, reco):
        maladies = reco.trouver_maladies(["symptome_inexistant"])
        assert maladies == []

    def test_seuil_minimum(self, reco):
        maladies = reco.trouver_maladies(["fievre"], seuil_min=1)
        assert len(maladies) > 0


class TestTrouverMedicaments:
    def test_medicaments_grippe(self, reco):
        meds = reco.trouver_medicaments("Grippe")
        noms = [m["nom"] for m in meds]
        assert "Paracetamol" in noms

    def test_medicament_ordonnance(self, reco):
        meds = reco.trouver_medicaments("Infection_urinaire")
        # Au moins un médicament sur ordonnance
        assert any(m["ordonnance_requise"] for m in meds)

    def test_maladie_inexistante(self, reco):
        meds = reco.trouver_medicaments("MaladieInexistante")
        assert meds == []


class TestRecommander:
    def test_pipeline_complet(self, reco):
        result = reco.recommander(["fievre", "mal_de_tete", "courbatures"])
        assert "maladies" in result
        assert "medicaments" in result
        assert len(result["maladies"]) > 0
        assert len(result["medicaments"]) > 0

    def test_medicaments_dedupliques(self, reco):
        result = reco.recommander(["fievre", "mal_de_tete"])
        noms = [m["nom"] for m in result["medicaments"]]
        # Pas de doublons
        assert len(noms) == len(set(noms))


class TestGetSymptomesMaladie:
    def test_grippe(self, reco):
        symptomes = reco.get_symptomes_maladie("Grippe")
        assert "fievre" in symptomes
        assert "courbatures" in symptomes

    def test_maladie_inexistante(self, reco):
        assert reco.get_symptomes_maladie("Inexistante") == []
