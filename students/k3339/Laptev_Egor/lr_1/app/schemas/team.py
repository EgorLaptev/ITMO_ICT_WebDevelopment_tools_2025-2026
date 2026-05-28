from typing import List, Optional

from pydantic import BaseModel, ConfigDict

from app.schemas.user import UserReadSimple


class TeamBase(BaseModel):
    name: str
    hackathon_id: int


class TeamCreate(TeamBase):
    pass


class TeamJoinRequest(BaseModel):
    role_in_team: str


class TeamMemberRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user: UserReadSimple
    role_in_team: str


class TeamRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    hackathon_id: int