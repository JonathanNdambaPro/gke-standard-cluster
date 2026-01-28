from pydantic import BaseModel, ConfigDict, Field


class EventModelV1(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id_: str = Field(..., alias="id", serialization_alias="id")
    name: str
    lastname: str
