"""Tests du pipeline chatbot (NLP + Neo4j + MongoDB)."""
from src.schemas.chatbot import ChatRequest


class TestChatbotPipeline:
    def test_symptomes_grippaux(self, chatbot_test, db_session):
        request = ChatRequest(message="J'ai mal à la tête et de la fièvre")
        response = chatbot_test.traiter(request, db_session)

        assert "mal_de_tete" in response.symptomes_detectes
        assert "fievre" in response.symptomes_detectes
        assert len(response.maladies_probables) > 0
        assert len(response.medicaments_recommandes) > 0
        assert response.est_urgent is False

    def test_cas_urgent(self, chatbot_test, db_session):
        request = ChatRequest(message="J'ai mal à la poitrine")
        response = chatbot_test.traiter(request, db_session)

        assert response.est_urgent is True
        assert "URGENCE" in response.reponse
        assert len(response.medicaments_recommandes) == 0

    def test_aucun_symptome(self, chatbot_test, db_session):
        request = ChatRequest(message="Bonjour, comment allez-vous ?")
        response = chatbot_test.traiter(request, db_session)

        assert response.symptomes_detectes == []
        assert "Pouvez-vous décrire" in response.reponse

    def test_avertissement_ordonnance(self, chatbot_test, db_session):
        # L'infection urinaire nécessite une ordonnance
        request = ChatRequest(message="J'ai mal au ventre et de la fièvre")
        response = chatbot_test.traiter(request, db_session)

        if any(m.ordonnance_requise for m in response.medicaments_recommandes):
            assert "ordonnance" in response.avertissement.lower()

    def test_log_mongodb(self, chatbot_test, db_session, chat_log_service_test):
        """Vérifie que la conversation est bien loggée."""
        request = ChatRequest(
            message="J'ai de la fièvre",
            session_id="test-session-1",
        )
        chatbot_test.traiter(request, db_session)

        # Vérifier dans MongoDB
        conversations = chat_log_service_test.get_conversations("test-session-1")
        assert len(conversations) == 1
        assert conversations[0]["message"] == "J'ai de la fièvre"
        assert "fievre" in conversations[0]["symptomes"]

    def test_log_cas_urgent(self, chatbot_test, db_session, chat_log_service_test):
        request = ChatRequest(
            message="J'ai mal à la poitrine",
            session_id="test-urgent",
        )
        chatbot_test.traiter(request, db_session)

        conversations = chat_log_service_test.get_conversations("test-urgent")
        assert len(conversations) == 1
        assert conversations[0]["est_urgent"] is True

