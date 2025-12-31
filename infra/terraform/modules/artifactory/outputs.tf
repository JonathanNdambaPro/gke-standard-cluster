output "artifactory_repository_id" {
  description = "Noms de l'artifactory créés"
  value       = google_artifact_registry_repository.repo-backend-dataascode-event-driven.repository_id
}
