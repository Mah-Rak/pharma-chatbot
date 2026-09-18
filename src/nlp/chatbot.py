"""
Orchestrateur du chatbot.
Combine : NLP + Neo4j + PostgreSQL + MongoDB
"""
from typing import List, Optional
from datetime import datetime

from sqlalchemy.orm import Session

from src.nlp.symptome_detector import get_detector
from src.nlp.recommandation import get_recommandation_service
from src.services.chat_service import get_chat_log_service
from src.services.stock_service import StockService
from src.schemas.chatbot import (
    ChatRequest,
    ChatResponse,
    MaladieProposee,
    MedicamentPropose,
)

# Dictionnaire d'accents pour les noms courants
ACCENTS = {
    "tete": "tête",
    "fievre": "fièvre",
    "nausee": "nausée",
    "nausees": "nausées",
    "diarrhee": "diarrhée",
    "vomissement": "vomissement",
    "brulures": "brûlures",
    "brulure": "brûlure",
    "estomac": "estomac",
    "demangeaisons": "démangeaisons",
    "rougeurs": "rougeurs",
    "oreille": "oreille",
    "douloureuse": "douloureuse",
    "peremption": "péremption",
    "paracetamol": "Paracétamol",
    "ibuprofene": "Ibuprofène",
    "cetirizine": "Cétirizine",
    "omeprazole": "Oméprazole",
}


def formatter_nom(nom: str) -> str:
    """
    Convertit un nom technique en nom lisible avec accents.
    """
    if not nom:
        return ""

    # Remplacer les underscores par des espaces
    nom = nom.replace("_", " ")

    # Appliquer les accents sur chaque mot
    mots = nom.split()
    mots_accentues = [ACCENTS.get(mot.lower(), mot) for mot in mots]

    return " ".join(mots_accentues)
AVERTISSEMENT_DEFAUT = (
    "Ces recommandations sont données à titre indicatif. "
    "Consultez un médecin ou un pharmacien en cas de doute."
)

AVERTISSEMENT_ORDONNANCE = (
    "Certains médicaments recommandés nécessitent une ordonnance. "
    "Consultez un médecin."
)


