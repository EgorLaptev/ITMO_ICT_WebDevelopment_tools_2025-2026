from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from app.core.security import get_current_user, require_role
from app.database import get_session
from app.schemas.task import TaskCreate, TaskReadSimple
from app.services.task_service import create_task, delete_task, get_task, list_tasks, update_task

router = APIRouter(tags=["tasks"])


@router.get("/", response_model=List[TaskReadSimple])
def read_tasks(session: Session = Depends(get_session)) -> List[TaskReadSimple]:
    return list_tasks(session)


@router.post("/", response_model=TaskReadSimple)
def create_task_route(
    task_in: TaskCreate,
    session: Session = Depends(get_session),
    current_user=Depends(require_role("organizer")),
) -> TaskReadSimple:
    return create_task(session, task_in)


@router.get("/{task_id}", response_model=TaskReadSimple)
def read_task(task_id: int, session: Session = Depends(get_session)) -> TaskReadSimple:
    task = get_task(session, task_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task


@router.put("/{task_id}", response_model=TaskReadSimple)
def update_task_route(
    task_id: int,
    task_in: TaskCreate,
    session: Session = Depends(get_session),
    current_user=Depends(require_role("organizer")),
) -> TaskReadSimple:
    task = update_task(session, task_id, task_in)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task


@router.delete("/{task_id}")
def delete_task_route(
    task_id: int,
    session: Session = Depends(get_session),
    current_user=Depends(require_role("organizer")),
) -> dict:
    success = delete_task(session, task_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return {"ok": True}
