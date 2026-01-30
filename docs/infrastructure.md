# Infrastructure (Terraform) 🏗️

The infrastructure is managed as code (IaC) using Terraform. It follows a modular design to ensure reusability, consistency, and separation of concerns.

## Global Infrastructure Schema

```mermaid
graph TD
    subgraph GCP["GCP Project: dataascode"]
        subgraph NetLayer["Network Layer"]
            VPC["VPC Network"]
            Subnet["Subnet (k8s-subnet)"]
            ExtIP["Global Static IP"]
            CloudDNS["Cloud DNS Zone"]

            VPC --> Subnet
            ExtIP -.->|Link| CloudDNS
        end

        subgraph ComputeLayer["Compute Layer"]
            GKE["GKE Standard Cluster"]
            NodePools["Node Pools"]

            Subnet --> GKE
            GKE --> NodePools
        end

        subgraph SecurityLayer["Security Layer"]
            SSL["SSL Policy"]
            Armor["Cloud Armor Policy"]
            IAM["Service Accounts"]
        end

        subgraph EventLayer["Event-Driven Layer"]
            PubSub["Pub/Sub Topics"]
            Eventarc["Eventarc Triggers"]

            PubSub --> Eventarc
            Eventarc -.->|Triggers| GKE
        end

        subgraph AppLayer["App Support"]
            Artifact["Artifact Registry"]
            Domains["Cloud Domains"]
        end
    end

    subgraph External["External Services"]
        Temporal["Temporal Cloud"]
    end

    GKE -.->|Workflows| Temporal

    style VPC fill:#e1f5fe,stroke:#01579b
    style GKE fill:#e8f5e9,stroke:#2e7d32
    style PubSub fill:#fff3e0,stroke:#ff6f00
    style Temporal fill:#f3e5f5,stroke:#7b1fa2
```


## Module Dependencies

The Terraform configuration is split into functional layers.

```mermaid
graph LR
    Network[module.network] --> GKE[module.gke-cluster]
    Network --> CloudDNS[module.cloud-dns]

    ServiceAccount[module.service-account] --> GKE
    ServiceAccount --> Eventarc[module.eventarc]

    PubSub[module.pubsub] --> Eventarc

    GKE --> Eventarc

    CloudDNS --> Domains[module.cloud-domains]
```

## Detailed Modules

### 1. Core Networking (`modules/network`)

* **VPC**: Custom VPC network (not using default).
* **Subnet**: Specific subnet (`10.0.0.0/24`) with secondary ranges for Pods and Services (VPC-native).
* **Global Address**: Reserves a static external IP (`google_compute_global_address`) used by the Ingress Controller.

### 2. Compute (`modules/gke-cluster`)

* **Cluster**: GKE Standard regional cluster.
* **Node Pools**: Dedicated node pools (e.g., `primary-pool`).
* **Security**:
  * Workload Identity enabled.
  * Shielded Nodes enabled.
  * Private nodes (no external IPs on nodes).

### 3. DNS & Domains (`modules/cloud-dns`, `modules/cloud-domains`)
*   **Cloud DNS**: Manages the managed zone `templatejojotest.com`.
*   **A Records**: Automatically maps the Global Static IP to the domain root.
*   **Cloud Domains**: (Optional) Handles domain registration and directs name servers to Cloud DNS.

### 4. Event Driven (`modules/pubsub`, `modules/eventarc`)
*   **Pub/Sub**: Creates topics (`event-ingestion`) and subscriptions.
*   **Eventarc**: Creates triggers that listen to Pub/Sub messages and forward them to the GKE Service (`event-driven-api`).
    *   *Note*: Requires the GKE Service to be exposed internally or via Cloud Run for Anthos (here using native GKE destinations).

### 5. Security & IAM (`modules/security`, `modules/service-accounts`)

- **Service Accounts**:
  - `cloudrun-runtime`: Used by Pods (Workload Identity).
  - `eventarc-triggers`: Used by Eventarc to invoke the service.
- **SSL Policy**: Enforces TLS 1.2+ configuration for the Load Balancer.

### 6. Temporal Cloud (External Service)

- **Durable Workflows**: Orchestrates long-running business processes with automatic retries.
- **Ephemeral Workers**: Workers are created per-request and destroyed after execution for efficient resource usage. (See [Adding Workers](kubernetes.md#adding-temporal-workers))
- **Configuration**:
  - `TEMPORAL_ADDRESS`: Temporal Cloud endpoint (e.g., `europe-west3.gcp.api.temporal.io:7233`)
  - `TEMPORAL_NAMESPACE`: Your Temporal namespace
  - `TEMPORAL_API_KEY`: Stored in Google Secret Manager

## Architecture Strategy 🧠

### Shared Cluster Topology

To optimize costs and provisioning time, we use a **Shared Cluster** strategy:

*   **Production (`default` workspace)**: Owns the "Physical" layer (VPC, GKE Cluster, DNS Zone).
*   **Ephemeral Workspaces (e.g., `feat-login`)**: Read the existing infrastructure via Terraform Data Sources. They Only deploy **Logical** isolated resources (Pub/Sub Topics, Eventarc Triggers).

```mermaid
graph TD
    subgraph ProdWorkspace["Production Workspace"]
        VPC["VPC Network"]
        GKE["GKE Cluster"]
        DNS["Cloud DNS"]
        ProdEvents["Prod Eventarc & PubSub"]
    end

    subgraph FeatWorkspace["Ephemeral Workspace: feat-xyz"]
        DataSources["Data Sources (Read-Only)"] -.-> VPC
        DataSources -.-> GKE
        FeatEvents["Ephemeral Eventarc & PubSub"]
    end

    style ProdWorkspace fill:#e1f5fe,stroke:#01579b
    style FeatWorkspace fill:#fff3e0,stroke:#ff6f00
```

## Deployment 🚀

### Manual Deployment

```bash
# 1. Initialize
make init_local_terraform

# 2. Select Workspace (Critical!)
# For Prod:
terraform workspace select default

# For Feature Dev:
terraform workspace new feat-my-feature || terraform workspace select feat-my-feature

# 3. Plan & Apply
make plan_local_terraform
make apply_local_terraform
```

### CI/CD Automation

References to workspaces are handled automatically by **GitHub Actions**:
*   **Main Branch** → Selects `default` workspace.
*   **Feature Branches** → Selects/Creates `feat-<branch-name>` workspace.
