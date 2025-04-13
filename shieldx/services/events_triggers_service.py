from shieldx.repositories.events_triggers_repository import EventsTriggersRepository
from shieldx.models.events_triggers import EventsTriggersModel


class EventsTriggersService:
    """
    Servicio encargado de gestionar la relación entre tipos de evento (`EventType`) y triggers,
    utilizando una tabla intermedia (`events_triggers`) para manejar asociaciones M:N.
    """

    def __init__(self, repository: EventsTriggersRepository):
        """
        Inicializa el servicio con una instancia del repositorio correspondiente.

        :param repository: Instancia de EventsTriggersRepository para interactuar con la base de datos.
        """
        self.repository = repository

    async def link_trigger(self, event_type_id: str, trigger_id: str):
        """
        Vincula un trigger a un tipo de evento.

        :param event_type_id: ID del tipo de evento.
        :param trigger_id: ID del trigger que se desea asociar.
        :return: Resultado de la operación de enlace.
        """
        return await self.repository.link(event_type_id, trigger_id)

    async def unlink_trigger(self, event_type_id: str, trigger_id: str):
        """
        Desvincula un trigger previamente asociado a un tipo de evento.

        :param event_type_id: ID del tipo de evento.
        :param trigger_id: ID del trigger que se desea desvincular.
        """
        await self.repository.unlink(event_type_id, trigger_id)

    async def list_triggers_for_event_type(self, event_type_id: str):
        """
        Lista todos los triggers vinculados a un tipo de evento específico.

        :param event_type_id: ID del tipo de evento.
        :return: Lista de asociaciones EventTriggerModel.
        """
        return await self.repository.get_triggers_by_event_type(event_type_id)

    async def replace_triggers_for_event_type(self, event_type_id: str, trigger_ids: list[str]):
        """
        Reemplaza todos los triggers asociados a un tipo de evento por una nueva lista.

        :param event_type_id: ID del tipo de evento.
        :param trigger_ids: Lista de IDs de triggers que deben quedar asociados.
        """
        await self.repository.replace_links(event_type_id, trigger_ids)
