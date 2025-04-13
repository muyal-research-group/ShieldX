from pydantic import BaseModel, Field, field_validator, model_validator
from typing import Dict, Optional
from bson import ObjectId

class ParameterDetailModel(BaseModel):
    """
    Modelo que representa los detalles de un parámetro requerido por una función asociada a una regla.

    Atributos:
    - type_: Tipo de dato del parámetro (ej. "string", "int", "float", "bool").
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
    Modelo que representa una regla de ejecución utilizada para activar funciones dentro del sistema ShieldX.

    Cada regla está vinculada a un `trigger` y define el objetivo (`target`) de ejecución junto con
    los parámetros requeridos por la función a invocar.

    Atributos:
    - rule_id: Identificador único de la regla (alias de `_id`, generado por MongoDB).
    - target: Ruta completa del método o función a ejecutar.
    - parameters: Diccionario de parámetros requeridos, donde la clave es el nombre del parámetro
                    y el valor es un objeto `ParameterDetailModel`.
    """

    rule_id: Optional[str] = Field(default=None, alias="_id")
    target: str  
    parameters: Dict[str, ParameterDetailModel]

    @field_validator("rule_id", mode="before")
    def convert_object_id(cls, v):
        """
        Convierte un ObjectId de MongoDB en cadena de texto.

        :param v: Valor del campo `_id` recibido desde la base de datos.
        :return: Representación en string del ObjectId.
        """
        if isinstance(v, ObjectId):
            return str(v)
        return v

    @model_validator(mode="after")
    def validate_required_parameters(self) -> "RuleModel":
        """
        Valida que la regla tenga los parámetros obligatorios para el target indicado
        y que cada parámetro tenga un tipo válido.

        :return: Instancia validada de RuleModel.
        :raises ValueError: Si faltan parámetros requeridos o si el tipo no es válido.
        """
        required_by_target = {
            "s_security.cipher_ops.encrypt_data": [
                "source_bucket_id", "source_key", "sink_bucket_id", "sink_key", "security_level"
            ],
            "s_ml.ml_clustering.skmean": ["source_bucket_id", "source_key", "k"],
            "mictlanx.put": ["bucket_id", "key", "source_path", "replication_factor", "num_chunks"],
            "mictlanx.get": ["bucket_id", "key", "sink_path"]
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

    model_config = {
        "populate_by_name": True,
        "json_encoders": {ObjectId: str}
    }
