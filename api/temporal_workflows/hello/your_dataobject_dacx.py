from pydantic import BaseModel


class YourParams(BaseModel):
    greeting: str
    name: str
