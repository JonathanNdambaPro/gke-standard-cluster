from pydantic import BaseModel, ConfigDict, Field


class EventInputModel(BaseModel):
    """Modèle d'entrée pour les endpoints (sans id généré automatiquement)."""

    name: str
    lastname: str


class EventModelV1(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id_: str = Field(..., alias="id", serialization_alias="id")
    name: str
    lastname: str
