variable "ssl_policy_name" {
  type        = string
  description = "value"
}

variable "security_policy_name" {
  type        = string
  description = "The name of the Cloud Armor security policy"
  default     = "cloud-armor-policy"
}
