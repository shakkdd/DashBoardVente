from fastapi import APIRouter, HTTPException, Depends
from back.schemas.Ventes import Vente, VenteOut
from back.database import get_db
from back.models.Ventes import Vente as MVente
from back.models.Region import Region as MRegion
from back.models.Vendeur import Vendeur as MVendeur
from sqlalchemy.orm import Session
from datetime import date
from typing import Optional

router = APIRouter(prefix="/Ventes", tags=["Ventes"])

@router.get("/", response_model=list[VenteOut])
def get_all_ventes(db : Session = Depends(get_db)):
    """Récupère toutes les ventes"""
    ventes = db.query(MVente).all()
    return ventes

@router.get("/dates", response_model=list[VenteOut])
def get_ventes(
    date_debut: Optional[date] = None,
    date_fin: Optional[date] = None,
    categorie: Optional[int] = None,
    region: Optional[int] = None,
    db: Session = Depends(get_db),
):
    """Récupère les ventes avec des filtres optionnels"""
    query = db.query(MVente)

    if date_debut:
        query = query.filter(MVente.date_vente >= date_debut)
    if date_fin:
        query = query.filter(MVente.date_vente <= date_fin)
    if categorie:
        query = query.filter(MVente.produit_id == categorie)
    if region:
        query = query.join(MVendeur, MVente.vendeur_id == MVendeur.id).filter(MVendeur.region_id == region)

    ventes = query.all()
    return ventes

@router.get("/{vente_id}", response_model=VenteOut)
def get_vente(vente_id: int, db : Session = Depends(get_db)):
    """Récupère une vente par son ID"""
    vente = db.query(MVente).filter(MVente.id == vente_id).first()
    if not vente:
        raise HTTPException(status_code=404, detail="Vente non trouvée")
    return vente

@router.post("/", response_model=VenteOut)
def create_vente(vente: Vente, db : Session = Depends(get_db)):
    """Crée une nouvelle vente"""
    new_vente = MVente(**vente.model_dump())
    db.add(new_vente)
    db.commit()
    db.refresh(new_vente)
    return new_vente
