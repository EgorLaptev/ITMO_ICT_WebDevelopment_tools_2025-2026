from typing import Optional

from pydantic import BaseModel, ConfigDict


class EvaluationBase(BaseModel):
    submission_id: int
    judge_id: int
    score: int
    comment: Optional[str] = None


class EvaluationCreate(EvaluationBase):
    pass


class EvaluationRead(EvaluationBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
