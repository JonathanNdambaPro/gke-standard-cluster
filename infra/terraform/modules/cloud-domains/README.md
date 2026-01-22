# cloud-domains

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
| [google_clouddomains_registration.my_domain](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/clouddomains_registration) | resource |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_contact_address_line"></a> [contact\_address\_line](#input\_contact\_address\_line) | n/a | `string` | n/a | yes |
| <a name="input_contact_city"></a> [contact\_city](#input\_contact\_city) | n/a | `string` | n/a | yes |
| <a name="input_contact_country_code"></a> [contact\_country\_code](#input\_contact\_country\_code) | n/a | `string` | n/a | yes |
| <a name="input_contact_email"></a> [contact\_email](#input\_contact\_email) | n/a | `string` | n/a | yes |
| <a name="input_contact_name"></a> [contact\_name](#input\_contact\_name) | Contact Params | `string` | n/a | yes |
| <a name="input_contact_phone"></a> [contact\_phone](#input\_contact\_phone) | n/a | `string` | n/a | yes |
| <a name="input_contact_postal_code"></a> [contact\_postal\_code](#input\_contact\_postal\_code) | n/a | `string` | n/a | yes |
| <a name="input_contact_state"></a> [contact\_state](#input\_contact\_state) | n/a | `string` | n/a | yes |
| <a name="input_create_domain_registration"></a> [create\_domain\_registration](#input\_create\_domain\_registration) | Whether to create the registration | `bool` | `true` | no |
| <a name="input_domain_name"></a> [domain\_name](#input\_domain\_name) | The domain name to register (e.g. example.com) | `string` | n/a | yes |
| <a name="input_name_servers"></a> [name\_servers](#input\_name\_servers) | List of name servers from Cloud DNS | `list(string)` | n/a | yes |
| <a name="input_yearly_price_units"></a> [yearly\_price\_units](#input\_yearly\_price\_units) | Maximum price in USD you are willing to pay | `string` | `"12"` | no |

## Outputs

No outputs.
<!-- END OF PRE-COMMIT-TERRAFORM DOCS HOOK -->