class ChatbotService:
    """Service principal du chatbot."""

    def __init__(self):
        self.detector = get_detector()
        self.recommandation = get_recommandation_service()
        self.chat_log = get_chat_log_service()

    def traiter(self, request: ChatRequest, db: Session) -> ChatResponse:
        """
        Pipeline complet :
        1. Détection des symptômes
        2. Recherche des maladies/médicaments
        3. Vérification du stock
        4. Formulation de la réponse
        5. Log MongoDB
        """
        # 1. Détection des symptômes
        details = self.detector.detecter_avec_details(request.message)
        symptomes = details["symptomes"]
        cas_graves = details["cas_graves"]
        est_urgent = details["est_urgent"]

        # 2. Cas urgent : réponse immédiate
        if est_urgent:
            reponse = self._formuler_reponse_urgente(cas_graves)
            self._logger(request, symptomes, [], [], reponse, est_urgent=True)

            return ChatResponse(
                message_original=request.message,
                symptomes_detectes=symptomes,
                maladies_probables=[],
                medicaments_recommandes=[],
                reponse=reponse,
                est_urgent=True,
                avertissement=None,
            )

        # 3. Si aucun symptôme détecté
        if not symptomes:
            reponse = (
                "Je n'ai pas réussi à identifier de symptômes précis dans votre message. "
                "Pouvez-vous décrire ce que vous ressentez ? "
                "Par exemple : « J'ai mal à la tête et de la fièvre »."
            )
            self._logger(request, [], [], [], reponse)

            return ChatResponse(
                message_original=request.message,
                symptomes_detectes=[],
                maladies_probables=[],
                medicaments_recommandes=[],
                reponse=reponse,
                avertissement=None,
            )

        # 4. Recommandation via Neo4j
        reco = self.recommandation.recommander(symptomes)

        maladies = [
            MaladieProposee(
                nom=m["nom"],
                nb_symptomes=m["nb_symptomes"],
                total_symptomes=m["total_symptomes"],
                score=round(m["score"], 3),
            )
            for m in reco["maladies"]
        ]

        # 5. Enrichir les médicaments avec le stock
        medicaments = []
        for med in reco["medicaments"]:
            stock_dispo = self._verifier_stock(db, med["nom"])
            medicaments.append(
                MedicamentPropose(
                    nom=med["nom"],
                    dci=med.get("dci"),
                    description=med.get("description"),
                    categorie=med.get("categorie"),
                    ordonnance_requise=med.get("ordonnance_requise", False),
                    maladie_associee=med.get("maladie_associee"),
                    stock_disponible=stock_dispo,
                )
            )

        # 6. Formuler la réponse
        reponse = self._formuler_reponse(symptomes, maladies, medicaments)

        # 7. Avertissement
        avertissement = AVERTISSEMENT_DEFAUT
        if any(m.ordonnance_requise for m in medicaments):
            avertissement = AVERTISSEMENT_ORDONNANCE + " " + AVERTISSEMENT_DEFAUT

        # 8. Log
        self._logger(
            request,
            symptomes,
            [m.nom for m in maladies],
            [m.nom for m in medicaments],
            reponse,
        )

        return ChatResponse(
            message_original=request.message,
            symptomes_detectes=symptomes,
            maladies_probables=maladies,
            medicaments_recommandes=medicaments,
            reponse=reponse,
            est_urgent=False,
            avertissement=avertissement,
        )

    def _verifier_stock(self, db: Session, medicament_nom: str) -> Optional[int]:
        """
        Cherche un produit en stock correspondant au nom du médicament.
        Retourne la quantité totale disponible, ou None.
        """
        from src.db.models import Produit, Stock

        # Recherche partielle par nom (insensible à la casse)
        produit = (
            db.query(Produit)
            .filter(Produit.nom.ilike(f"%{medicament_nom}%"))
            .first()
        )

        if not produit:
            return None

        stocks = db.query(Stock).filter(Stock.produit_id == produit.id).all()
        if not stocks:
            return 0

        return sum(s.quantite for s in stocks)

    def _formuler_reponse_urgente(self, cas_graves: List[dict]) -> str:
        """Formule une réponse pour les cas graves."""
        messages = [cg["message"] for cg in cas_graves]
        return "⚠️ URGENCE MÉDICALE\n\n" + "\n".join(messages)

    def _formuler_reponse(
        self,
        symptomes: List[str],
        maladies: List[MaladieProposee],
        medicaments: List[MedicamentPropose],
    ) -> str:
        """Formule une réponse textuelle."""
        if not maladies:
            return (
                "Je n'ai pas trouvé de maladie correspondant à ces symptômes "
                "dans ma base de connaissances. Consultez un médecin ou un pharmacien."
            )

        # Formater les symptômes
        symptomes_lisibles = [formatter_nom(s) for s in symptomes]

        # Formater les maladies
        maladies_lisibles = [formatter_nom(m.nom) for m in maladies[:2]]

        lignes = [
            f"J'ai identifié : {', '.join(symptomes_lisibles)}.",
            "",
            f"Maladie(s) probable(s) : {', '.join(maladies_lisibles)}.",
            "",
        ]

        if medicaments:
            lignes.append("Médicaments suggérés :")
            for m in medicaments[:5]:
                nom_lisible = formatter_nom(m.nom)
                dispo = ""
                if m.stock_disponible is not None:
                    if m.stock_disponible > 0:
                        dispo = f" (en stock : {m.stock_disponible})"
                    else:
                        dispo = " (⚠️ rupture de stock)"
                ord_ = " [ordonnance]" if m.ordonnance_requise else ""
                lignes.append(f"  • {nom_lisible}{ord_}{dispo}")
        else:
            lignes.append("Aucun médicament spécifique trouvé dans ma base.")

        return "\n".join(lignes)

    def _logger(
        self,
        request: ChatRequest,
        symptomes: List[str],
        maladies: List[str],
        medicaments: List[str],
        reponse: str,
        est_urgent: bool = False,
    ):
        """Enregistre la conversation dans MongoDB."""
        try:
            self.chat_log.log_conversation(
                message=request.message,
                symptomes=symptomes,
                maladies=maladies,
                medicaments=medicaments,
                reponse=reponse,
                est_urgent=est_urgent,
                session_id=request.session_id,
            )
        except Exception as e:
            print(f"[WARN] Impossible de logger la conversation : {e}")

    def close(self):
        self.recommandation.close()
        self.chat_log.close()


# Singleton
_instance: Optional[ChatbotService] = None


def get_chatbot_service() -> ChatbotService:
    global _instance
    if _instance is None:
        _instance = ChatbotService()
    return _instance
