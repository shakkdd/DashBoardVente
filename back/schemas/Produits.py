from pydantic import BaseModel, Field

class Produit(BaseModel):
    nom : str
    categorie : str
    prix_unitaire : float = Field(gt=0)
    
class ProduitOut(Produit):
    id : int
    