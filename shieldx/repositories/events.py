from motor.motor_asyncio import AsyncIOMotorDatabase
from shieldx.models import EventModel
from typing import List, Optional
from pymongo.errors import PyMongoError
from bson import ObjectId
from shieldx.log.logger_config import get_logger
import time as T


L = get_logger(__name__)  # Logger con nombre del módulo



class EventsRepository:


    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db["events"]

    async def create_event(self, event: EventModel) -> Optional[dict]:
        """
        Almacena un nuevo evento en MongoDB y devuelve el `_id` generado.
        """
        t1 = T.time()
        try:
            event_dict = event.model_dump(exclude_unset=True)
            result = await self.collection.insert_one(event_dict)

            if result.inserted_id:
                event_dict["_id"] = str(result.inserted_id)
                L.info({
                    "event": "EVENT.CREATED",
                    "event_id": event_dict["_id"],
                    "time": T.time() - t1
                })
                return event_dict

            L.warning({"event": "EVENT.CREATE.FAILED.NO_ID", "time": T.time() - t1})
            return None
        except PyMongoError as e:
            L.error({"event": "EVENT.CREATE.ERROR", 
                    "error": str(e)})
            return None
        

    async def find_events(self, filters: dict, limit: int = 100, skip: int = 0) -> List[EventModel]:
        """
        Obtiene eventos aplicando filtros dinámicos.
        """
        t1 = T.time()
        events = []
        try:
            cursor = self.collection.find(filters).skip(skip).limit(limit)
            async for document in cursor:
                document["id"] = str(document["_id"])
                events.append(EventModel(**document))
            L.debug({
                "event": "EVENT.SEARCH",
                "filters": filters,
                "count": len(events),
                "time": T.time() - t1
            })
        except PyMongoError as e:
            L.error({"event": "EVENT.SEARCH.ERROR", 
                    "error": str(e)})
        return events

    async def find_all_events(self) -> List[EventModel]:
        """
        Obtiene todos los eventos, con paginación.
        """
        t1 = T.time()
        events = []
        try:
            cursor = self.collection.find({})
            async for document in cursor:
                document["id"] = str(document["_id"])
                events.append(EventModel(**document))
            L.debug({
                "event": "EVENTS.FETCH.ALL",
                "count": len(events),
                "time": T.time() - t1
            })
        except Exception as e:
            L.error({"event": "EVENTS.FETCH.ALL.ERROR", 
                    "error": str(e)})
        return events

    async def find_events_by_service(self, service_id: str) -> List[EventModel]:
        """
        Obtiene eventos filtrados por `service_id`.
        """
        t1 = T.time()
        events = []
        try:
            cursor = self.collection.find({"service_id": service_id})
            async for document in cursor:
                document["id"] = str(document["_id"])
                events.append(EventModel(**document))
            L.debug({
                "event": "EVENTS.FETCH.BY_SERVICE",
                "service_id": service_id,
                "count": len(events),
                "time": T.time() - t1
            })
        except Exception as e:
            L.error({"event": "EVENTS.FETCH.BY_SERVICE.ERROR", 
                    "service_id": service_id, 
                    "error": str(e)})
        return events
    
    async def find_events_by_microservice(self, microservice_id: str) -> List[EventModel]:
        """
        Obtiene eventos filtrados por `microservice_id`.
        """
        t1 = T.time()
        events = []
        try:
            cursor = self.collection.find({"microservice_id": microservice_id})
            async for document in cursor:
                document["id"] = str(document["_id"])
                events.append(EventModel(**document))
            L.debug({
                "event": "EVENTS.FETCH.BY_MICROSERVICE",
                "microservice_id": microservice_id,
                "count": len(events),
                "time": T.time() - t1
            })
        except Exception as e:
            L.error({"event": "EVENTS.FETCH.BY_MICROSERVICE.ERROR", 
                    "microservice_id": microservice_id,
                    "error": str(e)})
        return events
    
    async def find_events_by_function(self, function_id: str) -> List[EventModel]:
        """
        Obtiene eventos filtrados por `function_id`.
        """
        t1 = T.time()
        events = []
        try:
            cursor = self.collection.find({"function_id": function_id})
            async for document in cursor:
                document["id"] = str(document["_id"])
                events.append(EventModel(**document))
            L.debug({
                "event": "EVENTS.FETCH.BY_FUNCTION",
                "function_id": function_id,
                "count": len(events),
                "time": T.time() - t1
            })
        except Exception as e:
            L.error({"event": "EVENTS.FETCH.BY_FUNCTION.ERROR", 
                    "function_id": function_id, 
                    "error": str(e)})
        return events
    

    async def delete_event(self, event_id: str) -> bool:
        """
        Elimina un evento por `event_id`.
        """
        t1 = T.time()
        try:
            result = await self.collection.delete_one({"_id": ObjectId(event_id)})
            if result.deleted_count > 0:
                L.info({
                    "event": "EVENT.DELETED",
                    "event_id": event_id,
                    "time": T.time() - t1
                })
                return True
            else:
                L.warning({
                    "event": "EVENT.DELETE.NOT_FOUND",
                    "event_id": event_id,
                    "time": T.time() - t1
                })
                return False
        except PyMongoError as e:
            L.error({"event": "EVENT.DELETE.ERROR", 
                    "event_id": event_id, 
                    "error": str(e)})
            return False

    async def update_event(self, event_id: str, update_data: dict) -> Optional[EventModel]:
        t1 = T.time()
        try:
            result = await self.collection.find_one_and_update(
                {"_id": ObjectId(event_id)},
                {"$set": update_data},
                return_document=True
            )
            if result:
                result["id"] = str(result["_id"])
                L.info({
                    "event": "EVENT.UPDATED",
                    "event_id": result["id"],
                    "time": T.time() - t1
                })
                return EventModel(**result)
            else:
                L.warning({
                    "event": "EVENT.UPDATE.NOT_FOUND",
                    "event_id": event_id,
                    "time": T.time() - t1
                })
                return None
        except PyMongoError as e:
            L.error({"event": "EVENT.UPDATE.ERROR", 
                    "event_id": event_id, 
                    "error": str(e)})
            return None


