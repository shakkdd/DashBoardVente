from collections import Counter
from datetime import date, timedelta

import altair as alt
import pandas as pd
import streamlit as st

from api import (
    ApiError,
    build_params,
    get_ca_par_region,
    get_ca_total,
    get_evolution_mensuelle,
    get_produits,
    get_regions,
    get_top_vendeurs,
    get_vendeurs,
    get_ventes,
)

TOUTES = "Toutes"
MOIS_ABBR = [
    "janv.", "févr.", "mars", "avr.", "mai", "juin",
    "juil.", "août", "sept.", "oct.", "nov.", "déc.",
]


def format_euros(montant):
    texte = f"{montant:,.2f}".replace(",", " ").replace(".", ",")
    return f"{texte} €"


def libelle_mois(annee, mois):
    return f"{MOIS_ABBR[mois - 1]} {annee}"


st.set_page_config(
    page_title="Dashboard KPI Ventes - NordCommerce",
    layout="wide",
)

st.sidebar.header("Filtres")

aujourd_hui = date.today()
periode = st.sidebar.date_input(
    "Période",
    value=(aujourd_hui - timedelta(days=365), aujourd_hui),
)

date_debut = date_fin = None
if isinstance(periode, (list, tuple)) and len(periode) == 2:
    date_debut, date_fin = periode

try:
    regions = get_regions()
    produits = get_produits()
    vendeurs = get_vendeurs()
except ApiError as exc:
    st.error(str(exc))
    st.info("Lance d'abord l'API : `uv run uvicorn back.main:app --reload`")
    st.stop()

noms_regions = [TOUTES] + [region["nom"] for region in regions]
region_choisie = st.sidebar.selectbox("Région", noms_regions)

categories = sorted({produit["categorie"] for produit in produits})
categorie_choisie = st.sidebar.selectbox("Catégorie", [TOUTES] + categories)

region_id = None
if region_choisie != TOUTES:
    region_id = next(region["id"] for region in regions if region["nom"] == region_choisie)

categorie = None if categorie_choisie == TOUTES else categorie_choisie
params = build_params(date_debut, date_fin, region_id, categorie)

try:
    ca_total = get_ca_total(params)["ca_total"]
    ca_par_region = get_ca_par_region(params)
    evolution = get_evolution_mensuelle(params)
    ventes = get_ventes(params)
    # /kpi/top_vendeurs joint déjà `vendeurs` : le query param `region`
    # déclenche une 2e jointure et un 500. Dans ce cas on classe depuis les ventes.
    if region_id:
        top_vendeurs = []
    else:
        top_vendeurs = get_top_vendeurs(params)
except ApiError as exc:
    st.error(str(exc))
    st.stop()

nb_ventes = len(ventes)
panier_moyen = (ca_total / nb_ventes) if nb_ventes else 0

if region_choisie != TOUTES:
    ca_par_region = [ligne for ligne in ca_par_region if ligne["region"] == region_choisie]

st.title("Dashboard KPI Ventes - NordCommerce")

col_ca, col_nb, col_panier = st.columns(3)
col_ca.metric("CA total", format_euros(ca_total))
col_nb.metric("Nombre de ventes", f"{nb_ventes}")
col_panier.metric("Panier moyen", format_euros(panier_moyen))

col_barres, col_courbe = st.columns(2)

with col_barres:
    st.subheader("CA par région")
    if ca_par_region:
        df_region = pd.DataFrame(ca_par_region).set_index("region")
        st.bar_chart(df_region["ca_total"])
    else:
        st.info("Aucune donnée pour ces filtres.")

with col_courbe:
    st.subheader("Évolution du CA")
    if evolution:
        df_evo = pd.DataFrame(evolution)
        df_evo["date"] = pd.to_datetime(
            {
                "year": df_evo["annee"].astype(int),
                "month": df_evo["mois"].astype(int),
                "day": 1,
            }
        )
        df_evo = df_evo.sort_values("date")
        df_evo["mois_annee"] = [
            libelle_mois(int(row.annee), int(row.mois)) for row in df_evo.itertuples()
        ]
        courbe = (
            alt.Chart(df_evo)
            .mark_line()
            .encode(
                x=alt.X(
                    "mois_annee:N",
                    title=None,
                    sort=alt.EncodingSortField(field="date", order="ascending"),
                    axis=alt.Axis(labelAngle=-40),
                ),
                y=alt.Y("ca_total:Q", title=None),
            )
        )
        st.altair_chart(courbe, width="stretch")
    else:
        st.info("Aucune donnée pour ces filtres.")

st.subheader("Top vendeurs")

regions_par_id = {region["id"]: region["nom"] for region in regions}
vendeurs_par_id = {vendeur["id"]: vendeur for vendeur in vendeurs}
nb_par_vendeur = Counter(vente["vendeur_id"] for vente in ventes)

if region_id:
    ca_par_vendeur = {}
    for vente in ventes:
        vendeur_id = vente["vendeur_id"]
        ca_par_vendeur[vendeur_id] = ca_par_vendeur.get(vendeur_id, 0) + vente["montant_total"]
    top_vendeurs = [
        {"vendeur_id": vendeur_id, "vendeur": vendeurs_par_id.get(vendeur_id, {}).get("nom", ""), "ca_total": montant}
        for vendeur_id, montant in sorted(ca_par_vendeur.items(), key=lambda item: item[1], reverse=True)[:10]
    ]

lignes = []
for row in top_vendeurs:
    vendeur = vendeurs_par_id.get(row["vendeur_id"])
    region_nom = ""
    if vendeur:
        region_nom = regions_par_id.get(vendeur["region_id"], "")
    lignes.append(
        {
            "Vendeur": row["vendeur"],
            "Région": region_nom,
            "CA": row["ca_total"],
            "Nb ventes": nb_par_vendeur.get(row["vendeur_id"], 0),
        }
    )

if lignes:
    st.dataframe(
        pd.DataFrame(lignes),
        hide_index=True,
        use_container_width=True,
        column_config={
            "CA": st.column_config.NumberColumn(format="%.2f €"),
        },
    )
else:
    st.info("Aucun vendeur pour ces filtres.")
