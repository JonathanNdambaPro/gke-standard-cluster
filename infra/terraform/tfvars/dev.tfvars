# GCP Project Configuration
project = "dataascode"
region  = "europe-west1"

# Environment Variable
environment = "dev"

# Network
vpc_name                  = "template-vpc"
subnet_name               = "template-subnet-vpc"
subnet_ip_cidr_range      = "10.128.0.0/20"
ip_address_ressource_name = "template-external-ip"

# GKE
gke_cluster_name   = "template-gke-cluster"
gke_nood_pool_name = "template-node-pool-1"
machine_type       = "e2-small"

# Cloud DNS
google_dns_managed_zone_ressource_name = "template-dns"
dns_name                               = "templatejojotest.com."

# Security
ssl_policy_name = "production-ssl-policy"

# Service account
gke_service_account_name = "gke-sa"

# Cloud Domains Contact
contact_name         = "Jonathan Ndamba"
contact_email        = "jonathan.ndamba.pro@gmail.com"
contact_phone        = "+33768042961"
contact_address_line = "1 Avenue Gabriel Péri"
contact_city         = "Vincennes"
contact_state        = "Ile-de-France"
contact_postal_code  = "94300"
contact_country_code = "FR"
