from motor.motor_asyncio import AsyncIOMotorCollection
from shieldx.models import EventModel
from typing import List, Optional
from pymongo.errors import PyMongoError
from bson import ObjectId

class EventsRepository:
    def __init__(self, collection: AsyncIOMotorCollection):
        self.collection = collection

    async def create_event(self, event: EventModel) -> Optional[dict]:
        """
        Almacena un nuevo evento en MongoDB y devuelve el `_id` generado.
        """
        event_dict = event.model_dump(exclude_unset=True)
        result = await self.collection.insert_one(event_dict)

        if result.inserted_id:
            event_dict["_id"] = str(result.inserted_id)  # Agregar el ID a la respuesta
            return event_dict  # Devuelve el diccionario con `_id`

        return None

    async def find_events(self, filters: dict, limit: int = 100, skip: int = 0) -> List[EventModel]:
        """
        Obtiene eventos aplicando filtros dinámicos.
        """
        events = []
        cursor = self.collection.find(filters).skip(skip).limit(limit)
        async for document in cursor:
            document["id"] = str(document["_id"])
            events.append(EventModel(**document))
        return events

    async def find_all_events(self) -> List[EventModel]:
        """
        Obtiene todos los eventos, con paginación.
        """
        events = []
        cursor = self.collection.find({})
        async for document in cursor:
            document["id"] = str(document["_id"])  # Convertir ObjectId a string
            events.append(EventModel(**document))
        return events

    async def find_events_by_service(self, service_id: str) -> List[EventModel]:
        """
        Obtiene eventos filtrados por `service_id`.
        """
        events = []
        cursor = self.collection.find({"service_id": service_id})
        async for document in cursor:
            document["id"] = str(document["_id"])
            events.append(EventModel(**document))
        return events

    async def find_events_by_microservice(self, microservice_id: str) -> List[EventModel]:
        """
        Obtiene eventos filtrados por `microservice_id`.
        """
        events = []
        cursor = self.collection.find({"microservice_id": microservice_id})
        async for document in cursor:
            document["id"] = str(document["_id"])
            events.append(EventModel(**document))
        return events

    async def find_events_by_function(self, function_id: str) -> List[EventModel]:
        """
        Obtiene eventos filtrados por `function_id`.
        """
        events = []
        cursor = self.collection.find({"function_id": function_id})
        async for document in cursor:
            document["id"] = str(document["_id"])
            events.append(EventModel(**document))
        return events

    async def delete_event(self, event_id: str) -> bool:
        """
        Elimina un evento por `event_id`.
        """
        try:
            result = await self.collection.delete_one({"_id": ObjectId(event_id)})
            return result.deleted_count > 0
        except PyMongoError as e:
            print(f"❌ Error al eliminar el evento: {e}")
            return False

    async def update_event(self, event_id: str, update_data: dict) -> Optional[EventModel]:
        """
        Actualiza un evento existente por su `event_id`.
        """
        try:
            result = await self.collection.find_one_and_update(
                {"_id": ObjectId(event_id)},
                {"$set": update_data},
                return_document=True
            )
            if result:
                result["id"] = str(result["_id"])
                return EventModel(**result)
            return None
        except PyMongoError as e:
            print(f"❌ Error al actualizar el evento: {e}")
            return None 