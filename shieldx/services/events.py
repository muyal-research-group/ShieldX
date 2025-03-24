from shieldx.models import EventModel
from shieldx.repositories import EventsRepository
from typing import List, Optional

class EventsService:
    def __init__(self, repository: EventsRepository):
        self.repository = repository

    async def create_event(self, event: EventModel) -> Optional[dict]:
        """
        Crea un evento en MongoDB y devuelve un diccionario con su ID.
        """
        created_event = await self.repository.create_event(event)

        if created_event:
            return {"event_id": str(created_event["_id"])}  # Devuelve solo el ID generado

        return None


    async def get_all_events(self) -> list[EventModel]:
        return await self.repository.find_all_events()
    
    async def get_events_filtered(
        self, service_id: Optional[str] = None, microservice_id: Optional[str] = None,
        function_id: Optional[str] = None, limit: int = 100, skip: int = 0
        ) -> List[EventModel]:
        """
        Obtiene eventos aplicando filtros dinámicos.
        """
        filters = {}
        if service_id:
            filters["service_id"] = service_id
        if microservice_id:
            filters["microservice_id"] = microservice_id
        if function_id:
            filters["function_id"] = function_id
        return await self.repository.find_events(filters, limit, skip)

    async def get_event_by_id(self, event_id: str) -> Optional[EventModel]:
        """
        Obtiene un evento específico por `event_id`.
        """
        return await self.repository.find_event_by_id(event_id)

    async def update_event(self, event_id: str, update_data: dict) -> Optional[EventModel]:
        """
        Actualiza un evento en la base de datos.
        """
        return await self.repository.update_event(event_id, update_data)

    async def delete_event(self, event_id: str) -> bool:
        """
        Elimina un evento de la base de datos.
        """
        return await self.repository.delete_event(event_id)
