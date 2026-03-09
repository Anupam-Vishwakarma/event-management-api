from fastapi import FastAPI
from app.database import engine, Base
from app.routers import events, participants

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Event Management API",
    description="A REST API to manage events and participant registrations",
    version="1.0.0"
)

app.include_router(events.router)
app.include_router(participants.router)


@app.get("/", tags=["Health"])
def root():
    return {"message": "Event Management API is running!"}

