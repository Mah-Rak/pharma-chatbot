"""Tests de l'endpoint HTTP /chatbot/."""


class TestChatbotAPI:
    def test_chat_simple(self, client):
        response = client.post(
            "/api/v1/chatbot/",
            json={"message": "J'ai mal à la tête et de la fièvre"},
        )
        assert response.status_code == 200
        data = response.json()
        assert "mal_de_tete" in data["symptomes_detectes"]
        assert "fievre" in data["symptomes_detectes"]
        assert data["est_urgent"] is False

    def test_chat_urgent(self, client):
        response = client.post(
            "/api/v1/chatbot/",
            json={"message": "J'ai mal à la poitrine"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["est_urgent"] is True

    def test_chat_message_vide(self, client):
        response = client.post(
            "/api/v1/chatbot/",
            json={"message": ""},
        )
        assert response.status_code == 422  # validation error

    def test_chat_sans_symptome(self, client):
        response = client.post(
            "/api/v1/chatbot/",
            json={"message": "Bonjour"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["symptomes_detectes"] == []

    def test_stats(self, client):
        # Envoyer quelques messages
        client.post("/api/v1/chatbot/", json={"message": "J'ai de la fièvre"})
        client.post("/api/v1/chatbot/", json={"message": "J'ai mal à la tête"})

        response = client.get("/api/v1/chatbot/stats")
        assert response.status_code == 200
        assert "total_conversations" in response.json()
        assert response.json()["total_conversations"] >= 2

    def test_historique(self, client):
        # Envoyer un message avec session_id
        client.post(
            "/api/v1/chatbot/",
            json={"message": "J'ai de la fièvre", "session_id": "test-hist"},
        )

        response = client.get("/api/v1/chatbot/historique/test-hist")
        assert response.status_code == 200
        assert len(response.json()) >= 1

    def test_historique_vide(self, client):
        response = client.get("/api/v1/chatbot/historique/session-inexistante")
        assert response.status_code == 200
        assert response.json() == []
