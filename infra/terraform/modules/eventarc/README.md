# eventarc

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
| [google_eventarc_trigger.gke_trigger](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/eventarc_trigger) | resource |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_cluster"></a> [cluster](#input\_cluster) | Name of the cluster gke | `string` | n/a | yes |
| <a name="input_eventarc_name"></a> [eventarc\_name](#input\_eventarc\_name) | The service account to use to execute the Eventarc triggers | `string` | n/a | yes |
| <a name="input_gke_run_service_path"></a> [gke\_run\_service\_path](#input\_gke\_run\_service\_path) | Path within the service to send events to | `string` | `"/"` | no |
| <a name="input_label"></a> [label](#input\_label) | Label for the Eventarc trigger | `string` | n/a | yes |
| <a name="input_namespace"></a> [namespace](#input\_namespace) | Namespace where the service is deployed | `string` | `"default"` | no |
| <a name="input_project"></a> [project](#input\_project) | The GCP project ID where resources will be created | `string` | n/a | yes |
| <a name="input_region"></a> [region](#input\_region) | Region where GCP services will be deployed | `string` | `"europe-west9"` | no |
| <a name="input_service"></a> [service](#input\_service) | Name of the GKE service to receive events | `string` | n/a | yes |
| <a name="input_service_account_email"></a> [service\_account\_email](#input\_service\_account\_email) | The service account to use to execute the Eventarc triggers | `string` | n/a | yes |
| <a name="input_source_topic_name"></a> [source\_topic\_name](#input\_source\_topic\_name) | The service account to use to execute the Eventarc triggers | `string` | n/a | yes |

## Outputs

| Name | Description |
|------|-------------|
| <a name="output_gke_trigger_id"></a> [gke\_trigger\_id](#output\_gke\_trigger\_id) | IDs of the created GKE Eventarc triggers |
| <a name="output_gke_trigger_name"></a> [gke\_trigger\_name](#output\_gke\_trigger\_name) | Names of the created GKE Eventarc triggers |
<!-- END_TF_DOCS -->
