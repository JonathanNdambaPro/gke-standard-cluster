#!/usr/bin/env python3
"""
Script to publish a test message to Pub/Sub with exponential backoff retry.

Usage:
    python scripts/publish_event.py
"""

import json
import time

from google.api_core import retry as api_retry
from google.api_core.exceptions import GoogleAPICallError
from google.cloud import pubsub_v1
from loguru import logger

# Configuration - matches config.yaml
PROJECT_ID = "dataascode"
TOPIC_ID = "event-ingestion"

# Retry configuration
MAX_RETRIES = 10
INITIAL_DELAY = 1.0  # seconds
MAX_DELAY = 60.0  # seconds
MULTIPLIER = 2.0

# Message matching EventModelV1 (name, lastname)
MESSAGE = {"name": "John", "lastname": "Doe"}

# Configure retry with exponential backoff
RETRY_CONFIG = api_retry.Retry(
    initial=INITIAL_DELAY,
    maximum=MAX_DELAY,
    multiplier=MULTIPLIER,
    deadline=300.0,  # 5 minutes total timeout
)


def publish_with_retry(message_data: dict) -> str | None:
    """Publish a message to Pub/Sub with exponential backoff retry."""
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(PROJECT_ID, TOPIC_ID)
    data = json.dumps(message_data).encode("utf-8")

    try:
        future = publisher.publish(topic_path, data, retry=RETRY_CONFIG)
        message_id = future.result(timeout=30)

        logger.info("✅ Message published")
        logger.info(f"Topic: {topic_path}")
        logger.info(f"Message ID: {message_id}")
        logger.info(f"Data: {message_data}")

    except GoogleAPICallError as e:
        logger.error(f"❌ All retries failed: {e}")
        send_to_dlq(message_data, str(e))


def send_to_dlq(message_data: dict, error: str) -> None:
    """Send failed message to Dead Letter Queue."""
    publisher = pubsub_v1.PublisherClient()
    dlq_topic_path = publisher.topic_path(PROJECT_ID, f"{TOPIC_ID}-dlq")

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
    publish_with_retry(MESSAGE)
