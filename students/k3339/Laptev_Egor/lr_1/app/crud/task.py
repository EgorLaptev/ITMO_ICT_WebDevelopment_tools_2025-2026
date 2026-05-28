from typing import List, Optional

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.task import Task
from app.schemas.task import TaskCreate


async def create_task(session: AsyncSession, task_in: TaskCreate) -> Task:
    task = Task.from_orm(task_in)
    session.add(task)
    await session.commit()
    await session.refresh(task)
    return task


async def get_task(session: AsyncSession, task_id: int) -> Optional[Task]:
    return await session.get(Task, task_id)


async def list_tasks(session: AsyncSession, offset: int = 0, limit: int = 100) -> List[Task]:
    statement = select(Task).offset(offset).limit(limit)
    result = await session.exec(statement)
    return result.all()


async def update_task(session: AsyncSession, task_id: int, task_in: TaskCreate) -> Optional[Task]:
    task = await session.get(Task, task_id)
    if not task:
        return None
    task_data = task_in.dict(exclude_unset=True)
    for key, value in task_data.items():
        setattr(task, key, value)
    session.add(task)
    await session.commit()
    await session.refresh(task)
    return task


async def delete_task(session: AsyncSession, task_id: int) -> bool:
    task = await session.get(Task, task_id)
    if not task:
        return False
    session.delete(task)
    await session.commit()
    return True
