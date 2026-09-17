# 4. Dashboard Streamlit

Le front est une page web qui **affiche** les chiffres de l’API. Il ne se connecte **jamais** à Postgres : il envoie des requêtes HTTP à FastAPI, puis dessine des indicateurs, des graphes et un tableau.

On suppose que Postgres et l’API tournent déjà (étapes [2](02-lancer-postgres.md) et [3](03-connecter-fastapi.md)).

## 1. À quoi ça sert

| Élément | Rôle |
| --- | --- |
| API FastAPI | Calcule les KPI (CA, régions, évolution, top vendeurs) |
| Front Streamlit | Demande ces KPI et les affiche |

Si tu changes un filtre (dates, région, catégorie), Streamlit relance la page, rappelle l’API, et tout se met à jour.

## 2. Paquets installés

Trois librairies ont été ajoutées au projet (`uv add streamlit pandas requests`) :

- **streamlit** : crée la page (sidebar, titres, graphes)
- **pandas** : met les réponses JSON dans un tableau, que Streamlit sait tracer
- **requests** : appelle l’API (`GET /kpi/...`)

## 3. Fichiers créés

Tout est dans le dossier `front/` :

| Fichier | Rôle |
| --- | --- |
| `api.py` | Parle à FastAPI : construit l’URL et récupère le JSON |
| `app.py` | Construit la page : filtres, KPI, graphes, tableau |
| `.streamlit/config.toml` | Thème sombre (comme la capture du TP) |

## 4. Comment le front appelle l’API

Dans `api.py` :

1. L’adresse de l’API est `http://127.0.0.1:8000` (ou la variable d’environnement `API_URL` si tu la définis).
2. `build_params()` ajoute à l’URL seulement les filtres choisis. « Toutes » = on n’envoie pas le paramètre.
3. `get_json("/kpi/ca_total", params)` fait un `GET` et renvoie le JSON.

Exemple d’URL générée :

```text
http://127.0.0.1:8000/kpi/ca_total?date_debut=2025-09-17&region=1&categorie=Informatique
```

Routes utilisées :

- `GET /Region/` et `GET /Produit/` : remplir les listes de la sidebar
- `GET /Vendeur/` : retrouver la région de chaque vendeur
- `GET /Ventes/dates` : compter le nombre de ventes (donc le panier moyen = CA / nb)
- `GET /kpi/ca_total`, `/kpi/ca_par_region`, `/kpi/evolution_mensuelle`, `/kpi/top_vendeurs` : les graphiques et le classement

## 5. Comment la page est construite

Dans `app.py`, de haut en bas :

1. **Sidebar « Filtres »** : plage de dates, région, catégorie.
2. **3 indicateurs** (`st.metric`) : CA total, nombre de ventes, panier moyen.
3. **2 graphes** (fonctions natives Streamlit, pas matplotlib) :
   - `st.bar_chart` : CA par région
   - `st.line_chart` : évolution mensuelle du CA
4. **Tableau** des top vendeurs. L’API ne renvoie que le nom et le CA : la région et le nombre de ventes sont ajoutés côté front, en croisant `/Vendeur/`, `/Region/` et `/Ventes/dates`.

Si l’API est éteinte, un message d’erreur s’affiche au lieu d’une page vide.

## 6. Lancer Streamlit

Dans un **premier** terminal, l’API :

```bash
uv run uvicorn back.main:app --reload
```

Dans un **deuxième** terminal, place-toi dans `front/` (pour que le thème sombre soit lu) :

```bash
cd front
uv run streamlit run app.py
```

Ouvre l’URL affichée (en général [http://localhost:8501](http://localhost:8501)).

Vérifie que ça marche :

1. Les 3 KPI en haut ne sont pas à 0
2. Le graphique barres et la courbe s’affichent
3. Changer la **région** ou la **catégorie** met à jour les chiffres

## 7. Filtre catégorie

Le paramètre `categorie` envoyé à l’API est le **nom** de la catégorie (`Informatique`, `Audio`, …), pas l’id d’un produit.

Côté API, ça filtre la table `produits` sur la colonne `categorie`.
