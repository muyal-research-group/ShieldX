from typing import ClassVar
from pydantic import BaseModel

class RulesTriggerModel(BaseModel):
    """
    Modelo que representa la relación entre un trigger y una regla.

    Esta entidad intermedia se utiliza para vincular un trigger con una regla específica,
    permitiendo que al activarse el trigger se ejecute la regla correspondiente.

    Atributos:
    - trigger_id: ID del trigger asociado.
    - rule_id: ID de la regla vinculada al trigger.
    """

    trigger_id: str
    rule_id: str

    model_config: ClassVar[dict] = {
        "json_schema_extra": {
            "example": {
                "trigger_id": "662018c50c9fba58a4fc1689",
                "rule_id": "662019dd2d132a9aa4fbe27b"
            }
        }
    }
