from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession

from app.auth.dependencies import get_current_user, require_role
from app.crud.team import create_team, delete_team, get_team, join_team, list_teams, update_team
from app.database import get_session
from app.schemas.team import TeamCreate, TeamJoinRequest, TeamRead

router = APIRouter(tags=['teams'])


@router.get('/', response_model=List[TeamRead])
async def read_teams(session: AsyncSession = Depends(get_session)) -> List[TeamRead]:
    return await list_teams(session)


@router.post('/', response_model=TeamRead)
async def create_team_route(
    team_in: TeamCreate,
    session: AsyncSession = Depends(get_session),
    current_user=Depends(get_current_user),
) -> TeamRead:
    return await create_team(session, team_in)


@router.get('/{team_id}', response_model=TeamRead)
async def read_team(team_id: int, session: AsyncSession = Depends(get_session)) -> TeamRead:
    team = await get_team(session, team_id)
    if not team:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Team not found')
    return team


@router.post('/{team_id}/join', response_model=TeamRead)
async def join_team_route(
    team_id: int,
    payload: TeamJoinRequest,
    session: AsyncSession = Depends(get_session),
    current_user=Depends(get_current_user),
) -> TeamRead:
    membership = await join_team(session, team_id, current_user.id, payload.role_in_team)
    if not membership:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Team not found')
    return await get_team(session, team_id)


@router.put('/{team_id}', response_model=TeamRead)
async def update_team_route(
    team_id: int,
    team_in: TeamCreate,
    session: AsyncSession = Depends(get_session),
    current_user=Depends(require_role('organizer')),
) -> TeamRead:
    team = await update_team(session, team_id, team_in.name)
    if not team:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Team not found')
    return team


@router.delete('/{team_id}')
async def delete_team_route(
    team_id: int,
    session: AsyncSession = Depends(get_session),
    current_user=Depends(require_role('organizer')),
) -> dict:
    success = await delete_team(session, team_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Team not found')
    return {'ok': True}
