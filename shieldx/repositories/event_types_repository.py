from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from shieldx.models.event_types import EventTypeModel


class EventTypeRepository:
    """
    Repositorio responsable de realizar operaciones CRUD sobre la colección `event_types`
    en la base de datos MongoDB.
    """

    def __init__(self, db: AsyncIOMotorDatabase):
        """
        Inicializa el repositorio con la conexión a la base de datos y selecciona la colección `event_types`.

        :param db: Instancia de la base de datos MongoDB.
        """
        self.collection = db["event_types"]

    async def create(self, event_type: dict) -> str:
        """
        Inserta un nuevo documento en la colección `event_types`.

        :param event_type: Diccionario con los datos del tipo de evento.
        :return: ID del documento insertado como cadena.
        """
        result = await self.collection.insert_one(event_type)
        return str(result.inserted_id)

    async def get_all(self):
        """
        Recupera todos los tipos de evento almacenados en la colección.

        :return: Lista de objetos `EventTypeModel`.
        """
        return [EventTypeModel(**doc) async for doc in self.collection.find()]

    async def get_by_id(self, event_type_id: str):
        """
        Recupera un tipo de evento por su ID.

        :param event_type_id: ID del documento a consultar.
        :return: Objeto `EventTypeModel` si existe, de lo contrario `None`.
        """
        doc = await self.collection.find_one({"_id": ObjectId(event_type_id)})
        return EventTypeModel(**doc) if doc else None

    async def delete(self, event_type_id: str):
        """
        Elimina un tipo de evento por su ID.

        :param event_type_id: ID del documento a eliminar.
        """
        await self.collection.delete_one({"_id": ObjectId(event_type_id)})
