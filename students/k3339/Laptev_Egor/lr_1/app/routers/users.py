from typing import List

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from app.auth.dependencies import get_current_user, require_role
from app.crud.user import get_user, list_users, update_user
from app.database import get_session
from app.schemas.user import UserRead, UserUpdate

router = APIRouter(tags=["users"])


@router.get("/", response_model=List[UserRead])
def read_users(
    session: Session = Depends(get_session),
    current_user=Depends(require_role("organizer")),
) -> List[UserRead]:
    return list_users(session)


@router.get("/{user_id}", response_model=UserRead)
def read_user(
    user_id: int,
    session: Session = Depends(get_session),
    current_user=Depends(get_current_user),
) -> UserRead:
    if current_user.id != user_id and current_user.role != "organizer":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
    user = get_user(session, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.put("/{user_id}", response_model=UserRead)
def update_user_route(
    user_id: int,
    user_in: UserUpdate,
    session: Session = Depends(get_session),
    current_user=Depends(get_current_user),
) -> UserRead:
    if current_user.id != user_id and current_user.role != "organizer":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
    updated = update_user(session, user_id, user_in)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return updated
