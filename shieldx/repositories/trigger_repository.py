from motor.motor_asyncio import AsyncIOMotorCollection
from typing import List, Optional
from pymongo.errors import PyMongoError
from bson import ObjectId
from shieldx.models.trigger_models import TriggerModel
from shieldx.log.logger_config import get_logger
import time as T


L = get_logger(__name__)  # Logger específico para este módulo



class TriggersRepository:
    """
    Repositorio encargado de realizar operaciones CRUD sobre la colección de `triggers`
    en MongoDB, incluyendo manejo de errores y conversión de ObjectId.
    """

    def __init__(self, collection: AsyncIOMotorCollection):
        """
        Inicializa el repositorio con una colección de MongoDB.

        :param collection: Colección `triggers` de la base de datos MongoDB.
        """
        self.collection = collection

    async def create_trigger(self, trigger: TriggerModel) -> Optional[dict]:
        """
        Inserta un nuevo trigger en la base de datos y registra el resultado en los logs.

        :param trigger: Objeto `TriggerModel` con los datos del nuevo trigger.
        :return: Diccionario del trigger insertado (incluyendo su `_id`), o `None` si falla.
        """
        t1 = T.time()  # Inicio del tiempo de ejecución
        try:
            trigger_dict = trigger.model_dump(by_alias=True, exclude_unset=True)
            result = await self.collection.insert_one(trigger_dict)
            if result.inserted_id:
                trigger_dict["_id"] = str(result.inserted_id)
                # Log de éxito
                L.info({
                    "event": "TRIGGER.CREATED",
                    "trigger_id": trigger_dict["_id"],
                    "time": T.time() - t1
                })
                return trigger_dict
            # Log si no se genera un ID (caso raro)
            L.warning({"event": "TRIGGER.CREATE.FAILED.NO_ID", 
                        "time": T.time() - t1})
            return None
        except PyMongoError as e:
            # Log de error
            L.error({"event": "TRIGGER.CREATE.ERROR", 
                    "error": str(e)})
            return None

    async def get_all_triggers(self) -> List[TriggerModel]:
        """
        Recupera todos los triggers almacenados en la base de datos y registra la operación.

        :return: Lista de objetos `TriggerModel`.
        """
        t1 = T.time()
        triggers = []
        try:
            cursor = self.collection.find({})
            async for document in cursor:
                document["id"] = str(document["_id"])
                triggers.append(TriggerModel(**document))
            # Log de depuración con número de resultados
            L.debug({
                "event": "TRIGGER.FETCH.ALL",
                "count": len(triggers),
                "time": T.time() - t1
            })
        except PyMongoError as e:
            # Log de error
            L.error({"event": "TRIGGER.FETCH.ALL.ERROR", 
                    "error": str(e)})
        return triggers

    async def get_trigger_by_name(self, name: str) -> Optional[TriggerModel]:
        """
        Obtiene un trigger específico por su nombre y registra la consulta.

        :param name: Nombre del trigger.
        :return: Objeto `TriggerModel` si existe, de lo contrario `None`.
        """
        t1 = T.time()
        try:
            document = await self.collection.find_one({"name": name})
            if document:
                document["id"] = str(document["_id"])
                # Log de éxito en la consulta
                L.debug({
                    "event": "TRIGGER.FETCH.BY_NAME",
                    "name": name,
                    "time": T.time() - t1
                })
                return TriggerModel(**document)
            else:
                # Log de advertencia si no se encuentra
                L.warning({
                    "event": "TRIGGER.NOT_FOUND",
                    "name": name,
                    "time": T.time() - t1
                })
                return None
        except PyMongoError as e:
            # Log de error
            L.error({"event": "TRIGGER.FETCH.BY_NAME.ERROR", 
                    "name": name, 
                    "error": str(e)})
            return None

    async def update_trigger(self, name: str, update_data: dict) -> Optional[TriggerModel]:
        """
        Actualiza un trigger existente según su nombre y registra el resultado.

        :param name: Nombre del trigger a actualizar.
        :param update_data: Diccionario con los campos a modificar.
        :return: Objeto `TriggerModel` actualizado o `None` si no se encuentra.
        """
        t1 = T.time()
        try:
            updated = await self.collection.find_one_and_update(
                {"name": name},
                {"$set": update_data},
                return_document=True
            )
            if updated:
                updated["id"] = str(updated["_id"])
                # Log de éxito
                L.info({
                    "event": "TRIGGER.UPDATED",
                    "name": name,
                    "time": T.time() - t1
                })
                return TriggerModel(**updated)
            else:
                # Log si no se encuentra el trigger
                L.warning({
                    "event": "TRIGGER.UPDATE.NOT_FOUND",
                    "name": name,
                    "time": T.time() - t1
                })
                return None
        except PyMongoError as e:
            # Log de error
            L.error({"event": "TRIGGER.UPDATE.ERROR", 
                    "name": name, 
                    "error": str(e)})
            return None

    async def delete_trigger(self, name: str) -> bool:
        """
        Elimina un trigger por su nombre y registra la operación.

        :param name: Nombre del trigger a eliminar.
        :return: `True` si fue eliminado correctamente, `False` si no se encontró o falló.
        """
        t1 = T.time()
        try:
            result = await self.collection.delete_one({"name": name})
            if result.deleted_count > 0:
                # Log de éxito
                L.info({
                    "event": "TRIGGER.DELETED",
                    "name": name,
                    "time": T.time() - t1
                })
                return True
            else:
                # Log si no se encuentra el trigger
                L.warning({
                    "event": "TRIGGER.DELETE.NOT_FOUND",
                    "name": name,
                    "time": T.time() - t1
                })
                return False
        except PyMongoError as e:
            # Log de error
            L.error({"event": "TRIGGER.DELETE.ERROR", 
                    "name": name, 
                    "error": str(e)})
            return False
