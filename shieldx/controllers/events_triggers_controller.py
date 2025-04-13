from fastapi import APIRouter, Depends, HTTPException, status
from shieldx.services.events_triggers_service import EventsTriggersService
from shieldx.repositories.events_triggers_repository import EventsTriggersRepository
from shieldx.models.events_triggers import EventsTriggersModel
from shieldx.db import get_database

router = APIRouter()

def get_service(db=Depends(get_database)):
    repo = EventsTriggersRepository(db)
    return EventsTriggersService(repo)

@router.get(
    "/event-types/{event_type_id}/triggers",
    response_model=list[EventsTriggersModel],
    status_code=200,
    summary="Listar triggers de un tipo de evento",
    description="Devuelve todos los triggers vinculados al tipo de evento especificado."
)
async def list_triggers(event_type_id: str, service: EventsTriggersService = Depends(get_service)):
    return await service.list_triggers_for_event_type(event_type_id)

@router.post(
    "/event-types/{event_type_id}/triggers/{trigger_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Vincular trigger a tipo de evento",
    description="Asocia un trigger existente a un tipo de evento. Si ya existe la relación, no hace nada (idempotente)."
)
async def link_trigger(event_type_id: str, trigger_id: str, service: EventsTriggersService = Depends(get_service)):
    await service.link_trigger(event_type_id, trigger_id)

@router.put(
    "/event-types/{event_type_id}/triggers",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Reemplazar triggers de tipo de evento",
    description="Reemplaza completamente la lista de triggers asociados a un tipo de evento."
)
async def replace_triggers(event_type_id: str, trigger_ids: list[str], service: EventsTriggersService = Depends(get_service)):
    await service.replace_triggers_for_event_type(event_type_id, trigger_ids)

@router.delete(
    "/event-types/{event_type_id}/triggers/{trigger_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Desvincular trigger de tipo de evento",
    description="Elimina la relación entre un trigger y un tipo de evento. Si ya estaba desvinculado, también devuelve 204 (idempotente)."
)
async def unlink_trigger(event_type_id: str, trigger_id: str, service: EventsTriggersService = Depends(get_service)):
    await service.unlink_trigger(event_type_id, trigger_id)
