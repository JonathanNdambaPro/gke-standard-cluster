"""
one worker for multiple workflow
async def main():
    client = await get_temporal_client()

    # Worker pour le RAG
    worker_rag = Worker(client, task_queue="rag-queue", workflows=[...], activities=[...])

    # Worker pour les Emails
    worker_email = Worker(client, task_queue="email-queue", workflows=[...], activities=[...])

    # Tu lances les deux en même temps dans le même Pod
    await asyncio.gather(
        worker_rag.run(),
        worker_email.run()
    )
"""

import asyncio

from loguru import logger
from temporalio.worker import Worker

from api.temporal_workflows.client import get_temporal_client
from api.temporal_workflows.hello.config_excution_temporal import config_temporal_hello, config_temporal_hello_eventarc
from api.temporal_workflows.hello.workflow import YourWorkflow, YourWorkflowMultiStep
from api.temporal_workflows.hello.your_activities_dacx import HelloActivities, HelloActivitiesMultiStep


async def main():
    client = await get_temporal_client()
    instance_hello_worker = HelloActivities()

    worker = Worker(
        client,
        task_queue=config_temporal_hello.task_queue,
        workflows=[YourWorkflow],
        activities=[instance_hello_worker.your_activity],
    )

    logger.info("Worker started...")
    await worker.run()


async def mutiple_main():
    client = await get_temporal_client()
    instance_hello_worker = HelloActivities()
    instance_hello_worker_multi_step = HelloActivitiesMultiStep()

    worker = Worker(
        client,
        task_queue=config_temporal_hello.task_queue,
        workflows=[YourWorkflow],
        activities=[instance_hello_worker.your_activity],
    )

    worker_multi_step = Worker(
        client,
        task_queue=config_temporal_hello.task_queue,
        workflows=[YourWorkflowMultiStep],
        activities=[
            instance_hello_worker_multi_step.your_activity_name,
            instance_hello_worker_multi_step.your_activity_lastname,
        ],
    )

    worker_eventrarc = Worker(
        client,
        task_queue=config_temporal_hello_eventarc.task_queue,
        workflows=[YourWorkflow],
        activities=[instance_hello_worker.your_activity],
    )

    logger.info("Worker started...")

    await asyncio.gather(worker.run(), worker_eventrarc.run(), worker_multi_step.run())


if __name__ == "__main__":
    asyncio.run(mutiple_main())
