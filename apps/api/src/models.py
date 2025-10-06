from datetime import datetime
from typing import List
from sqlmodel import SQLModel, Field, Relationship


# Basic model for a user (skeleton)
class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    email: str = Field(index=True, unique=True)
    name: str | None = None
    school: str | None = None
    role: str = "student"  # student/tutor/admin
    created_at: datetime = Field(default_factory=datetime.now(datetime.timezone.utc))
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
    file_url: str
    file_type: str | None = None
    created_at: datetime = Field(default_factory=datetime.now(datetime.timezone.utc))
    author: User | None = Relationship(back_populates="notes")
