from enum import Enum
from typing import List, Optional
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.evaluation import Evaluation
    from app.models.team import TeamMember


class UserRole(str, Enum):
    participant = "participant"
    organizer = "organizer"
    judge = "judge"


class UserBase(SQLModel):
    email: str
    name: str
    role: UserRole = UserRole.participant


class User(UserBase, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    password_hash: str
    memberships: List["TeamMember"] = Relationship(back_populates="user")
    evaluations: List["Evaluation"] = Relationship(back_populates="judge")
