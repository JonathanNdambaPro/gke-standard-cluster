# terraform

<!-- BEGINNING OF PRE-COMMIT-TERRAFORM DOCS HOOK -->
## Requirements

| Name | Version |
|------|---------|
| <a name="requirement_google"></a> [google](#requirement\_google) | ~> 7.12.0 |

## Providers

No providers.

## Modules

| Name | Source | Version |
|------|--------|---------|
| <a name="module_cloud-dns"></a> [cloud-dns](#module\_cloud-dns) | ./modules/cloud-dns | n/a |
| <a name="module_cloud-domains"></a> [cloud-domains](#module\_cloud-domains) | ./modules/cloud-domains | n/a |
| <a name="module_gke-cluster"></a> [gke-cluster](#module\_gke-cluster) | ./modules/gke-cluster | n/a |
| <a name="module_network"></a> [network](#module\_network) | ./modules/network | n/a |
| <a name="module_security"></a> [security](#module\_security) | ./modules/security | n/a |
| <a name="module_service-account"></a> [service-account](#module\_service-account) | ./modules/service-accounts | n/a |

## Resources

No resources.

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_contact_address_line"></a> [contact\_address\_line](#input\_contact\_address\_line) | n/a | `string` | n/a | yes |
| <a name="input_contact_city"></a> [contact\_city](#input\_contact\_city) | n/a | `string` | n/a | yes |
| <a name="input_contact_country_code"></a> [contact\_country\_code](#input\_contact\_country\_code) | n/a | `string` | n/a | yes |
| <a name="input_contact_email"></a> [contact\_email](#input\_contact\_email) | n/a | `string` | n/a | yes |
| <a name="input_contact_name"></a> [contact\_name](#input\_contact\_name) | Cloud Domains Contact Info | `string` | n/a | yes |
| <a name="input_contact_phone"></a> [contact\_phone](#input\_contact\_phone) | n/a | `string` | n/a | yes |
| <a name="input_contact_postal_code"></a> [contact\_postal\_code](#input\_contact\_postal\_code) | n/a | `string` | n/a | yes |
| <a name="input_contact_state"></a> [contact\_state](#input\_contact\_state) | n/a | `string` | n/a | yes |
| <a name="input_dns_name"></a> [dns\_name](#input\_dns\_name) | value | `string` | n/a | yes |
| <a name="input_environment"></a> [environment](#input\_environment) | Environment Variable used as a prefix | `string` | n/a | yes |
| <a name="input_gke_cluster_name"></a> [gke\_cluster\_name](#input\_gke\_cluster\_name) | value | `string` | n/a | yes |
| <a name="input_gke_nood_pool_name"></a> [gke\_nood\_pool\_name](#input\_gke\_nood\_pool\_name) | value | `string` | n/a | yes |
| <a name="input_gke_service_account_name"></a> [gke\_service\_account\_name](#input\_gke\_service\_account\_name) | value | `string` | n/a | yes |
| <a name="input_google_dns_managed_zone_ressource_name"></a> [google\_dns\_managed\_zone\_ressource\_name](#input\_google\_dns\_managed\_zone\_ressource\_name) | value | `string` | n/a | yes |
| <a name="input_ip_address_ressource_name"></a> [ip\_address\_ressource\_name](#input\_ip\_address\_ressource\_name) | value | `string` | n/a | yes |
| <a name="input_machine_type"></a> [machine\_type](#input\_machine\_type) | Compute Engine Machine Type | `string` | n/a | yes |
| <a name="input_project"></a> [project](#input\_project) | GCP project ID where all resources will be created. | `string` | n/a | yes |
| <a name="input_region"></a> [region](#input\_region) | GCP region where regional resources will be deployed. | `string` | n/a | yes |
| <a name="input_ssl_policy_name"></a> [ssl\_policy\_name](#input\_ssl\_policy\_name) | value | `string` | n/a | yes |
| <a name="input_subnet_ip_cidr_range"></a> [subnet\_ip\_cidr\_range](#input\_subnet\_ip\_cidr\_range) | value | `string` | n/a | yes |
| <a name="input_subnet_name"></a> [subnet\_name](#input\_subnet\_name) | value | `string` | n/a | yes |
| <a name="input_vpc_name"></a> [vpc\_name](#input\_vpc\_name) | value | `string` | n/a | yes |

## Outputs

No outputs.
<!-- END OF PRE-COMMIT-TERRAFORM DOCS HOOK -->
