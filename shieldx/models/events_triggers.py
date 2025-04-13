from pydantic import BaseModel
from typing import ClassVar

class EventsTriggersModel(BaseModel):
    """
    Modelo que representa la relación muchos-a-muchos entre tipos de evento (`EventType`)
    y triggers (`Trigger`) en el sistema ShieldX.

    Esta entidad intermedia permite vincular múltiples triggers a un mismo tipo de evento
    y viceversa.

    Atributos:
    - event_type_id: ID del tipo de evento (referencia a EventTypes).
    - trigger_id: ID del trigger asociado (referencia a Triggers).
    """

    event_type_id: str  # FK to EventTypes
    trigger_id: str     # FK to Triggers

    model_config: ClassVar[dict] = {
        "populate_by_name": True,
        "json_schema_extra": {
            "example": {
                "event_type_id": "661f8d933e3a2eac62cce7ad",
                "trigger_id": "66200e847a824ad0dbb622e1"
            }
        }
    }
