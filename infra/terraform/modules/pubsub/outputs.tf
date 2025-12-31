output "pubsub_topic_name" {
  description = "Name of the Pub/Sub topic"
  value       = google_pubsub_topic.topic.name
}

output "pubsub_topic_id" {
  description = "ID of the Pub/Sub topic"
  value       = google_pubsub_topic.topic.id
}

output "pubsub_topic" {
  description = "Full Pub/Sub topic resource for dependency management"
  value       = google_pubsub_topic.topic
}

output "pubsub_dlq_topic_name" {
  description = "Name of the Dead Letter Queue topic"
  value       = google_pubsub_topic.dlq.name
}

output "pubsub_dlq_subscription_name" {
  description = "Name of the DLQ subscription"
  value       = google_pubsub_subscription.dlq_subscription.name
}
