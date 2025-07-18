from pydantic import BaseModel, Field
from datetime import datetime, timezone

class EventTypeDTO(BaseModel):
    event_type_id: str = Field(alias="_id")
    event_type: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    model_config = {
        "populate_by_name": True,
        "serialization_config": {
            "use_aliases": True
        }
    }
