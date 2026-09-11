"""
Point d'entrée de l'API Pharma Chatbot.
Lance avec : uvicorn src.main:app --reload
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api import produits, fournisseurs, stocks
app = FastAPI(
    title="Pharma Chatbot API",
    description="API de gestion de stock pharmaceutique + chatbot",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS — autorise les appels depuis un frontend (Streamlit, React…)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],       # à restreindre en production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Enregistrement des routes
app.include_router(produits.router, prefix="/api/v1")
app.include_router(fournisseurs.router, prefix="/api/v1")
app.include_router(stocks.router, prefix="/api/v1")


@app.get("/", tags=["Racine"])
def root():
    """Point d'entrée de l'API."""
    return {
        "message": "Pharma Chatbot API",
        "version": "0.1.0",
        "docs": "/docs",
    }


@app.get("/health", tags=["Santé"])
def health():
    """Vérifie que l'API est en ligne."""
    return {"status": "ok"}




