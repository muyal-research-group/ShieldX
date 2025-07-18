from typing import Any, Dict
from pydantic import BaseModel, Field

class RuleDTO(BaseModel):
    rule_id: str = Field(..., alias="_id")
    target: str
    parameters: Dict[str, Any]

    model_config = {
        "populate_by_name": True
    }