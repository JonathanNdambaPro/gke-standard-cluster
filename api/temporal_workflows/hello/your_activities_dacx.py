from temporalio import activity

from api.models.events import EventModelV1


@activity.defn(name="your_activity")
async def your_activity(input_hello: EventModelV1) -> str:
    return f"hello {input_hello.name}, {input_hello.lastname}!"
