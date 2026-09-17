from fastapi import APIRouter, HTTPException, Depends
from back.schemas.Regions import Region, RegionOut
from back.database import get_db
from back.models.Region import Region as MRegion
from sqlalchemy.orm import Session

router = APIRouter(prefix="/Region", tags=["Region"])

@router.get("/", response_model=list[RegionOut])
def get_all_regions(db : Session = Depends(get_db)):
    """Récupère toutes les régions"""
    regions = db.query(MRegion).all()
    return regions

@router.get("/{region_id}", response_model=RegionOut)
def get_region(region_id: int, db : Session = Depends(get_db)):
    """Récupère une région par son ID"""
    region = db.query(MRegion).filter(MRegion.id == region_id).first()
    if not region:
        raise HTTPException(status_code=404, detail="Région non trouvée")
    return region

@router.post("/", response_model=RegionOut)
def create_region(region: Region, db : Session = Depends(get_db)):
    """Crée une nouvelle région"""
    new_region = Region(**region.model_dump())
    db.add(new_region)
    db.commit()
    db.refresh(new_region)
    return new_region