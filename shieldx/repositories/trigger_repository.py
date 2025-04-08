from motor.motor_asyncio import AsyncIOMotorCollection
from typing import List, Optional
from pymongo.errors import PyMongoError
from bson import ObjectId
from shieldx.models.trigger_models import TriggerModel

class TriggersRepository:
    def __init__(self, collection: AsyncIOMotorCollection):
        self.collection = collection

    async def create_trigger(self, trigger: TriggerModel) -> Optional[dict]:
        try:
            trigger_dict = trigger.model_dump(by_alias=True, exclude_unset=True)
            result = await self.collection.insert_one(trigger_dict)
            if result.inserted_id:
                trigger_dict["_id"] = str(result.inserted_id)
                return trigger_dict
            return None
        except PyMongoError as e:
            print(f"❌ Error al crear trigger: {e}")
            return None

    async def get_all_triggers(self) -> List[TriggerModel]:
        triggers = []
        cursor = self.collection.find({})
        async for document in cursor:
            document["id"] = str(document["_id"])
            triggers.append(TriggerModel(**document))
        return triggers

    async def get_trigger_by_name(self, name: str) -> Optional[TriggerModel]:
        document = await self.collection.find_one({"name": name})
        if document:
            document["id"] = str(document["_id"])
            return TriggerModel(**document)
        return None

    async def update_trigger(self, name: str, update_data: dict) -> Optional[TriggerModel]:
        try:
            updated = await self.collection.find_one_and_update(
                {"name": name},
                {"$set": update_data},
                return_document=True
            )
            if updated:
                updated["id"] = str(updated["_id"])
                return TriggerModel(**updated)
            return None
        except PyMongoError as e:
            print(f"❌ Error al actualizar trigger: {e}")
            return None

    async def delete_trigger(self, name: str) -> bool:
        try:
            result = await self.collection.delete_one({"name": name})
            return result.deleted_count > 0
        except PyMongoError as e:
            print(f"❌ Error al eliminar trigger: {e}")
            return False
