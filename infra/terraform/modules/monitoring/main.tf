resource "google_monitoring_notification_channel" "email" {
  display_name = "Email Notification Channel"
  type         = "email"
  labels = {
    email_address = var.notification_email
  }
  project = var.project_id
}

resource "google_monitoring_alert_policy" "dlq_policy" {
  display_name = "DLQ Messages Alert"
  combiner     = "OR"
  project      = var.project_id

  conditions {
    display_name = "Messages in DLQ"
    condition_threshold {
      filter          = "resource.type = \"pubsub_subscription\" AND resource.labels.subscription_id = one_of(${join(",", formatlist("\"%s\"", var.dlq_subscriptions))}) AND metric.type = \"pubsub.googleapis.com/subscription/num_undelivered_messages\""
      duration        = "60s"
      comparison      = "COMPARISON_GT"
      threshold_value = 0
      aggregations {
        alignment_period   = "60s"
        per_series_aligner = "ALIGN_MAX"
      }
    }
  }

  notification_channels = [google_monitoring_notification_channel.email.name]
  alert_strategy {
    auto_close = "604800s" # 7 days
  }
}
