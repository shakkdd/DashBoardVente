from back.database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

class Vendeur(Base):
    __tablename__ = "vendeurs"
    id : Mapped[int] = mapped_column(primary_key=True)
    nom : Mapped[str] = mapped_column(String(100), nullable=False)
    region_id : Mapped[int] = mapped_column(nullable=False)