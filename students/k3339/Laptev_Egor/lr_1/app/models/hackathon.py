from typing import List, Optional
from typing import TYPE_CHECKING

from datetime import datetime

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.task import Task
    from app.models.team import Team


class Hackathon(SQLModel, table=True):
    __tablename__ = "hackathons"

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: str
    start_date: datetime
    end_date: datetime

    teams: List["Team"] = Relationship(back_populates="hackathon")
    tasks: List["Task"] = Relationship(back_populates="hackathon")
