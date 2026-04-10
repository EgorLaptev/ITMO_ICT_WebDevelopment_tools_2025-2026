from typing import List, Optional

from sqlmodel import Session, select

from app.core.security import get_password_hash, verify_password
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


def get_user(session: Session, user_id: int) -> Optional[User]:
    return session.get(User, user_id)


def get_user_by_email(session: Session, email: str) -> Optional[User]:
    statement = select(User).where(User.email == email)
    return session.exec(statement).one_or_none()


def list_users(session: Session, offset: int = 0, limit: int = 100) -> List[User]:
    statement = select(User).offset(offset).limit(limit)
    return session.exec(statement).all()


def create_user(session: Session, user_in: UserCreate) -> User:
    user = User(
        email=user_in.email,
        name=user_in.name,
        role=user_in.role,
        password_hash=get_password_hash(user_in.password),
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def authenticate_user(session: Session, email: str, password: str) -> Optional[User]:
    user = get_user_by_email(session, email)
    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user


def update_user(session: Session, user_id: int, user_in: UserUpdate) -> Optional[User]:
    user = get_user(session, user_id)
    if not user:
        return None
    user_data = user_in.dict(exclude_unset=True)
    for key, value in user_data.items():
        setattr(user, key, value)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def change_password(session: Session, user: User, raw_password: str) -> User:
    user.password_hash = get_password_hash(raw_password)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user
