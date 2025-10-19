from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
import uvicorn

from .settings import settings
from .db import engine
from .routers import health, auth, files
from .minio_client import create_bucket

BUCKET_NAME = settings.MINIO_BUCKET

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_bucket(BUCKET_NAME)
    # STARTUP: verify DB connection
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    yield
    # SHUTDOWN: nothing to dispose of explicitly


app = FastAPI(title="SwampNotes API", lifespan=lifespan)

# --- CORS ---
# CORS setup for the Next.js dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,  # e.g. ["http://localhost:3000", "http://127.0.0.1:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(health.router, tags=["meta"])
app.include_router(auth.router, tags=["auth"])
app.include_router(files.router, tags=["files"])


# Simple root so we won't (won't see 404 error at "/")
@app.get("/")
def root():
    return {"ok": True, "service": "SwampNotes API", "try": ["/health", "/auth/me"]}


# Run:
# uvicorn src.main:app --reload --port 8000

# Run main to start the server
# Go to localhost:8000
# if __name__ == "__main__":
#     uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
