from datetime import datetime
from typing import Optional

from pydantic import BaseModel, HttpUrl, ConfigDict


class SubmissionBase(BaseModel):
    team_id: int
    task_id: int
    github_url: HttpUrl


class SubmissionCreate(SubmissionBase):
    pass


class SubmissionRead(SubmissionBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
