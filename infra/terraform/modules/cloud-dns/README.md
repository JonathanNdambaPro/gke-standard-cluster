# cloud-dns

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
| [google_dns_managed_zone.template-dns](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/dns_managed_zone) | resource |
| [google_dns_record_set.default](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/dns_record_set) | resource |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_dns_name"></a> [dns\_name](#input\_dns\_name) | value | `string` | n/a | yes |
| <a name="input_extern_ip_adress"></a> [extern\_ip\_adress](#input\_extern\_ip\_adress) | value | `list(string)` | n/a | yes |
| <a name="input_google_dns_managed_zone_ressource_name"></a> [google\_dns\_managed\_zone\_ressource\_name](#input\_google\_dns\_managed\_zone\_ressource\_name) | value | `string` | n/a | yes |

## Outputs

| Name | Description |
|------|-------------|
| <a name="output_nameservers"></a> [nameservers](#output\_nameservers) | The name servers of the managed zone |
<!-- END_TF_DOCS -->
