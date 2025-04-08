from pydantic import BaseModel, Field, model_validator
from typing import Dict, List

""" Modelos de Trigger y Rule """

class ParameterDetailModel(BaseModel):
    """
    Representa los detalles de un parámetro necesario para ejecutar una función.

    Atributos:
    - type_: Tipo del parámetro (por ejemplo, "string", "int"). Se mapea desde la clave 'type' del YAML.
    - description: Descripción textual del propósito del parámetro.
    """
    type_: str = Field(..., alias="type")
    description: str

    model_config = {
        "populate_by_name": True,
        "from_attributes": True,
        "json_schema_extra": {
            "examples": [
                {"type": "string", "description": "ID del bucket origen"}
            ]
        }
    }

class RuleModel(BaseModel):
    """
    Define una regla de ejecución que se activa mediante un trigger.

    Atributos:
    - target: Identificador completo de la función a ejecutar (e.g., "mictlanx.get").
    - parameters: Diccionario de parámetros requeridos por la función, donde cada clave es el nombre del parámetro
                y su valor es un objeto `ParameterDetailModel` con tipo y descripción.
    """
    target: str
    parameters: Dict[str, ParameterDetailModel]

    @model_validator(mode="after")
    def validate_required_parameters(self) -> "RuleModel":
        """
        Valida que se incluyan los parámetros requeridos por target y que los tipos sean válidos.
        """
        required_by_target = {
            "s_security.cipher_ops.encrypt_data": [
                "source_bucket_id", "source_key", "sink_bucket_id", "sink_key", "security_level"
            ],
            "s_ml.ml_clustering.skmean": [
                "source_bucket_id", "source_key", "k"
            ],
            "mictlanx.put": [
                "bucket_id", "key", "source_path", "replication_factor", "num_chunks"
            ],
            "mictlanx.get": [
                "bucket_id", "key", "sink_path"
            ]
        }

        expected = required_by_target.get(self.target)
        if expected:
            missing = [param for param in expected if param not in self.parameters]
            if missing:
                raise ValueError(f"El target '{self.target}' requiere los siguientes parámetros: {missing}")

        valid_types = {"string", "int", "float", "bool"}
        for key, param in self.parameters.items():
            if param.type_ not in valid_types:
                raise ValueError(f"Parámetro '{key}' tiene un tipo no válido: '{param.type_}'")

        return self

class TriggerModel(BaseModel):
    """
    Representa un trigger que activa una regla.

    Atributos:
    - name: Nombre único del trigger.
    - rule: Objeto `RuleModel` que especifica la función objetivo y sus parámetros requeridos.
    """
    name: str
    rule: RuleModel

class PolicyTriggersModel(BaseModel):
    """
    Contenedor general de todos los triggers definidos en una política.

    Atributos:
    - triggers: Lista de objetos `TriggerModel`, cada uno representando un disparador independiente.
    """
    triggers: List[TriggerModel]