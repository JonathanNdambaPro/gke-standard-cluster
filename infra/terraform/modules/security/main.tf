resource "google_compute_ssl_policy" "prod-ssl-policy" {
  name    = var.ssl_policy_name
  profile = "MODERN"
}
