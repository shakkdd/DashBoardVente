from fastapi import APIRouter, HTTPException, Depends
from back.schemas.Ventes import Vente, VenteOut
from back.database import get_db
from back.models.Ventes import Vente as MVente
from sqlalchemy.orm import Session

router = APIRouter(prefix="/Ventes", tags=["Ventes"])

@router.get("/", response_model=list[VenteOut])
def get_all_ventes(db : Session = Depends(get_db)):
    """Récupère toutes les ventes"""
    ventes = db.query(MVente).all()
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
