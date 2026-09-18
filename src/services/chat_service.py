"""
Service de logs des conversations dans MongoDB.
"""
from datetime import datetime, timezone
from typing import Optional, List

from pymongo import MongoClient
from pymongo.collection import Collection

from src.config import get_settings


class ChatLogService:
    """Gère les logs de conversations dans MongoDB."""

    def __init__(self, db_name: Optional[str] = None):
        settings = get_settings()
        self.client = MongoClient(
            host=settings.mongo_host,
            port=settings.mongo_port,
            username=settings.mongo_user,
            password=settings.mongo_password,
            authSource="admin",
        )
        # Utilise db_name si fourni (tests), sinon la base de dev
        self.db = self.client[db_name or settings.mongo_db]
        self.collection: Collection = self.db["conversations"]

    def log_conversation(
        self,
        message: str,
        symptomes: List[str],
        maladies: List[str],
        medicaments: List[str],
        reponse: str,
        est_urgent: bool = False,
        session_id: Optional[str] = None,
    ) -> str:
        """Enregistre une conversation."""
        doc = {
            "session_id": session_id,
            "message": message,
            "symptomes": symptomes,
            "maladies": maladies,
            "medicaments": medicaments,
            "reponse": reponse,
            "est_urgent": est_urgent,
	    "timestamp": datetime.now(timezone.utc),
        }
        result = self.collection.insert_one(doc)
        return str(result.inserted_id)

    def get_conversations(self, session_id: str, limit: int = 50) -> List[dict]:
        """Récupère l'historique d'une session."""
        cursor = (
            self.collection.find({"session_id": session_id})
            .sort("timestamp", -1)
            .limit(limit)
        )
        conversations = []
        for doc in cursor:
            doc["_id"] = str(doc["_id"])
            conversations.append(doc)
        return conversations

    def count(self) -> int:
        """Nombre total de conversations."""
        return self.collection.count_documents({})

    def close(self):
        self.client.close()


# Singleton
_instance: Optional[ChatLogService] = None


def get_chat_log_service() -> ChatLogService:
    global _instance
    if _instance is None:
        _instance = ChatLogService()
    return _instance
