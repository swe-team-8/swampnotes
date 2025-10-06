# skeleton database code
from sqlmodel import SQLModel, create_engine, Session  # noqa: F401
from .settings import settings

engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)


def get_session():
    with Session(engine) as session:
        yield session
