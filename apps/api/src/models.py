from datetime import datetime, timezone
from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship


# Basic model for a user
class User(SQLModel, table=True):
    # explicit primary key
    id: int | None = Field(default=None, primary_key=True)

    # clerk user ID = 'sub'ject, nullable
    # TODO: can backfill/enforce uniqueness later
    sub: Optional[str] = Field(default=None, index=True)

    email: str = Field(index=True, unique=True)
    name: Optional[str] = None
    avatar_url: Optional[str] = None
    school: Optional[str] = None
    role: Optional[str] = Field(default=None, index=True)
    is_admin: bool = Field(default=False)

    # App-specific profile settings
    display_name: Optional[str] = None
    bio: Optional[str] = None
    is_profile_public: bool = Field(default=False)
    show_email: bool = Field(default=False)

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    # notes/author relationship
    notes: List["Note"] = Relationship(back_populates="author")

    points: int = 10000


# Coure object skeleton
class Course(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    code: str = Field(index=True)
    title: str
    school: str


# Note object skeleton
class Note(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    author_id: int = Field(foreign_key="user.id", index=True)
    course_id: int = Field(foreign_key="course.id", index=True)
    title: str
    course_name: str
    semester: str
    description: str | None = None
    object_key: str | None = None  # Use this NOT file_url
    file_type: str | None = None
    author: Optional[User] = Relationship(back_populates="notes")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    ratings: List["Rating"] = Relationship(back_populates="note")
    downloads: int = 0
    views: int = 0
    price: int = Field(default=100)  # Points required to purchase
    is_free: bool = Field(default=False)  # Allow free notes
    purchases: List["Purchase"] = Relationship(back_populates="note")


# Ratings object skeleton
class Rating(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    author_id: int = Field(foreign_key="user.id", index=True)
    note_id: int = Field(foreign_key="note.id", index=True)
    description: Optional[str] = None
    rating: float
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    author: Optional[User] = Relationship()
    note: Optional[Note] = Relationship(back_populates="ratings")


# Purchase object skeleton, tracks note purchases by users
class Purchase(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", index=True)
    note_id: int = Field(foreign_key="note.id", index=True)
    price_paid: int = Field(default=100)  # Points spent
    purchased_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    # Relationships
    user: Optional[User] = Relationship()
    note: Optional[Note] = Relationship()

    class Config:
        # Prevent duplicate purchases
        table_args = ({"schema": None},)
