"""
Connexion à PostgreSQL via SQLAlchemy.
Fournit :
- engine : moteur de connexion
- SessionLocal : fabrique de sessions
- Base : classe parente des modèles ORM
- get_db : dépendance FastAPI
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from src.config import get_settings

settings = get_settings()

# Moteur de connexion
engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,   # vérifie la connexion avant usage
    echo=False,           # mettre True pour voir les requêtes SQL
)

# Fabrique de sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Classe parente des modèles
Base = declarative_base()


def get_db():
    """
    Dépendance FastAPI : fournit une session DB
    et la ferme automatiquement après la requête.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
