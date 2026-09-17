# 3. Relier FastAPI à Postgres

FastAPI tourne **sur ton ordinateur**. Postgres tourne **dans Docker**, exposé sur `localhost` et le port défini dans `.env` (5432 par défaut).

On suppose que le conteneur est déjà lancé (voir [l’étape 2](02-lancer-postgres.md)).

## Installer les paquets Python

Dans ton environnement virtuel :

```bash
pip install fastapi uvicorn sqlalchemy psycopg[binary] python-dotenv
```

- `fastapi` / `uvicorn` : l’API
- `sqlalchemy` : pour parler à la base
- `psycopg[binary]` : le driver Postgres
- `python-dotenv` : pour lire le fichier `.env`

## Lire l’URL de connexion

Le fichier `.env` contient déjà :

```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/dashboardvente
```

Format : `postgresql://UTILISATEUR:MOT_DE_PASSE@HOTE:PORT/NOM_DE_LA_BASE`

Comme FastAPI n’est pas dans Docker, l’hôte est `localhost` (pas `db`).

## Exemple minimal

Fichier `main.py` à la racine du projet :

```python
import os

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, text

load_dotenv()

database_url = os.getenv("DATABASE_URL")
if not database_url:
    raise RuntimeError("DATABASE_URL est manquant dans le fichier .env")

engine = create_engine(database_url)
app = FastAPI()


@app.get("/health/db")
def db_health():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
    except Exception:
        raise HTTPException(status_code=503, detail="Base de données injoignable")
    return {"db": "ok"}
```

Lance l’API :

```bash
uvicorn main:app --reload
```

Ouvre [http://127.0.0.1:8000/health/db](http://127.0.0.1:8000/health/db). Tu dois voir `{"db":"ok"}`.

Si tu as une erreur de connexion :

1. Docker Desktop est ouvert
2. `docker compose ps` montre le conteneur `running`
3. `DATABASE_URL` dans `.env` a le même utilisateur, mot de passe, port et nom de base que le reste du fichier

## Suite possible

Une fois la connexion OK, tu pourras créer des tables avec SQLAlchemy (modèles + `Base.metadata.create_all`) ou un outil de migration comme Alembic. Ce n’est pas nécessaire pour vérifier que FastAPI parle à Postgres.
