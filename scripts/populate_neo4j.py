"""
Script d'insertion du dataset médical dans Neo4j.
Crée le graphe : Symptome -> Maladie -> Medicament

Usage :
    python scripts/populate_neo4j.py
"""
import json
import sys
from pathlib import Path

from neo4j import GraphDatabase

# Ajouter le projet au path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.config import get_settings


def load_dataset(path: str = "data/dataset_medical.json") -> dict:
    """Charge le dataset JSON."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def clear_database(driver):
    """Supprime tout le contenu du graphe (attention !)."""
    with driver.session() as session:
        session.run("MATCH (n) DETACH DELETE n")
        print("✓ Base Neo4j nettoyée")


def create_constraints(driver):
    """Crée les contraintes d'unicité."""
    with driver.session() as session:
        # Contraintes d'unicité sur les noms
        session.run(
            "CREATE CONSTRAINT symptome_nom IF NOT EXISTS "
            "FOR (s:Symptome) REQUIRE s.nom IS UNIQUE"
        )
        session.run(
            "CREATE CONSTRAINT maladie_nom IF NOT EXISTS "
            "FOR (m:Maladie) REQUIRE m.nom IS UNIQUE"
        )
        session.run(
            "CREATE CONSTRAINT medicament_nom IF NOT EXISTS "
            "FOR (m:Medicament) REQUIRE m.nom IS UNIQUE"
        )
        print("✓ Contraintes créées")


def insert_symptomes(driver, symptomes: list):
    """Insère les symptômes."""
    with driver.session() as session:
        for s in symptomes:
            session.run(
                """
                MERGE (s:Symptome {nom: $nom})
                SET s.synonymes = $synonymes,
                    s.gravite = $gravite
                """,
                nom=s["nom"],
                synonymes=s["synonymes"],
                gravite=s["gravite"],
            )
        print(f"✓ {len(symptomes)} symptômes insérés")


def insert_maladies(driver, maladies: list):
    """Insère les maladies."""
    with driver.session() as session:
        for m in maladies:
            session.run(
                """
                MERGE (m:Maladie {nom: $nom})
                SET m.gravite = $gravite
                """,
                nom=m["nom"],
                gravite=m["gravite"],
            )
        print(f"✓ {len(maladies)} maladies insérées")


def insert_medicaments(driver, medicaments: list):
    """Insère les médicaments."""
    with driver.session() as session:
        for m in medicaments:
            session.run(
                """
                MERGE (m:Medicament {nom: $nom})
                SET m.dci = $dci,
                    m.ordonnance_requise = $ordonnance_requise,
                    m.description = $description,
                    m.categorie = $categorie
                """,
                nom=m["nom"],
                dci=m["dci"],
                ordonnance_requise=m["ordonnance_requise"],
                description=m["description"],
                categorie=m["categorie"],
            )
        print(f"✓ {len(medicaments)} médicaments insérés")


def create_relations_symptome_maladie(driver, maladies: list):
    """Crée les relations (:Symptome)-[:INDIQUE]->(:Maladie)."""
    with driver.session() as session:
        count = 0
        for m in maladies:
            for symptome_nom in m["symptomes"]:
                session.run(
                    """
                    MATCH (s:Symptome {nom: $symptome})
                    MATCH (m:Maladie {nom: $maladie})
                    MERGE (s)-[:INDIQUE]->(m)
                    """,
                    symptome=symptome_nom,
                    maladie=m["nom"],
                )
                count += 1
        print(f"✓ {count} relations INDIQUE créées")


def create_relations_maladie_medicament(driver, associations: list):
    """Crée les relations (:Maladie)-[:TRAITEE_PAR]->(:Medicament)."""
    with driver.session() as session:
        count = 0
        for assoc in associations:
            for medicament_nom in assoc["medicaments"]:
                session.run(
                    """
                    MATCH (m:Maladie {nom: $maladie})
                    MATCH (med:Medicament {nom: $medicament})
                    MERGE (m)-[:TRAITEE_PAR]->(med)
                    """,
                    maladie=assoc["maladie"],
                    medicament=medicament_nom,
                )
                count += 1
        print(f"✓ {count} relations TRAITEE_PAR créées")


def main():
    print("=" * 60)
    print("INSERTION DU DATASET MÉDICAL DANS NEO4J")
    print("=" * 60)

    settings = get_settings()
    print(f"\nConnexion à Neo4j : {settings.neo4j_uri}")

    # Charger le dataset
    data = load_dataset()
    print(f"\nDataset chargé :")
    print(f"  - {len(data['symptomes'])} symptômes")
    print(f"  - {len(data['maladies'])} maladies")
    print(f"  - {len(data['medicaments'])} médicaments")
    print(f"  - {len(data['associations'])} associations")
    print()

    # Connexion Neo4j
    driver = GraphDatabase.driver(
        settings.neo4j_uri,
        auth=(settings.neo4j_user, settings.neo4j_password),
    )

    try:
        driver.verify_connectivity()
        print("✓ Connexion Neo4j OK\n")

        # Nettoyer
        clear_database(driver)

        # Contraintes
        create_constraints(driver)

        # Insertion
        insert_symptomes(driver, data["symptomes"])
        insert_maladies(driver, data["maladies"])
        insert_medicaments(driver, data["medicaments"])

        # Relations
        create_relations_symptome_maladie(driver, data["maladies"])
        create_relations_maladie_medicament(driver, data["associations"])

        # Statistiques finales
        with driver.session() as session:
            result = session.run("MATCH (n) RETURN count(n) AS total")
            total = result.single()["total"]
            result = session.run("MATCH ()-[r]->() RETURN count(r) AS total")
            total_rel = result.single()["total"]

        print(f"\n{'=' * 60}")
        print(f"✓ INSERTION TERMINÉE")
        print(f"  - Nœuds     : {total}")
        print(f"  - Relations : {total_rel}")
        print(f"{'=' * 60}")

    finally:
        driver.close()


if __name__ == "__main__":
    main()
