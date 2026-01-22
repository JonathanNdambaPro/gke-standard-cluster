resource "google_service_account" "gke_sa" {
  account_id   = var.gke_service_account_name
  display_name = "GKE Service Account"
}

resource "google_project_iam_member" "gcs_object_user" {
  project = var.project
  role    = "roles/storage.objectUser"
  member  = "serviceAccount:${google_service_account.gke_sa.email}"
}

resource "google_project_iam_member" "bq_data_editor" {
  project = var.project
  role    = "roles/bigquery.dataEditor"
  member  = "serviceAccount:${google_service_account.gke_sa.email}"
}

resource "google_project_iam_member" "bq_job_user" {
  project = var.project
  role    = "roles/bigquery.jobUser"
  member  = "serviceAccount:${google_service_account.gke_sa.email}"
}

resource "google_project_iam_member" "gke_secret_accessor" {
  project = var.project
  role    = "roles/secretmanager.secretAccessor"
  member  = "serviceAccount:${google_service_account.gke_sa.email}"
}

# Workload Identity binding - allows K8s service account to impersonate GCP service account
resource "google_service_account_iam_member" "workload_identity_binding" {
  service_account_id = google_service_account.gke_sa.name
  role               = "roles/iam.workloadIdentityUser"
  member             = "serviceAccount:${var.project}.svc.id.goog[default/event-driven-api-sa]"
}

resource "google_service_account" "eventarc_triggers" {
  account_id   = "eventarc-triggers-gke"
  display_name = "Eventarc Triggers Service Account"
  description  = "Service account for Eventarc triggers with least privilege access"
}

# Eventarc specific IAM bindings with least privilege
resource "google_project_iam_member" "eventarc_event_receiver" {
  project = var.project
  role    = "roles/eventarc.eventReceiver"
  member  = "serviceAccount:${google_service_account.eventarc_triggers.email}"
}


resource "google_project_iam_member" "eventarc_pubsub_subscriber" {
  project = var.project
  role    = "roles/pubsub.subscriber"
  member  = "serviceAccount:${google_service_account.eventarc_triggers.email}"
}

# Eventarc GKE destinations - required roles
resource "google_project_iam_member" "eventarc_compute_viewer" {
  project = var.project
  role    = "roles/compute.viewer"
  member  = "serviceAccount:${google_service_account.eventarc_triggers.email}"
}

resource "google_project_iam_member" "eventarc_container_developer" {
  project = var.project
  role    = "roles/container.developer"
  member  = "serviceAccount:${google_service_account.eventarc_triggers.email}"
}

resource "google_project_iam_member" "eventarc_sa_admin" {
  project = var.project
  role    = "roles/iam.serviceAccountAdmin"
  member  = "serviceAccount:${google_service_account.eventarc_triggers.email}"
}

# Eventarc Service Agent - creates Google's managed service account for GKE destinations
# This replaces the need for "gcloud eventarc gke-destinations init"
resource "google_project_service_identity" "eventarc_agent" {
  provider = google-beta
  project  = var.project
  service  = "eventarc.googleapis.com"
}

resource "google_project_iam_member" "eventarc_agent_compute_viewer" {
  project = var.project
  role    = "roles/compute.viewer"
  member  = google_project_service_identity.eventarc_agent.member
}

resource "google_project_iam_member" "eventarc_agent_container_developer" {
  project = var.project
  role    = "roles/container.developer"
  member  = google_project_service_identity.eventarc_agent.member
}

resource "google_project_iam_member" "eventarc_agent_sa_admin" {
  project = var.project
  role    = "roles/iam.serviceAccountAdmin"
  member  = google_project_service_identity.eventarc_agent.member
}
