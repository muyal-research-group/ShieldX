from pydantic import BaseModel

class RulesTriggerDTO(BaseModel):
    rule_id: str
    trigger_id: str
