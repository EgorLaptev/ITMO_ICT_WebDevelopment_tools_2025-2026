from typing import List, Optional

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.evaluation import Evaluation
from app.schemas.evaluation import EvaluationCreate


async def create_evaluation(session: AsyncSession, evaluation_in: EvaluationCreate) -> Evaluation:
    evaluation = Evaluation.from_orm(evaluation_in)
    session.add(evaluation)
    await session.commit()
    await session.refresh(evaluation)
    return evaluation


async def get_evaluation(session: AsyncSession, evaluation_id: int) -> Optional[Evaluation]:
    return await session.get(Evaluation, evaluation_id)


async def list_evaluations(session: AsyncSession, offset: int = 0, limit: int = 100) -> List[Evaluation]:
    statement = select(Evaluation).offset(offset).limit(limit)
    result = await session.exec(statement)
    return result.all()


async def update_evaluation(session: AsyncSession, evaluation_id: int, evaluation_in: EvaluationCreate) -> Optional[Evaluation]:
    evaluation = await session.get(Evaluation, evaluation_id)
    if not evaluation:
        return None
    evaluation_data = evaluation_in.dict(exclude_unset=True)
    for key, value in evaluation_data.items():
        setattr(evaluation, key, value)
    session.add(evaluation)
    await session.commit()
    await session.refresh(evaluation)
    return evaluation


async def delete_evaluation(session: AsyncSession, evaluation_id: int) -> bool:
    evaluation = await session.get(Evaluation, evaluation_id)
    if not evaluation:
        return False
    session.delete(evaluation)
    await session.commit()
    return True
