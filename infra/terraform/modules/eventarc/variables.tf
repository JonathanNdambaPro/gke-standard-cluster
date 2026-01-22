variable "project" {
  type        = string
  description = "The GCP project ID where resources will be created"
}

variable "region" {
  type        = string
  default     = "europe-west9"
  description = "Region where GCP services will be deployed"
}

variable "service_account_email" {
  type        = string
  description = "The service account to use to execute the Eventarc triggers"
}

variable "eventarc_name" {
  type        = string
  description = "The service account to use to execute the Eventarc triggers"
}

variable "cluster" {
  type        = string
  description = "Name of the cluster gke"
}

variable "label" {
  type        = string
  description = "Label for the Eventarc trigger"
}

variable "source_topic_name" {
  type        = string
  description = "The service account to use to execute the Eventarc triggers"
}
variable "namespace" {
  type        = string
  default     = "default"
  description = "Namespace where the service is deployed"
}

variable "service" {
  type        = string
  description = "Name of the GKE service to receive events"
}

variable "gke_run_service_path" {
  type        = string
  default     = "/"
  description = "Path within the service to send events to"
}
