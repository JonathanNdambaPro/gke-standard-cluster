from fastapi import FastAPI

from .routers import ingest_delta
from .utils.config import Settings

settings = Settings()

description = """
Cutting Edge Event-Driven GCP API 🚀

A State-of-the-Art data platform leveraging the modern python streaming stack.

## ✨ Features

* **⚡ Ultra-Fast Processing**: Powered by **Polars** for lightning-fast data manipulation.
* **⏱️ Durable Execution**: Robust workflow orchestration with **Temporal**.
* **🗄️ ACID Storage**: Reliable **Delta Lake** tables on Google Cloud Storage.
* **🔍 Next-Gen Observability**: Deep insights with **Logfire**.
* **🚀 Modern Infra**: Cloud-Native deployment on **GKE Standard** with **Eventarc**.

## 🏗️ Architecture

* **Event-Driven**: Decoupled architecture using **Pub/Sub**.
* **Serverless-like**: Auto-scaling worker deployments on Kubernetes.
* **Declarative**: Infrastructure as Code with Terraform.
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
