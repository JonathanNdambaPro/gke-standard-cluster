import pytest
from temporalio.testing import WorkflowEnvironment
from temporalio.worker import Worker

from api.temporal_workflows.hello.workflow import YourWorkflow, YourWorkflowMultiStep
from api.temporal_workflows.hello.your_activities_dacx import HelloActivitiesMultiStep


@pytest.mark.asyncio
async def test_your_workflow(mock_event_model_v1, mock_hello_your_activy):
    output = "hello Jonathan, Ndamba!"
    async with (
        await WorkflowEnvironment.start_time_skipping() as env,
        Worker(
            env.client,
            task_queue="test-math-queue",
            workflows=[YourWorkflow],
            activities=[mock_hello_your_activy],
        ),
    ):
        result = await env.client.execute_workflow(
            YourWorkflow.run,
            mock_event_model_v1,
            id="test-sum-of-squares",
            task_queue="test-math-queue",
        )

        assert output == result


@pytest.mark.asyncio
async def test_your_workflow_name(mock_event_model_v1, mock_hello_your_activy_name):
    output = "hello Jonathan, Ndamba!"
    instance_hello_worker_multi_step = HelloActivitiesMultiStep()

    async with (
        await WorkflowEnvironment.start_time_skipping() as env,
        Worker(
            env.client,
            task_queue="test-math-queue",
            workflows=[YourWorkflowMultiStep],
            activities=[mock_hello_your_activy_name, instance_hello_worker_multi_step.your_activity_lastname],
        ),
    ):
        result = await env.client.execute_workflow(
            YourWorkflowMultiStep.run,
            mock_event_model_v1,
            id="test-sum-of-squares",
            task_queue="test-math-queue",
        )

        assert output == result


@pytest.mark.asyncio
async def test_your_workflow_lastname(mock_event_model_v1, mock_hello_your_activy_lastname):
    output = "hello Jonathan, Ndamba!"
    instance_hello_worker_multi_step = HelloActivitiesMultiStep()

    async with (
        await WorkflowEnvironment.start_time_skipping() as env,
        Worker(
            env.client,
            task_queue="test-math-queue",
            workflows=[YourWorkflowMultiStep],
            activities=[instance_hello_worker_multi_step.your_activity_name, mock_hello_your_activy_lastname],
        ),
    ):
        result = await env.client.execute_workflow(
            YourWorkflowMultiStep.run,
            mock_event_model_v1,
            id="test-sum-of-squares",
            task_queue="test-math-queue",
        )

        assert output == result


@pytest.mark.asyncio
async def test_your_workflow_name_and_lastname(
    mock_event_model_v1, mock_hello_your_activy_name, mock_hello_your_activy_lastname
):
    output = "hello Jonathan, Ndamba!"
    async with (
        await WorkflowEnvironment.start_time_skipping() as env,
        Worker(
            env.client,
            task_queue="test-math-queue",
            workflows=[YourWorkflowMultiStep],
            activities=[mock_hello_your_activy_name, mock_hello_your_activy_lastname],
        ),
    ):
        result = await env.client.execute_workflow(
            YourWorkflowMultiStep.run,
            mock_event_model_v1,
            id="test-sum-of-squares",
            task_queue="test-math-queue",
        )

        assert output == result
