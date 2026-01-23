locals {
  is_prod = terraform.workspace == "default"

  # Dynamic configuration based on workspace
  vpc_name         = local.is_prod ? module.network[0].vpc : data.google_compute_network.vpc[0].name
  subnet_name      = local.is_prod ? module.network[0].subnet : data.google_compute_subnetwork.subnet[0].name
  gke_cluster_name = local.is_prod ? module.gke-cluster[0].gke_cluster_name : data.google_container_cluster.gke_cluster[0].name
}

# ==============================================================================
# CORE INFRASTRUCTURE
# ==============================================================================

module "google-api" {
  count  = local.is_prod ? 1 : 0
  source = "./modules/google-api"
}

module "network" {
  count                     = local.is_prod ? 1 : 0
  source                    = "./modules/network"
  subnet_ip_cidr_range      = var.subnet_ip_cidr_range
  vpc_name                  = var.vpc_name
  subnet_name               = var.subnet_name
  ip_address_ressource_name = var.ip_address_ressource_name
}

# Fallbacks for ephemeral workspaces
data "google_compute_network" "vpc" {
  count   = local.is_prod ? 0 : 1
  name    = var.vpc_name
  project = var.project
}

data "google_compute_subnetwork" "subnet" {
  count   = local.is_prod ? 0 : 1
  name    = var.subnet_name
  region  = var.region
  project = var.project
}

module "cloud-dns" {
  count                                  = local.is_prod ? 1 : 0
  source                                 = "./modules/cloud-dns"
  dns_name                               = var.dns_name
  google_dns_managed_zone_ressource_name = var.google_dns_managed_zone_ressource_name
  extern_ip_adress                       = [module.network[0].extern_ip_adress]
}

module "security" {
  count                = local.is_prod ? 1 : 0
  source               = "./modules/security"
  ssl_policy_name      = var.ssl_policy_name
  security_policy_name = var.security_policy_name
}

# ==============================================================================
# COMPUTE & IAM
# ==============================================================================

module "service-account" {
  count                    = local.is_prod ? 1 : 0
  source                   = "./modules/service-accounts"
  gke_service_account_name = var.gke_service_account_name
  project                  = var.project
}

data "google_service_account" "gke_sa" {
  count      = local.is_prod ? 0 : 1
  account_id = var.gke_service_account_name
  project    = var.project
}

# Workload Identity binding for Ephemeral Environments
resource "google_service_account_iam_member" "workload_identity_binding_ephemeral" {
  count              = local.is_prod ? 0 : 1
  service_account_id = data.google_service_account.gke_sa[0].name
  role               = "roles/iam.workloadIdentityUser"
  member             = "serviceAccount:${var.project}.svc.id.goog[${var.eventarc_trigger_namespace}/event-driven-api-sa]"
}

module "gke-cluster" {
  count            = local.is_prod ? 1 : 0
  source           = "./modules/gke-cluster"
  gke_cluster_name = var.gke_cluster_name
  vpc              = module.network[0].vpc
  subnet           = module.network[0].subnet
  email            = module.service-account[0].service_account_gke_email
}

data "google_container_cluster" "gke_cluster" {
  count    = local.is_prod ? 0 : 1
  name     = var.gke_cluster_name
  location = var.region
  project  = var.project
}

# ==============================================================================
# APPLICATION SUPPORT
# ==============================================================================

module "artifactory" {
  count                     = local.is_prod ? 1 : 0
  source                    = "./modules/artifactory"
  region                    = var.region
  artifactory_repository_id = var.artifactory_repository_id
}

module "cloud-domains" {
  count                      = local.is_prod ? 1 : 0
  source                     = "./modules/cloud-domains"
  create_domain_registration = var.create_domain_registration
  domain_name                = trimsuffix(var.dns_name, ".")
  name_servers               = module.cloud-dns[0].nameservers
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

# ==============================================================================
# EVENT DRIVEN ARCHITECTURE
# ==============================================================================

module "pubsub" {
  for_each   = var.event_pipelines
  source     = "./modules/pubsub"
  topic_name = local.is_prod ? each.value.topic_name : "${each.value.topic_name}-${terraform.workspace}"
}

module "eventarc" {
  for_each = var.event_pipelines
  source   = "./modules/eventarc"

  project               = var.project
  region                = var.region
  service_account_email = local.is_prod ? module.service-account[0].service_account_eventarc_name_email : data.google_service_account.gke_sa[0].email

  label              = each.value.label
  source_topic_name  = module.pubsub[each.key].pubsub_topic_id
  eventarc_name      = local.is_prod ? "trigger-${each.key}" : "trigger-${each.key}-${terraform.workspace}"
  environment_filter = var.eventarc_environment_filter

  cluster              = local.is_prod ? module.gke-cluster[0].gke_cluster_name : data.google_container_cluster.gke_cluster[0].name
  service              = var.eventarc_service_name
  namespace            = var.eventarc_trigger_namespace
  gke_run_service_path = each.value.path

  depends_on = [module.pubsub]
}

# ==============================================================================
# MONITORING EMAIL NOTIFICATION
# ==============================================================================

module "monitoring" {
  count              = local.is_prod ? 1 : 0
  source             = "./modules/monitoring"
  project_id         = var.project
  notification_email = var.contact_email
  dlq_subscriptions  = [for p in module.pubsub : p.pubsub_dlq_subscription_name]
}
