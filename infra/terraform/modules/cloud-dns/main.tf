resource "google_dns_managed_zone" "template-dns" {
  name        = var.google_dns_managed_zone_ressource_name
  dns_name    = var.dns_name
  description = "Example DNS zone"
  visibility  = "public"
  labels = {
    foo = "bar"
  }
}

resource "google_dns_record_set" "default" {
  name         = google_dns_managed_zone.template-dns.dns_name
  managed_zone = google_dns_managed_zone.template-dns.name
  type         = "A"
  ttl          = 300

  routing_policy {
    wrr {
      weight  = 1
      rrdatas = var.extern_ip_adress
    }
  }
}
