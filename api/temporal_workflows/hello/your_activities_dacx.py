from temporalio import activity
from your_dataobject_dacx import YourParams


@activity.defn(name="your_activity")
async def your_activity(input_value: YourParams) -> str:
    return f"{input_value.greeting}, {input_value.name}!"
