from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel.ext.asyncio.session import AsyncSession

from app.auth.dependencies import get_current_user
from app.auth.hashing import verify_password
from app.auth.jwt import create_access_token
from app.crud.user import authenticate_user, create_user, change_password
from app.database import get_session
from app.schemas.auth import ChangePasswordRequest, UserRegister
from app.schemas.token import Token
from app.schemas.user import UserRead

router = APIRouter(prefix='/auth', tags=['auth'])


@router.post('/register', response_model=UserRead)
async def register(user_in: UserRegister, session: AsyncSession = Depends(get_session)) -> UserRead:
    existing = await authenticate_user(session, user_in.email, user_in.password)
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='User already exists')
    created = await create_user(session, user_in)
    return created


@router.post('/login', response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), session: AsyncSession = Depends(get_session)) -> Token:
    user = await authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid credentials')
    access_token = create_access_token(subject=user.email)
    return Token(access_token=access_token, token_type='bearer')


@router.get('/me', response_model=UserRead)
async def read_me(current_user=Depends(get_current_user)) -> UserRead:
    return current_user


@router.post('/change-password')
async def change_password_route(
    payload: ChangePasswordRequest,
    session: AsyncSession = Depends(get_session),
    current_user=Depends(get_current_user),
) -> dict:
    if not verify_password(payload.current_password, current_user.password_hash):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Current password is incorrect')
    await change_password(session, current_user, payload.new_password)
    return {'ok': True}
