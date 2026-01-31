from temporalio import activity

from api.models.events import EventModelV1
from api.temporal_workflows.hello.config_excution_temporal import config_temporal_hello


@activity.defn(name=config_temporal_hello.activity_name)
async def your_activity(input_hello: EventModelV1) -> str:
    return f"hello {input_hello.name}, {input_hello.lastname}!"
