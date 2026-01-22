variable "region" {
  type        = string
  description = "Région GCP où les ressources seront déployées."
}

variable "artifactory_repository_id" {
  type        = string
  description = "Nom du dépôt Artifact Registry où stocker les images Docker."
}
