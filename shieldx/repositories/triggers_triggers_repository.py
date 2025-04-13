from motor.motor_asyncio import AsyncIOMotorDatabase
from shieldx.models.triggers_triggers import TriggersTriggersModel

class TriggersTriggersRepository:
    """
    Repositorio encargado de manejar relaciones jerárquicas entre triggers,
    representando conexiones de activación entre triggers padres e hijos
    mediante la colección `triggers_triggers`.
    """

    def __init__(self, db: AsyncIOMotorDatabase):
        """
        Inicializa el repositorio y selecciona la colección `triggers_triggers`.

        :param db: Instancia de la base de datos MongoDB.
        """
        self.collection = db["triggers_triggers"]

    async def link(self, parent_id: str, child_id: str):
        """
        Crea una relación de activación entre un trigger padre y un trigger hijo si no existe previamente.

        :param parent_id: ID del trigger que actúa como padre.
        :param child_id: ID del trigger que actúa como hijo.
        :return: Mensaje de confirmación o `None` si ya existía la relación.
        """
        exists = await self.collection.find_one({
            "trigger_parent_id": parent_id,
            "trigger_child_id": child_id
        })
        if exists:
            return None
        await self.collection.insert_one({
            "trigger_parent_id": parent_id,
            "trigger_child_id": child_id
        })
        return {"message": "Linked"}

    async def unlink(self, parent_id: str, child_id: str):
        """
        Elimina la relación entre un trigger padre y un trigger hijo.

        :param parent_id: ID del trigger padre.
        :param child_id: ID del trigger hijo.
        """
        await self.collection.delete_one({
            "trigger_parent_id": parent_id,
            "trigger_child_id": child_id
        })

    async def get_children(self, parent_id: str):
        """
        Obtiene todos los triggers hijos asociados a un trigger padre.

        :param parent_id: ID del trigger padre.
        :return: Lista de objetos `TriggersTriggersModel` representando las relaciones hijo.
        """
        cursor = self.collection.find({"trigger_parent_id": parent_id})
        return [TriggersTriggersModel(**doc) async for doc in cursor]

    async def get_parents(self, child_id: str):
        """
        Obtiene todos los triggers padres que activan a un trigger hijo.

        :param child_id: ID del trigger hijo.
        :return: Lista de objetos `TriggersTriggersModel` representando las relaciones padre.
        """
        cursor = self.collection.find({"trigger_child_id": child_id})
        return [TriggersTriggersModel(**doc) async for doc in cursor]
