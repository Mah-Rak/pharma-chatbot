"""
Configuration centrale du projet.
Lit les variables d'environnement depuis .env
"""
from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # ===== PostgreSQL =====
    postgres_user: str = "pharma"
    postgres_password: str = "pharma_dev"
    postgres_db: str = "pharma_db"
    postgres_host: str = "localhost"
    postgres_port: int = 5433

    # ===== MongoDB =====
    mongo_user: str = "pharma"
    mongo_password: str = "pharma_dev"
    mongo_host: str = "localhost"
    mongo_port: int = 27017
    mongo_db: str = "pharma_chat"

    # ===== Neo4j =====
    neo4j_uri: str = "bolt://localhost:7687"
    neo4j_user: str = "neo4j"
    neo4j_password: str = "pharma_dev"

    # ===== Redis =====
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_db: int = 0

    # ===== API =====
    api_host: str = "0.0.0.0"
    api_port: int = 8000

    @property
    def database_url(self) -> str:
        return (
            f"postgresql://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

    class Config:
        env_file = ".env"
        extra = "ignore"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
