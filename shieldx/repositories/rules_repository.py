from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from shieldx.models.rule_models import RuleModel

class RuleRepository:
    """
    Repositorio encargado de realizar operaciones CRUD sobre la colección `rules`
    en la base de datos MongoDB.
    """

    def __init__(self, db: AsyncIOMotorDatabase):
        """
        Inicializa el repositorio seleccionando la colección `rules`.

        :param db: Instancia de la base de datos MongoDB.
        """
        self.collection = db["rules"]

    async def create(self, rule_data: dict) -> str:
        """
        Inserta una nueva regla en la colección.

        :param rule_data: Diccionario con los datos de la regla.
        :return: ID del documento insertado como cadena.
        """
        result = await self.collection.insert_one(rule_data)
        return str(result.inserted_id)

    async def get_all(self):
        """
        Recupera todas las reglas almacenadas en la base de datos.

        :return: Lista de objetos `RuleModel`.
        """
        return [RuleModel(**doc) async for doc in self.collection.find()]

    async def get_by_id(self, rule_id: str):
        """
        Recupera una regla específica por su ID.

        :param rule_id: ID del documento a consultar.
        :return: Objeto `RuleModel` si se encuentra, de lo contrario `None`.
        """
        doc = await self.collection.find_one({"_id": ObjectId(rule_id)})
        return RuleModel(**doc) if doc else None
    
    async def update(self, rule_id: str, rule_data: dict):
        """
        Actualiza una regla existente en la base de datos.

        :param rule_id: ID del documento a actualizar.
        :param rule_data: Diccionario con los campos que se deben actualizar.
        """
        await self.collection.update_one(
            {"_id": ObjectId(rule_id)},
            {"$set": rule_data}
        )

    async def delete(self, rule_id: str):
        """
        Elimina una regla de la base de datos por su ID.

        :param rule_id: ID del documento a eliminar.
        """
        await self.collection.delete_one({"_id": ObjectId(rule_id)})
