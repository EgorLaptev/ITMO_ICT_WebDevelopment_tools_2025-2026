from typing import List, Optional

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.auth.hashing import get_password_hash, verify_password
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


async def get_user(session: AsyncSession, user_id: int) -> Optional[User]:
    return await session.get(User, user_id)


async def get_user_by_email(session: AsyncSession, email: str) -> Optional[User]:
    statement = select(User).where(User.email == email)
    result = await session.exec(statement)
    return result.one_or_none()


async def list_users(session: AsyncSession, offset: int = 0, limit: int = 100) -> List[User]:
    statement = select(User).offset(offset).limit(limit)
    result = await session.exec(statement)
    return result.all()


async def create_user(session: AsyncSession, user_in: UserCreate) -> User:
    user = User(
        email=user_in.email,
        name=user_in.name,
        role=user_in.role,
        password_hash=get_password_hash(user_in.password),
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


async def authenticate_user(session: AsyncSession, email: str, password: str) -> Optional[User]:
    user = await get_user_by_email(session, email)
    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user


async def update_user(session: AsyncSession, user_id: int, user_in: UserUpdate) -> Optional[User]:
    user = await get_user(session, user_id)
    if not user:
        return None
    user_data = user_in.dict(exclude_unset=True)
    for key, value in user_data.items():
        setattr(user, key, value)
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


async def change_password(session: AsyncSession, user: User, raw_password: str) -> User:
    user.password_hash = get_password_hash(raw_password)
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user
