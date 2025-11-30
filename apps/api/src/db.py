# skeleton database code
from collections.abc import Generator
from typing import Optional
from sqlmodel import SQLModel, create_engine, Session, select  # noqa: F401
from .settings import settings
from .models import User, Note, Course

engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


def get_all_notes() -> list[Note]:
    # Needs to return all note objects
    with Session(engine) as session:
        return list(session.exec(select(Note)))


def get_course_by_ID(course_id: int) -> Course | None:
    with get_session() as session:
        return session.get(Course, course_id)


# Helpers for creating/fetching records
def get_or_create_user(
    session: Session,
    *,
    sub: Optional[str],
    email: str,
    name: Optional[str] = None,
    avatar_url: Optional[str] = None,
    school: Optional[str] = None,
) -> User:
    # Prefer lookup by email; fallback to sub if provided
    stmt = select(User).where(User.email == email)
    user = session.exec(stmt).first()
    if user:
        # Minimal profile sync
        if sub and user.sub != sub:
            user.sub = sub
        if name is not None:
            user.name = name
        if avatar_url is not None:
            user.avatar_url = avatar_url
        if school is not None:
            user.school = school
        session.add(user)
        session.commit()
        session.refresh(user)
        return user

    user = User(email=email, sub=sub, name=name, avatar_url=avatar_url, school=school)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def create_course(session: Session, *, code: str, title: str, school: str) -> Course:
    course = Course(code=code, title=title, school=school)
    session.add(course)
    session.commit()
    session.refresh(course)
    return course


def create_note(
    session: Session,
    *,
    author_id: int,
    course_id: int,
    title: str,
    course_name: str,
    semester: str,
    description: Optional[str] = None,
    object_key: Optional[str] = None,
    file_type: Optional[str] = None,
) -> Note:
    note = Note(
        author_id=author_id,
        course_id=course_id,
        title=title,
        course_name=course_name,
        semester=semester,
        description=description,
        object_key=object_key,
        file_type=file_type,
    )
    note.downloads = 0
    note.views = 0
    session.add(note)
    session.commit()
    session.refresh(note)
    return note
