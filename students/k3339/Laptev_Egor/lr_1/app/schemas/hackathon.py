from typing import List

from pydantic import BaseModel, ConfigDict

from app.schemas.task import TaskReadSimple
from app.schemas.team import TeamRead


class HackathonBase(BaseModel):
    title: str
    description: str
    start_date: str
    end_date: str


class HackathonCreate(HackathonBase):
    pass


class HackathonRead(HackathonBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    teams: List[TeamRead] = []
    tasks: List[TaskReadSimple] = []
