from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlalchemy import text
from .settings import settings  # noqa: F401
from .db import engine
from .routers import health, auth

# Remove this once we move to alembic migrations
from sqlmodel import SQLModel


@asynccontextmanager
async def lifespan(app: FastAPI):
    # STARTUP: verify DB connection
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
        # Early dev only (we'd prefer Alembic):
        SQLModel.metadata.create_all(engine)
    yield
    # SHUTDOWN: nothing to dispose explicitly for a process-wide Engine
    # (SQLAlchemy will handle cleanup on interpreter exit)


app = FastAPI(title="SwampNotes API", lifespan=lifespan)

# Routers
app.include_router(health.router, tags=["meta"])
app.include_router(auth.router, tags=["auth"])

# Run:
# uvicorn src.main:app --reload --port 8000
