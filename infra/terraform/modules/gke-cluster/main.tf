# Resource: GKE Cluster
resource "google_container_cluster" "gke_cluster" {
  name             = var.gke_cluster_name
  enable_autopilot = true

  network    = var.vpc
  subnetwork = var.subnet

  deletion_protection = false # Set to true if production
}
