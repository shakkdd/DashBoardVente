from back.database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String


class Region(Base):
    __tablename__ = "regions"
    
    id : Mapped[int] = mapped_column(primary_key=True)
    nom : Mapped[str] = mapped_column(String(50), nullable=False)