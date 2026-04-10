from typing import Optional

from pydantic import BaseModel, ConfigDict


class TaskBase(BaseModel):
    title: str
    description: str
    hackathon_id: int


class TaskCreate(TaskBase):
    pass


class TaskReadSimple(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str


class TaskRead(TaskReadSimple):
    hackathon_id: int
