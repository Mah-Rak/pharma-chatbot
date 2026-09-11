"""Tests des routes API Fournisseur."""


class TestFournisseurAPI:
    def test_create(self, client):
        payload = {"nom": "PharmaDistrib", "email": "contact@test.com"}
        response = client.post("/api/v1/fournisseurs/", json=payload)
        assert response.status_code == 201
        assert response.json()["nom"] == "PharmaDistrib"

    def test_create_email_invalide(self, client):
        payload = {"nom": "Test", "email": "pas-un-email"}
        response = client.post("/api/v1/fournisseurs/", json=payload)
        assert response.status_code == 422

    def test_list(self, client):
        client.post("/api/v1/fournisseurs/", json={"nom": "A"})
        client.post("/api/v1/fournisseurs/", json={"nom": "B"})
        response = client.get("/api/v1/fournisseurs/")
        assert response.status_code == 200
        assert len(response.json()) == 2

    def test_get_by_id(self, client):
        created = client.post("/api/v1/fournisseurs/", json={"nom": "Test"}).json()
        response = client.get(f"/api/v1/fournisseurs/{created['id']}")
        assert response.status_code == 200
        assert response.json()["nom"] == "Test"

    def test_get_inexistant(self, client):
        response = client.get("/api/v1/fournisseurs/99999")
        assert response.status_code == 404

    def test_update(self, client):
        created = client.post("/api/v1/fournisseurs/", json={"nom": "Test"}).json()
        response = client.put(f"/api/v1/fournisseurs/{created['id']}", json={"nom": "Test2"})
        assert response.status_code == 200
        assert response.json()["nom"] == "Test2"

    def test_delete(self, client):
        created = client.post("/api/v1/fournisseurs/", json={"nom": "Test"}).json()
        response = client.delete(f"/api/v1/fournisseurs/{created['id']}")
        assert response.status_code == 204

    def test_search(self, client):
        client.post("/api/v1/fournisseurs/", json={"nom": "PharmaDistrib"})
        client.post("/api/v1/fournisseurs/", json={"nom": "MediPlus"})
        response = client.get("/api/v1/fournisseurs/search/?q=pharma")
        assert response.status_code == 200
        assert len(response.json()) == 1
