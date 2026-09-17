from pydantic import BaseModel, Field
from datetime import date

class Vente(BaseModel):
    date_vente : date
    vendeur_id : int
    produit_id : int
    quantite : int = Field(gt=0)
    montant_total : float = Field(gt=0)

class VenteOut(Vente):
    id : int