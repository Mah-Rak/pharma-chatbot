"""
Client HTTP pour communiquer avec l'API FastAPI.
"""
import os
from typing import Optional, List, Dict, Any

import requests


# URL de l'API (configurable via variable d'environnement)
API_URL = os.getenv("API_URL", "http://localhost:8000/api/v1")


class APIClient:
    """Client pour l'API Pharma Chatbot."""

    def __init__(self, base_url: str = API_URL):
        self.base_url = base_url
        self.timeout = 30

    # ============ CHATBOT ============

    def chat(self, message: str, session_id: Optional[str] = None) -> Dict[str, Any]:
        """Envoie un message au chatbot."""
        payload = {"message": message}
        if session_id:
            payload["session_id"] = session_id

        r = requests.post(
            f"{self.base_url}/chatbot/",
            json=payload,
            timeout=self.timeout,
        )
        r.raise_for_status()
        return r.json()

    def chatbot_stats(self) -> Dict[str, Any]:
        """Récupère les stats du chatbot."""
        r = requests.get(f"{self.base_url}/chatbot/stats", timeout=self.timeout)
        r.raise_for_status()
        return r.json()

    def chatbot_historique(self, session_id: str) -> List[Dict]:
        """Récupère l'historique d'une session."""
        r = requests.get(
            f"{self.base_url}/chatbot/historique/{session_id}",
            timeout=self.timeout,
        )
        r.raise_for_status()
        return r.json()

    # ============ PRODUITS ============

    def list_produits(self, skip: int = 0, limit: int = 100) -> List[Dict]:
        r = requests.get(
            f"{self.base_url}/produits/",
            params={"skip": skip, "limit": limit},
            timeout=self.timeout,
        )
        r.raise_for_status()
        return r.json()

    def create_produit(self, data: Dict) -> Dict:
        r = requests.post(f"{self.base_url}/produits/", json=data, timeout=self.timeout)
        r.raise_for_status()
        return r.json()

    def delete_produit(self, produit_id: int) -> None:
        r = requests.delete(
            f"{self.base_url}/produits/{produit_id}", timeout=self.timeout
        )
        r.raise_for_status()

    # ============ STOCK ============

    def list_stocks(self, limit: int = 100) -> List[Dict]:
        r = requests.get(
            f"{self.base_url}/stocks/", params={"limit": limit}, timeout=self.timeout
        )
        r.raise_for_status()
        return r.json()

    def create_stock(self, data: Dict) -> Dict:
        r = requests.post(f"{self.base_url}/stocks/", json=data, timeout=self.timeout)
        r.raise_for_status()
        return r.json()

    def update_stock(self, stock_id: int, data: Dict) -> Dict:
        r = requests.put(
            f"{self.base_url}/stocks/{stock_id}", json=data, timeout=self.timeout
        )
        r.raise_for_status()
        return r.json()

    # ============ ALERTES ============

    def list_alertes(self, resolue: Optional[bool] = None) -> List[Dict]:
        params = {}
        if resolue is not None:
            params["resolue"] = resolue
        r = requests.get(
            f"{self.base_url}/alertes/", params=params, timeout=self.timeout
        )
        r.raise_for_status()
        return r.json()

    # ============ SANTÉ ============

    def health(self) -> bool:
        """Vérifie que l'API est en ligne."""
        try:
            r = requests.get(
                self.base_url.replace("/api/v1", "") + "/health", timeout=5
            )
            return r.status_code == 200
        except requests.RequestException:
            return False


# Singleton
_client: Optional[APIClient] = None


def get_api_client() -> APIClient:
    global _client
    if _client is None:
        _client = APIClient()
    return _client
