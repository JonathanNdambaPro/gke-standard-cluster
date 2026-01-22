from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    BUCKET_NAME: str = "event-driven"
    API_V1_STR: str = "/api/v1"
    GCP_PROJECT_ID: str = "dataascode"
    LOGFIRE_SECRET_NAME: str = "LOGFIRE_TOKEN_EVENT_DRIVEN_TEMPLATE"  # noqa: S105


settings = Settings()
