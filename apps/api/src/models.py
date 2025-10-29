from datetime import datetime, timezone
from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship


# Basic model for a user (skeleton)
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
    role: str = "student"  # student/tutor/admin

    # App-specific profile settings
    display_name: Optional[str] = None
    bio: Optional[str] = None
    is_profile_public: bool = Field(default=False)
    show_email: bool = Field(default=False)

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    # notes/author relationship
    notes: List["Note"] = Relationship(back_populates="author")

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    notes: List["Note"] = Relationship(back_populates="author")


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
    description: str | None = None
    object_key: str | None = None  # Use this NOT file_url
    file_type: str | None = None
    author: User | None = Relationship(back_populates="notes")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
