#!/usr/bin/env python3
"""
Script to publish a test message to Pub/Sub with exponential backoff retry.

Usage:
    python scripts/publish_event.py [ingest|temporal]
"""

import json
import time

from google.api_core import retry as api_retry
from google.api_core.exceptions import GoogleAPICallError
from google.cloud import pubsub_v1
from loguru import logger
from pydantic import BaseModel, Field

# Configuration - matches config.yaml
PROJECT_ID = "dataascode"
TOPIC_ID_INGEST = "event-ingestion"
TOPIC_ID_TEMPORAL = "temporal-workflow"

# Retry configuration
MAX_RETRIES = 10
INITIAL_DELAY = 1.0  # seconds
MAX_DELAY = 60.0  # seconds
MULTIPLIER = 2.0

# Configure retry with exponential backoff
RETRY_CONFIG = api_retry.Retry(
    initial=INITIAL_DELAY,
    maximum=MAX_DELAY,
    multiplier=MULTIPLIER,
    deadline=3600.0,  # 60 minutes total timeout
)


class PublishConfig(BaseModel):
    environment: str = Field("production", pattern=r"^(production|feat.*|fix.*)$")


class SchemaMessage(BaseModel):
    name: str = "John"
    lastname: str = "Doe"


# Validated configuration
CONFIG = PublishConfig()

# Message matching EventModelV1 (name, lastname)
MESSAGE = SchemaMessage(name="John", lastname="Doe")


def publish_with_retry(
    topic_id: str,
    message_data: SchemaMessage = MESSAGE,
    config: PublishConfig = CONFIG,
) -> None:
    """Publish a message to Pub/Sub with exponential backoff retry."""
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(PROJECT_ID, topic_id)
    data = message_data.model_dump_json().encode("utf-8")

    try:
        future = publisher.publish(
            topic_path,
            data,
            environment=config.environment,  # Attribute for Eventarc filtering
            retry=RETRY_CONFIG,
        )
        message_id = future.result(timeout=30)

        logger.info("✅ Message published")
        logger.info(f"Topic: {topic_path}")
        logger.info(f"Message ID: {message_id}")
        logger.info(f"Data: {message_data}")

    except GoogleAPICallError as e:
        logger.error(f"❌ All retries failed: {e}")
        send_to_dlq(topic_id, message_data, str(e))


def send_to_dlq(topic_id: str, message_data: dict, error: str) -> None:
    """Send failed message to Dead Letter Queue."""
    publisher = pubsub_v1.PublisherClient()
    dlq_topic_path = publisher.topic_path(PROJECT_ID, f"{topic_id}-dlq")

    dlq_message = {
        "original_message": message_data,
        "error": error,
        "timestamp": time.time(),
    }

    try:
        data = json.dumps(dlq_message).encode("utf-8")
        future = publisher.publish(dlq_topic_path, data)
        message_id = future.result(timeout=30)
        logger.info(f"📬 Message sent to DLQ: {dlq_topic_path}")
        logger.info(f"DLQ Message ID: {message_id}")
    except GoogleAPICallError as e:
        logger.error(f"❌ Failed to send to DLQ: {e}")


if __name__ == "__main__":
    logger.info("🕐 Publishing to Temporal workflow topic...")
    publish_with_retry(TOPIC_ID_TEMPORAL, MESSAGE)
