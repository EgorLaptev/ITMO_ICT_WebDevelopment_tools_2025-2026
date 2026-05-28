from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession

from app.auth.dependencies import get_current_user, require_role
from app.crud.evaluation import (
    create_evaluation,
    delete_evaluation,
    get_evaluation,
    list_evaluations,
    update_evaluation,
)
from app.database import get_session
from app.schemas.evaluation import EvaluationCreate, EvaluationRead

router = APIRouter(tags=['evaluations'])


@router.get('/', response_model=List[EvaluationRead])
async def read_evaluations(session: AsyncSession = Depends(get_session)) -> List[EvaluationRead]:
    return await list_evaluations(session)


@router.post('/', response_model=EvaluationRead)
async def create_evaluation_route(
    evaluation_in: EvaluationCreate,
    session: AsyncSession = Depends(get_session),
    current_user=Depends(require_role('judge')),
) -> EvaluationRead:
    return await create_evaluation(session, evaluation_in)


@router.get('/{evaluation_id}', response_model=EvaluationRead)
async def read_evaluation(evaluation_id: int, session: AsyncSession = Depends(get_session)) -> EvaluationRead:
    evaluation = await get_evaluation(session, evaluation_id)
    if not evaluation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Evaluation not found')
    return evaluation


@router.put('/{evaluation_id}', response_model=EvaluationRead)
async def update_evaluation_route(
    evaluation_id: int,
    evaluation_in: EvaluationCreate,
    session: AsyncSession = Depends(get_session),
    current_user=Depends(require_role('judge')),
) -> EvaluationRead:
    evaluation = await update_evaluation(session, evaluation_id, evaluation_in)
    if not evaluation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Evaluation not found')
    return evaluation


@router.delete('/{evaluation_id}')
async def delete_evaluation_route(
    evaluation_id: int,
    session: AsyncSession = Depends(get_session),
    current_user=Depends(require_role('judge', 'organizer')),
) -> dict:
    success = await delete_evaluation(session, evaluation_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Evaluation not found')
    return {'ok': True}
