import asyncio
from datetime import timedelta

from temporalio import workflow
from temporalio.common import RetryPolicy

from api.temporal_workflows.hello.config_excution_temporal import config_temporal_hello

with workflow.unsafe.imports_passed_through():
    from api.models.events import EventModelV1
    from api.temporal_workflows.hello.your_activities_dacx import HelloActivities, HelloActivitiesMultiStep


@workflow.defn(name=config_temporal_hello.workflow_name)
class YourWorkflow:
    @workflow.run
    async def run(self, event_model_v1: EventModelV1) -> str:
        retry_policy = RetryPolicy(
            initial_interval=timedelta(seconds=15),
            backoff_coefficient=2.0,
            maximum_interval=timedelta(seconds=160),
            maximum_attempts=100,
        )

        await asyncio.sleep(10)  # Timers can set from second to years
        # await asyncio.sleep(timedelta(days=700).total_seconds()) Syntax for long waiting

        # workflow.execute_activity( if fonction

        return await workflow.execute_activity_method(
            HelloActivities.your_activity,
            event_model_v1,
            start_to_close_timeout=timedelta(seconds=10),
            retry_policy=retry_policy,
        )


@workflow.defn(name=f"{config_temporal_hello.workflow_name}MultiStep")
class YourWorkflowMultiStep:
    @workflow.run
    async def run(self, event_model_v1: EventModelV1) -> str:
        retry_policy = RetryPolicy(
            initial_interval=timedelta(seconds=15),
            backoff_coefficient=2.0,
            maximum_interval=timedelta(seconds=160),
            maximum_attempts=100,
        )

        first_step = await workflow.execute_activity_method(
            HelloActivitiesMultiStep.your_activity_name,
            event_model_v1,
            start_to_close_timeout=timedelta(seconds=10),
            retry_policy=retry_policy,
        )

        full_sentence = await workflow.execute_activity_method(
            HelloActivitiesMultiStep.your_activity_lastname,
            args=[event_model_v1, first_step],
            start_to_close_timeout=timedelta(seconds=10),
            retry_policy=retry_policy,
        )

        return full_sentence


################################ Managing error without retry ####################################################

# async def main():

#       async with aiohttp.ClientSession() as session:
#           async with session.get('http://temporal.io') as response:


#####################################################################################################################
