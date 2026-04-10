from typing import List, Optional

from sqlmodel import Session, select

from app.models.task import Task
from app.schemas.task import TaskCreate


def create_task(session: Session, task_in: TaskCreate) -> Task:
    task = Task.from_orm(task_in)
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


def get_task(session: Session, task_id: int) -> Optional[Task]:
    return session.get(Task, task_id)


def list_tasks(session: Session, offset: int = 0, limit: int = 100) -> List[Task]:
    statement = select(Task).offset(offset).limit(limit)
    return session.exec(statement).all()


def update_task(session: Session, task_id: int, task_in: TaskCreate) -> Optional[Task]:
    task = session.get(Task, task_id)
    if not task:
        return None
    task_data = task_in.dict(exclude_unset=True)
    for key, value in task_data.items():
        setattr(task, key, value)
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


def delete_task(session: Session, task_id: int) -> bool:
    task = session.get(Task, task_id)
    if not task:
        return False
    session.delete(task)
    session.commit()
    return True
