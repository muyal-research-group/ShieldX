from pydantic import BaseModel, Field
from typing import Optional, Any
from datetime import datetime, timezone

"""Modelos de Eventos"""

class EventModel(BaseModel):
    """
    Modelo base que representa un evento generado dentro del sistema ShieldX.

    Este modelo se utiliza para registrar la ejecución de funciones dentro de un microservicio
    y contiene información clave para su trazabilidad y procesamiento.

    Atributos:
    - service_id: Identificador del servicio que origina el evento.
    - microservice_id: Identificador del microservicio específico.
    - function_id: Identificador de la función involucrada.
    - event_type: Tipo de evento generado (por ejemplo, EncryptStart, SkmeansDone, etc.).
    - timestamp: Fecha y hora en la que ocurrió el evento (UTC por defecto).
    - payload: Carga útil opcional con datos adicionales del evento.
    """

    service_id: str
    microservice_id: str
    function_id: str
    event_type: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    payload: Optional[Any] = None
