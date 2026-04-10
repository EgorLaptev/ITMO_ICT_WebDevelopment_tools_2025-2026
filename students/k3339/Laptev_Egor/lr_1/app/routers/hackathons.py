from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from app.core.security import get_current_user, require_role
from app.database import get_session
from app.schemas.hackathon import HackathonCreate, HackathonRead
from app.services.hackathon_service import (
    create_hackathon,
    delete_hackathon,
    get_hackathon,
    list_hackathons,
    update_hackathon,
)

router = APIRouter(tags=["hackathons"])


@router.get("/", response_model=List[HackathonRead])
def read_hackathons(session: Session = Depends(get_session)) -> List[HackathonRead]:
    return list_hackathons(session)


@router.post("/", response_model=HackathonRead)
def create_hackathon_route(
    hackathon_in: HackathonCreate,
    session: Session = Depends(get_session),
    current_user=Depends(require_role("organizer")),
) -> HackathonRead:
    return create_hackathon(session, hackathon_in)


@router.get("/{hackathon_id}", response_model=HackathonRead)
def read_hackathon(hackathon_id: int, session: Session = Depends(get_session)) -> HackathonRead:
    hackathon = get_hackathon(session, hackathon_id)
    if not hackathon:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hackathon not found")
    return hackathon


@router.put("/{hackathon_id}", response_model=HackathonRead)
def update_hackathon_route(
    hackathon_id: int,
    hackathon_in: HackathonCreate,
    session: Session = Depends(get_session),
    current_user=Depends(require_role("organizer")),
) -> HackathonRead:
    updated = update_hackathon(session, hackathon_id, hackathon_in)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hackathon not found")
    return updated


@router.delete("/{hackathon_id}")
def delete_hackathon_route(
    hackathon_id: int,
    session: Session = Depends(get_session),
    current_user=Depends(require_role("organizer")),
) -> dict:
    success = delete_hackathon(session, hackathon_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hackathon not found")
    return {"ok": True}
