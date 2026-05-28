from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession

from app.auth.dependencies import get_current_user, require_role
from app.crud.hackathon import (
    create_hackathon,
    delete_hackathon,
    get_hackathon,
    list_hackathons,
    update_hackathon,
)
from app.database import get_session
from app.schemas.hackathon import HackathonCreate, HackathonRead

router = APIRouter(tags=['hackathons'])


@router.get('/', response_model=List[HackathonRead])
async def read_hackathons(session: AsyncSession = Depends(get_session)) -> List[HackathonRead]:
    return await list_hackathons(session)


@router.post('/', response_model=HackathonRead)
async def create_hackathon_route(
    hackathon_in: HackathonCreate,
    session: AsyncSession = Depends(get_session),
    current_user=Depends(require_role('organizer')),
) -> HackathonRead:
    return await create_hackathon(session, hackathon_in)


@router.get('/{hackathon_id}', response_model=HackathonRead)
async def read_hackathon(hackathon_id: int, session: AsyncSession = Depends(get_session)) -> HackathonRead:
    hackathon = await get_hackathon(session, hackathon_id)
    if not hackathon:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Hackathon not found')
    return hackathon


@router.put('/{hackathon_id}', response_model=HackathonRead)
async def update_hackathon_route(
    hackathon_id: int,
    hackathon_in: HackathonCreate,
    session: AsyncSession = Depends(get_session),
    current_user=Depends(require_role('organizer')),
) -> HackathonRead:
    updated = await update_hackathon(session, hackathon_id, hackathon_in)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Hackathon not found')
    return updated


@router.delete('/{hackathon_id}')
async def delete_hackathon_route(
    hackathon_id: int,
    session: AsyncSession = Depends(get_session),
    current_user=Depends(require_role('organizer')),
) -> dict:
    success = await delete_hackathon(session, hackathon_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Hackathon not found')
    return {'ok': True}
