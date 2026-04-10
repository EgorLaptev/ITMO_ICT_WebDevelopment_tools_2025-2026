from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from app.core.security import get_current_user
from app.database import get_session
from app.schemas.submission import SubmissionCreate, SubmissionRead
from app.services.submission_service import (
    create_submission,
    delete_submission,
    get_submission,
    list_submissions,
    update_submission,
)

router = APIRouter(tags=["submissions"])


@router.get("/", response_model=List[SubmissionRead])
def read_submissions(session: Session = Depends(get_session)) -> List[SubmissionRead]:
    return list_submissions(session)


@router.post("/", response_model=SubmissionRead)
def create_submission_route(
    submission_in: SubmissionCreate,
    session: Session = Depends(get_session),
    current_user=Depends(get_current_user),
) -> SubmissionRead:
    return create_submission(session, submission_in)


@router.get("/{submission_id}", response_model=SubmissionRead)
def read_submission(submission_id: int, session: Session = Depends(get_session)) -> SubmissionRead:
    submission = get_submission(session, submission_id)
    if not submission:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Submission not found")
    return submission


@router.put("/{submission_id}", response_model=SubmissionRead)
def update_submission_route(
    submission_id: int,
    submission_in: SubmissionCreate,
    session: Session = Depends(get_session),
    current_user=Depends(get_current_user),
) -> SubmissionRead:
    submission = update_submission(session, submission_id, submission_in)
    if not submission:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Submission not found")
    return submission


@router.delete("/{submission_id}")
def delete_submission_route(
    submission_id: int,
    session: Session = Depends(get_session),
    current_user=Depends(get_current_user),
) -> dict:
    success = delete_submission(session, submission_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Submission not found")
    return {"ok": True}
