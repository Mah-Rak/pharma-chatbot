"""Tests du module NLP (normalisation + détection de symptômes)."""
from src.utils.text_utils import normaliser_texte, contient_expression
from src.nlp.symptome_detector import SymptomeDetector, get_detector


class TestNormalisation:
    def test_minuscules(self):
        assert normaliser_texte("BONJOUR") == "bonjour"

    def test_accents(self):
        assert normaliser_texte("fièvre") == "fievre"
        assert normaliser_texte("tête") == "tete"

    def test_apostrophes(self):
        assert normaliser_texte("j'ai") == "j ai"

    def test_ponctuation(self):
        assert normaliser_texte("Bonjour !") == "bonjour"
        assert normaliser_texte("Ça va ?") == "ca va"

    def test_espaces_multiples(self):
        assert normaliser_texte("bonjour    monde") == "bonjour monde"

    def test_chaine_vide(self):
        assert normaliser_texte("") == ""
        assert normaliser_texte(None) == ""

    def test_exemple_complet(self):
        result = normaliser_texte("J'ai MAL à la tête !")
        assert result == "j ai mal a la tete"


class TestContientExpression:
    def test_expression_presente(self):
        assert contient_expression("j ai mal a la tete", "mal a la tete") is True

    def test_expression_absente(self):
        assert contient_expression("j ai mal a la tete", "fievre") is False

    def test_word_boundary(self):
        # "mal" ne doit pas matcher dans "normalement"
        assert contient_expression("normalement", "mal") is False

    def test_expression_vide(self):
        assert contient_expression("bonjour", "") is False


class TestSymptomeDetector:
    def test_chargement_dataset(self):
        detector = get_detector()
        assert len(detector.symptomes) > 0
        assert "fievre" in detector.symptomes

    def test_detection_simple(self):
        d = get_detector()
        result = d.detecter("J'ai de la fièvre")
        assert "fievre" in result

    def test_detection_multiple(self):
        d = get_detector()
        result = d.detecter("J'ai mal à la tête et de la fièvre")
        assert "fievre" in result
        assert "mal_de_tete" in result

    def test_detection_avec_synonymes(self):
        d = get_detector()
        # "température" est synonyme de "fièvre"
        result = d.detecter("J'ai de la température")
        assert "fievre" in result

    def test_detection_aucun_symptome(self):
        d = get_detector()
        result = d.detecter("Bonjour, comment allez-vous ?")
        assert result == []

    def test_detection_texte_vide(self):
        d = get_detector()
        assert d.detecter("") == []
        assert d.detecter(None) == []

    def test_detection_cas_grave(self):
        d = get_detector()
        result = d.detecter("J'ai mal à la poitrine")
        assert "douleur_thoracique" in result

    def test_detecter_avec_details_urgent(self):
        d = get_detector()
        details = d.detecter_avec_details("J'ai mal à la poitrine")
        assert details["est_urgent"] is True
        assert len(details["cas_graves"]) > 0

    def test_detecter_avec_details_non_urgent(self):
        d = get_detector()
        details = d.detecter_avec_details("J'ai de la fièvre")
        assert details["est_urgent"] is False
