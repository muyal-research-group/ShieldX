from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from shieldx.models.event_types import EventTypeModel
from shieldx.log.logger_config import get_logger
import time as T
from pymongo.errors import PyMongoError

L = get_logger(__name__)

class EventTypeRepository:
    """
    Repositorio responsable de realizar operaciones CRUD sobre la colección `event_types`
    en la base de datos MongoDB.
    """

    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db["event_types"]

    async def create(self, event_type: dict) -> str:
        """
        Inserta un nuevo documento en la colección `event_types`.
        """
        t1 = T.time()
        try:
            result = await self.collection.insert_one(event_type)
            event_type_id = str(result.inserted_id)
            L.info({
                "event": "EVENT_TYPE.CREATED",
                "event_type_id": event_type_id,
                "time": T.time() - t1
            })
            return event_type_id
        except PyMongoError as e:
            L.error({"event": "EVENT_TYPE.CREATE.ERROR", 
                    "error": str(e)})
            raise

    async def get_all(self):
        """
        Recupera todos los tipos de evento almacenados en la colección.
        """
        t1 = T.time()
        try:
            docs = [EventTypeModel(**doc) async for doc in self.collection.find()]
            L.debug({
                "event": "EVENT_TYPE.FETCH.ALL",
                "count": len(docs),
                "time": T.time() - t1
            })
            return docs
        except PyMongoError as e:
            L.error({"event": "EVENT_TYPE.FETCH.ALL.ERROR", 
                    "error": str(e)})
            return []
        
    async def get_by_name(self, name: str):
        """
        Recupera un tipo de evento por su nombre (event_type).
        """
        doc = await self.collection.find_one({"event_type": name})
        return EventTypeModel(**doc) if doc else None

    async def get_by_id(self, event_type_id: str):
        """
        Recupera un tipo de evento por su ID.
        """
        t1 = T.time()
        try:
            doc = await self.collection.find_one({"_id": ObjectId(event_type_id)})
            if doc:
                L.debug({
                    "event": "EVENT_TYPE.FETCH.BY_ID",
                    "event_type_id": event_type_id,
                    "time": T.time() - t1
                })
                return EventTypeModel(**doc)
            else:
                L.warning({
                    "event": "EVENT_TYPE.NOT_FOUND",
                    "event_type_id": event_type_id,
                    "time": T.time() - t1
                })
                return None
        except PyMongoError as e:
            L.error({"event": "EVENT_TYPE.FETCH.BY_ID.ERROR", 
                    "event_type_id": event_type_id, 
                    "error": str(e)})
            return None

    async def delete(self, event_type_id: str):
        """
        Elimina un tipo de evento por su ID.
        """
        t1 = T.time()
        try:
            result = await self.collection.delete_one({"_id": ObjectId(event_type_id)})
            if result.deleted_count > 0:
                L.info({
                    "event": "EVENT_TYPE.DELETED",
                    "event_type_id": event_type_id,
                    "time": T.time() - t1
                })
            else:
                L.warning({
                    "event": "EVENT_TYPE.DELETE.NOT_FOUND",
                    "event_type_id": event_type_id,
                    "time": T.time() - t1
                })
        except PyMongoError as e:
            L.error({"event": "EVENT_TYPE.DELETE.ERROR", 
                    "event_type_id": event_type_id, 
                    "error": str(e)})
