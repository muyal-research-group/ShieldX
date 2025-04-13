from motor.motor_asyncio import AsyncIOMotorCollection
from typing import List, Optional
from pymongo.errors import PyMongoError
from bson import ObjectId
from shieldx.models.trigger_models import TriggerModel

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
        Inserta un nuevo trigger en la base de datos.

        :param trigger: Objeto `TriggerModel` con los datos del nuevo trigger.
        :return: Diccionario del trigger insertado (incluyendo su `_id`), o `None` si falla.
        """
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
        """
        Recupera todos los triggers almacenados en la base de datos.

        :return: Lista de objetos `TriggerModel`.
        """
        triggers = []
        cursor = self.collection.find({})
        async for document in cursor:
            document["id"] = str(document["_id"])
            triggers.append(TriggerModel(**document))
        return triggers

    async def get_trigger_by_name(self, name: str) -> Optional[TriggerModel]:
        """
        Obtiene un trigger específico por su nombre.

        :param name: Nombre del trigger.
        :return: Objeto `TriggerModel` si existe, de lo contrario `None`.
        """
        document = await self.collection.find_one({"name": name})
        if document:
            document["id"] = str(document["_id"])
            return TriggerModel(**document)
        return None

    async def update_trigger(self, name: str, update_data: dict) -> Optional[TriggerModel]:
        """
        Actualiza un trigger existente según su nombre.

        :param name: Nombre del trigger a actualizar.
        :param update_data: Diccionario con los campos a modificar.
        :return: Objeto `TriggerModel` actualizado o `None` si falla.
        """
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
        """
        Elimina un trigger por su nombre.

        :param name: Nombre del trigger a eliminar.
        :return: `True` si fue eliminado correctamente, `False` si no se encontró o falló.
        """
        try:
            result = await self.collection.delete_one({"name": name})
            return result.deleted_count > 0
        except PyMongoError as e:
            print(f"❌ Error al eliminar trigger: {e}")
            return False
