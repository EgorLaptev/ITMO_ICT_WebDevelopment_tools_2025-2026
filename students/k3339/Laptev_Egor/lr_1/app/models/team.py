from typing import List, Optional
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.submission import Submission


class Team(SQLModel, table=True):
    __tablename__ = "teams"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    hackathon_id: Optional[int] = Field(default=None, foreign_key="hackathons.id")

    members: List["TeamMember"] = Relationship(back_populates="team")
    submissions: List["Submission"] = Relationship(back_populates="team")
    hackathon: Optional["Hackathon"] = Relationship(back_populates="teams")


class TeamMember(SQLModel, table=True):
    __tablename__ = "team_members"

    user_id: Optional[int] = Field(default=None, foreign_key="users.id", primary_key=True)
    team_id: Optional[int] = Field(default=None, foreign_key="teams.id", primary_key=True)
    role_in_team: str

    user: Optional["User"] = Relationship(back_populates="memberships")
    team: Optional["Team"] = Relationship(back_populates="members")
