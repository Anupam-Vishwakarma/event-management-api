from sqlalchemy.orm import Session
from sqlalchemy import func
from app import models, schemas
from fastapi import HTTPException, status


# ─── Event CRUD ───────────────────────────────────────────────

def get_all_events(db: Session):
    return db.query(models.Event).all()


def get_event_by_id(db: Session, event_id: int):
    event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Event with id {event_id} not found"
        )
    return event


def create_event(db: Session, event: schemas.EventCreate):
    db_event = models.Event(**event.model_dump())
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event


def update_event(db: Session, event_id: int, event_data: schemas.EventUpdate):
    db_event = get_event_by_id(db, event_id)
    update_data = event_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_event, field, value)
    db.commit()
    db.refresh(db_event)
    return db_event


def delete_event(db: Session, event_id: int):
    db_event = get_event_by_id(db, event_id)
    db.delete(db_event)
    db.commit()
    return {"message": f"Event {event_id} deleted successfully"}


# ─── Participant CRUD ─────────────────────────────────────────

def register_participant(db: Session, event_id: int, participant: schemas.ParticipantCreate):
    db_event = get_event_by_id(db, event_id)

    # Check capacity
    current_count = db.query(func.count(models.Participant.id)).filter(
        models.Participant.event_id == event_id
    ).scalar()

    if current_count >= db_event.max_capacity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Event has reached maximum capacity"
        )

    # Check duplicate registration
    existing = db.query(models.Participant).filter(
        models.Participant.event_id == event_id,
        models.Participant.email == participant.email
    ).first()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This email is already registered for this event"
        )

    db_participant = models.Participant(event_id=event_id, **participant.model_dump())
    db.add(db_participant)
    db.commit()
    db.refresh(db_participant)
    return db_participant


def get_participants(db: Session, event_id: int):
    get_event_by_id(db, event_id)  # Validate event exists
    return db.query(models.Participant).filter(
        models.Participant.event_id == event_id
    ).all()