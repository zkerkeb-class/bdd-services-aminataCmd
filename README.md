# AI Planning Service

Ce projet est un service web basé sur FastAPI pour la gestion de tournois et la planification assistée par IA.

## Structure du projet

```
ai-planning-service/
│
├── app/                # Code source principal
│   ├── main.py         # Point d'entrée FastAPI
│   ├── api/            # Dépendances et routes
│   ├── core/           # Config, sécurité, exceptions
│   ├── models/         # Modèles Pydantic
│   ├── services/       # Logique métier et IA
│   └── schemas/        # Schémas de validation
│
├── tests/              # Tests unitaires et fixtures
├── requirements.txt    # Dépendances principales
├── Dockerfile          # Image Docker
├── API.md              # Documentation des routes
├── docker-compose.yml  # Orchestration locale
└── README.md           # Ce fichier
```

## Installation rapide

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Lancement du serveur

```bash
uvicorn app.main:app --reload
```