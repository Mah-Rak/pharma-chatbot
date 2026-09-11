"""Tests des routes API Stock."""


def _create_produit(client, nom="Test Produit"):
    return client.post("/api/v1/produits/", json={"nom": nom, "prix": "2.50"}).json()


def _create_fournisseur(client, nom="Test Fournisseur"):
    return client.post("/api/v1/fournisseurs/", json={"nom": nom}).json()


class TestStockAPI:
    def test_create(self, client):
        produit = _create_produit(client)
        payload = {"produit_id": produit["id"], "quantite": 50, "seuil_alerte": 10}
        response = client.post("/api/v1/stocks/", json=payload)
        assert response.status_code == 201
        data = response.json()
        assert data["quantite"] == 50
        assert data["produit"]["nom"] == "Test Produit"

    def test_create_avec_fournisseur(self, client):
        produit = _create_produit(client)
        fournisseur = _create_fournisseur(client)
        payload = {
            "produit_id": produit["id"],
            "fournisseur_id": fournisseur["id"],
            "quantite": 30,
        }
        response = client.post("/api/v1/stocks/", json=payload)
        assert response.status_code == 201
        assert response.json()["fournisseur"]["nom"] == "Test Fournisseur"

    def test_create_produit_inexistant(self, client):
        response = client.post("/api/v1/stocks/", json={"produit_id": 99999, "quantite": 10})
        assert response.status_code == 400
        assert "introuvable" in response.json()["detail"]

    def test_list(self, client):
        produit = _create_produit(client)
        client.post("/api/v1/stocks/", json={"produit_id": produit["id"], "quantite": 10})
        client.post("/api/v1/stocks/", json={"produit_id": produit["id"], "quantite": 20})
        response = client.get("/api/v1/stocks/")
        assert response.status_code == 200
        assert len(response.json()) == 2

    def test_get_by_id(self, client):
        produit = _create_produit(client)
        created = client.post("/api/v1/stocks/", json={
            "produit_id": produit["id"], "quantite": 50
        }).json()
        response = client.get(f"/api/v1/stocks/{created['id']}")
        assert response.status_code == 200
        assert response.json()["quantite"] == 50

    def test_get_inexistant(self, client):
        response = client.get("/api/v1/stocks/99999")
        assert response.status_code == 404

    def test_update(self, client):
        produit = _create_produit(client)
        created = client.post("/api/v1/stocks/", json={
            "produit_id": produit["id"], "quantite": 50
        }).json()
        response = client.put(f"/api/v1/stocks/{created['id']}", json={"quantite": 30})
        assert response.status_code == 200
        assert response.json()["quantite"] == 30

    def test_delete(self, client):
        produit = _create_produit(client)
        created = client.post("/api/v1/stocks/", json={
            "produit_id": produit["id"], "quantite": 50
        }).json()
        response = client.delete(f"/api/v1/stocks/{created['id']}")
        assert response.status_code == 204

    def test_alertes(self, client):
        produit = _create_produit(client)
        client.post("/api/v1/stocks/", json={
            "produit_id": produit["id"], "quantite": 5, "seuil_alerte": 10
        })
        client.post("/api/v1/stocks/", json={
            "produit_id": produit["id"], "quantite": 100, "seuil_alerte": 10
        })
        response = client.get("/api/v1/stocks/alertes/")
        assert response.status_code == 200
        assert len(response.json()) == 1

    def test_by_produit(self, client):
        produit = _create_produit(client)
        client.post("/api/v1/stocks/", json={"produit_id": produit["id"], "quantite": 10})
        response = client.get(f"/api/v1/stocks/produit/{produit['id']}")
        assert response.status_code == 200
        assert len(response.json()) == 1
