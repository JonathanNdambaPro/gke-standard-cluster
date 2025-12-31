# Event-Driven API Helm Chart

Helm chart for deploying the Event-Driven API on Google Kubernetes Engine (GKE).

## Features

- **GKE Autopilot compatible**
- **Workload Identity** for secure GCP service authentication
- **GCE Ingress** with managed SSL certificates
- **Horizontal Pod Autoscaler** based on CPU utilization
- **Cloud Armor** security policy integration
- **Cloud CDN** caching support

---

## Prerequisites

- GKE cluster with Workload Identity enabled
- GCP Service Account with required permissions
- Terraform-managed infrastructure (network, DNS, security policies)

---

## Installation

```bash
# Example for a feature branch
helm upgrade --install event-driven-api ./infra/helm \
  --namespace feat-my-feature \
  --create-namespace \
  --set image.repository=<REGISTRY>/<IMAGE> \
  --set image.tag=<TAG> \
  --values infra/helm/values.yaml
```

---

## Configuration

### Service Account & Workload Identity

The chart creates a Kubernetes ServiceAccount that is linked to a GCP Service Account via Workload Identity.

```yaml
serviceAccount:
  create: true
  automount: true
  annotations:
    iam.gke.io/gcp-service-account: gke-sa@<PROJECT>.iam.gserviceaccount.com
  name: "event-driven-api-sa"
```

**Required Terraform resources:**
```hcl
# GCP Service Account
resource "google_service_account" "gke_sa" {
  account_id = "gke-sa"
}

# Workload Identity binding
resource "google_service_account_iam_member" "workload_identity_binding" {
  service_account_id = google_service_account.gke_sa.name
  role               = "roles/iam.workloadIdentityUser"
  member             = "serviceAccount:<PROJECT>.svc.id.goog[<NAMESPACE>/<K8S_SA_NAME>]"
}
```

**GCP Permissions needed on `gke-sa`:**
| Role | Purpose |
|------|---------|
| `roles/secretmanager.secretAccessor` | Access secrets from Secret Manager |
| `roles/storage.objectUser` | Read/write to GCS buckets |
| `roles/bigquery.dataEditor` | Write to BigQuery tables |
| `roles/bigquery.jobUser` | Run BigQuery jobs |

---

### Health Probes

Three probes are configured for pod health management:

| Probe | Path | Purpose | Timing |
|-------|------|---------|--------|
| **startupProbe** | `/` | Allow slow startup | 5s initial, max 150s |
| **readinessProbe** | `/` | Ready for traffic | 10s initial, every 10s |
| **livenessProbe** | `/` | Still alive (restart if fails) | 30s initial, every 15s |

```yaml
readinessProbe:
  httpGet:
    path: /
    port: 8000
  initialDelaySeconds: 10
  periodSeconds: 10
  timeoutSeconds: 5
  failureThreshold: 3

livenessProbe:
  httpGet:
    path: /
    port: 8000
  initialDelaySeconds: 30
  periodSeconds: 15
  timeoutSeconds: 5
  failureThreshold: 3

startupProbe:
  httpGet:
    path: /
    port: 8000
  initialDelaySeconds: 5
  periodSeconds: 5
  failureThreshold: 30  # 30 * 5s = 150s max
```

---

### Horizontal Pod Autoscaler (HPA)

Automatic scaling based on CPU utilization:

```yaml
autoscaling:
  enabled: true
  minReplicas: 1
  maxReplicas: 10
  targetCPUUtilizationPercentage: 80
```

**Note:** The percentage is calculated against `resources.requests.cpu`, not the limit.

---

### Resource Requests & Limits

```yaml
resources:
  requests:
    memory: 256Mi
    cpu: 300m
  limits:
    memory: 512Mi
    cpu: 600m
```

**Sizing guidelines:**
- `requests`: What K8s guarantees for scheduling
- `limits`: Maximum allowed (pod killed if exceeded for memory)
- HPA scales based on `requests`, not `limits`

---

### GCE Load Balancer (Ingress)

The chart configures a GCE Ingress with:

```yaml
ingress:
  enabled: true
  className: "gce"
  annotations:
    kubernetes.io/ingress.class: gce
    kubernetes.io/ingress.global-static-ip-name: template-external-ip
    networking.gke.io/managed-certificates: managed-cert-for-ingress
    networking.gke.io/v1beta1.FrontendConfig: my-frontend-config
```

**Components:**
- **Static IP**: Reserved external IP address
- **Managed Certificate**: Auto-provisioned SSL certificate
- **FrontendConfig**: HTTPS redirect, SSL policy

---

### BackendConfig

GCE Load Balancer backend configuration:

