from pydantic import BaseModel
from typing import ClassVar
from datetime import datetime, timezone

class TriggersTriggersModel(BaseModel):
    """
    Modelo que representa la relación jerárquica entre triggers en el sistema ShieldX.

    Este modelo permite definir un flujo de activación entre triggers, donde uno actúa como
    padre (disparador) y el otro como hijo (activado).

    Atributos:
    - trigger_parent_id: ID del trigger que actúa como padre.
    - trigger_child_id: ID del trigger que actúa como hijo.
    """

    trigger_parent_id: str
    trigger_child_id: str

    model_config: ClassVar[dict] = {
        "json_schema_extra": {
            "example": {
                "trigger_parent_id": "661f9124aa3deebd71eaaa99",
                "trigger_child_id": "661f913faa3deebd71eaaabc"
            }
        }
    }
