from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.api.v1.routes import router as corpus_router
from app.core.db import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize database tables on startup
    await init_db()
    yield

app = FastAPI(
    title="LyricLingo API",
    description="Multilingual Lyrics & Slang Corpus Manager API",
    version="0.1.0",
    lifespan=lifespan
)

app.include_router(corpus_router)

@app.get("/")
async def root():
    return {"message": "Welcome to LyricLingo API"}
