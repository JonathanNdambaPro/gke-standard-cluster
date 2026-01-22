from fastapi import status

from api.docs.openapi_docs_model import OpenApiDocs

docs_ingest_event = OpenApiDocs(
    summary="CloudEvent ingestion",
    description="Endpoint to receive and ingest CloudEvents from Pub/Sub into a Delta Lake table on GCS. Performs an UPSERT (merge) if the table exists, otherwise creates it. Automatically optimizes and cleans up the table after each ingestion.",
    response_description="Ingestion status and processed data",
    responses={
        200: {
            "description": "Event successfully ingested",
            "content": {
                "application/json": {
                    "example": {"status": "success", "message_data": '{"name": "John", "lastname": "Doe"}'}
                }
            },
        },
        400: {
            "description": "Invalid request - incorrect CloudEvent format or missing data",
            "content": {"application/json": {"example": {"detail": "Invalid CloudEvent format"}}},
        },
        500: {
            "description": "Internal error during ingestion or writing to Delta Lake",
            "content": {"application/json": {"example": {"detail": "Error writing to Delta Lake"}}},
        },
    },
    openapi_extra={
        "requestBody": {
            "content": {
                "application/json": {
                    "schema": {
                        "type": "object",
                        "properties": {
                            "message": {
                                "type": "object",
                                "properties": {
                                    "data": {
                                        "type": "string",
                                        "description": "Base64-encoded data containing the event",
                                        "example": "eyJuYW1lIjogIkpvaG4iLCAibGFzdG5hbWUiOiAiRG9lIn0=",
                                    }
                                },
                                "required": ["data"],
                            }
                        },
                        "required": ["message"],
                    },
                    "example": {
                        "message": {
                            "data": "eyJuYW1lIjogIkpvaG4iLCAibGFzdG5hbWUiOiAiRG9lIn0=",
                            "messageId": "123456789",
                            "publishTime": "2025-11-24T10:00:00Z",
                        }
                    },
                }
            },
            "description": "CloudEvent in Pub/Sub format with base64-encoded data. Headers ce-id and ce-type are also required.",
        }
    },
    status_code=status.HTTP_200_OK,
)
