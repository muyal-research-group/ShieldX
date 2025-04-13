from fastapi import APIRouter, Depends, HTTPException, status
from shieldx.db import get_database
from shieldx.models.rule_models import RuleModel
from shieldx.repositories.rules_repository import RuleRepository
from shieldx.services.rules_service import RuleService

router = APIRouter()

def get_service(db=Depends(get_database)):
    repository = RuleRepository(db)
    return RuleService(repository)

@router.post(
    "/rules",
    response_model=str,
    status_code=status.HTTP_201_CREATED,
    summary="Crear una nueva regla",
    description="Crea una regla nueva especificando el `target` a ejecutar y sus `parameters` correspondientes."
)
async def create_rule(data: RuleModel, service: RuleService = Depends(get_service)):
    return await service.create_rule(data)

@router.get(
    "/rules",
    response_model=list[RuleModel],
    status_code=status.HTTP_200_OK,
    summary="Listar todas las reglas",
    description="Devuelve una lista con todas las reglas existentes en la base de datos."
)
async def list_rules(service: RuleService = Depends(get_service)):
    return await service.list_rules()

@router.get(
    "/rules/{rule_id}",
    response_model=RuleModel,
    status_code=status.HTTP_200_OK,
    summary="Obtener una regla por ID",
    description="Recupera una regla específica utilizando su identificador único."
)
async def get_rule(rule_id: str, service: RuleService = Depends(get_service)):
    return await service.get_rule(rule_id)

@router.put(
    "/rules/{rule_id}",
    status_code=status.HTTP_200_OK,
    summary="Actualizar una regla existente",
    description="Actualiza completamente una regla mediante su ID. Se debe enviar el objeto `RuleModel` actualizado."
)
async def update_rule(rule_id: str, data: RuleModel, service: RuleService = Depends(get_service)):
    existing = await service.get_rule(rule_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Rule not found")
    await service.update_rule(rule_id, data)
    return {"message": "Rule updated"}

@router.delete(
    "/rules/{rule_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar una regla",
    description="Elimina de forma permanente una regla identificada por su ID."
)
async def delete_rule(rule_id: str, service: RuleService = Depends(get_service)):
    await service.delete_rule(rule_id)
