from motor.motor_asyncio import AsyncIOMotorCollection
from shieldx.models import EventModel

class EventsRepository:
    def __init__(self, collection: AsyncIOMotorCollection):
        self.collection = collection

    async def create_event(self, event: EventModel) -> EventModel:
        event_dict = event.model_dump(exclude_unset=True)
        result = await self.collection.insert_one(event_dict)
        event_dict["id"] = str(result.inserted_id)
        return EventModel(**event_dict)

    async def find_all_events(self) -> list[EventModel]:
        events = []
        cursor = self.collection.find({})
        async for document in cursor:
            # Convert MongoDB _id field to string if needed
            document["id"] = str(document.get("_id"))
            events.append(EventModel(**document))
        return events