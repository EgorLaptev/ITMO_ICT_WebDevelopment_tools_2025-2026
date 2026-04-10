from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from app.core.security import get_current_user, require_role
from app.database import get_session
from app.schemas.team import TeamCreate, TeamJoinRequest, TeamRead
from app.services.team_service import create_team, delete_team, get_team, join_team, list_teams, update_team

router = APIRouter(tags=["teams"])


@router.get("/", response_model=List[TeamRead])
def read_teams(session: Session = Depends(get_session)) -> List[TeamRead]:
    return list_teams(session)


@router.post("/", response_model=TeamRead)
def create_team_route(
    team_in: TeamCreate,
    session: Session = Depends(get_session),
    current_user=Depends(get_current_user),
) -> TeamRead:
    return create_team(session, team_in)


@router.get("/{team_id}", response_model=TeamRead)
def read_team(team_id: int, session: Session = Depends(get_session)) -> TeamRead:
    team = get_team(session, team_id)
    if not team:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team not found")
    return team


@router.post("/{team_id}/join", response_model=TeamRead)
def join_team_route(
    team_id: int,
    payload: TeamJoinRequest,
    session: Session = Depends(get_session),
    current_user=Depends(get_current_user),
) -> TeamRead:
    membership = join_team(session, team_id, current_user.id, payload.role_in_team)
    if not membership:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team not found")
    return get_team(session, team_id)


@router.put("/{team_id}", response_model=TeamRead)
def update_team_route(
    team_id: int,
    team_in: TeamCreate,
    session: Session = Depends(get_session),
    current_user=Depends(require_role("organizer")),
) -> TeamRead:
    team = update_team(session, team_id, team_in.name)
    if not team:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team not found")
    return team


@router.delete("/{team_id}")
def delete_team_route(
    team_id: int,
    session: Session = Depends(get_session),
    current_user=Depends(require_role("organizer")),
) -> dict:
    success = delete_team(session, team_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team not found")
    return {"ok": True}
