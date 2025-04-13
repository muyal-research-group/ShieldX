from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from shieldx.models.events_triggers import EventsTriggersModel

class EventsTriggersRepository:
    """
    Repositorio encargado de manejar la relación muchos-a-muchos entre tipos de evento (`EventType`)
    y triggers, usando la colección `events_triggers`.
    """

    def __init__(self, db: AsyncIOMotorDatabase):
        """
        Inicializa el repositorio seleccionando la colección `events_triggers`.

        :param db: Instancia de la base de datos MongoDB.
        """
        self.collection = db["events_triggers"]

    async def link(self, event_type_id: str, trigger_id: str):
        """
        Crea una relación entre un tipo de evento y un trigger si no existe previamente.

        :param event_type_id: ID del tipo de evento.
        :param trigger_id: ID del trigger.
        :return: Mensaje de confirmación o None si ya existía.
        """
        exists = await self.collection.find_one({
            "event_type_id": event_type_id,
            "trigger_id": trigger_id
        })
        if exists:
            return None
        await self.collection.insert_one({
            "event_type_id": event_type_id,
            "trigger_id": trigger_id
        })
        return {"message": "Linked"}

    async def unlink(self, event_type_id: str, trigger_id: str):
        """
        Elimina la relación entre un tipo de evento y un trigger.

        :param event_type_id: ID del tipo de evento.
        :param trigger_id: ID del trigger.
        """
        await self.collection.delete_one({
            "event_type_id": event_type_id,
            "trigger_id": trigger_id
        })

    async def get_triggers_by_event_type(self, event_type_id: str):
        """
        Obtiene todos los triggers vinculados a un tipo de evento específico.

        :param event_type_id: ID del tipo de evento.
        :return: Lista de objetos `EventsTriggersModel`.
        """
        cursor = self.collection.find({"event_type_id": event_type_id})
        return [EventsTriggersModel(**doc) async for doc in cursor]

    async def replace_links(self, event_type_id: str, triggers: list[str]):
        """
        Reemplaza todos los triggers asociados a un tipo de evento por una nueva lista.

        :param event_type_id: ID del tipo de evento.
        :param triggers: Lista de IDs de triggers que deben vincularse.
        """
        await self.collection.delete_many({"event_type_id": event_type_id})
        docs = [{"event_type_id": event_type_id, "trigger_id": t} for t in triggers]
        if docs:
            await self.collection.insert_many(docs)
