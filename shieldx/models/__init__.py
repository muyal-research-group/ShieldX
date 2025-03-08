from pydantic import BaseModel
from typing import Optional, Any

class EncryptStart(BaseModel):
    function_id:str
    source:str
    sink: str


class EventModel(BaseModel):
    service_id: str
    microservice_id: str
    function_id: str
    event_type: str
    timestamp: float
    payload: Optional[Any] = None

