# skeleton database code
from collections.abc import Generator
from sqlmodel import SQLModel, create_engine, Session  # noqa: F401
from .settings import settings
from .models import *

engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


def get_all_notes() -> list[Note]:
    # TODO: Have this function connect to the database and return all notes
    # Needs to return all note objects
    return []


def get_course_by_ID() -> Course:
    # TODO: Have this function return the course by searching through all courses and finding a
    #  matching ID
    pass
