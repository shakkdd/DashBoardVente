import os

import requests

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")
TIMEOUT_SECONDS = 10


class ApiError(Exception):
    """L'API FastAPI n'a pas répondu correctement."""


def build_params(date_debut=None, date_fin=None, region_id=None, categorie=None):
    """Ne met dans l'URL que les filtres vraiment choisis (pas « Toutes »)."""
    params = {}
    if date_debut:
        params["date_debut"] = date_debut.isoformat()
    if date_fin:
        params["date_fin"] = date_fin.isoformat()
    if region_id:
        params["region"] = region_id
    if categorie:
        params["categorie"] = categorie
    return params


def get_json(path, params=None):
    url = f"{API_URL}{path}"
    try:
        response = requests.get(url, params=params, timeout=TIMEOUT_SECONDS)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as exc:
        raise ApiError(f"Impossible de joindre l'API ({url}) : {exc}") from exc


def get_regions():
    return get_json("/Region/")


def get_produits():
    return get_json("/Produit/")


def get_vendeurs():
    return get_json("/Vendeur/")


def get_ventes(params):
    return get_json("/Ventes/dates", params)


def get_ca_total(params):
    return get_json("/kpi/ca_total", params)


def get_ca_par_region(params):
    return get_json("/kpi/ca_par_region", params)


def get_evolution_mensuelle(params):
    return get_json("/kpi/evolution_mensuelle", params)


def get_top_vendeurs(params):
    return get_json("/kpi/top_vendeurs", params)
