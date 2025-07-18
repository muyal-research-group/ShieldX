from pydantic import BaseModel

class TriggersTriggersDTO(BaseModel):
    trigger_parent_id: str
    trigger_child_id: str