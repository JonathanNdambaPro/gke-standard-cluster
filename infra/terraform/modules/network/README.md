# network

<!-- BEGINNING OF PRE-COMMIT-TERRAFORM DOCS HOOK -->
## Requirements

No requirements.

## Providers

| Name | Version |
|------|---------|
| <a name="provider_google"></a> [google](#provider\_google) | n/a |

## Modules

No modules.

## Resources

| Name | Type |
|------|------|
| [google_compute_global_address.ip_address](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/compute_global_address) | resource |
| [google_compute_network.myvpc](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/compute_network) | resource |
| [google_compute_subnetwork.mysubnet](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/compute_subnetwork) | resource |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_ip_address_ressource_name"></a> [ip\_address\_ressource\_name](#input\_ip\_address\_ressource\_name) | value | `string` | n/a | yes |
| <a name="input_subnet_ip_cidr_range"></a> [subnet\_ip\_cidr\_range](#input\_subnet\_ip\_cidr\_range) | value | `string` | n/a | yes |
| <a name="input_subnet_name"></a> [subnet\_name](#input\_subnet\_name) | value | `string` | n/a | yes |
| <a name="input_vpc_name"></a> [vpc\_name](#input\_vpc\_name) | value | `string` | n/a | yes |

## Outputs

| Name | Description |
|------|-------------|
| <a name="output_extern_ip_adress"></a> [extern\_ip\_adress](#output\_extern\_ip\_adress) | value |
| <a name="output_subnet"></a> [subnet](#output\_subnet) | Noms de l'artifactory créés |
| <a name="output_vpc"></a> [vpc](#output\_vpc) | Noms de l'artifactory créés |
<!-- END OF PRE-COMMIT-TERRAFORM DOCS HOOK -->
