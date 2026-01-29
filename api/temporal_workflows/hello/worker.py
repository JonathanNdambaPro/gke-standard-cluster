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
from temporalio.client import Client
from temporalio.worker import Worker

from api.temporal_workflows.client import get_temporal_client
from api.temporal_workflows.hello.workflow import YourWorkflow
from api.temporal_workflows.hello.your_activities_dacx import your_activity


async def main():
    client_temporal = await get_temporal_client()
    client = await Client.connect(client_temporal)

    worker = Worker(
        client,
        task_queue="hello-task-queue",
        workflows=[YourWorkflow],
        activities=[your_activity],
    )

    logger.info("Worker started...")
    await worker.run()


async def mutiple_main():
    client_temporal = await get_temporal_client()
    client = await Client.connect(client_temporal)

    worker = Worker(
        client,
        task_queue="hello-task-queue",
        workflows=[YourWorkflow],
        activities=[your_activity],
    )

    worker_eventrarc = Worker(
        client,
        task_queue="hello-task-queue-eventarc",
        workflows=[YourWorkflow],
        activities=[your_activity],
    )

    logger.info("Worker started...")

    await asyncio.gather(worker.run(), worker_eventrarc.run())


if __name__ == "__main__":
    asyncio.run(mutiple_main())
