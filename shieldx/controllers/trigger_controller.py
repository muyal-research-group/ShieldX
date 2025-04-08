from fastapi import APIRouter, Depends
from typing import List
from shieldx.models.trigger_models import TriggerModel
from shieldx.services.trigger_service import TriggerService
from shieldx.db import get_collection
from shieldx.repositories import TriggersRepository

router = APIRouter()


# Crea la instancia del servicio pasando la colección MongoDB
def get_triggers_service() -> TriggerService:
    collection = get_collection("triggers")  # nombre de la colección en tu DB
    repository = TriggersRepository(collection)
    return TriggerService(repository)


@router.post(
    "/triggers/",
    response_model=TriggerModel,
    response_model_by_alias=True,
    summary="Crear un nuevo trigger",
    description=(
        "Crea un nuevo trigger en la base de datos. "
        "El trigger debe incluir un nombre único y una regla (`RuleModel`) "
        "que contenga el `target` y un diccionario de `parameters`, definidos como `ParameterDetailModel`."
    ),
)
async def create_trigger(trigger: TriggerModel, service: TriggerService = Depends(get_triggers_service)):
    return await service.create_trigger(trigger)


@router.get(
    "/triggers/",
    response_model=List[TriggerModel],
    response_model_by_alias=True,
    summary="Obtener todos los triggers",
    description="Recupera todos los triggers almacenados en la base de datos."
)
async def get_all_triggers(service: TriggerService = Depends(get_triggers_service)):
    return await service.get_all_triggers()

@router.get(
    "/triggers/{name}",
    response_model=TriggerModel,
    response_model_by_alias=True,
    summary="Obtener un trigger por nombre",
    description="Devuelve un trigger específico dado su nombre único."
)
async def get_trigger(name: str, service: TriggerService = Depends(get_triggers_service)):
    return await service.get_trigger(name)

@router.put(
    "/triggers/{name}",
    response_model=TriggerModel,
    summary="Actualizar un trigger por nombre",
    description=(
        "Actualiza la definición completa de un trigger existente identificado por su nombre. "
        "Se debe enviar el objeto `TriggerModel` actualizado."
    )
)
async def update_trigger(name: str, updated_trigger: TriggerModel, service: TriggerService = Depends(get_triggers_service)):
    return await service.update_trigger(name, updated_trigger)

@router.delete(
    "/triggers/{name}",
    summary="Eliminar un trigger por nombre",
    description="Elimina un trigger de la base de datos según su nombre."
)
async def delete_trigger(name: str, service: TriggerService = Depends(get_triggers_service)):
    return await service.delete_trigger(name)