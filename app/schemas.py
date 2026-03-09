from pydantic import BaseModel, EmailStr, field_validator
from datetime import datetime
from typing import Optional


# ─── Event Schemas ───────────────────────────────────────────

class EventBase(BaseModel):
    title: str
    description: Optional[str] = None
    location: Optional[str] = None
    start_time: datetime
    end_time: datetime
    max_capacity: int

    @field_validator("max_capacity")
    @classmethod
    def capacity_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError("max_capacity must be greater than 0")
        return v

    @field_validator("end_time")
    @classmethod
    def end_time_must_be_after_start(cls, v, info):
        if "start_time" in info.data and v <= info.data["start_time"]:
            raise ValueError("end_time must be after start_time")
        return v


class EventCreate(EventBase):
    pass


class EventUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    max_capacity: Optional[int] = None


class EventResponse(EventBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


# ─── Participant Schemas ──────────────────────────────────────

class ParticipantBase(BaseModel):
    name: str
    email: str


class ParticipantCreate(ParticipantBase):
    pass


class ParticipantResponse(ParticipantBase):
    id: int
    event_id: int
    registered_at: datetime

    model_config = {"from_attributes": True}