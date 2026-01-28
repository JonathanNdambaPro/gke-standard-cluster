from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings

from api.utils.secrets import get_secret_from_gcp

load_dotenv()


class Settings(BaseSettings):
    BUCKET_NAME: str = "event-driven"
    API_V1_STR: str = "/api/v1"
    GCP_PROJECT_ID: str = "dataascode"
    LOGFIRE_TOKEN: str = Field(
        default_factory=lambda: get_secret_from_gcp(
            project_id="dataascode",
            secret_name="LOGFIRE_TOKEN_EVENT_DRIVEN_TEMPLATE",  # noqa: S106  # nosec B106
        )
    )
    TEMPORAL_ADDRESS: str = "europe-west3.gcp.api.temporal.io:7233"
    TEMPORAL_NAMESPACE: str = "gke-standard-cluster.hhwdx"
    TEMPORAL_API_KEY: str = Field(
        default_factory=lambda: get_secret_from_gcp(
            project_id="dataascode",
            secret_name="TEMPORAL_API_KEY",  # noqa: S106  # nosec B106
        )
    )


settings = Settings()
