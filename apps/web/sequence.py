from pydantic import BaseModel

class SequenceResponse(BaseModel):
    name: str
    frames: str