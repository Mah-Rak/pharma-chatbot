"""
Service de détection de symptômes dans un texte libre.
Approche : normalisation + correspondance de synonymes.
"""
import json
from pathlib import Path
from typing import List, Dict, Set

from src.utils.text_utils import normaliser_texte, contient_expression


class SymptomeDetector:
    """
    Détecte les symptômes mentionnés dans un texte.
    Utilise les synonymes du dataset médical.
    """

    def __init__(self, dataset_path: str = "data/dataset_medical.json"):
        self.dataset_path = dataset_path
        self.symptomes: Dict[str, dict] = {}
        self.synonymes_index: Dict[str, str] = {}
        self.cas_graves: List[dict] = []
        self._charger_dataset()

    def _charger_dataset(self):
        """Charge le dataset et construit l'index des synonymes."""
        path = Path(self.dataset_path)
        if not path.exists():
            raise FileNotFoundError(f"Dataset introuvable : {self.dataset_path}")

        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        for s in data["symptomes"]:
            nom = s["nom"]
            self.symptomes[nom] = s

            for syn in s["synonymes"]:
                syn_norm = normaliser_texte(syn)
                if syn_norm:
                    self.synonymes_index[syn_norm] = nom

            nom_norm = normaliser_texte(nom)
            if nom_norm:
                self.synonymes_index[nom_norm] = nom

        self.cas_graves = data.get("cas_graves", [])

    def detecter(self, texte: str) -> List[str]:
        """
        Détecte les symptômes dans un texte.
        Retourne la liste des noms canoniques.
        """
        if not texte:
            return []

        texte_norm = normaliser_texte(texte)
        if not texte_norm:
            return []

        detectes: Set[str] = set()

        # Parcourir du plus long au plus court pour éviter les faux positifs
        for syn_norm, nom_canonique in sorted(
            self.synonymes_index.items(),
            key=lambda x: len(x[0]),
            reverse=True,
        ):
            if contient_expression(texte_norm, syn_norm):
                detectes.add(nom_canonique)

        return sorted(detectes)

    def detecter_avec_details(self, texte: str) -> dict:
        """Version détaillée avec gravité et cas graves."""
        symptomes = self.detecter(texte)

        cas_graves_detectes = [
            cg for cg in self.cas_graves if cg["symptome"] in symptomes
        ]

        return {
            "symptomes": symptomes,
            "cas_graves": cas_graves_detectes,
            "est_urgent": len(cas_graves_detectes) > 0,
        }

    def get_symptome(self, nom: str) -> dict:
        """Retourne les infos d'un symptôme."""
        return self.symptomes.get(nom, {})


# Singleton
_detector_instance: SymptomeDetector | None = None


def get_detector() -> SymptomeDetector:
    """Retourne l'instance unique du détecteur."""
    global _detector_instance
    if _detector_instance is None:
        _detector_instance = SymptomeDetector()
    return _detector_instance
