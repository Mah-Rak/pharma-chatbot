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
