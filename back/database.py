from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

DATABASE_URL = "postgresql+psycopg2://postgres:root@localhost:5432/Vente"

engine = create_engine(DATABASE_URL)

session_local = sessionmaker(bind = engine, autocommit = False)

class Base(DeclarativeBase):
    """classe mère de tous les modèles"""
    pass

def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()
        
    