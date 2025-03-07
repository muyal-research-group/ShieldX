from pydantic import BaseModel

class EncryptStart(BaseModel):
    function_id:str
    source:str
    sink: str
    