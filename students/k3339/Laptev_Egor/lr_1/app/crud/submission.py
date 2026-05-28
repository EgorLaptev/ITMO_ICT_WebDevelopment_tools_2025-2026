from typing import List, Optional

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.submission import Submission
from app.schemas.submission import SubmissionCreate


async def create_submission(session: AsyncSession, submission_in: SubmissionCreate) -> Submission:
    submission = Submission.from_orm(submission_in)
    session.add(submission)
    await session.commit()
    await session.refresh(submission)
    return submission


async def get_submission(session: AsyncSession, submission_id: int) -> Optional[Submission]:
    return await session.get(Submission, submission_id)


async def list_submissions(session: AsyncSession, offset: int = 0, limit: int = 100) -> List[Submission]:
    statement = select(Submission).offset(offset).limit(limit)
    result = await session.exec(statement)
    return result.all()


async def update_submission(session: AsyncSession, submission_id: int, submission_in: SubmissionCreate) -> Optional[Submission]:
    submission = await session.get(Submission, submission_id)
    if not submission:
        return None
    submission_data = submission_in.dict(exclude_unset=True)
    for key, value in submission_data.items():
        setattr(submission, key, value)
    session.add(submission)
    await session.commit()
    await session.refresh(submission)
    return submission


async def delete_submission(session: AsyncSession, submission_id: int) -> bool:
    submission = await session.get(Submission, submission_id)
    if not submission:
        return False
    session.delete(submission)
    await session.commit()
    return True
