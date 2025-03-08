from shieldx.models import EventModel
from shieldx.repositories import EventsRepository

class EventsService:
    def __init__(self, repository: EventsRepository):
        self.repository = repository

    async def create_event(self, event: EventModel) -> EventModel:
        return await self.repository.create_event(event)

    async def get_all_events(self) -> list[EventModel]:
        return await self.repository.find_all_events()