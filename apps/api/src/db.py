# skeleton database code
from collections.abc import Generator
from typing import Optional, Tuple
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
    role: Optional[str] = None,
    is_admin: Optional[bool] = None,
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
        # Sync role and is_admin from JWT claims
        if role is not None:
            user.role = role
        if is_admin is not None:
            user.is_admin = is_admin
        session.add(user)
        session.commit()
        session.refresh(user)
        return user

    user = User(
        email=email,
        sub=sub,
        name=name,
        avatar_url=avatar_url,
        school=school,
        role=role,
        is_admin=is_admin or False,
    )
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


# Subtract "amount" points from the user while preventing negative balances. Returns the updated user.
def decrement_user_points(session: Session, *, user_id: int, amount: int) -> User:
    if amount <= 0:
        raise ValueError("amount must be > 0")

    user = session.get(User, user_id)
    if not user:
        raise ValueError("User not found")

    # We default points to 0 if null
    if user.points is None:
        user.points = 0

    if user.points < amount:
        raise ValueError("Insufficient points")

    user.points -= amount
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


# Deduct points to 'purchase' a note. Returns (updated_user, note), with the new user state and purchase details.
# Does not create a purchase record atm.
def purchase_note(
    session: Session, *, buyer_id: int, note_id: int, cost: int
) -> Tuple[User, Note]:
    if cost < 0:
        raise ValueError("cost must be >= 0")

    note = session.get(Note, note_id)
    if not note:
        raise ValueError("Note not found")

    updated_user = decrement_user_points(session, user_id=buyer_id, amount=cost)
    return updated_user, note
