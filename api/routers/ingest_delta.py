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
from temporalio.common import WorkflowIDReusePolicy

from api.docs.ingest_delta import docs_ingest_event
from api.models.events import EventInputModel, EventModelV1
from api.temporal_workflows.client import get_temporal_client
from api.temporal_workflows.hello.config_excution_temporal import config_temporal_hello, config_temporal_hello_eventarc
from api.temporal_workflows.hello.workflow import YourWorkflow, YourWorkflowMultiStep
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


@router.post("/start_temporal_hello")
async def start_temporal_hello(
    event_input: EventInputModel,
    client_temporal: Client = Depends(get_temporal_client),  # noqa: B008
):
    body = event_input.model_dump()
    unique_id = generate_unique_id(body)

    handle = await client_temporal.start_workflow(  # return handle for freeing the api
        YourWorkflow.run,
        EventModelV1(id=unique_id, **body),
        id=f"wf-{unique_id}",
        task_queue=config_temporal_hello.task_queue,
        id_reuse_policy=WorkflowIDReusePolicy.ALLOW_DUPLICATE_FAILED_ONLY,
    )

    logger.info(f"Started workflow {handle.id}")

    return {"status": "workflow_started", "id": handle.id}


@router.get("/status_temporal_hello/{workflow_id}")
async def get_status(
    workflow_id: str,
    client_temporal: Client = Depends(get_temporal_client),  # noqa: B008
):
    handle = client_temporal.get_workflow_handle(workflow_id)
    description = await handle.describe()

    # Renvoie l'état actuel : RUNNING, COMPLETED, FAILED, etc.
    return {
        "workflow_id": workflow_id,
        "status": str(description.status),
        "start_time": description.start_time,
        "close_time": description.close_time,
    }


@router.get("/receive_temporal_hello")
async def receive_temporal_hello(
    workflow_id: str,
    client_temporal: Client = Depends(get_temporal_client),  # noqa: B008
):
    handle = client_temporal.get_workflow_handle(workflow_id)

    # 2. On attend le résultat (ou on le récupère s'il est déjà fini)
    # Si le workflow est fini, handle.result() renvoie la valeur immédiatement.
    # S'il tourne encore, cette ligne attend (bloque la requête HTTP).
    result = await handle.result()

    return {"status": "completed", "workflow_id": workflow_id, "result": result}


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

    result = await client_temporal.execute_workflow(  # wait for operation to finish and receive output
        YourWorkflow.run,
        data_to_ingest,
        id=f"your-workflow-id-{uuid.uuid4()}",
        task_queue=config_temporal_hello_eventarc.task_queue,
        id_reuse_policy=WorkflowIDReusePolicy.ALLOW_DUPLICATE_FAILED_ONLY,
    )

    logger.info(f"Workflow result: {result}")
    return {"status": "success", "result": result}


@router.post("/temporal_hello_multi_step")
async def temporal_hello_multi_step(request: Request, client_temporal: Client = Depends(get_temporal_client)):  # noqa: B008
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

    result = await client_temporal.execute_workflow(  # wait for operation to finish and receive output
        YourWorkflowMultiStep.run,
        data_to_ingest,
        id=f"your-workflow-multi-step-id-{uuid.uuid4()}",
        task_queue=config_temporal_hello.task_queue,
        id_reuse_policy=WorkflowIDReusePolicy.ALLOW_DUPLICATE_FAILED_ONLY,
    )

    logger.info(f"Workflow multi-step result: {result}")
    return {"status": "success", "result": result}
