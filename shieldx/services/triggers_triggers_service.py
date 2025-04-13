from shieldx.repositories.triggers_triggers_repository import TriggersTriggersRepository

class TriggersTriggersService:
    """
    Servicio encargado de gestionar la relación jerárquica entre triggers,
    permitiendo la vinculación de triggers padres e hijos mediante la colección `triggers_triggers`.
    """

    def __init__(self, repository: TriggersTriggersRepository):
        """
        Inicializa el servicio con una instancia del repositorio correspondiente.

        :param repository: Instancia de TriggersTriggersRepository para interactuar con la base de datos.
        """
        self.repository = repository

    async def link_triggers(self, parent_id: str, child_id: str):
        """
        Crea una relación de dependencia entre un trigger padre y un trigger hijo.

        :param parent_id: ID del trigger que actuará como padre.
        :param child_id: ID del trigger que actuará como hijo.
        :return: Resultado de la operación de enlace.
        """
        return await self.repository.link(parent_id, child_id)

    async def unlink_triggers(self, parent_id: str, child_id: str):
        """
        Elimina la relación entre un trigger padre y su trigger hijo.

        :param parent_id: ID del trigger padre.
        :param child_id: ID del trigger hijo.
        """
        await self.repository.unlink(parent_id, child_id)

    async def list_children(self, parent_id: str):
        """
        Lista todos los triggers hijos asociados a un trigger padre.

        :param parent_id: ID del trigger padre.
        :return: Lista de triggers hijos.
        """
        return await self.repository.get_children(parent_id)

    async def list_parents(self, child_id: str):
        """
        Lista todos los triggers padres asociados a un trigger hijo.

        :param child_id: ID del trigger hijo.
        :return: Lista de triggers padres.
        """
        return await self.repository.get_parents(child_id)
