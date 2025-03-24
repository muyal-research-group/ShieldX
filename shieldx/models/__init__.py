from pydantic import BaseModel, Field
from typing import Optional, Any
from datetime import datetime

class EventModel(BaseModel):
    service_id: str
    microservice_id: str
    function_id: str
    event_type: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    payload: Optional[Any] = None

class EncryptStart(EventModel):
    """
    Evento específico para cuando se inicia el cifrado.
    """
    
    source: str = Field(..., title="Source of Data")  # De dónde vienen los datos
    sink: str = Field(..., title="Data Destination")  # Dónde se guardarán después de cifrarse


class EncryptDone(EventModel):
    """
    Evento que indica que el cifrado ha finalizado.
    """
    encrypted_file: str = Field(..., title="Encrypted File Path")


class SkmeansStart(EventModel):
    """
    Evento que indica que se inicia el clustering con SKMeans.
    """
    cluster_count: int = Field(..., title="Number of Clusters", ge=1)


class SkmeansDone(EventModel):
    """
    Evento que indica que el clustering ha finalizado.
    """
    output_data: str = Field(..., title="Path to Clustered Data")


class DecryptStart(EventModel):
    """
    Evento que indica que se inicia el descifrado.
    """
    encrypted_file: str = Field(..., title="Encrypted File Path")


class DecryptDone(EventModel):
    """
    Evento que indica que el descifrado ha finalizado.
    """
    decrypted_file: str = Field(..., title="Decrypted File Path")


class PlottingStart(EventModel):
    """
    Evento que indica que la visualización de datos ha comenzado.
    """
    visualization_type: str = Field(..., title="Type of Visualization")


class PlottingDone(EventModel):
    """
    Evento que indica que la visualización de datos ha finalizado.
    """
    graph_path: str = Field(..., title="Path to Generated Graph")