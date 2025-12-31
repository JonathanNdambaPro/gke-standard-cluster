# gke-cluster

<!-- BEGIN_TF_DOCS -->
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
| [google_container_cluster.gke_cluster](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/container_cluster) | resource |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_email"></a> [email](#input\_email) | value | `string` | n/a | yes |
| <a name="input_gke_cluster_name"></a> [gke\_cluster\_name](#input\_gke\_cluster\_name) | value | `string` | n/a | yes |
| <a name="input_subnet"></a> [subnet](#input\_subnet) | value | `string` | n/a | yes |
| <a name="input_vpc"></a> [vpc](#input\_vpc) | value | `string` | n/a | yes |

## Outputs

| Name | Description |
|------|-------------|
| <a name="output_gke_cluster_name"></a> [gke\_cluster\_name](#output\_gke\_cluster\_name) | n/a |
<!-- END_TF_DOCS -->
