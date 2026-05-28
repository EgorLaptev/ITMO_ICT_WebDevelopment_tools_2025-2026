from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession

from app.auth.dependencies import get_current_user, require_role
from app.crud.task import create_task, delete_task, get_task, list_tasks, update_task
from app.database import get_session
from app.schemas.task import TaskCreate, TaskReadSimple

router = APIRouter(tags=['tasks'])


@router.get('/', response_model=List[TaskReadSimple])
async def read_tasks(session: AsyncSession = Depends(get_session)) -> List[TaskReadSimple]:
    return await list_tasks(session)


@router.post('/', response_model=TaskReadSimple)
async def create_task_route(
    task_in: TaskCreate,
    session: AsyncSession = Depends(get_session),
    current_user=Depends(require_role('organizer')),
) -> TaskReadSimple:
    return await create_task(session, task_in)


@router.get('/{task_id}', response_model=TaskReadSimple)
async def read_task(task_id: int, session: AsyncSession = Depends(get_session)) -> TaskReadSimple:
    task = await get_task(session, task_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Task not found')
    return task


@router.put('/{task_id}', response_model=TaskReadSimple)
async def update_task_route(
    task_id: int,
    task_in: TaskCreate,
    session: AsyncSession = Depends(get_session),
    current_user=Depends(require_role('organizer')),
) -> TaskReadSimple:
    task = await update_task(session, task_id, task_in)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Task not found')
    return task


@router.delete('/{task_id}')
async def delete_task_route(
    task_id: int,
    session: AsyncSession = Depends(get_session),
    current_user=Depends(require_role('organizer')),
) -> dict:
    success = await delete_task(session, task_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Task not found')
    return {'ok': True}
