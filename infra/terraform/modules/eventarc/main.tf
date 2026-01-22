resource "google_eventarc_trigger" "gke_trigger" {
  name            = var.eventarc_name
  location        = var.region
  project         = var.project
  service_account = var.service_account_email
  matching_criteria {
    attribute = "type"
    value     = var.event_type
  }
  destination {
    gke {
      cluster   = var.cluster
      path      = var.gke_run_service_path
      location  = var.region
      namespace = var.namespace
      service   = var.service
    }
  }

  transport {
    pubsub {
      topic = var.source_topic_name
    }
  }
}
