import dataclasses

import temporalio
from temporalio.client import Client
from temporalio.contrib.opentelemetry import TracingInterceptor

from api.temporal_workflows.codex import CompressionCodex, EncryptionCodec  # noqa: F401
from api.utils.config import settings


async def get_temporal_client() -> Client:
    client_temporal_cloud = await Client.connect(
        settings.TEMPORAL_ADDRESS,
        namespace=settings.TEMPORAL_NAMESPACE,
        api_key=settings.TEMPORAL_API_KEY,
        tls=True,
        interceptors=[TracingInterceptor()],
        data_converter=dataclasses.replace(
            temporalio.converter.default(),
            # 1. On active notre Codec (ex: ton CompressionCodex)
            # 1. On active notre Codec (ex: ton CompressionCodex)
            payload_codec=EncryptionCodec(secret_key=settings.FERNET_ENCRYPTION_KEY),
        ),
        # 2. LA LIGNE MAGIQUE : On force les erreurs
        # à passer par ce même Codec !
        failure_converter_class=temporalio.converter.DefaultFailureConverterWithEncodedAttributes,
    )

    return client_temporal_cloud
