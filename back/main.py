from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from back.database import get_db
from back.routers import Region

@asynccontextmanager
async def lifespan(app : FastAPI):
    get_db()
    yield
    
app = FastAPI(title="Dashboard Vente", lifespan= lifespan)

app.include_router(router= Region.router)