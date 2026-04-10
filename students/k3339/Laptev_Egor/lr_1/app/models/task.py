from typing import List, Optional
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.submission import Submission


class Task(SQLModel, table=True):
    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: str
    hackathon_id: Optional[int] = Field(default=None, foreign_key="hackathons.id")

    hackathon: Optional["Hackathon"] = Relationship(back_populates="tasks")
    submissions: List["Submission"] = Relationship(back_populates="task")
