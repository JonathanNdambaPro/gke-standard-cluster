resource "google_artifact_registry_repository" "repo-backend-dataascode-event-driven" {
  location      = var.region
  repository_id = var.artifactory_repository_id
  description   = "Image whom manage all data transformation and logique to dataascode"
  format        = "DOCKER"
}
