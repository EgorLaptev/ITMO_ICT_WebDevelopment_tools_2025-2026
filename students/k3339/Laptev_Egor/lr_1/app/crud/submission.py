from typing import List, Optional

from sqlmodel import Session, select

from app.models.submission import Submission
from app.schemas.submission import SubmissionCreate


def create_submission(session: Session, submission_in: SubmissionCreate) -> Submission:
    submission = Submission.from_orm(submission_in)
    session.add(submission)
    session.commit()
    session.refresh(submission)
    return submission


def get_submission(session: Session, submission_id: int) -> Optional[Submission]:
    return session.get(Submission, submission_id)


def list_submissions(session: Session, offset: int = 0, limit: int = 100) -> List[Submission]:
    statement = select(Submission).offset(offset).limit(limit)
    return session.exec(statement).all()


def update_submission(session: Session, submission_id: int, submission_in: SubmissionCreate) -> Optional[Submission]:
    submission = session.get(Submission, submission_id)
    if not submission:
        return None
    submission_data = submission_in.dict(exclude_unset=True)
    for key, value in submission_data.items():
        setattr(submission, key, value)
    session.add(submission)
    session.commit()
    session.refresh(submission)
    return submission


def delete_submission(session: Session, submission_id: int) -> bool:
    submission = session.get(Submission, submission_id)
    if not submission:
        return False
    session.delete(submission)
    session.commit()
    return True
