from fastapi import APIRouter, HTTPException, Depends
from back.schemas.Produits import Produit, ProduitOut
from back.database import get_db
from back.models.Produit import Produit as MProduit
from sqlalchemy.orm import Session

router = APIRouter(prefix="/Produit", tags=["Produit"])

@router.get("/", response_model=list[ProduitOut])
def get_all_produits(db : Session = Depends(get_db)):
    """Récupère tous les produits"""
    produits = db.query(MProduit).all()
    return produits

@router.get("/{produit_id}", response_model=ProduitOut)
def get_produit(produit_id: int, db : Session = Depends(get_db)):
    """Récupère un produit par son ID"""
    produit = db.query(MProduit).filter(MProduit.id == produit_id).first()
    if not produit:
        raise HTTPException(status_code=404, detail="Produit non trouvé")
    return produit

@router.post("/", response_model=ProduitOut)
def create_produit(produit: Produit, db : Session = Depends(get_db)):
    """Crée un nouveau produit"""
    new_produit = MProduit(**produit.model_dump())
    db.add(new_produit)
    db.commit()
    db.refresh(new_produit)
    return new_produit

@router.put("/{produit_id}", response_model=ProduitOut)
def update_produit(produit_id: int, produit: Produit, db : Session = Depends(get_db)):
    """Met à jour un produit existant"""
    existing_produit = db.query(MProduit).filter(MProduit.id == produit_id).first()
    if not existing_produit:
        raise HTTPException(status_code=404, detail="Produit non trouvé")
    
    for key, value in produit.model_dump().items():
        setattr(existing_produit, key, value)
    
    db.commit()
    db.refresh(existing_produit)
    return existing_produit

@router.delete("/{produit_id}", response_model=ProduitOut)
def delete_produit(produit_id: int, db : Session = Depends(get_db)):
    """Supprime un produit existant"""
    existing_produit = db.query(MProduit).filter(MProduit.id == produit_id).first()
    if not existing_produit:
        raise HTTPException(status_code=404, detail="Produit non trouvé")
    
    db.delete(existing_produit)
    db.commit()
    return existing_produit