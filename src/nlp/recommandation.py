"""
Service de recommandation de médicaments.
Utilise Neo4j pour trouver les maladies et médicaments associés.
"""
from typing import List, Dict, Optional
from neo4j import GraphDatabase

from src.config import get_settings


class RecommandationService:
    """
    Recommande des médicaments à partir d'une liste de symptômes.
    """

    def __init__(self):
        settings = get_settings()
        self.driver = GraphDatabase.driver(
            settings.neo4j_uri,
            auth=(settings.neo4j_user, settings.neo4j_password),
        )

    def close(self):
        self.driver.close()

    def trouver_maladies(self, symptomes: List[str], seuil_min: int = 1) -> List[Dict]:
        """
        Trouve les maladies correspondant aux symptômes.
        Classe par nombre de symptômes correspondants (décroissant).

        Args:
            symptomes: liste des noms canoniques des symptômes
            seuil_min: nombre minimum de symptômes en commun

        Returns:
            liste de dict {nom, nb_symptomes, total_symptomes, score}
        """
        if not symptomes:
            return []

        query = """
        MATCH (s:Symptome)-[:INDIQUE]->(m:Maladie)
        WHERE s.nom IN $symptomes
        WITH m, collect(DISTINCT s.nom) AS symptomes_trouves
        OPTIONAL MATCH (m)<-[:INDIQUE]-(tous:Symptome)
        WITH m, symptomes_trouves, count(DISTINCT tous) AS total
        WHERE size(symptomes_trouves) >= $seuil
        RETURN m.nom AS nom,
               size(symptomes_trouves) AS nb_symptomes,
               total AS total_symptomes,
               toFloat(size(symptomes_trouves)) / total AS score
		ORDER BY nb_symptomes DESC, score DESC
		"""

        with self.driver.session() as session:
            result = session.run(
                query,
                symptomes=symptomes,
                seuil=seuil_min,
            )
            return [dict(record) for record in result]

    def trouver_medicaments(self, maladie_nom: str) -> List[Dict]:
        """
        Trouve les médicaments associés à une maladie.
        """
        query = """
        MATCH (m:Maladie {nom: $nom})-[:TRAITEE_PAR]->(med:Medicament)
        RETURN med.nom AS nom,
               med.dci AS dci,
               med.ordonnance_requise AS ordonnance_requise,
               med.description AS description,
               med.categorie AS categorie
        ORDER BY med.ordonnance_requise ASC, med.nom ASC
        """

        with self.driver.session() as session:
            result = session.run(query, nom=maladie_nom)
            return [dict(record) for record in result]

    def recommander(
        self,
        symptomes: List[str],
        seuil_min: int = 1,
        max_maladies: int = 3,
    ) -> Dict:
        """
        Pipeline complet : symptômes → maladies → médicaments.

        Returns:
            {
                "maladies": [...],
                "medicaments": [...],  # dédupliqués
            }
        """
        maladies = self.trouver_maladies(symptomes, seuil_min)[:max_maladies]

        medicaments_vus = set()
        medicaments_finaux = []

        for maladie in maladies:
            meds = self.trouver_medicaments(maladie["nom"])
            for med in meds:
                if med["nom"] not in medicaments_vus:
                    medicaments_vus.add(med["nom"])
                    med["maladie_associee"] = maladie["nom"]
                    medicaments_finaux.append(med)

        return {
            "maladies": maladies,
            "medicaments": medicaments_finaux,
        }

    def get_symptomes_maladie(self, maladie_nom: str) -> List[str]:
        """Retourne tous les symptômes d'une maladie."""
        query = """
        MATCH (s:Symptome)-[:INDIQUE]->(m:Maladie {nom: $nom})
        RETURN s.nom AS nom
        ORDER BY s.nom
        """
        with self.driver.session() as session:
            result = session.run(query, nom=maladie_nom)
            return [record["nom"] for record in result]


# Singleton
_instance: Optional[RecommandationService] = None


def get_recommandation_service() -> RecommandationService:
    global _instance
    if _instance is None:
        _instance = RecommandationService()
    return _instance
