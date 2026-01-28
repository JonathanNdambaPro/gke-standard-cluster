from typing import Optional
from api.utils.config import settings
from temporalio.client import Client


async def get_temporal_client() -> Client:
    client_temporal_cloud = await Client.connect(
        settings.TEMPORAL_ADDRESS,
        namespace=settings.TEMPORAL_NAMESPACE,
        api_key=settings.TEMPORAL_API_KEY,
        tls=True
    )

    return client_temporal_cloud
