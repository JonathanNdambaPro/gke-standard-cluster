import asyncio

from temporalio.worker import Worker

from api.temporal_workflows.client import get_temporal_client
from api.temporal_workflows.hello.workflow import YourWorkflow
from api.temporal_workflows.hello.your_activities_dacx import your_activity

"""dacx
To develop a Worker, use the `Worker()` constructor and add your Client, Task Queue, Workflows, and Activities as arguments.
The following code example creates a Worker that polls for tasks from the Task Queue and executes the Workflow.
When a Worker is created, it accepts a list of Workflows in the workflows parameter, a list of Activities in the activities parameter, or both.
dacx"""

"""dacx
When a `Worker` is created, it accepts a list of Workflows in the `workflows` parameter, a list of Activities in the `activities` parameter, or both.
dacx"""


async def main():
    client = await get_temporal_client()
    worker = Worker(
        client,
        task_queue="your-task-queue",
        workflows=[YourWorkflow],
        activities=[your_activity],
    )
    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())