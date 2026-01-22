# pubsub

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
| [google_pubsub_subscription.dlq_subscription](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/pubsub_subscription) | resource |
| [google_pubsub_topic.dlq](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/pubsub_topic) | resource |
| [google_pubsub_topic.topic](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/pubsub_topic) | resource |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_topic_name"></a> [topic\_name](#input\_topic\_name) | Pub/Sub topic name. | `string` | n/a | yes |

## Outputs

| Name | Description |
|------|-------------|
| <a name="output_pubsub_dlq_subscription_name"></a> [pubsub\_dlq\_subscription\_name](#output\_pubsub\_dlq\_subscription\_name) | Name of the DLQ subscription |
| <a name="output_pubsub_dlq_topic_name"></a> [pubsub\_dlq\_topic\_name](#output\_pubsub\_dlq\_topic\_name) | Name of the Dead Letter Queue topic |
| <a name="output_pubsub_topic"></a> [pubsub\_topic](#output\_pubsub\_topic) | Full Pub/Sub topic resource for dependency management |
| <a name="output_pubsub_topic_id"></a> [pubsub\_topic\_id](#output\_pubsub\_topic\_id) | ID of the Pub/Sub topic |
| <a name="output_pubsub_topic_name"></a> [pubsub\_topic\_name](#output\_pubsub\_topic\_name) | Name of the Pub/Sub topic |
<!-- END_TF_DOCS -->
