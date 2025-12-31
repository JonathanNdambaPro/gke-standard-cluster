from pydantic import BaseModel, Field


class EventModelV1(BaseModel):
    id_: str = Field(..., alias="id", serialization_alias="id")
    name: str
    lastname: str
