from typing import List, Optional

from sqlalchemy.orm import selectinload
from sqlmodel import Session, select

from app.models.team import Team, TeamMember
from app.schemas.team import TeamCreate


def create_team(session: Session, team_in: TeamCreate) -> Team:
    team = Team.from_orm(team_in)
    session.add(team)
    session.commit()
    session.refresh(team)
    return team


def get_team(session: Session, team_id: int) -> Optional[Team]:
    statement = select(Team).where(Team.id == team_id).options(
        selectinload(Team.members).selectinload(TeamMember.user)
    )
    return session.exec(statement).one_or_none()


def list_teams(session: Session, offset: int = 0, limit: int = 100) -> List[Team]:
    statement = select(Team).options(
        selectinload(Team.members).selectinload(TeamMember.user)
    ).offset(offset).limit(limit)
    return session.exec(statement).all()


def update_team(session: Session, team_id: int, name: str) -> Optional[Team]:
    team = session.get(Team, team_id)
    if not team:
        return None
    team.name = name
    session.add(team)
    session.commit()
    session.refresh(team)
    return team


def delete_team(session: Session, team_id: int) -> bool:
    team = session.get(Team, team_id)
    if not team:
        return False
    session.delete(team)
    session.commit()
    return True


def join_team(session: Session, team_id: int, user_id: int, role_in_team: str) -> Optional[TeamMember]:
    team = session.get(Team, team_id)
    if not team:
        return None
    statement = select(TeamMember).where(
        TeamMember.team_id == team_id,
        TeamMember.user_id == user_id,
    )
    existing = session.exec(statement).one_or_none()
    if existing:
        return existing
    membership = TeamMember(team_id=team_id, user_id=user_id, role_in_team=role_in_team)
    session.add(membership)
    session.commit()
    session.refresh(membership)
    return membership
