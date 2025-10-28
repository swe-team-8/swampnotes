from datetime import datetime, timezone
from typing import List
from sqlmodel import SQLModel, Field, Relationship


# Basic model for a user (skeleton)
class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    email: str = Field(index=True, unique=True)
    password: str | None = None
    auth_provider: str | None = "clerk"
    name: str | None = None
    school: str | None = None
    role: str = "student"  # student/tutor/admin
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    notes: List["Note"] = Relationship(back_populates="author")


# The necessary info from above for logging in
class UserLogin(SQLModel):
    email: str | None = None
    password: str | None = None


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
    file_url: str
    file_type: str | None = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    author: User | None = Relationship(back_populates="notes")

