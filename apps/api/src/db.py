# skeleton database code
from collections.abc import Generator
from sqlmodel import SQLModel, create_engine, Session  # noqa: F401
from .settings import settings

engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
