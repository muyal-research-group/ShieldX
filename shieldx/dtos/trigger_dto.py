from pydantic import BaseModel, Field
from typing import Optional

class TriggerDTO(BaseModel):
    trigger_id: Optional[str] = Field(default=None, alias="_id")
    name: str


    model_config = {
        "populate_by_name": True
    }