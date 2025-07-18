from pydantic import BaseModel, Field
from typing import Any, Optional
from datetime import datetime

class EventDTO(BaseModel):
    
    service_id: str
    microservice_id: str
    function_id: str
    event_type: str
    payload: Optional[Any] = None
    timestamp: datetime

    model_config = {
        "populate_by_name": True,
        "from_attributes": True  # <- permite convertir desde EventModel sin usar .dict()
    }