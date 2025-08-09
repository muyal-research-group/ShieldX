from motor.motor_asyncio import AsyncIOMotorDatabase
from shieldx.models import EventTypeModel
from shieldx.log.logger_config import get_logger
import time as T
from shieldx.repositories import BaseRepository

L = get_logger(__name__)

class EventTypeRepository(BaseRepository[EventTypeModel]):
    """
    Repositorio responsable de realizar operaciones CRUD sobre la colección `event_types`
    en la base de datos MongoDB.
    """

    def __init__(self, db: AsyncIOMotorDatabase):
        super().__init__(collection=db["event_types"], model=EventTypeModel)
        
    async def get_by_name(self, name: str):
        """
        Recupera un tipo de evento por su nombre (event_type).
        """
        doc = await self.collection.find_one({"event_type": name})
        return EventTypeModel(**doc) if doc else None

