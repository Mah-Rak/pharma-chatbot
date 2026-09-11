"""Tests des routes API Alerte."""


def _create_produit(client, nom="Test"):
    return client.post("/api/v1/produits/", json={"nom": nom, "prix": "2.50"}).json()


class TestAlerteAPI:
    def test_list_vide(self, client):
        response = client.get("/api/v1/alertes/")
        assert response.status_code == 200
        assert response.json() == []

    def test_creation_stock_bas_genere_alerte(self, client):
        produit = _create_produit(client)
        client.post("/api/v1/stocks/", json={
            "produit_id": produit["id"], "quantite": 3, "seuil_alerte": 10
        })
        response = client.get("/api/v1/alertes/non-resolues/")
        assert response.status_code == 200
        assert len(response.json()) == 1
        assert response.json()[0]["type"] == "epuisement"

    def test_resolution_automatique(self, client):
        produit = _create_produit(client)
        stock = client.post("/api/v1/stocks/", json={
            "produit_id": produit["id"], "quantite": 3, "seuil_alerte": 10
        }).json()

        # Vérifier l'alerte
        assert len(client.get("/api/v1/alertes/non-resolues/").json()) == 1

        # Remonter le stock
        client.put(f"/api/v1/stocks/{stock['id']}", json={"quantite": 50})

        # L'alerte doit être résolue
        assert len(client.get("/api/v1/alertes/non-resolues/").json()) == 0

    def test_get_by_id(self, client):
        produit = _create_produit(client)
        client.post("/api/v1/stocks/", json={
            "produit_id": produit["id"], "quantite": 3, "seuil_alerte": 10
        })
        alerte_id = client.get("/api/v1/alertes/non-resolues/").json()[0]["id"]
        response = client.get(f"/api/v1/alertes/{alerte_id}")
        assert response.status_code == 200

    def test_get_inexistant(self, client):
        response = client.get("/api/v1/alertes/99999")
        assert response.status_code == 404

    def test_resoudre_manuellement(self, client):
        produit = _create_produit(client)
        client.post("/api/v1/stocks/", json={
            "produit_id": produit["id"], "quantite": 3, "seuil_alerte": 10
        })
        alerte_id = client.get("/api/v1/alertes/non-resolues/").json()[0]["id"]

        response = client.put(f"/api/v1/alertes/{alerte_id}", json={"resolue": True})
        assert response.status_code == 200
        assert response.json()["resolue"] is True

    def test_alertes_par_produit(self, client):
        produit = _create_produit(client)
        client.post("/api/v1/stocks/", json={
            "produit_id": produit["id"], "quantite": 3, "seuil_alerte": 10
        })
        response = client.get(f"/api/v1/alertes/produit/{produit['id']}")
        assert response.status_code == 200
        assert len(response.json()) == 1

    def test_delete(self, client):
        produit = _create_produit(client)
        client.post("/api/v1/stocks/", json={
            "produit_id": produit["id"], "quantite": 3, "seuil_alerte": 10
        })
        alerte_id = client.get("/api/v1/alertes/non-resolues/").json()[0]["id"]

        response = client.delete(f"/api/v1/alertes/{alerte_id}")
        assert response.status_code == 204
