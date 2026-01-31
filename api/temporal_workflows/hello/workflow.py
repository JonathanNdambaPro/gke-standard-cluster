from datetime import timedelta

from temporalio import workflow

from api.temporal_workflows.hello.config_excution_temporal import config_temporal_hello

with workflow.unsafe.imports_passed_through():
    from api.models.events import EventModelV1
    from api.temporal_workflows.hello.your_activities_dacx import your_activity


@workflow.defn(name=config_temporal_hello.workflow_name)
class YourWorkflow:
    @workflow.run
    async def run(self, event_model_v1: EventModelV1) -> str:
        return await workflow.execute_activity(
            your_activity,
            event_model_v1,
            start_to_close_timeout=timedelta(seconds=10),
        )
