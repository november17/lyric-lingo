from fastapi import FastAPI

app = FastAPI(
    title="LyricLingo API",
    description="Multilingual Lyrics & Slang Corpus Manager API",
    version="0.1.0",
)

@app.get("/")
async def root():
    return {"message": "Welcome to LyricLingo API"}
