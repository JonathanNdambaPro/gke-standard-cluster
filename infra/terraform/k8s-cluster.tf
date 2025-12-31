module "network" {
  source                    = "./modules/network"
  subnet_ip_cidr_range      = var.subnet_ip_cidr_range
  vpc_name                  = var.vpc_name
  subnet_name               = var.subnet_name
  ip_address_ressource_name = var.ip_address_ressource_name
}

module "cloud-dns" {
  source                                 = "./modules/cloud-dns"
  dns_name                               = var.dns_name
  google_dns_managed_zone_ressource_name = var.google_dns_managed_zone_ressource_name
  extern_ip_adress                       = [module.network.extern_ip_adress]
}

module "security" {
  source          = "./modules/security"
  ssl_policy_name = var.ssl_policy_name
}

module "service-account" {
  source                   = "./modules/service-accounts"
  gke_service_account_name = var.gke_service_account_name
  project                  = var.project
}

module "cloud-domains" {
  source       = "./modules/cloud-domains"
  domain_name  = trimsuffix(var.dns_name, ".") # Cloud Domains doesn't want the trailing dot
  name_servers = module.cloud-dns.nameservers

  contact_name         = var.contact_name
  contact_email        = var.contact_email
  contact_phone        = var.contact_phone
  contact_country_code = var.contact_country_code
  contact_postal_code  = var.contact_postal_code
  contact_state        = var.contact_state
  contact_city         = var.contact_city
  contact_address_line = var.contact_address_line
}

module "gke-cluster" {
  source             = "./modules/gke-cluster"
  gke_cluster_name   = var.gke_cluster_name
  gke_nood_pool_name = var.gke_nood_pool_name
  vpc                = module.network.vpc
  subnet             = module.network.subnet
  email              = module.service-account.service_account_name_email
  machine_type       = var.machine_type
}
