# 🚀 [Pharma-chatbot]

> [Courte description en une ligne — ex: "API REST de gestion de tâches collaboratives"]

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-green?logo=fastapi)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue?logo=postgresql)
![Docker](https://img.shields.io/badge/Docker-ready-blue?logo=docker)
![Tests](https://img.shields.io/badge/tests-passing-brightgreen)
![License](https://img.shields.io/badge/license-MIT-yellow)

---

## 📋 Description

**[Nom du Projet]** est une API REST développée avec **FastAPI** permettant de
[**décrire en 2-3 phrases ce que fait le projet et pour qui**].

Elle fournit une base solide et scalable avec authentification JWT, CRUD complet,
documentation Swagger automatique et déploiement conteneurisé.

### ✨ Fonctionnalités principales

- 🔐 Authentification JWT (register / login / refresh)
- 👥 Gestion des utilisateurs (CRUD + rôles)
- 📦 [Ressource principale] : CRUD complet
- 🔍 Pagination, filtres et recherche
- 🐳 Conteneurisation Docker / Docker Compose
- ✅ Tests unitaires et d'intégration (Pytest, +XX% coverage)
- 📚 Documentation Swagger / ReDoc automatique
- 🚦 Health check endpoint

### 🛠️ Stack technique

| Composant | Technologie |
|-----------|-------------|
| Langage | Python 3.11 |
| Framework API | FastAPI |
| Base de données | PostgreSQL 15 |
| ORM | SQLAlchemy 2.0 |
| Migrations | Alembic |
| Validation | Pydantic v2 |
| Auth | JWT (python-jose) + bcrypt |
| Tests | Pytest + httpx |
| Conteneurisation | Docker & Docker Compose |
| Gateway | Nginx |

---

## 🏗️ Architecture

### Schéma global

```
┌─────────────────────────────────────────────────────────────┐
│                 CLIENT (Browser / Mobile)                    │
└──────────────────────────┬──────────────────────────────────┘
                           │ HTTP / HTTPS
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                    API GATEWAY (Nginx)                       │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                    FASTAPI APPLICATION                       │
│                                                              │
│   ┌──────────────┐    ┌──────────────┐    ┌──────────────┐  │
│   │   Routers    │    │   Services   │    │   Schemas    │  │
│   │  (endpoints) │───▶│  (business)  │───▶│  (pydantic)  │  │
│   └──────────────┘    └──────────────┘    └──────────────┘  │
│          │                    │                              │
│          ▼                    ▼                              │
│   ┌──────────────┐    ┌──────────────┐                      │
│   │    Models    │    │     Auth     │                      │
│   │ (SQLAlchemy) │    │    (JWT)     │                      │
│   └──────────────┘    └──────────────┘                      │
│                                                              │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                    PostgreSQL DATABASE                       │
└─────────────────────────────────────────────────────────────┘
```

### Structure du projet

```
[projet]/
├── app/
│   ├── __init__.py
│   ├── main.py              # Point d'entrée FastAPI
│   ├── config.py            # Configuration (env vars)
│   ├── database.py          # Connexion DB + session
│   ├── models/              # Modèles SQLAlchemy
│   ├── schemas/             # Schémas Pydantic
│   ├── routers/             # Routes API (endpoints)
│   ├── services/            # Logique métier
│   └── core/                # Auth, sécurité, deps
├── tests/
│   ├── conftest.py
│   ├── unit/
│   └── integration/
├── alembic/                 # Migrations
│   └── versions/
├── docker/
│   ├── Dockerfile
│   └── nginx.conf
├── docker-compose.yml
├── .env.example
├── requirements.txt
├── pyproject.toml
└── README.md
```

---

## ⚙️ Installation

### Prérequis

- **Python 3.11+**
- **Docker** & **Docker Compose**
- **Git**

### 🐳 Option 1 : Avec Docker (recommandé)

```bash
# 1. Cloner le repo
git clone https://github.com/[ton-user]/[ton-projet].git
cd [ton-projet]

# 2. Copier les variables d'environnement
cp .env.example .env

# 3. Lancer les conteneurs (API + DB + Nginx)
docker compose up --build -d

# 4. Appliquer les migrations
docker compose exec api alembic upgrade head

# 5. Vérifier que l'API répond
curl http://localhost:8000/health
```

L'API est accessible sur :
- **API** : http://localhost:8000
- **Swagger UI** : http://localhost:8000/docs
- **ReDoc** : http://localhost:8000/redoc

### 🐍 Option 2 : Avec venv (développement local)

```bash
# 1. Créer et activer l'environnement virtuel
python -m venv venv

source venv/bin/activate      # Linux / macOS
# ou
venv\Scripts\activate         # Windows

# 2. Installer les dépendances
pip install -r requirements.txt

# 3. Configurer l'environnement
cp .env.example .env
# Éditer .env avec vos valeurs (DATABASE_URL, SECRET_KEY...)

# 4. Lancer PostgreSQL via Docker
docker run -d --name postgres \
  -e POSTGRES_USER=user \
  -e POSTGRES_PASSWORD=password \
  -e POSTGRES_DB=appdb \
  -p 5432:5432 postgres:15

# 5. Appliquer les migrations
alembic upgrade head

# 6. Lancer l'API en mode dev
uvicorn app.main:app --reload
```

---

## 🧪 Tests

```bash
# Lancer tous les tests
pytest

# Avec rapport de couverture
pytest --cov=app --cov-report=html --cov-report=term

# Tests unitaires uniquement
pytest tests/unit/ -v

# Tests d'intégration uniquement
pytest tests/integration/ -v

# Un fichier / une fonction spécifique
pytest tests/unit/test_users.py::test_create_user -v
```

Le rapport HTML de couverture est généré dans `htmlcov/index.html`.

---

## 📸 Captures d'écran

### Swagger UI — Vue d'ensemble

![Swagger Overview](docs/images/swagger-overview.png)

### Swagger UI — Détail d'un endpoint

![Swagger Endpoint](docs/images/swagger-endpoint.png)

### Exemple de requête / réponse

```bash
# Login
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "secret"}'
```

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

---

## 🔑 Variables d'environnement

| Variable | Description | Exemple / Défaut |
|----------|-------------|------------------|
| `DATABASE_URL` | URL de connexion PostgreSQL | `postgresql://user:pass@db:5432/appdb` |
| `SECRET_KEY` | Clé secrète pour signer les JWT | *obligatoire* |
| `ALGORITHM` | Algorithme JWT | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Durée de vie du token | `30` |
| `ENV` | Environnement d'exécution | `development` |
| `CORS_ORIGINS` | Origines autorisées | `*` |

---

## 🚦 Endpoints principaux

| Méthode | Endpoint | Description | Auth |
|---------|----------|-------------|:----:|
| `GET` | `/health` | Health check | ❌ |
| `POST` | `/api/v1/auth/register` | Inscription | ❌ |
| `POST` | `/api/v1/auth/login` | Connexion | ❌ |
| `GET` | `/api/v1/users/me` | Profil de l'utilisateur courant | ✅ |
| `GET` | `/api/v1/users` | Liste des utilisateurs | ✅ |
| `POST` | `/api/v1/[ressource]` | Créer une ressource | ✅ |
| `GET` | `/ap					i/v1/[ressource]` | Lister les ressources | ✅ |
| `GET` | `/api/v1/[ressource]/{id}` | Détail d'une ressource | ✅ |
| `PUT` | `/api/v1/[ressource]/{id}` | Mettre à jour | ✅ |
| `DELETE` | `/api/v1/[ressource]/{id}` | Supprimer | ✅ |

> 📚 Documentation interactive complète : [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🤝 Contribution

Les contributions sont les bienvenues !

1. Fork le projet
2. Créer une branche : `git checkout -b feature/ma-feature`
3. Commit : `git commit -m 'feat: ajout de ma feature'`
4. Push : `git push origin feature/ma-feature`
5. Ouvrir une **Pull Request**

Merci de respecter les conventions [Conventional Commits](https://www.conventionalcommits.org/).

---

## 📝 Licence

Ce projet est sous licence **MIT**. Voir le fichier [LICENSE](LICENSE) pour plus d'informations.

---

## 👤 Auteur

**[Mah-Rak]**
- 🐙 GitHub : https://github.com/Mah-Rak
- 💼 LinkedIn : https://www.linkedin.com/in/andriamahery-rakotoarivony-3913813a6
- 📧 Email : andriamaheryrakotoarivony@gmail.com

---

