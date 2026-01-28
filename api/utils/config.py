from api.utils.secrets import get_secret_from_gcp
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

get_secret_from_gcp()

class Settings(BaseSettings):
    BUCKET_NAME: str = "event-driven"
    API_V1_STR: str = "/api/v1"
    GCP_PROJECT_ID: str = "dataascode"
    LOGFIRE_SECRET_NAME: str = "LOGFIRE_TOKEN_EVENT_DRIVEN_TEMPLATE"  # noqa: S105
    TEMPORAL_ADDRESS: str = "europe-west3.gcp.api.temporal.io:7233"
    TEMPORAL_NAMESPACE: str = "gke-standard-cluster.hhwdx"
    TEMPORAL_API_KEY: str = get_secret_from_gcp(
        project_id="dataascode",
        secret_name="TEMPORAL_API_KEY"
    )
