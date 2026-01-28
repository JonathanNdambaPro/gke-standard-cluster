from temporalio.client import Client

from api.utils.config import settings


async def get_temporal_client() -> Client:
    client_temporal_cloud = await Client.connect(
        settings.TEMPORAL_ADDRESS, namespace=settings.TEMPORAL_NAMESPACE, api_key=settings.TEMPORAL_API_KEY, tls=True
    )

    return client_temporal_cloud
