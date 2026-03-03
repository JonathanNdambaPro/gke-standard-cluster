import pytest
from temporalio.testing import WorkflowEnvironment
from temporalio.worker import Worker

from api.temporal_workflows.hello.workflow import YourWorkflow, YourWorkflowMultiStep
from api.temporal_workflows.hello.your_activities_dacx import HelloActivities, HelloActivitiesMultiStep


@pytest.mark.asyncio
async def test_your_workflow(mock_event_model_v1):
    output = "hello Jonathan, Ndamba!"
    async with await WorkflowEnvironment.start_time_skipping() as env:
        activities = HelloActivities()
        async with Worker(
            env.client,
            task_queue="test-math-queue",
            workflows=[YourWorkflow],
            activities=[activities.your_activity],
        ):
            result = await env.client.execute_workflow(
                YourWorkflow.run,
                mock_event_model_v1,
                id="test-sum-of-squares",
                task_queue="test-math-queue",
            )

            assert output == result


@pytest.mark.asyncio
async def test_your_workflow_multi_step(mock_event_model_v1):
    output = "hello Jonathan, Ndamba!"
    task_queue = "test-math-queue-multi-step"
    id_ = "test-muli-step"

    async with await WorkflowEnvironment.start_time_skipping() as env:
        activities = HelloActivitiesMultiStep()
        async with Worker(
            env.client,
            task_queue=task_queue,
            workflows=[YourWorkflowMultiStep],
            activities=[activities.your_activity_name, activities.your_activity_lastname],
        ):
            result = await env.client.execute_workflow(
                YourWorkflowMultiStep.run,
                mock_event_model_v1,
                id=id_,
                task_queue=task_queue,
            )

            assert output == result
