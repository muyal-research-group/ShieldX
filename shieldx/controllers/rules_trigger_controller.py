from fastapi import APIRouter, Depends, status
from shieldx.db import get_database
from shieldx.services.rules_trigger_service import RulesTriggerService
from shieldx.repositories.rules_trigger_repository import RulesTriggerRepository
from shieldx.models.rules_trigger import RulesTriggerModel
from shieldx.models.rule_models import RuleModel
from shieldx.repositories.rules_repository import RuleRepository
from shieldx.services.rules_service import RuleService

router = APIRouter()

def get_service(db=Depends(get_database)):
    repo = RulesTriggerRepository(db)
    return RulesTriggerService(repo)

@router.get(
    "/triggers/{trigger_id}/rules",
    response_model=list[RulesTriggerModel],
    status_code=status.HTTP_200_OK,
    summary="Listar reglas asociadas a un trigger",
    description="Devuelve todas las reglas actualmente vinculadas a un trigger específico."
)
async def list_rules(trigger_id: str, service: RulesTriggerService = Depends(get_service)):
    return await service.list_rules(trigger_id)

@router.post(
    "/triggers/{trigger_id}/rules/{rule_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Vincular regla a trigger",
    description="Asocia una regla existente a un trigger específico. Si ya está vinculada, no hace nada (idempotente)."
)
async def link_rule(trigger_id: str, rule_id: str, service: RulesTriggerService = Depends(get_service)):
    await service.link_rule(trigger_id, rule_id)

@router.post(
    "/triggers/{trigger_id}/rules",
    response_model=str,
    status_code=status.HTTP_201_CREATED,
    summary="Crear y vincular una nueva regla",
    description=(
        "Crea una nueva regla a partir del cuerpo JSON enviado, y la vincula automáticamente al trigger indicado. "
        "Esto combina la creación de la regla y su asociación en un solo paso."
    )
)
async def create_and_link_rule(trigger_id: str, rule_data: RuleModel,
                                db=Depends(get_database)):
    rule_repo = RuleRepository(db)
    rule_service = RuleService(rule_repo)
    rule_id = await rule_service.create_rule(rule_data)

    repo = RulesTriggerRepository(db)
    service = RulesTriggerService(repo)
    await service.link_rule(trigger_id, rule_id)

    return rule_id

@router.delete(
    "/triggers/{trigger_id}/rules/{rule_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Desvincular regla de trigger",
    description="Elimina la relación entre una regla y un trigger. Si no existe la relación, no hace nada (idempotente)."
)
async def unlink_rule(trigger_id: str, rule_id: str, service: RulesTriggerService = Depends(get_service)):
    await service.unlink_rule(trigger_id, rule_id)
