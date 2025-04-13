from shieldx.repositories.rules_trigger_repository import RulesTriggerRepository

class RulesTriggerService:
    """
    Servicio encargado de gestionar la relación entre triggers y reglas,
    utilizando la colección intermedia `rules_trigger` para vincular reglas a triggers.
    """

    def __init__(self, repository: RulesTriggerRepository):
        """
        Inicializa el servicio con una instancia del repositorio correspondiente.

        :param repository: Instancia de RulesTriggerRepository para interactuar con la base de datos.
        """
        self.repository = repository

    async def link_rule(self, trigger_id: str, rule_id: str):
        """
        Crea una asociación entre un trigger y una regla.

        :param trigger_id: ID del trigger.
        :param rule_id: ID de la regla que se desea vincular.
        :return: Resultado de la operación de enlace.
        """
        return await self.repository.link(trigger_id, rule_id)

    async def unlink_rule(self, trigger_id: str, rule_id: str):
        """
        Elimina la asociación entre una regla y un trigger.

        :param trigger_id: ID del trigger.
        :param rule_id: ID de la regla que se desea desvincular.
        """
        await self.repository.unlink(trigger_id, rule_id)

    async def list_rules(self, trigger_id: str):
        """
        Lista todas las reglas asociadas a un trigger específico.

        :param trigger_id: ID del trigger.
        :return: Lista de reglas asociadas.
        """
        return await self.repository.list_by_trigger(trigger_id)
