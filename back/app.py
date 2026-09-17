from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from database import get_db

@asynccontextmanager
async def lifespan(app : FastAPI):
    get_db()
    yield
    
app = FastAPI(title="Dashboard Vente", lifespan= lifespan)