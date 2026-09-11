"""Tests des routes API (HTTP)."""
from decimal import Decimal


class TestHealth:
    def test_root(self, client):
        response = client.get("/")
        assert response.status_code == 200
        assert response.json()["message"] == "Pharma Chatbot API"

    def test_health(self, client):
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}


class TestProduitsAPI:
    def test_list_vide(self, client):
        response = client.get("/api/v1/produits/")
        assert response.status_code == 200
        assert response.json() == []

    def test_create(self, client):
        payload = {
            "nom": "Paracétamol 500mg",
            "description": "Antidouleur",
            "prix": "2.50",
            "categorie": "Antalgique",
            "ordonnance_requise": False,
        }
        response = client.post("/api/v1/produits/", json=payload)
        assert response.status_code == 201
        data = response.json()
        assert data["nom"] == "Paracétamol 500mg"
        assert data["prix"] == "2.50"
        assert "id" in data
        assert "created_at" in data

    def test_create_prix_invalide(self, client):
        payload = {"nom": "Test", "prix": "-5"}
        response = client.post("/api/v1/produits/", json=payload)
        assert response.status_code == 422  # validation error

    def test_get_by_id(self, client):
        # Créer d'abord
        created = client.post("/api/v1/produits/", json={
            "nom": "Ibuprofène", "prix": "3.20"
        }).json()

        # Puis lire
        response = client.get(f"/api/v1/produits/{created['id']}")
        assert response.status_code == 200
        assert response.json()["nom"] == "Ibuprofène"

    def test_get_by_id_inexistant(self, client):
        response = client.get("/api/v1/produits/99999")
        assert response.status_code == 404
        assert "non trouvé" in response.json()["detail"]

    def test_update(self, client):
        created = client.post("/api/v1/produits/", json={
            "nom": "Aspirine", "prix": "1.80"
        }).json()

        response = client.put(
            f"/api/v1/produits/{created['id']}",
            json={"prix": "2.10"},
        )
        assert response.status_code == 200
        assert response.json()["prix"] == "2.10"
        assert response.json()["nom"] == "Aspirine"  # inchangé

    def test_update_inexistant(self, client):
        response = client.put("/api/v1/produits/99999", json={"prix": "2.10"})
        assert response.status_code == 404

    def test_delete(self, client):
        created = client.post("/api/v1/produits/", json={
            "nom": "Test", "prix": "1.00"
        }).json()

        response = client.delete(f"/api/v1/produits/{created['id']}")
        assert response.status_code == 204

        # Vérifier qu'il n'existe plus
        response = client.get(f"/api/v1/produits/{created['id']}")
        assert response.status_code == 404

    def test_delete_inexistant(self, client):
        response = client.delete("/api/v1/produits/99999")
        assert response.status_code == 404

    def test_search(self, client):
        client.post("/api/v1/produits/", json={"nom": "Paracétamol", "prix": "2"})
        client.post("/api/v1/produits/", json={"nom": "Ibuprofène", "prix": "3"})

        response = client.get("/api/v1/produits/search/?q=para")
        assert response.status_code == 200
        resultats = response.json()
        assert len(resultats) == 1
        assert resultats[0]["nom"] == "Paracétamol"
