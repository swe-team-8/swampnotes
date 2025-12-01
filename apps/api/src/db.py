# skeleton database code
from collections.abc import Generator
from typing import List, Optional, Tuple
from sqlmodel import SQLModel, create_engine, Session, select  # noqa: F401
from .settings import settings
from .models import User, Course, Note, Purchase

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


# Get all notes a user has purchased
def get_user_purchased_notes(session: Session, *, user_id: int) -> List[Note]:
    stmt = (
        select(Note)
        .join(Purchase, Purchase.note_id == Note.id)
        .where(Purchase.user_id == user_id)
        .order_by(Purchase.purchased_at.desc())
    )
    return list(session.exec(stmt))


# Get all notes a user has uploaded
def get_user_uploaded_notes(session: Session, *, user_id: int) -> List[Note]:
    stmt = (
        select(Note).where(Note.author_id == user_id).order_by(Note.created_at.desc())
    )
    return list(session.exec(stmt))


# Check if user already owns this note
def has_purchased_note(session: Session, *, user_id: int, note_id: int) -> bool:
    # Check if user already owns this note
    stmt = select(Purchase).where(
        Purchase.user_id == user_id, Purchase.note_id == note_id
    )
    return session.exec(stmt).first() is not None


def create_purchase(
    session: Session, *, user_id: int, note_id: int, price: int
) -> Purchase:
    # Record a note purchase (checks for duplicates)
    # Check if already purchased
    if has_purchased_note(session, user_id=user_id, note_id=note_id):
        raise ValueError("Note already purchased")

    # Get user and note
    user = session.get(User, user_id)
    note = session.get(Note, note_id)

    if not user or not note:
        raise ValueError("User or note not found")

    # Check if user can afford it
    if price > 0:
        if user.points is None or user.points < price:
            raise ValueError("Insufficient points")

        # Deduct points from buyer
        user.points -= price
        session.add(user)

    # Create purchase record
    purchase = Purchase(user_id=user_id, note_id=note_id, price_paid=price)
    session.add(purchase)

    # Award points to note author (50% revenue share)
    if price > 0:
        author = session.get(User, note.author_id)
        if author and author.id != user_id:  # Don't reward self-purchases
            if author.points is None:
                author.points = 0
            author.points += int(price * 0.5)
            session.add(author)

    session.commit()
    session.refresh(purchase)

    return purchase


def search_notes(
    session: Session,
    *,
    query: Optional[str] = None,
    course_id: Optional[int] = None,
    semester: Optional[str] = None,
    limit: int = 20,
    offset: int = 0,
) -> List[Note]:
    # Full-text search across notes with filters
    stmt = select(Note)

    if query:
        # PostgreSQL full-text search (case-insensitive)
        search_pattern = f"%{query}%"
        stmt = stmt.where(
            (Note.title.ilike(search_pattern))
            | (Note.description.ilike(search_pattern))
            | (Note.course_name.ilike(search_pattern))
        )

    if course_id:
        stmt = stmt.where(Note.course_id == course_id)

    if semester:
        stmt = stmt.where(Note.semester == semester)

    stmt = stmt.order_by(Note.created_at.desc()).offset(offset).limit(limit)
    return list(session.exec(stmt))


def get_all_courses(session: Session) -> List[Course]:
    # Get all available courses for directory browsing
    return list(session.exec(select(Course).order_by(Course.code)))
