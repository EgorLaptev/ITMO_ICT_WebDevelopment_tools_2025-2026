from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession

from app.auth.dependencies import get_current_user
from app.crud.submission import (
    create_submission,
    delete_submission,
    get_submission,
    list_submissions,
    update_submission,
)
from app.database import get_session
from app.schemas.submission import SubmissionCreate, SubmissionRead

router = APIRouter(tags=['submissions'])


@router.get('/', response_model=List[SubmissionRead])
async def read_submissions(session: AsyncSession = Depends(get_session)) -> List[SubmissionRead]:
    return await list_submissions(session)


@router.post('/', response_model=SubmissionRead)
async def create_submission_route(
    submission_in: SubmissionCreate,
    session: AsyncSession = Depends(get_session),
    current_user=Depends(get_current_user),
) -> SubmissionRead:
    return await create_submission(session, submission_in)


@router.get('/{submission_id}', response_model=SubmissionRead)
async def read_submission(submission_id: int, session: AsyncSession = Depends(get_session)) -> SubmissionRead:
    submission = await get_submission(session, submission_id)
    if not submission:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Submission not found')
    return submission


@router.put('/{submission_id}', response_model=SubmissionRead)
async def update_submission_route(
    submission_id: int,
    submission_in: SubmissionCreate,
    session: AsyncSession = Depends(get_session),
    current_user=Depends(get_current_user),
) -> SubmissionRead:
    submission = await update_submission(session, submission_id, submission_in)
    if not submission:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Submission not found')
    return submission


@router.delete('/{submission_id}')
async def delete_submission_route(
    submission_id: int,
    session: AsyncSession = Depends(get_session),
    current_user=Depends(get_current_user),
) -> dict:
    success = await delete_submission(session, submission_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Submission not found')
    return {'ok': True}
