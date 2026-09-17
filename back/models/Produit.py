from back.database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

class Produit(Base):
    __tablename__ = "produits"
    
    id : Mapped[int] = mapped_column(primary_key=True)
    nom : Mapped[str] = mapped_column(String(100), nullable=False)
    categorie : Mapped[str] = mapped_column(String(50), nullable=False)
    prix_unitaire : Mapped[float]