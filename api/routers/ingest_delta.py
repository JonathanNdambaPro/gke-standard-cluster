import base64
import hashlib
import json
import uuid
from pathlib import Path

import logfire
import polars as pl
from deltalake import DeltaTable, write_deltalake
from fastapi import APIRouter, Depends, Request
from loguru import logger
from temporalio.client import Client
from temporalio.worker import Worker

from api.docs.ingest_delta import docs_ingest_event
from api.models.events import EventModelV1
from api.temporal_workflows.client import get_temporal_client
from api.temporal_workflows.hello.workflow import YourWorkflow
from api.temporal_workflows.hello.your_activities_dacx import your_activity
from api.utils.config import settings

router = APIRouter(tags=["ingest"])

logfire.configure(token=settings.LOGFIRE_TOKEN)
logger.configure(handlers=[logfire.loguru_handler()])

PATH_TO_FOLDER_JINJA_SQL = Path(__file__).parent / "sql"
GCS_PATH = f"gs://{settings.BUCKET_NAME}/ingest_table"


def generate_unique_id(data: dict) -> str:
    """
    Génère un ID unique et déterministe basé sur le contenu de l'événement.
    Le même contenu produit toujours le même ID, évitant les doublons.
    """
    sorted_data = json.dumps(data, sort_keys=True)
    return hashlib.sha256(sorted_data.encode()).hexdigest()


@router.post("/ingest_event", **docs_ingest_event.model_dump())
async def ingest_delta(request: Request):
    cloudevent = await request.json()
    pubsub_data_base64 = cloudevent.get("message").get("data")
    data_decoded_str = base64.b64decode(pubsub_data_base64).decode("utf-8")
    data_decoded = json.loads(data_decoded_str)

    unique_id = generate_unique_id(data_decoded)

    logger.info(f"🗓️ CloudEvent Pub/Sub decoded: {data_decoded}")
    logger.info(f"🆔 ID unique généré: {unique_id}")
    logger.info(f"🔖 CE-ID original: {request.headers.get('ce-id')}")
    logger.info(f"🏷️ Type (ce-type): {request.headers.get('ce-type')}")

    data_to_ingest = EventModelV1(id=unique_id, **data_decoded)
    source_data = pl.DataFrame(data_to_ingest.model_dump(by_alias=True))

    if DeltaTable.is_deltatable(GCS_PATH):
        dt = DeltaTable(GCS_PATH)

        (
            dt.merge(
                source=source_data,
                predicate="target.id = source.id",
                source_alias="source",
                target_alias="target",
                merge_schema=True,
            )
            .when_matched_update_all(except_cols=["id"])
            .when_not_matched_insert_all()
            .execute()
        )
        logger.info(f"🚀 Event merged in table {GCS_PATH}")

        dt.optimize.compact()
        dt.vacuum(retention_hours=0, enforce_retention_duration=False, dry_run=False)

        logger.info(f"⚙️ Table {GCS_PATH} optimize")
        return {"status": "success", "message_data": data_decoded_str}

    write_deltalake(GCS_PATH, source_data)
    logger.info(f"✨ Table {GCS_PATH} create")

    return {"status": "success", "message_data": data_decoded_str}


@router.post("/temporal_hello")
async def temporal_hello(request: Request, client_temporal: Client = Depends(get_temporal_client)):  # noqa: B008
    # Récupérer le body JSON directement (test local, pas de Eventarc)
    body = await request.json()

    unique_id = generate_unique_id(body)

    logger.info(f"🗓️ Request body: {body}")
    logger.info(f"🆔 ID unique généré: {unique_id}")

    # Créer le modèle EventModelV1 depuis le body
    data_to_ingest = EventModelV1(id=unique_id, **body)

    task_queue = "hello-task-queue"

    worker = Worker(
        client_temporal,
        task_queue=task_queue,
        workflows=[YourWorkflow],
        activities=[your_activity],
    )

    async with worker:
        result = await client_temporal.execute_workflow(
            YourWorkflow.run,
            data_to_ingest,
            id=f"your-workflow-id-{uuid.uuid4()}",
            task_queue=task_queue,
        )

    logger.info(f"Workflow result: {result}")
    return {"status": "success", "result": result}


@router.post("/temporal_hello_eventarc")
async def temporal_hello_eventarc(request: Request, client_temporal: Client = Depends(get_temporal_client)):  # noqa: B008
    cloudevent = await request.json()
    pubsub_data_base64 = cloudevent.get("message").get("data")
    data_decoded_str = base64.b64decode(pubsub_data_base64).decode("utf-8")
    data_decoded = json.loads(data_decoded_str)

    unique_id = generate_unique_id(data_decoded)

    logger.info(f"🗓️ CloudEvent Pub/Sub decoded: {data_decoded}")
    logger.info(f"🆔 ID unique généré: {unique_id}")
    logger.info(f"🔖 CE-ID original: {request.headers.get('ce-id')}")
    logger.info(f"🏷️ Type (ce-type): {request.headers.get('ce-type')}")

    data_to_ingest = EventModelV1(id=unique_id, **data_decoded)
    task_queue = "hello-task-queue-eventarc"

    worker = Worker(
        client_temporal,
        task_queue=task_queue,
        workflows=[YourWorkflow],
        activities=[your_activity],
    )

    async with worker:
        result = await client_temporal.execute_workflow(
            YourWorkflow.run,
            data_to_ingest,
            id=f"your-workflow-id-{uuid.uuid4()}",
            task_queue=task_queue,
        )

    logger.info(f"Workflow result: {result}")
    return {"status": "success", "result": result}
