# Kubernetes & Ingress ☸️

## Global Architecture

The architecture relies on **GKE Standard** for container orchestration, coupled with **GCE Ingress** for global traffic management and **Workload Identity** for secure GCP access.

```mermaid
graph TD
    user(("User")) -->|HTTPS| GSLB["Global Load Balancer"]

    subgraph GCP["Google Cloud Platform"]
        GSLB -->|"Managed Cert"| SSL{"SSL Termination"}
        SSL -->|HTTP| Backend["Backend Service"]

        subgraph GKECluster["GKE Cluster"]
            Backend -->|"NodePort"| Service["K8s Service"]

            subgraph Workloads["Workloads"]
                Service -->|"Selector"| Pod1["API Pod 1"]
                Service -->|"Selector"| Pod2["API Pod 2"]
            end

            HPA["HPA"] -.->|"CPU > 80%"| Workloads

            Pod1 -.->|"Workload Identity"| GSA["GCP Service Account"]
        end

        GSA -->|IAM| SecretMgr["Secret Manager"]
        GSA -->|IAM| BigQuery["BigQuery"]
        GSA -->|IAM| GCS["Cloud Storage"]
    end

    style GSLB fill:#4285f4,stroke:#fff,color:#fff
    style GKECluster fill:#34a853,stroke:#fff,color:#fff
    style Workloads fill:#e6f4ea,stroke:#34a853
```

## Detailed Components

### 1. Ingress (GCE L7 Load Balancer)

We use the Google Cloud native Ingress controller (`gce`), which provisions a Global External HTTP(S) Load Balancer.

*   **Managed Certificate** (`ManagedCertificate`): Automatically provisions and renews Google-managed SSL certificates.
    *   **Domain**: `templatejojotest.com` (Production)
    *   **Status Check**: `kubectl get managedcertificate` (State should be `ACTIVE`).
*   **FrontendConfig**: Controls the Load Balancer frontend behavior.
    *   **HTTP-to-HTTPS Redirect**: Enforced automatically.
    *   **SSL Policy**: Uses a modern SSL policy (TLS 1.2+).
*   **BackendConfig**: Controls backend configuration.
    *   **Health Checks**: Custom health check path (`/`) and timeout settings.
    *   **Cloud Armor**: (Optional) WAF integration.
    *   **Connection Draining**: Timeout ensuring graceful shutdowns.

### 2. Workload Identity (Security)

We do **not** use JSON keys. We use **Workload Identity** to map Kubernetes Service Accounts (KSA) to Google Service Accounts (GSA).

```mermaid
sequenceDiagram
    participant Pod
    participant MetadataServer
    participant IAM

    Pod->>MetadataServer: Request Token (audience: gcp)
    MetadataServer->>IAM: Exchange K8s Token for GCP Token
    IAM-->>MetadataServer: Valid GCP Access Token
    MetadataServer-->>Pod: GCP Access Token
    Pod->>GCS: Access Bucket (Authorized)
```

**Configuration steps:**
1.  **GCP**: Create GSA (`gke-sa@project.iam.gserviceaccount.com`).
2.  **IAM**: Grant `roles/iam.workloadIdentityUser` to `serviceAccount:project.svc.id.goog[namespace/ksa-name]`.
3.  **K8s**: Annotate KSA with `iam.gke.io/gcp-service-account: gke-sa@...`.

### 3. Scaling (HPA)

The Horizontal Pod Autoscaler (HPA) automatically adjusts the number of pods based on CPU utilization.

*   **Metric**: `targetCPUUtilizationPercentage: 80`
*   **Min Replicas**: `1` (Can be raised for prod high-availability)
*   **Max Replicas**: `10`
*   **Behavior**: When average CPU across pods exceeds 80% of the *Requested* CPU, new replicas are added.

## Deployment Strategy

### Production (`default` namespace)
*   **DNS**: `templatejojotest.com`
*   **Certificate**: Production Managed Certificate.
*   **Ingress**: Static IP reservation (`google_compute_global_address`).

### ⚡ Ephemeral Environments (`feat-*`)
*   **Namespace**: Dynamic (e.g., `feat-login`).
*   **Routing**:
    *   Deployed via Helm.
    *   Uses the **same** Ingress Controller but differentiates via **Traffic Splitting** (if configuring Istio) or separate Ingress resources (if configuring distinct hostnames).
    *   *Current Setup*: Deploys a separate Ingress. Note that creating multiple GCE Ingresses can take time (~5-10 mins) for LB provisioning.

## Troubleshooting 🛠️

### ⚠️ 502 Bad Gateway
This is the most common error with GCE Ingress.

| Cause | Verification | Fix |
|-------|--------------|-----|
| **Pod Startup** | `kubectl get pods` | Wait for `Running` state (Probe success). |
| **Health Check** | `kubectl describe ingress` | Check `Backends` section for `Unhealthy`. |
| **Firewall** | `gcloud compute firewall-rules list` | Ensure GFE IPs (130.211.0.0/22, 35.191.0.0/16) can reach Nodes. |
| **TargetPort** | `kubectl get svc` | Service `targetPort` **must** match Pod `containerPort`. |

### ⚠️ 403 Permission Denied (GCP)
If the pod cannot access GCS or Secret Manager:

1.  **Check Annotation**:
    ```bash
    kubectl get sa -n <namespace> <sa-name> -o yaml
    # Look for: iam.gke.io/gcp-service-account
    ```
2.  **Check Binding**:
    ```bash
    gcloud iam service-accounts get-iam-policy <gsa-email>
    # Look for: roles/iam.workloadIdentityUser bound to the correct K8s SA.
    ```

### ⚠️ Certificate Provisioning Fails
*   **Check DNS**: The domain **must** point to the Ingress static IP. Google won't provision the cert if DNS validation fails.
*   **Check Quota**: Ensure you haven't exceeded SSL cert quotas.
