from typing import List, Optional

from sqlmodel import Session, select

from app.models.evaluation import Evaluation
from app.schemas.evaluation import EvaluationCreate


def create_evaluation(session: Session, evaluation_in: EvaluationCreate) -> Evaluation:
    evaluation = Evaluation.from_orm(evaluation_in)
    session.add(evaluation)
    session.commit()
    session.refresh(evaluation)
    return evaluation


def get_evaluation(session: Session, evaluation_id: int) -> Optional[Evaluation]:
    return session.get(Evaluation, evaluation_id)


def list_evaluations(session: Session, offset: int = 0, limit: int = 100) -> List[Evaluation]:
    statement = select(Evaluation).offset(offset).limit(limit)
    return session.exec(statement).all()


def update_evaluation(session: Session, evaluation_id: int, evaluation_in: EvaluationCreate) -> Optional[Evaluation]:
    evaluation = session.get(Evaluation, evaluation_id)
    if not evaluation:
        return None
    evaluation_data = evaluation_in.dict(exclude_unset=True)
    for key, value in evaluation_data.items():
        setattr(evaluation, key, value)
    session.add(evaluation)
    session.commit()
    session.refresh(evaluation)
    return evaluation


def delete_evaluation(session: Session, evaluation_id: int) -> bool:
    evaluation = session.get(Evaluation, evaluation_id)
    if not evaluation:
        return False
    session.delete(evaluation)
    session.commit()
    return True
