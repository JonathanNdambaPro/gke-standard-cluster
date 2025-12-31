variable "project" {
  type        = string
  description = "GCP project ID where all resources will be created."
}

variable "region" {
  type        = string
  description = "GCP region where regional resources will be deployed."
}

# GCP Compute Engine Machine Type
variable "machine_type" {
  description = "Compute Engine Machine Type"
  type        = string
}

# Environment Variable
variable "environment" {
  description = "Environment Variable used as a prefix"
  type        = string
}


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

variable "gke_nood_pool_name" {
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

variable "gke_service_account_name" {
  type        = string
  description = "value"
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
