from typing import List, Optional

from sqlalchemy.orm import selectinload
from sqlmodel import Session, select

from app.models.hackathon import Hackathon
from app.schemas.hackathon import HackathonBase, HackathonCreate


def create_hackathon(session: Session, hackathon_in: HackathonCreate) -> Hackathon:
    hackathon = Hackathon.from_orm(hackathon_in)
    session.add(hackathon)
    session.commit()
    session.refresh(hackathon)
    return hackathon


def get_hackathon(session: Session, hackathon_id: int) -> Optional[Hackathon]:
    statement = select(Hackathon).where(Hackathon.id == hackathon_id).options(
        selectinload(Hackathon.teams), selectinload(Hackathon.tasks)
    )
    return session.exec(statement).one_or_none()


def list_hackathons(session: Session, offset: int = 0, limit: int = 100) -> List[Hackathon]:
    statement = select(Hackathon).options(
        selectinload(Hackathon.teams), selectinload(Hackathon.tasks)
    ).offset(offset).limit(limit)
    return session.exec(statement).all()


def update_hackathon(session: Session, hackathon_id: int, hackathon_in: HackathonBase) -> Optional[Hackathon]:
    hackathon = session.get(Hackathon, hackathon_id)
    if not hackathon:
        return None
    hackathon_data = hackathon_in.dict(exclude_unset=True)
    for key, value in hackathon_data.items():
        setattr(hackathon, key, value)
    session.add(hackathon)
    session.commit()
    session.refresh(hackathon)
    return hackathon


def delete_hackathon(session: Session, hackathon_id: int) -> bool:
    hackathon = session.get(Hackathon, hackathon_id)
    if not hackathon:
        return False
    session.delete(hackathon)
    session.commit()
    return True
