from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from app import crud, schemas
from app.database import get_db

router = APIRouter(
    prefix="/events",
    tags=["Participants"]
)


@router.post("/{event_id}/register", response_model=schemas.ParticipantResponse,
             status_code=status.HTTP_201_CREATED)
def register_for_event(event_id: int, participant: schemas.ParticipantCreate,
                       db: Session = Depends(get_db)):
    return crud.register_participant(db, event_id, participant)


@router.get("/{event_id}/participants", response_model=List[schemas.ParticipantResponse])
def get_event_participants(event_id: int, db: Session = Depends(get_db)):
    return crud.get_participants(db, event_id)