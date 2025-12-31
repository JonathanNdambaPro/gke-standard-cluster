output "vpc" {
  description = "Noms de l'artifactory créés"
  value       = google_compute_network.myvpc.self_link
}

output "subnet" {
  description = "Noms de l'artifactory créés"
  value       = google_compute_subnetwork.mysubnet.self_link
}

output "extern_ip_adress" {
  description = "value"
  value       = google_compute_global_address.ip_address.address
}
