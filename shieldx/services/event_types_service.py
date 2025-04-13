from fastapi import HTTPException 
from shieldx.repositories.event_types_repository import EventTypeRepository
from shieldx.models.event_types import EventTypeModel


class EventTypeService:
    """
    Servicio encargado de gestionar la lógica relacionada con los tipos de evento (`EventType`),
    incluyendo su creación, consulta y eliminación.
    """

    def __init__(self, repository: EventTypeRepository):
        """
        Inicializa el servicio con una instancia del repositorio correspondiente.

        :param repository: Instancia de EventTypeRepository para interactuar con la base de datos.
        """
        self.repository = repository

    async def create_event_type(self, data: EventTypeModel) -> str:
        """
        Crea un nuevo tipo de evento en la base de datos.

        :param data: Objeto EventTypeModel con los datos del nuevo tipo de evento.
        :return: ID del tipo de evento creado.
        """
        return await self.repository.create(data.model_dump(by_alias=True, exclude_none=True))

    async def list_event_types(self):
        """
        Devuelve todos los tipos de evento registrados en la base de datos.

        :return: Lista de tipos de evento.
        """
        return await self.repository.get_all()

    async def get_event_type(self, event_type_id: str):
        """
        Recupera un tipo de evento específico por su ID.

        :param event_type_id: Identificador único del tipo de evento.
        :return: Objeto EventTypeModel si se encuentra, de lo contrario None.
        """
        result = await self.repository.get_by_id(event_type_id)

        if not result:
            raise HTTPException(status_code=404, detail="Event type not found")
        return result 
    

    async def delete_event_type(self, event_type_id: str):
        """
        Elimina un tipo de evento de la base de datos por su ID.

        :param event_type_id: Identificador único del tipo de evento a eliminar.
        """
        result = await self.repository.get_by_id(event_type_id)

        if not result:
            raise HTTPException(status_code=404, detail="Event type not found")
        await self.repository.delete(event_type_id)
