# DashBoardVente

Pour installer Docker, lancer Postgres, relier FastAPI et afficher le dashboard, suis le guide dans [`docs/`](docs/README.md).

## Lancer le projet

Dans un terminal, l’API :

```bash
uv run uvicorn back.main:app --reload
```

Dans un autre terminal, le front Streamlit :

```bash
cd front
uv run streamlit run app.py
```

Le dashboard s’ouvre sur [http://localhost:8501](http://localhost:8501). Détail de la partie Streamlit : [`docs/04-dashboard-streamlit.md`](docs/04-dashboard-streamlit.md).