```yaml
backendConfig:
  name: my-backendconfig
  timeoutSec: 42
  drainingTimeoutSec: 62
  healthCheck:
    requestPath: /
    port: 8000
    checkIntervalSec: 15
  cdn:
    enabled: true
  securityPolicy:
    name: cloud-armor-policy
```

**Features:**
| Feature | Description |
|---------|-------------|
| **Health Check** | Custom health check path for LB |
| **CDN** | Cloud CDN caching for static content |
| **Cloud Armor** | WAF and DDoS protection |
| **Connection Draining** | Graceful shutdown timeout |

---

### FrontendConfig

HTTPS and SSL configuration:

```yaml
frontendConfig:
  name: my-frontend-config
  redirectToHttps: true
  sslPolicy: production-ssl-policy
```

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    GCE Load Balancer                        │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐ │
│  │ Static IP   │  │ SSL Cert    │  │ Cloud Armor Policy  │ │
│  └─────────────┘  └─────────────┘  └─────────────────────┘ │
└────────────────────────────┬────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────┐
│                     GKE Cluster                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │                    Ingress                           │   │
│  │  ┌─────────────┐  ┌─────────────┐                   │   │
│  │  │BackendConfig│  │FrontendConfig│                   │   │
│  │  └─────────────┘  └─────────────┘                   │   │
│  └────────────────────────┬────────────────────────────┘   │
│                           │                                 │
│                           ▼                                 │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              Service (NodePort)                      │   │
│  └────────────────────────┬────────────────────────────┘   │
│                           │                                 │
│            ┌──────────────┼──────────────┐                 │
│            ▼              ▼              ▼                 │
│       ┌─────────┐   ┌─────────┐   ┌─────────┐             │
│       │  Pod 1  │   │  Pod 2  │   │  Pod N  │             │
│       │   SA    │   │   SA    │   │   SA    │             │
│       └────┬────┘   └────┬────┘   └────┬────┘             │
│            │              │              │                  │
│            └──────────────┼──────────────┘                 │
│                           │                                 │
│                    Workload Identity                        │
└───────────────────────────┼─────────────────────────────────┘
                            │
                            ▼
              ┌─────────────────────────┐
              │   GCP Service Account   │
              │   (gke-sa@project)      │
              └────────────┬────────────┘
                           │
         ┌─────────────────┼─────────────────┐
         ▼                 ▼                 ▼
   ┌───────────┐    ┌───────────┐    ┌───────────┐
   │  Secret   │    │    GCS    │    │ BigQuery  │
   │  Manager  │    │           │    │           │
   └───────────┘    └───────────┘    └───────────┘
```

---

## Troubleshooting

### Pods stuck in Pending

```bash
kubectl describe pod <pod-name> -n default
```
Common causes:
- Insufficient CPU/Memory on nodes (wait for autoscaling or reduce requests)
- PVC not bound

### 403 Permission Denied on Secret Manager

1. Check Workload Identity binding exists:
```bash
gcloud iam service-accounts get-iam-policy gke-sa@<PROJECT>.iam.gserviceaccount.com
```

2. Verify K8s ServiceAccount has correct annotation:
```bash
kubectl get sa event-driven-api-sa -n default -o yaml
```

### Health check failures (502 errors)

1. Check pod logs:
```bash
kubectl logs -n default deployment/event-driven-api
```

2. Verify endpoint responds:
```bash
kubectl port-forward deployment/event-driven-api 8080:8000
curl http://localhost:8080/
```

### HPA not scaling down

- HPA calculates `current CPU / requests.cpu`
- If pods use more CPU than requested, percentage > 100%
- Increase `resources.requests.cpu` to match actual usage

---

## Values Reference

| Parameter | Description | Default |
|-----------|-------------|---------|
| `replicaCount` | Initial replicas (if HPA disabled) | `5` |
| `image.repository` | Container image repository | `stacksimplify/kube-nginxapp1` |
| `image.tag` | Container image tag | `1.0.0` |
| `fullnameOverride` | Override release name | `event-driven-api` |
| `serviceAccount.name` | K8s ServiceAccount name | `event-driven-api-sa` |
| `serviceAccount.annotations` | SA annotations (Workload Identity) | See values.yaml |
| `service.type` | Service type | `NodePort` |
| `service.port` | Service port | `8000` |
| `resources.requests.cpu` | CPU request | `300m` |
| `resources.requests.memory` | Memory request | `256Mi` |
| `resources.limits.cpu` | CPU limit | `600m` |
| `resources.limits.memory` | Memory limit | `512Mi` |
| `autoscaling.enabled` | Enable HPA | `true` |
| `autoscaling.minReplicas` | Min replicas | `1` |
| `autoscaling.maxReplicas` | Max replicas | `10` |
| `autoscaling.targetCPUUtilizationPercentage` | Target CPU % | `80` |
