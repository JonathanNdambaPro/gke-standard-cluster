output "nameservers" {
  description = "The name servers of the managed zone"
  value       = google_dns_managed_zone.template-dns.name_servers
}
