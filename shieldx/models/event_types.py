from pydantic import BaseModel, Field, field_validator
from datetime import datetime, timezone
from typing import Optional
from bson import ObjectId

class EventTypeModel(BaseModel):
    """
    Modelo que representa un tipo de evento dentro del sistema ShieldX.

    Este modelo permite categorizar los eventos generados por servicios y microservicios
    para facilitar su clasificación, monitoreo y análisis.

    Atributos:
    - event_type_id: Identificador único del tipo de evento (alias de `_id`, autogenerado por MongoDB).
    - event_type: Nombre o descripción del tipo de evento (ej. "EncryptStart", "SkmeansDone").
    - timestamp: Fecha y hora de creación del tipo de evento.
    """

    event_type_id: Optional[str] = Field(default=None, alias="_id")
    event_type: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    @field_validator("event_type_id", mode="before")
    def convert_object_id(cls, v):
        """
        Validador que convierte un ObjectId de MongoDB en una cadena de texto.

        :param v: Valor del campo `_id` recibido desde la base de datos.
        :return: Representación en string del ObjectId.
        """
        if isinstance(v, ObjectId):
            return str(v)
        return v

    model_config = {
        "populate_by_name": True,
        "json_encoders": {ObjectId: str}
    }
