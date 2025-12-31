# Resource: VPC
resource "google_compute_network" "myvpc" {
  name                    = var.vpc_name
  auto_create_subnetworks = false
}

# Resource: Subnet
resource "google_compute_subnetwork" "mysubnet" {
  name                     = var.subnet_name
  ip_cidr_range            = var.subnet_ip_cidr_range
  network                  = google_compute_network.myvpc.id
  private_ip_google_access = true
}

resource "google_compute_global_address" "ip_address" { #Doit être global pour que le ingress de GKE puisse l'intégrer
  name         = var.ip_address_ressource_name
  address_type = "EXTERNAL"
}
