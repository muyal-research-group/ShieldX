from pydantic import BaseModel, Field

class EventsTriggersDTO(BaseModel):
    event_type_id: str
    trigger_id: str


    model_config = {
        "populate_by_name": True,
        "from_attributes": True
    }