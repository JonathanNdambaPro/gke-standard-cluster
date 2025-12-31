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
