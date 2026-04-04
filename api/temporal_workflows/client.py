import dataclasses

import logfire
import temporalio
from pydantic_ai.durable_exec.temporal import LogfirePlugin, PydanticAIPlugin
from temporalio.client import Client
from temporalio.contrib.opentelemetry import TracingInterceptor

from api.temporal_workflows.codex import EncryptionCodec
from api.utils.config import settings


def setup_logfire_with_token() -> logfire.Logfire:
    instance = logfire.configure(token=settings.LOGFIRE_TOKEN)
    instance.instrument_pydantic_ai()
    return instance


async def get_temporal_client() -> Client:
    client_temporal_cloud = await Client.connect(
        settings.TEMPORAL_ADDRESS,
        namespace=settings.TEMPORAL_NAMESPACE,
        api_key=settings.TEMPORAL_API_KEY,
        tls=True,
        interceptors=[TracingInterceptor()],
        data_converter=dataclasses.replace(
            temporalio.converter.default(),
            payload_codec=EncryptionCodec(secret_key=settings.FERNET_ENCRYPTION_KEY),
            failure_converter_class=temporalio.converter.DefaultFailureConverterWithEncodedAttributes,
        ),
        plugins=[PydanticAIPlugin(), LogfirePlugin(setup_logfire=setup_logfire_with_token)],
    )

    return client_temporal_cloud
