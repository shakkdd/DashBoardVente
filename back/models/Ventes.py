from back.database import Base
from sqlalchemy.orm import Mapped, mapped_column
from datetime import date


class Vente(Base):
    __tablename__ = "ventes" 
    
    id : Mapped[int] = mapped_column(primary_key=True)
    date_vente : Mapped[date] = mapped_column(nullable=False)
    vendeur_id : Mapped[int] = mapped_column(nullable=False)
    produit_id : Mapped[int] = mapped_column(nullable=False)
    quantite : Mapped[int] = mapped_column(nullable=False)
    montant_total : Mapped[float] = mapped_column(nullable=False)