from typing import Optional
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.submission import Submission
    from app.models.user import User


class Evaluation(SQLModel, table=True):
    __tablename__ = "evaluations"

    id: Optional[int] = Field(default=None, primary_key=True)
    submission_id: Optional[int] = Field(default=None, foreign_key="submissions.id")
    judge_id: Optional[int] = Field(default=None, foreign_key="users.id")
    score: int
    comment: Optional[str] = None

    submission: Optional["Submission"] = Relationship(back_populates="evaluations")
    judge: Optional["User"] = Relationship(back_populates="evaluations")
