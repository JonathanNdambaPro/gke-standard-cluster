# Infrastructure (Terraform) 🏗️

The infrastructure is managed via Terraform and organized into reusable modules.

## Modules

### `gke-cluster`
Provisions the GKE Standard cluster.
*   **Best Practice**: Uses `remove_default_node_pool = true` to allow safer node pool upgrades.
*   **Node Pools**: Defined as separate `google_container_node_pool` resources.
*   **Networking**: Enforces VPC-native IPs using `ip_allocation_policy`.

### `cloud-dns`
Manages the Google Cloud DNS zone and records.
*   **Inputs**: Accepts a list of external IPs to create `A` records automatically.
*   **Outputs**: Exports nameservers for domain registration.

### `cloud-domains`
**Optional Module**. Automates the purchase and configuration of a domain name.
*   **Resource**: `google_clouddomains_registration`
*   **Contact Info**: Requires real physical address and contact details (Privacy Redacted by default).

### `network`
Sets up the foundational networking.
*   **Global IP**: Reserves a static global IP for the GKE Ingress (`google_compute_global_address`).
*   **VPC/Subnet**: Creates the dedicated network for the cluster.

## Deployment

To deploy the infrastructure:

```bash
# 1. Initialize
make init_local_terraform

# 2. Plan
make plan_local_terraform

# 3. Apply
make apply_local_terraform
```
