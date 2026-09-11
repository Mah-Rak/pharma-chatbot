"""
Modèles ORM SQLAlchemy.
Représentent les tables PostgreSQL en classes Python.
"""
from sqlalchemy import (
    Column,
    Integer,
    String,
    Numeric,
    Boolean,
    Date,
    DateTime,
    ForeignKey,
    Text,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from src.db.database import Base


class Produit(Base):
    __tablename__ = "produits"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String(255), nullable=False, index=True)
    description = Column(Text)
    prix = Column(Numeric(10, 2), nullable=False)
    categorie = Column(String(100))
    ordonnance_requise = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())

    # Relations
    stocks = relationship("Stock", back_populates="produit")
    alertes = relationship("Alerte", back_populates="produit")

    def __repr__(self):
        return f"<Produit(id={self.id}, nom='{self.nom}')>"


class Fournisseur(Base):
    __tablename__ = "fournisseurs"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String(255), nullable=False)
    contact = Column(String(255))
    email = Column(String(255))
    telephone = Column(String(50))
    adresse = Column(Text)

    stocks = relationship("Stock", back_populates="fournisseur")

    def __repr__(self):
        return f"<Fournisseur(id={self.id}, nom='{self.nom}')>"


class Stock(Base):
    __tablename__ = "stock"

    id = Column(Integer, primary_key=True, index=True)
    produit_id = Column(Integer, ForeignKey("produits.id"), nullable=False)
    fournisseur_id = Column(Integer, ForeignKey("fournisseurs.id"))
    quantite = Column(Integer, nullable=False, default=0)
    seuil_alerte = Column(Integer, default=10)
    date_peremption = Column(Date)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    produit = relationship("Produit", back_populates="stocks")
    fournisseur = relationship("Fournisseur", back_populates="stocks")

    def __repr__(self):
        return f"<Stock(id={self.id}, produit_id={self.produit_id}, quantite={self.quantite})>"


class Alerte(Base):
    __tablename__ = "alertes"

    id = Column(Integer, primary_key=True, index=True)
    produit_id = Column(Integer, ForeignKey("produits.id"), nullable=False)
    type = Column(String(50))  # 'epuisement', 'peremption'
    message = Column(Text)
    resolue = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())

    produit = relationship("Produit", back_populates="alertes")

    def __repr__(self):
        return f"<Alerte(id={self.id}, type='{self.type}', resolue={self.resolue})>"
