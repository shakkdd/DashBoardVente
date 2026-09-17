from fastapi import APIRouter, HTTPException, Depends
from back.schemas.Vendeurs import Vendeur, VendeurOut
from back.database import get_db
from back.models.Vendeur import Vendeur as MVendeur
from sqlalchemy.orm import Session

routeur = APIRouter(prefix="/Vendeur", tags=["Vendeur"])

@routeur.get("/", response_model=list[VendeurOut])
def get_all_vendeurs(db : Session = Depends(get_db)):
    """Récupère tous les vendeurs"""
    vendeurs = db.query(MVendeur).all()
    return vendeurs

@routeur.get("/{vendeur_id}", response_model=VendeurOut)
def get_vendeur(vendeur_id: int, db : Session = Depends(get_db)):
    """Récupère un vendeur par son ID"""
    vendeur = db.query(MVendeur).filter(MVendeur.id == vendeur_id).first()
    if not vendeur:
        raise HTTPException(status_code=404, detail="Vendeur non trouvé")
    return vendeur

@routeur.post("/", response_model=VendeurOut)
def create_vendeur(vendeur: Vendeur, db : Session = Depends(get_db)):
    """Crée un nouveau vendeur"""
    new_vendeur = MVendeur(**vendeur.model_dump())
    db.add(new_vendeur)
    db.commit()
    db.refresh(new_vendeur)
    return new_vendeur

@routeur.put("/{vendeur_id}", response_model=VendeurOut)
def update_vendeur(vendeur_id: int, vendeur: Vendeur, db : Session = Depends(get_db)):
    """Met à jour un vendeur existant"""
    existing_vendeur = db.query(MVendeur).filter(MVendeur.id == vendeur_id).first()
    if not existing_vendeur:
        raise HTTPException(status_code=404, detail="Vendeur non trouvé")
    
    for key, value in vendeur.model_dump().items():
        setattr(existing_vendeur, key, value)
    
    db.commit()
    db.refresh(existing_vendeur)
    return existing_vendeur