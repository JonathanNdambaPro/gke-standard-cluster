from fastapi import FastAPI

from .routers import ingest_delta
from .utils.config import Settings

settings = Settings()

description = """
Event-Driven GCP API 🚀

## Features

**Event Ingestion**: Receive and process CloudEvents via Pub/Sub
**Delta Lake Storage**: Data persistence in Delta Lake tables on GCS
**Automatic UPSERT**: Intelligent merge of events based on ID
**Automatic Optimization**: Table compaction and cleanup after each ingestion
**Observability**: Structured logging with Logfire and Loguru

## Architecture

* **Event-Driven**: Event-based architecture with Google Cloud Pub/Sub
* **Delta Lake**: ACID-compliant storage with merge and time-travel support
* **Cloud Run**: Serverless deployment on Google Cloud Platform
* **Eventarc**: Cloud-native event routing
"""

app = FastAPI(
    debug=True,
    title="Event-Driven GCP API",
    description=description,
    version="0.0.1",
    contact={
        "name": "Jonathan Ndamba",
        "email": "jonathan@dataascode.tech",
    },
    license_info={
        "name": "MIT",
    },
)


@app.get("/")
async def health_check():
    """Health check endpoint for GCE Load Balancer and K8s probes."""
    return {"status": "healthy", "service": "event-driven-api"}


app.include_router(ingest_delta.router, prefix=settings.API_V1_STR)
