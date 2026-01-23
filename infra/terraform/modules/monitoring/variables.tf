variable "project_id" {
  description = "The GCP project ID"
  type        = string
}

variable "notification_email" {
  description = "Email address for alert notifications"
  type        = string
}

variable "dlq_subscriptions" {
  description = "List of DLQ subscription names to monitor"
  type        = list(string)
}
