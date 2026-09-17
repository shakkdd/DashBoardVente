from pydantic import BaseModel

class Vendeur(BaseModel):
    nom : str
    region_id : int
    
class VendeurOut(Vendeur):
    id : int