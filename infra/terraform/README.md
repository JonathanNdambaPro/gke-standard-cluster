# terraform

<!-- BEGIN_TF_DOCS -->
## Requirements

| Name | Version |
|------|---------|
| <a name="requirement_google"></a> [google](#requirement\_google) | ~> 7.12.0 |

## Providers

No providers.

## Modules

| Name | Source | Version |
|------|--------|---------|
| <a name="module_artifactory"></a> [artifactory](#module\_artifactory) | ./modules/artifactory | n/a |
| <a name="module_cloud-dns"></a> [cloud-dns](#module\_cloud-dns) | ./modules/cloud-dns | n/a |
| <a name="module_cloud-domains"></a> [cloud-domains](#module\_cloud-domains) | ./modules/cloud-domains | n/a |
| <a name="module_eventarc"></a> [eventarc](#module\_eventarc) | ./modules/eventarc | n/a |
| <a name="module_gke-cluster"></a> [gke-cluster](#module\_gke-cluster) | ./modules/gke-cluster | n/a |
| <a name="module_network"></a> [network](#module\_network) | ./modules/network | n/a |
| <a name="module_pubsub"></a> [pubsub](#module\_pubsub) | ./modules/pubsub | n/a |
| <a name="module_security"></a> [security](#module\_security) | ./modules/security | n/a |
| <a name="module_service-account"></a> [service-account](#module\_service-account) | ./modules/service-accounts | n/a |

## Resources

No resources.

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_artifactory_repository_id"></a> [artifactory\_repository\_id](#input\_artifactory\_repository\_id) | Nom du dépôt Artifact Registry où stocker les images Docker. | `string` | n/a | yes |
| <a name="input_contact_address_line"></a> [contact\_address\_line](#input\_contact\_address\_line) | n/a | `string` | n/a | yes |
| <a name="input_contact_city"></a> [contact\_city](#input\_contact\_city) | n/a | `string` | n/a | yes |
| <a name="input_contact_country_code"></a> [contact\_country\_code](#input\_contact\_country\_code) | n/a | `string` | n/a | yes |
| <a name="input_contact_email"></a> [contact\_email](#input\_contact\_email) | n/a | `string` | n/a | yes |
| <a name="input_contact_name"></a> [contact\_name](#input\_contact\_name) | Cloud Domains Contact Info | `string` | n/a | yes |
| <a name="input_contact_phone"></a> [contact\_phone](#input\_contact\_phone) | n/a | `string` | n/a | yes |
| <a name="input_contact_postal_code"></a> [contact\_postal\_code](#input\_contact\_postal\_code) | n/a | `string` | n/a | yes |
| <a name="input_contact_state"></a> [contact\_state](#input\_contact\_state) | n/a | `string` | n/a | yes |
| <a name="input_create_domain_registration"></a> [create\_domain\_registration](#input\_create\_domain\_registration) | Whether to create the Cloud Domain registration | `bool` | `true` | no |
| <a name="input_dns_name"></a> [dns\_name](#input\_dns\_name) | value | `string` | n/a | yes |
| <a name="input_event_type"></a> [event\_type](#input\_event\_type) | The event type to trigger on (default: Pub/Sub message published) | `string` | `"google.cloud.pubsub.topic.v1.messagePublished"` | no |
| <a name="input_eventarc_name"></a> [eventarc\_name](#input\_eventarc\_name) | Name of the Eventarc trigger | `string` | n/a | yes |
| <a name="input_eventarc_service_name"></a> [eventarc\_service\_name](#input\_eventarc\_service\_name) | Name of the Kubernetes service receiving events | `string` | n/a | yes |
| <a name="input_eventarc_trigger_namespace"></a> [eventarc\_trigger\_namespace](#input\_eventarc\_trigger\_namespace) | Namespace of the Kubernetes service | `string` | `"default"` | no |
| <a name="input_gke_cluster_name"></a> [gke\_cluster\_name](#input\_gke\_cluster\_name) | value | `string` | n/a | yes |
| <a name="input_gke_run_service_path"></a> [gke\_run\_service\_path](#input\_gke\_run\_service\_path) | Path for the GKE service receiving events | `string` | `"/"` | no |
| <a name="input_gke_service_account_name"></a> [gke\_service\_account\_name](#input\_gke\_service\_account\_name) | value | `string` | n/a | yes |
| <a name="input_google_dns_managed_zone_ressource_name"></a> [google\_dns\_managed\_zone\_ressource\_name](#input\_google\_dns\_managed\_zone\_ressource\_name) | value | `string` | n/a | yes |
| <a name="input_ip_address_ressource_name"></a> [ip\_address\_ressource\_name](#input\_ip\_address\_ressource\_name) | value | `string` | n/a | yes |
| <a name="input_label"></a> [label](#input\_label) | Label for the Eventarc trigger | `string` | n/a | yes |
| <a name="input_project"></a> [project](#input\_project) | GCP project ID where all resources will be created. | `string` | n/a | yes |
| <a name="input_region"></a> [region](#input\_region) | GCP region where regional resources will be deployed. | `string` | n/a | yes |
| <a name="input_security_policy_name"></a> [security\_policy\_name](#input\_security\_policy\_name) | The name of the Cloud Armor security policy | `string` | `"cloud-armor-policy"` | no |
| <a name="input_ssl_policy_name"></a> [ssl\_policy\_name](#input\_ssl\_policy\_name) | value | `string` | n/a | yes |
| <a name="input_subnet_ip_cidr_range"></a> [subnet\_ip\_cidr\_range](#input\_subnet\_ip\_cidr\_range) | value | `string` | n/a | yes |
| <a name="input_subnet_name"></a> [subnet\_name](#input\_subnet\_name) | value | `string` | n/a | yes |
| <a name="input_topic_name"></a> [topic\_name](#input\_topic\_name) | Pub/Sub topic name. | `string` | n/a | yes |
| <a name="input_vpc_name"></a> [vpc\_name](#input\_vpc\_name) | value | `string` | n/a | yes |
| <a name="input_yearly_price_units"></a> [yearly\_price\_units](#input\_yearly\_price\_units) | Maximum price in USD you are willing to pay for the domain | `string` | `"12"` | no |

## Outputs

No outputs.
<!-- END_TF_DOCS -->
