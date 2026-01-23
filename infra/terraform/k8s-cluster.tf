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
  source               = "./modules/security"
  ssl_policy_name      = var.ssl_policy_name
  security_policy_name = var.security_policy_name
}

module "service-account" {
  source                   = "./modules/service-accounts"
  gke_service_account_name = var.gke_service_account_name
  project                  = var.project
}

module "cloud-domains" {
  source                     = "./modules/cloud-domains"
  create_domain_registration = var.create_domain_registration
  domain_name                = trimsuffix(var.dns_name, ".") # Cloud Domains doesn't want the trailing dot
  name_servers               = module.cloud-dns.nameservers
  yearly_price_units         = var.yearly_price_units

  contact_name         = var.contact_name
  contact_email        = var.contact_email
  contact_phone        = var.contact_phone
  contact_country_code = var.contact_country_code
  contact_postal_code  = var.contact_postal_code
  contact_state        = var.contact_state
  contact_city         = var.contact_city
  contact_address_line = var.contact_address_line
}

# Create Pub/Sub topics for each pipeline
module "pubsub" {
  for_each   = var.event_pipelines
  source     = "./modules/pubsub"
  topic_name = each.value.topic_name
}

# Create Eventarc triggers for each pipeline
module "eventarc" {
  for_each              = var.event_pipelines
  source                = "./modules/eventarc"
  project               = var.project
  region                = var.region
  service_account_email = module.service-account.service_account_eventarc_name_email
  label                 = each.value.label
  source_topic_name     = module.pubsub[each.key].pubsub_topic_id
  eventarc_name         = "trigger-${each.key}"
  cluster               = module.gke-cluster.gke_cluster_name
  service               = var.eventarc_service_name
  namespace             = var.eventarc_trigger_namespace
  gke_run_service_path  = each.value.path
  environment_filter    = var.eventarc_environment_filter

  depends_on = [module.service-account, module.pubsub]
}

module "gke-cluster" {
  source           = "./modules/gke-cluster"
  gke_cluster_name = var.gke_cluster_name
  vpc              = module.network.vpc
  subnet           = module.network.subnet
  email            = module.service-account.service_account_gke_email
}

module "artifactory" {
  source                    = "./modules/artifactory"
  region                    = var.region
  artifactory_repository_id = var.artifactory_repository_id
}

module "monitoring" {
  source             = "./modules/monitoring"
  project_id         = var.project
  notification_email = var.contact_email
  dlq_subscriptions  = [for p in module.pubsub : p.pubsub_dlq_subscription_name]
}
