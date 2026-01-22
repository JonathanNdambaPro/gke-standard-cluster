# Main topic for event ingestion
resource "google_pubsub_topic" "topic" {
  name = var.topic_name
}

# Dead Letter Queue topic
resource "google_pubsub_topic" "dlq" {
  name = "${var.topic_name}-dlq"
}

# DLQ subscription to consume failed messages
resource "google_pubsub_subscription" "dlq_subscription" {
  name  = "${var.topic_name}-dlq-sub"
  topic = google_pubsub_topic.dlq.id

  # Retain messages for 7 days
  message_retention_duration = "604800s"

  # Keep acknowledged messages for debugging
  retain_acked_messages = true

  ack_deadline_seconds = 60

  expiration_policy {
    ttl = "" # Never expires
  }
}
