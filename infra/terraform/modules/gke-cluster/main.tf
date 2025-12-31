# Resource: GKE Cluster
resource "google_container_cluster" "gke_cluster" {
  name                     = var.gke_cluster_name
  remove_default_node_pool = true
  initial_node_count       = 1

  network    = var.vpc
  subnetwork = var.subnet

  deletion_protection = false # Set to true if production
}

resource "google_container_node_pool" "nodepool_1" {
  name               = var.gke_nood_pool_name
  cluster            = google_container_cluster.gke_cluster.name
  initial_node_count = 1 # the number of nodes to create in each zone

  autoscaling { # Becareful to the pricing
    min_node_count  = 1
    max_node_count  = 3
    location_policy = "ANY"
  }

  node_config {
    preemptible  = true
    machine_type = var.machine_type
    # Google recommends custom service accounts that have cloud-platform scope and permissions granted via IAM Roles.
    service_account = var.email
    oauth_scopes = [
      "https://www.googleapis.com/auth/cloud-platform"
    ]
    disk_size_gb = 20
    disk_type    = "pd-standard"
  }
}
