from fastapi import APIRouter, Depends
from sqlalchemy import func, extract, desc
from sqlalchemy.orm import Session
from datetime import date
from typing import Optional

from back.database import get_db
from back.models.Produit import Produit as MProduit
from back.models.Region import Region as MRegion
from back.models.Ventes import Vente as MVente
from back.models.Vendeur import Vendeur as MVendeur

router = APIRouter(prefix="/kpi", tags=["KPI"])


def apply_filters(query, date_debut: Optional[date] = None, date_fin: Optional[date] = None,
                 categorie: Optional[int] = None, region: Optional[int] = None):
    if date_debut:
        query = query.filter(MVente.date_vente >= date_debut)
    if date_fin:
        query = query.filter(MVente.date_vente <= date_fin)
    if categorie:
        query = query.filter(MVente.produit_id == categorie)
    if region:
        query = query.join(MVendeur, MVente.vendeur_id == MVendeur.id).filter(MVendeur.region_id == region)
    return query


@router.get("/ca_total")
def get_ca_total(
    date_debut: Optional[date] = None,
    date_fin: Optional[date] = None,
    categorie: Optional[int] = None,
    region: Optional[int] = None,
    db: Session = Depends(get_db),
):
    """Chiffre d'affaires total selon les filtres"""
    query = apply_filters(db.query(MVente), date_debut, date_fin, categorie, region)
    total = query.with_entities(func.coalesce(func.sum(MVente.montant_total), 0)).scalar()
    return {"ca_total": float(total or 0)}


@router.get("/ca_par_region")
def get_ca_par_region(
    date_debut: Optional[date] = None,
    date_fin: Optional[date] = None,
    categorie: Optional[int] = None,
    db: Session = Depends(get_db),
):
    """CA agrégé par région"""
    query = apply_filters(
        db.query(
            MRegion.id.label("region_id"),
            MRegion.nom.label("region"),
            func.coalesce(func.sum(MVente.montant_total), 0).label("ca_total"),
        )
        .join(MVendeur, MVente.vendeur_id == MVendeur.id)
        .join(MRegion, MVendeur.region_id == MRegion.id),
        date_debut,
        date_fin,
        categorie,
        None,
    )
    query = query.group_by(MRegion.id, MRegion.nom).order_by(desc("ca_total"))
    return [{"region_id": row.region_id, "region": row.region, "ca_total": float(row.ca_total)} for row in query.all()]


@router.get("/ca_par_produit")
def get_ca_par_produit(
    date_debut: Optional[date] = None,
    date_fin: Optional[date] = None,
    region: Optional[int] = None,
    db: Session = Depends(get_db),
):
    """CA agrégé par produit ou catégorie"""
    query = apply_filters(
        db.query(
            MProduit.id.label("produit_id"),
            MProduit.nom.label("produit"),
            MProduit.categorie.label("categorie"),
            func.coalesce(func.sum(MVente.montant_total), 0).label("ca_total"),
        )
        .join(MProduit, MVente.produit_id == MProduit.id),
        date_debut,
        date_fin,
        None,
        region,
    )
    query = query.group_by(MProduit.id, MProduit.nom, MProduit.categorie).order_by(desc("ca_total"))
    return [{"produit_id": row.produit_id, "produit": row.produit, "categorie": row.categorie, "ca_total": float(row.ca_total)} for row in query.all()]


@router.get("/evolution_mensuelle")
def get_evolution_mensuelle(
    date_debut: Optional[date] = None,
    date_fin: Optional[date] = None,
    categorie: Optional[int] = None,
    region: Optional[int] = None,
    db: Session = Depends(get_db),
):
    """CA par mois pour une courbe d'évolution"""
    query = apply_filters(
        db.query(
            extract('year', MVente.date_vente).label("annee"),
            extract('month', MVente.date_vente).label("mois"),
            func.coalesce(func.sum(MVente.montant_total), 0).label("ca_total"),
        ),
        date_debut,
        date_fin,
        categorie,
        region,
    )
    query = query.group_by("annee", "mois").order_by("annee", "mois")
    return [{"annee": int(row.annee), "mois": int(row.mois), "ca_total": float(row.ca_total)} for row in query.all()]


@router.get("/top_vendeurs")
def get_top_vendeurs(
    date_debut: Optional[date] = None,
    date_fin: Optional[date] = None,
    categorie: Optional[int] = None,
    region: Optional[int] = None,
    limit: int = 10,
    db: Session = Depends(get_db),
):
    """Classement des vendeurs par CA généré"""
    query = apply_filters(
        db.query(
            MVendeur.id.label("vendeur_id"),
            MVendeur.nom.label("vendeur"),
            func.coalesce(func.sum(MVente.montant_total), 0).label("ca_total"),
        )
        .join(MVendeur, MVente.vendeur_id == MVendeur.id),
        date_debut,
        date_fin,
        categorie,
        region,
    )
    query = query.group_by(MVendeur.id, MVendeur.nom).order_by(desc("ca_total")).limit(limit)
    return [{"vendeur_id": row.vendeur_id, "vendeur": row.vendeur, "ca_total": float(row.ca_total)} for row in query.all()]
