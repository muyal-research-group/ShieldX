from pydantic import BaseModel

class DeleteResultDTO(BaseModel):
    deleted: bool


class IDResponseDTO(BaseModel):
    id: str

class MessageWithIDDTO(BaseModel):
    message: str
    event_id: str

class MessageDTO(BaseModel):
    message: str