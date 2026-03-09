from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from app import crud, schemas
from app.database import get_db

router = APIRouter(
    prefix="/events",
    tags=["Events"]
)


@router.post("/", response_model=schemas.EventResponse, status_code=status.HTTP_201_CREATED)
def create_event(event: schemas.EventCreate, db: Session = Depends(get_db)):
    return crud.create_event(db, event)


@router.get("/", response_model=List[schemas.EventResponse])
def get_all_events(db: Session = Depends(get_db)):
    return crud.get_all_events(db)


@router.get("/{event_id}", response_model=schemas.EventResponse)
def get_event(event_id: int, db: Session = Depends(get_db)):
    return crud.get_event_by_id(db, event_id)


@router.put("/{event_id}", response_model=schemas.EventResponse)
def update_event(event_id: int, event: schemas.EventUpdate, db: Session = Depends(get_db)):
    return crud.update_event(db, event_id, event)


@router.delete("/{event_id}", status_code=status.HTTP_200_OK)
def delete_event(event_id: int, db: Session = Depends(get_db)):
    return crud.delete_event(db, event_id)