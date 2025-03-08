from fastapi import APIRouter, HTTPException, Depends
from typing import List
from shieldx.models import EventModel
from shieldx.services import EventsService
from shieldx.repositories import EventsRepository
from shieldx.db import get_collection
import os

router = APIRouter()

# Dependency: create a MongoDB client and initialize the repository and service.
def get_events_service() -> EventsService:
    collection = get_collection("events")
    repository = EventsRepository(collection)
    return EventsService(repository)

@router.post("/events", response_model=EventModel)
async def create_event(event: EventModel, events_service: EventsService = Depends(get_events_service)):
    created_event = await events_service.create_event(event)
    return created_event

@router.get("/events", response_model=List[EventModel])
async def get_events(events_service: EventsService = Depends(get_events_service)):
    events = await events_service.get_all_events()
    return events
