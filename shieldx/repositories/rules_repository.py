from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from shieldx.models.rule_models import RuleModel
from shieldx.log.logger_config import get_logger
import time as T
import os
from pymongo.errors import PyMongoError

L = get_logger(__name__)

class RuleRepository:
    """
    Repositorio encargado de realizar operaciones CRUD sobre la colección `rules`
    en la base de datos MongoDB.
    """

    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db["rules"]

    async def create(self, rule_data: dict) -> str:
        """
        Inserta una nueva regla en la colección.
        """
        t1 = T.time()
        try:
            result = await self.collection.insert_one(rule_data)
            rule_id = str(result.inserted_id)
            L.info({
                "event": "RULE.CREATED",
                "rule_id": rule_id,
                "time": T.time() - t1
            })
            return rule_id
        except PyMongoError as e:
            L.error({"event": "RULE.CREATE.ERROR", 
                    "error": str(e)})
            raise

    async def get_all(self):
        """
        Recupera todas las reglas almacenadas en la base de datos.
        """
        t1 = T.time()
        try:
            docs = [RuleModel(**doc) async for doc in self.collection.find()]
            L.debug({
                "event": "RULE.FETCH.ALL",
                "count": len(docs),
                "time": T.time() - t1
            })
            return docs
        except PyMongoError as e:
            L.error({"event": "RULE.FETCH.ALL.ERROR", 
                    "error": str(e)})
            return []

    async def get_by_id(self, rule_id: str):
        """
        Recupera una regla específica por su ID.
        """
        t1 = T.time()
        try:
            doc = await self.collection.find_one({"_id": ObjectId(rule_id)})
            if doc:
                L.debug({
                    "event": "RULE.FETCH.BY_ID",
                    "rule_id": rule_id,
                    "time": T.time() - t1
                })
                return RuleModel(**doc)
            else:
                L.warning({
                    "event": "RULE.NOT_FOUND",
                    "rule_id": rule_id,
                    "time": T.time() - t1
                })
                return None
        except PyMongoError as e:
            L.error({"event": "RULE.FETCH.BY_ID.ERROR", 
                    "rule_id": rule_id, 
                    "error": str(e)})
            return None

    async def update(self, rule_id: str, rule_data: dict):
        """
        Actualiza una regla existente en la base de datos.
        """
        t1 = T.time()
        try:
            result = await self.collection.update_one(
                {"_id": ObjectId(rule_id)},
                {"$set": rule_data}
            )
            if result.modified_count > 0:
                L.info({
                    "event": "RULE.UPDATED",
                    "rule_id": rule_id,
                    "time": T.time() - t1
                })
            else:
                L.warning({
                    "event": "RULE.UPDATE.NO_CHANGE",
                    "rule_id": rule_id,
                    "time": T.time() - t1
                })
        except PyMongoError as e:
            L.error({"event": "RULE.UPDATE.ERROR", 
                    "rule_id": rule_id, 
                    "error": str(e)})

    async def delete(self, rule_id: str):
        """
        Elimina una regla de la base de datos por su ID.
        """
        t1 = T.time()
        try:
            result = await self.collection.delete_one({"_id": ObjectId(rule_id)})
            if result.deleted_count > 0:
                L.info({
                    "event": "RULE.DELETED",
                    "rule_id": rule_id,
                    "time": T.time() - t1
                })
            else:
                L.warning({
                    "event": "RULE.DELETE.NOT_FOUND",
                    "rule_id": rule_id,
                    "time": T.time() - t1
                })
        except PyMongoError as e:
            L.error({"event": "RULE.DELETE.ERROR", 
                    "rule_id": rule_id, 
                    "error": str(e)})
