from fastapi import HTTPException
from shieldx.repositories.rules_repository import RuleRepository
from shieldx.models.rule_models import RuleModel

class RuleService:
    """
    Servicio encargado de gestionar la lógica relacionada con las reglas (`Rule`),
    incluyendo su creación, consulta, actualización y eliminación.
    """

    def __init__(self, repository: RuleRepository):
        """
        Inicializa el servicio con una instancia del repositorio correspondiente.

        :param repository: Instancia de RuleRepository para interactuar con la base de datos.
        """
        self.repository = repository

    async def create_rule(self, rule: RuleModel) -> str:
        """
        Crea una nueva regla en la base de datos.

        :param rule: Objeto RuleModel con los datos de la regla.
        :return: ID de la nueva regla creada.
        """
        return await self.repository.create(rule.model_dump(by_alias=True, exclude_none=True))

    async def list_rules(self):
        """
        Devuelve todas las reglas almacenadas en la base de datos.

        :return: Lista de objetos RuleModel.
        """
        return await self.repository.get_all()

    async def get_rule(self, rule_id: str):
        """
        Obtiene una regla específica a partir de su identificador único.

        :param rule_id: ID de la regla a consultar.
        :return: Objeto RuleModel si existe, de lo contrario None.
        """
        rule = await self.repository.get_by_id(rule_id)
        if not rule:
            raise HTTPException(status_code=404, detail="Rule not found")
        return rule
    
    async def update_rule(self, rule_id: str, rule: RuleModel):
        """
        Actualiza los datos de una regla existente.

        :param rule_id: ID de la regla a actualizar.
        :param rule: Objeto RuleModel con los datos actualizados.
        """
        await self.repository.update(rule_id, rule.model_dump(by_alias=True, exclude_none=True))

    async def delete_rule(self, rule_id: str):
        """
        Elimina una regla de la base de datos por su ID.

        :param rule_id: ID de la regla a eliminar.
        """
        rule = await self.repository.get_by_id(rule_id)
        if not rule:
            raise HTTPException(status_code=404, detail="Rule not found")
        await self.repository.delete(rule_id)
        
