variable "project" {
  type        = string
  description = "GCP project ID where all resources will be created."
}

variable "create_domain_registration" {
  description = "Whether to create the Cloud Domain registration"
  type        = bool
  default     = true
}

variable "region" {
  type        = string
  description = "GCP region where regional resources will be deployed."
}

# GCP Compute Engine Machine Type


variable "vpc_name" {
  type        = string
  description = "value"
}

variable "subnet_ip_cidr_range" {
  type        = string
  description = "value"
}

variable "dns_name" {
  type        = string
  description = "value"
}


variable "gke_cluster_name" {
  type        = string
  description = "value"
}



# variable "compute_address_name" {
#     type = string
#     description = "value"
# }

variable "google_dns_managed_zone_ressource_name" {
  type        = string
  description = "value"
}

variable "subnet_name" {
  type        = string
  description = "value"
}

variable "ip_address_ressource_name" {
  type        = string
  description = "value"
}

variable "ssl_policy_name" {
  type        = string
  description = "value"
}

variable "security_policy_name" {
  type        = string
  description = "The name of the Cloud Armor security policy"
  default     = "cloud-armor-policy"
}

variable "gke_service_account_name" {
  type        = string
  description = "value"
}

variable "topic_name" {
  type        = string
  description = "Pub/Sub topic name."
}

# Cloud Domains Contact Info
variable "contact_name" { type = string }
variable "contact_email" { type = string }
variable "contact_phone" { type = string }
variable "contact_country_code" { type = string }
variable "contact_postal_code" { type = string }
variable "contact_state" { type = string }
variable "contact_city" { type = string }
variable "contact_address_line" { type = string }

variable "eventarc_name" {
  type        = string
  description = "Name of the Eventarc trigger"
}

variable "label" {
  type        = string
  description = "Label for the Eventarc trigger"
}

variable "gke_run_service_path" {
  type        = string
  description = "Path for the GKE service receiving events"
  default     = "/"
}

variable "eventarc_service_name" {
  type        = string
  description = "Name of the Kubernetes service receiving events"
}

variable "eventarc_trigger_namespace" {
  type        = string
  description = "Namespace of the Kubernetes service"
  default     = "default"
}

variable "artifactory_repository_id" {
  type        = string
  description = "Nom du dépôt Artifact Registry où stocker les images Docker."
}

variable "yearly_price_units" {
  type        = string
  description = "Maximum price in USD you are willing to pay for the domain"
  default     = "12"
}

variable "event_type" {
  type        = string
  default     = "google.cloud.pubsub.topic.v1.messagePublished"
  description = "The event type to trigger on (default: Pub/Sub message published)"
}
