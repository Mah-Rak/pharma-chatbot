"""
Configuration partagée pour pytest.
Fournit les fixtures : client HTTP, session DB de test, données de test.
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.config import get_settings
from src.db.database import Base, get_db
from src.main import app

settings = get_settings()

# Base de test séparée (pour ne pas toucher aux données de dev)
TEST_DATABASE_URL = settings.database_url.replace("/pharma_db", "/pharma_test_db")

engine_test = create_engine(TEST_DATABASE_URL, pool_pre_ping=True)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine_test)


@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    """Crée les tables de test une fois pour toute la session."""
    Base.metadata.create_all(bind=engine_test)
    yield
    Base.metadata.drop_all(bind=engine_test)


@pytest.fixture
def db_session():
    """Fournit une session DB de test avec rollback automatique."""
    connection = engine_test.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def client(db_session):
    """Client HTTP de test avec la DB de test injectée."""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()

# ============================================================
# Fixtures MongoDB (tests d'intégration)
# ============================================================

@pytest.fixture
def chat_log_service_test():
    """
    Service de logs MongoDB utilisant une base de test séparée.
    Nettoie la base avant et après chaque test.
    """
    from src.services.chat_service import ChatLogService

    service = ChatLogService(db_name="pharma_chat_test")
    # Nettoyer avant
    service.collection.delete_many({})
    yield service
    # Nettoyer après
    service.collection.delete_many({})
    service.close()


@pytest.fixture
def chatbot_test(monkeypatch, chat_log_service_test):
    """
    ChatbotService avec MongoDB de test.
    Reset le singleton pour garantir l'isolation.
    """
    import src.nlp.chatbot as chatbot_module

    # Reset le singleton
    chatbot_module._instance = None

    # Monkeypatch get_chat_log_service
    monkeypatch.setattr(
        chatbot_module,
        "get_chat_log_service",
        lambda: chat_log_service_test,
    )

    yield chatbot_module.get_chatbot_service()

    # Reset après
    chatbot_module._instance = None
