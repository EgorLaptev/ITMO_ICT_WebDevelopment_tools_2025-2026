from typing import List, Optional

from sqlalchemy.orm import selectinload
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.hackathon import Hackathon
from app.schemas.hackathon import HackathonBase, HackathonCreate


async def create_hackathon(session: AsyncSession, hackathon_in: HackathonCreate) -> Hackathon:
    hackathon = Hackathon.from_orm(hackathon_in)
    session.add(hackathon)
    await session.commit()
    await session.refresh(hackathon)
    return hackathon


async def get_hackathon(session: AsyncSession, hackathon_id: int) -> Optional[Hackathon]:
    statement = select(Hackathon).where(Hackathon.id == hackathon_id).options(
        selectinload(Hackathon.teams), selectinload(Hackathon.tasks)
    )
    result = await session.exec(statement)
    return result.one_or_none()


async def list_hackathons(session: AsyncSession, offset: int = 0, limit: int = 100) -> List[Hackathon]:
    statement = select(Hackathon).options(
        selectinload(Hackathon.teams), selectinload(Hackathon.tasks)
    ).offset(offset).limit(limit)
    result = await session.exec(statement)
    return result.all()


async def update_hackathon(session: AsyncSession, hackathon_id: int, hackathon_in: HackathonBase) -> Optional[Hackathon]:
    hackathon = await session.get(Hackathon, hackathon_id)
    if not hackathon:
        return None
    hackathon_data = hackathon_in.dict(exclude_unset=True)
    for key, value in hackathon_data.items():
        setattr(hackathon, key, value)
    session.add(hackathon)
    await session.commit()
    await session.refresh(hackathon)
    return hackathon


async def delete_hackathon(session: AsyncSession, hackathon_id: int) -> bool:
    hackathon = await session.get(Hackathon, hackathon_id)
    if not hackathon:
        return False
    session.delete(hackathon)
    await session.commit()
    return True
