# artifactory

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
| [google_artifact_registry_repository.repo-backend-dataascode-event-driven](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/artifact_registry_repository) | resource |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_artifactory_repository_id"></a> [artifactory\_repository\_id](#input\_artifactory\_repository\_id) | Nom du dépôt Artifact Registry où stocker les images Docker. | `string` | n/a | yes |
| <a name="input_region"></a> [region](#input\_region) | Région GCP où les ressources seront déployées. | `string` | n/a | yes |

## Outputs

| Name | Description |
|------|-------------|
| <a name="output_artifactory_repository_id"></a> [artifactory\_repository\_id](#output\_artifactory\_repository\_id) | Noms de l'artifactory créés |
<!-- END OF PRE-COMMIT-TERRAFORM DOCS HOOK -->
