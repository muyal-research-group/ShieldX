from motor.motor_asyncio import AsyncIOMotorDatabase
from shieldx.models.rules_trigger import RulesTriggerModel

class RulesTriggerRepository:
    """
    Repositorio encargado de manejar la relación muchos-a-muchos entre triggers y reglas,
    utilizando la colección intermedia `rules_trigger`.
    """

    def __init__(self, db: AsyncIOMotorDatabase):
        """
        Inicializa el repositorio y selecciona la colección `rules_trigger`.

        :param db: Instancia de la base de datos MongoDB.
        """
        self.collection = db["rules_trigger"]

    async def link(self, trigger_id: str, rule_id: str):
        """
        Crea una relación entre un trigger y una regla si no existe previamente.

        :param trigger_id: ID del trigger.
        :param rule_id: ID de la regla.
        :return: Mensaje de confirmación.
        """
        exists = await self.collection.find_one({
            "trigger_id": trigger_id,
            "rule_id": rule_id
        })
        if not exists:
            await self.collection.insert_one({
                "trigger_id": trigger_id,
                "rule_id": rule_id
            })
        return {"message": "Linked"}

    async def unlink(self, trigger_id: str, rule_id: str):
        """
        Elimina la relación entre un trigger y una regla.

        :param trigger_id: ID del trigger.
        :param rule_id: ID de la regla.
        """
        await self.collection.delete_one({
            "trigger_id": trigger_id,
            "rule_id": rule_id
        })

    async def list_by_trigger(self, trigger_id: str):
        """
        Obtiene todas las reglas asociadas a un trigger específico.

        :param trigger_id: ID del trigger.
        :return: Lista de objetos `RulesTriggerModel`.
        """
        cursor = self.collection.find({"trigger_id": trigger_id})
        return [RulesTriggerModel(**doc) async for doc in cursor]
