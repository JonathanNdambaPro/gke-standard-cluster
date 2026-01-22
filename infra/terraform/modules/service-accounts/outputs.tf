output "service_account_gke_email" {
  description = "Noms de l'artifactory créés"
  value       = google_service_account.gke_sa.email
}

output "service_account_eventarc_name_email" {
  description = "Noms de l'artifactory créés"
  value       = google_service_account.eventarc_triggers.email
}
