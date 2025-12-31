output "gke_trigger_name" {
  description = "Names of the created GKE Eventarc triggers"
  value       = google_eventarc_trigger.gke_trigger.name
}

output "gke_trigger_id" {
  description = "IDs of the created GKE Eventarc triggers"
  value       = google_eventarc_trigger.gke_trigger.id
}
