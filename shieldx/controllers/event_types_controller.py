from fastapi import APIRouter, Depends, status
from shieldx.services.event_types_service import EventTypeService
from shieldx.repositories.event_types_repository import EventTypeRepository
from shieldx.models.event_types import EventTypeModel
from shieldx.db import get_database

router = APIRouter()

def get_service(db=Depends(get_database)):
    repository = EventTypeRepository(db)
    return EventTypeService(repository)

@router.post(
    "/event-types",
    response_model=str,
    status_code=status.HTTP_201_CREATED,
    summary="Crear un tipo de evento",
    description="Crea un nuevo tipo de evento que podrá ser asociado a uno o más triggers."
)
async def create_event_type(data: EventTypeModel, service: EventTypeService = Depends(get_service)):
    return await service.create_event_type(data)

@router.get(
    "/event-types",
    response_model=list[EventTypeModel],
    status_code=status.HTTP_200_OK,
    summary="Listar tipos de evento",
    description="Devuelve todos los tipos de evento registrados en el sistema."
)
async def list_event_types(service: EventTypeService = Depends(get_service)):
    return await service.list_event_types()

@router.get(
    "/event-types/{type_id}",
    response_model=EventTypeModel,
    status_code=status.HTTP_200_OK,
    summary="Obtener tipo de evento por ID",
    description="Obtiene un tipo de evento específico mediante su identificador único."
)
async def get_event_type(type_id: str, service: EventTypeService = Depends(get_service)):
    return await service.get_event_type(type_id)

@router.delete(
    "/event-types/{type_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar un tipo de evento",
    description="Elimina de forma permanente un tipo de evento según su identificador."
)
async def delete_event_type(type_id: str, service: EventTypeService = Depends(get_service)):
    await service.delete_event_type(type_id)
