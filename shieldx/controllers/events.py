from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List, Optional
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

# ✅ GET /events → Obtener todos los eventos con paginación
@router.get("/events", response_model=List[EventModel])
async def get_events(
    events_service: EventsService = Depends(get_events_service),
    service_id: Optional[str] = Query(None, description="Filtrar por service_id"),
    microservice_id: Optional[str] = Query(None, description="Filtrar por microservice_id"),
    function_id: Optional[str] = Query(None, description="Filtrar por function_id"),
    limit: int = Query(100, description="Cantidad máxima de eventos a devolver"),
    skip: int = Query(0, description="Número de eventos a omitir para paginación")
):
    events = await events_service.get_events_filtered(
        service_id=service_id, microservice_id=microservice_id,
        function_id=function_id, limit=limit, skip=skip
    )
    return events

# ✅ GET /events/service/{service_id} → Obtener eventos por service_id
@router.get("/events/service/{service_id}", response_model=List[EventModel])
async def get_events_by_service(service_id: str, events_service: EventsService = Depends(get_events_service)):
    return await events_service.get_events_filtered(service_id=service_id)

# ✅ GET /events/microservice/{microservice_id} → Obtener eventos por microservice_id
@router.get("/events/microservice/{microservice_id}", response_model=List[EventModel])
async def get_events_by_microservice(microservice_id: str, events_service: EventsService = Depends(get_events_service)):
    return await events_service.get_events_filtered(microservice_id=microservice_id)

# ✅ GET /events/function/{function_id} → Obtener eventos por function_id
@router.get("/events/function/{function_id}", response_model=List[EventModel])
async def get_events_by_function(function_id: str, events_service: EventsService = Depends(get_events_service)):
    return await events_service.get_events_filtered(function_id=function_id)

# ✅ GET /events/{event_id} → Obtener un evento por ID
@router.get("/events/{event_id}", response_model=EventModel)
async def get_event_by_id(event_id: str, events_service: EventsService = Depends(get_events_service)):
    event = await events_service.get_event_by_id(event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Evento no encontrado")
    return event

# (Opcional) ✅ POST /events → Crear un nuevo evento
@router.post("/events", response_model=dict)
async def create_event(event: EventModel, events_service: EventsService = Depends(get_events_service)):
    created_event = await events_service.create_event(event)

    if not created_event:
        raise HTTPException(status_code=500, detail="No se pudo crear el evento")

    return {"message": "Evento creado exitosamente", "event_id": created_event["event_id"]}




# (Opcional) ✅ PUT /events/{event_id} → Actualizar un evento
@router.put("/events/{event_id}", response_model=EventModel)
async def update_event(event_id: str, update_data: dict, events_service: EventsService = Depends(get_events_service)):
    updated_event = await events_service.update_event(event_id, update_data)
    if not updated_event:
        raise HTTPException(status_code=404, detail="No se pudo actualizar el evento")
    return updated_event

# (Opcional) ✅ DELETE /events/{event_id} → Eliminar un evento
@router.delete("/events/{event_id}")
async def delete_event(event_id: str, events_service: EventsService = Depends(get_events_service)):
    success = await events_service.delete_event(event_id)
    if not success:
        raise HTTPException(status_code=404, detail="No se pudo eliminar el evento")
    return {"message": "Evento eliminado"}