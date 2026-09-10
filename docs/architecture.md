# Architecture du projet Pharma Chatbot

## Vue d'ensemble

[Votre schéma ASCII ici]

## Composants

### Interface Web (Streamlit)
- Page accueil
- Espace client (chatbot)
- Espace pharmacien (stock, ordonnances)
- Espace admin

### API Backend (FastAPI)
- Gestion stock (CRUD produits, fournisseurs)
- Gestion ordonnances
- Chatbot (symptômes → médicaments)
- Alertes

### Bases de données
- PostgreSQL : stock, produits, fournisseurs, ordonnances
- MongoDB : logs de chat, conversations
- Neo4j : graphe symptômes ↔ maladies ↔ médicaments
- Redis : cache, alertes temps réel

### Modèle IA
- NLP pour détection de symptômes
- Recommandation de médicaments
