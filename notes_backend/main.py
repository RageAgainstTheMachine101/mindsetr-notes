from fastapi import FastAPI
from contextlib import asynccontextmanager
from .database import engine, init_db
from .routers import notes

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(notes.router)

@app.get("/health")
def health_check():
    return {"status": "ok"}
