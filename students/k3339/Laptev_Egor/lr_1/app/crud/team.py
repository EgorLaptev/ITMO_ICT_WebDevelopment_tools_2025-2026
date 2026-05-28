from typing import List, Optional

from sqlalchemy.orm import selectinload
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.team import Team, TeamMember
from app.schemas.team import TeamCreate


async def create_team(session: AsyncSession, team_in: TeamCreate) -> Team:
    team = Team.from_orm(team_in)
    session.add(team)
    await session.commit()
    await session.refresh(team)
    return team


async def get_team(session: AsyncSession, team_id: int) -> Optional[Team]:
    statement = select(Team).where(Team.id == team_id).options(
        selectinload(Team.members).selectinload(TeamMember.user)
    )
    result = await session.exec(statement)
    return result.one_or_none()


async def list_teams(session: AsyncSession, offset: int = 0, limit: int = 100) -> List[Team]:
    statement = select(Team).options(
        selectinload(Team.members).selectinload(TeamMember.user)
    ).offset(offset).limit(limit)
    result = await session.exec(statement)
    return result.all()


async def update_team(session: AsyncSession, team_id: int, name: str) -> Optional[Team]:
    team = await session.get(Team, team_id)
    if not team:
        return None
    team.name = name
    session.add(team)
    await session.commit()
    await session.refresh(team)
    return team


async def delete_team(session: AsyncSession, team_id: int) -> bool:
    team = await session.get(Team, team_id)
    if not team:
        return False
    session.delete(team)
    await session.commit()
    return True


async def join_team(session: AsyncSession, team_id: int, user_id: int, role_in_team: str) -> Optional[TeamMember]:
    team = await session.get(Team, team_id)
    if not team:
        return None
    statement = select(TeamMember).where(
        TeamMember.team_id == team_id,
        TeamMember.user_id == user_id,
    )
    result = await session.exec(statement)
    existing = result.one_or_none()
    if existing:
        return existing
    membership = TeamMember(team_id=team_id, user_id=user_id, role_in_team=role_in_team)
    session.add(membership)
    await session.commit()
    await session.refresh(membership)
    return membership
