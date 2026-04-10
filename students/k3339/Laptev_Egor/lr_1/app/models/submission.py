from datetime import datetime
from typing import List, Optional
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.team import Team
    from app.models.task import Task


class Submission(SQLModel, table=True):
    __tablename__ = "submissions"

    id: Optional[int] = Field(default=None, primary_key=True)
    team_id: Optional[int] = Field(default=None, foreign_key="teams.id")
    task_id: Optional[int] = Field(default=None, foreign_key="tasks.id")
    github_url: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    team: Optional["Team"] = Relationship(back_populates="submissions")
    task: Optional["Task"] = Relationship(back_populates="submissions")
    evaluations: List["Evaluation"] = Relationship(back_populates="submission")
