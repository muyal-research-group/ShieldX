from fastapi import APIRouter, Depends, status
from shieldx.db import get_database
from shieldx.services.triggers_triggers_service import TriggersTriggersService
from shieldx.repositories.triggers_triggers_repository import TriggersTriggersRepository
from shieldx.models.triggers_triggers import TriggersTriggersModel

router = APIRouter()

def get_service(db=Depends(get_database)):
    repo = TriggersTriggersRepository(db)
    return TriggersTriggersService(repo)

@router.get(
    "/triggers/{trigger_id}/children",
    response_model=list[TriggersTriggersModel],
    status_code=status.HTTP_200_OK,
    summary="Listar triggers hijos",
    description="Devuelve todos los triggers hijos que son activados por el trigger padre especificado."
)
async def list_children(trigger_id: str, service: TriggersTriggersService = Depends(get_service)):
    return await service.list_children(trigger_id)

@router.get(
    "/triggers/{trigger_id}/parents",
    response_model=list[TriggersTriggersModel],
    status_code=status.HTTP_200_OK,
    summary="Listar triggers padres",
    description="Devuelve todos los triggers padres que activan al trigger especificado como hijo."
)
async def list_parents(trigger_id: str, service: TriggersTriggersService = Depends(get_service)):
    return await service.list_parents(trigger_id)

@router.post(
    "/triggers/{parent_id}/children/{child_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Vincular trigger hijo a trigger padre",
    description="Asocia un trigger hijo a un trigger padre, estableciendo que cuando se active el padre, también se dispare el hijo. Idempotente."
)
async def link_triggers(parent_id: str, child_id: str, service: TriggersTriggersService = Depends(get_service)):
    await service.link_triggers(parent_id, child_id)

@router.delete(
    "/triggers/{parent_id}/children/{child_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Desvincular trigger hijo de trigger padre",
    description="Elimina la relación entre un trigger padre y un trigger hijo. Si ya estaba desvinculado, también responde 204 (idempotente)."
)
async def unlink_triggers(parent_id: str, child_id: str, service: TriggersTriggersService = Depends(get_service)):
    await service.unlink_triggers(parent_id, child_id)
