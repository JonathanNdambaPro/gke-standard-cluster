# Configuration Sync

## Source of Truth: `config.yaml`

The `config.yaml` file at the project root is the **source of truth** for shared values. The CI/CD workflow automatically parses it using `yq`.

```yaml
# Central project configuration
gcp:
  project_id: dataascode
  region: europe-west1

gke:
  cluster_name: template-gke-cluster

artifactory:
  repository_id: docker-repository

app:
  image_name: event-driven
  service_name: event-driven-api  # Must match fullnameOverride in values.yaml
```

**⚠️ The following files must be manually synchronized with `config.yaml`:**

- `infra/terraform/tfvars/main.tfvars`
- `infra/terraform/tfvars/local.tfvars`
- `infra/helm/values.yaml`

## Mapping Table

| Value | `.github/workflows/main.yml` | `infra/terraform/tfvars/main.tfvars` | `infra/helm/values.yaml` |
|-------|------------------------------|--------------------------------------|--------------------------|
| **Project ID** | `GCP_PROJECT_ID: dataascode` | `project = "dataascode"` | - |
| **Region** | `GCP_ZONE: europe-west1` | `region = "europe-west1"` | - |
| **Cluster Name** | `GKE_CLUSTER_NAME: template-gke-cluster` | `gke_cluster_name = "template-gke-cluster"` | - |
| **Artifact Repository** | `REPO_ARTIFACTORY: docker-repository` | `artifactory_repository_id = "docker-repository"` | - |
| **K8s Service Name** | - | `eventarc_service_name = "event-driven-api"` | `fullnameOverride: "event-driven-api"` |

### Temporal Cloud Configuration

| Value | Location | Description |
|-------|----------|-------------|
| **TEMPORAL_ADDRESS** | `api/utils/config.py` | Temporal Cloud endpoint |
| **TEMPORAL_NAMESPACE** | `api/utils/config.py` | Temporal namespace |
| **TEMPORAL_API_KEY** | Google Secret Manager | API key for authentication |

## File Details

### `.github/workflows/main.yml`

```yaml
env:
  GCP_PROJECT_ID: dataascode          # → main.tfvars: project
  GCP_ZONE: europe-west1              # → main.tfvars: region
  REPO_ARTIFACTORY: docker-repository # → main.tfvars: artifactory_repository_id
  GKE_CLUSTER_NAME: template-gke-cluster # → main.tfvars: gke_cluster_name
```

### `infra/terraform/tfvars/main.tfvars`

```hcl
project = "dataascode"                      # → main.yml: GCP_PROJECT_ID
region  = "europe-west1"                    # → main.yml: GCP_ZONE
gke_cluster_name = "template-gke-cluster"   # → main.yml: GKE_CLUSTER_NAME
artifactory_repository_id = "docker-repository" # → main.yml: REPO_ARTIFACTORY
eventarc_service_name = "event-driven-api"  # → values.yaml: fullnameOverride

# Event pipelines - add new topics/triggers here
event_pipelines = {
  ingest = {
    topic_name = "event-ingestion"
    path       = "/api/v1/ingest_event"
    label      = "event-driven-ingest"
  }
}
```

### `infra/helm/values.yaml`

```yaml
fullnameOverride: "event-driven-api"  # → main.tfvars: eventarc_service_name
```

## Modification Checklist

### Change GCP Project Name

- [ ] `.github/workflows/main.yml` → `GCP_PROJECT_ID`
- [ ] `infra/terraform/tfvars/main.tfvars` → `project`
- [ ] `infra/terraform/tfvars/local.tfvars` → `project`

### Change Region

- [ ] `.github/workflows/main.yml` → `GCP_ZONE`
- [ ] `infra/terraform/tfvars/main.tfvars` → `region`
- [ ] `infra/terraform/tfvars/local.tfvars` → `region`

### Change GKE Cluster Name

- [ ] `.github/workflows/main.yml` → `GKE_CLUSTER_NAME`
- [ ] `infra/terraform/tfvars/main.tfvars` → `gke_cluster_name`
- [ ] `infra/terraform/tfvars/local.tfvars` → `gke_cluster_name`

### Change Artifact Registry Repository Name

- [ ] `.github/workflows/main.yml` → `REPO_ARTIFACTORY`
- [ ] `infra/terraform/tfvars/main.tfvars` → `artifactory_repository_id`
- [ ] `infra/terraform/tfvars/local.tfvars` → `artifactory_repository_id`

### Change Kubernetes Service Name

- [ ] `infra/terraform/tfvars/main.tfvars` → `eventarc_service_name`
- [ ] `infra/terraform/tfvars/local.tfvars` → `eventarc_service_name`
- [ ] `infra/helm/values.yaml` → `fullnameOverride`

## ⚠️ Important Notes

1. **K8s service name** (`eventarc_service_name` / `fullnameOverride`) must be identical because Eventarc uses this name to route events to the correct service.

2. **Artifact Registry repository** must exist before pushing Docker images.

3. **GKE cluster** must exist before Helm deployment.
