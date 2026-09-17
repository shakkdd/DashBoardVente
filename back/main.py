from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from back.database import get_db
from back.routers import Region, Vente, Vendeur, Produit

@asynccontextmanager
async def lifespan(app : FastAPI):
    get_db()
    yield
    
app = FastAPI(title="Dashboard NordCommerce", lifespan= lifespan)

app.include_router(router= Region.router)
app.include_router(router= Vente.router)
app.include_router(router= Vendeur.routeur)
app.include_router(router= Produit.router)