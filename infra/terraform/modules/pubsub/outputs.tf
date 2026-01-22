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
