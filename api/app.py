# On importe ton vrai codec (celui qui a la clé secrète)
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from google.protobuf import json_format
from temporalio.api.common.v1 import Payloads

from api.temporal_workflows.codex import EncryptionCodec

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

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.TEMPORAL_ADDRESS], # En prod, mets l'URL exacte de ton interface Temporal Cloud/Web
    allow_credentials=True,
    # Temporal n'a besoin que du POST (et OPTIONS pour la vérification du navigateur)
    allow_methods=["POST", "OPTIONS"],
    # Les headers envoyés par Temporal
    allow_headers=["content-type", "x-namespace"],
)

codec = EncryptionCodec(secret_key=settings.FERNET_ENCRYPTION_KEY)

@app.post("/decode")
async def decode_payloads(request: Request):
    """On doit impérativement ajouter l'URL à temporal pour que le serveur sache à qui envoyé le message"""

    # 1. Lire les données envoyées par l'interface Web
    body = await request.body()
    payloads = json_format.Parse(body, Payloads())

    # 2. Utiliser ton Codec pour déchiffrer
    decoded_payloads = await codec.decode(payloads.payloads)

    # 3. Renvoyer les données en clair au navigateur
    result = Payloads(payloads=decoded_payloads)
    return Response(
        content=json_format.MessageToJson(result),
        media_type="application/json"
    )

@app.get("/")
async def health_check():
    """Health check endpoint for GCE Load Balancer and K8s probes."""
    return {"status": "healthy", "service": "event-driven-api"}


app.include_router(ingest_delta.router, prefix=settings.API_V1_STR)
