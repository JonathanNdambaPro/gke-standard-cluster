variable "project" {
  description = "The project ID"
  type        = string
}

variable "region" {
  description = "The region"
  type        = string
}

variable "service_account_email" {
  description = "The service account email"
  type        = string
}

variable "label" {
  description = "Label for the trigger"
  type        = string
}

variable "source_topic_name" {
  description = "The source Pub/Sub topic name"
  type        = string
}

variable "eventarc_name" {
  description = "The name of the eventarc trigger"
  type        = string
}

variable "cluster" {
  description = "The GKE cluster name"
  type        = string
}

variable "service" {
  description = "The GKE service name"
  type        = string
}

variable "namespace" {
  description = "The GKE namespace"
  type        = string
}

variable "gke_run_service_path" {
  description = "The path for the GKE service"
  type        = string
}

variable "environment_filter" {
  description = "The environment to filter events for (e.g. production, feature-x)"
  type        = string
  default     = "production"
}
