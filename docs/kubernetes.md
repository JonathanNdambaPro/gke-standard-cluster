# Kubernetes & Ingress ☸️

This section details how applications are exposed on the GKE cluster.

## Ingress Architecture

We use the **GKE Ingress Controller** (GCE L7 Load Balancer).

1.  **ManagedCertificate**: Google-managed SSL certificate for `templatejojotest.com`.
2.  **FrontendConfig**: Configures HTTP->HTTPS redirection.
3.  **Ingress**: Defines the host rules and backend routing.
4.  **Service**: `NodePort` service is required for the Ingress Controller to route traffic.

## Troubleshooting Ingress

Common issues and fixes during deployment.

### 502 Bad Gateway / Server Error

This usually means the Load Balancer cannot reach your Pods.

**Checklist:**
1.  **Health Code 502**: Use `kubectl describe ingress` and look at the `Backends` column.
    *   If it says `Unhealthy` or `Unknown`, the health check is failing.
2.  **Port Mismatch (Common Error)**:
    *   **Container Port**: Check your `Dockerfile` (e.g., `EXPOSE 80`).
    *   **Deployment Port**: `containerPort` must match the Dockerfile port.
    *   **Service Port**: `targetPort` must match the `containerPort`.
3.  **Selector Mismatch**:
    *   Ensure `Service.spec.selector` matches `Deployment.spec.template.metadata.labels`.

**Debug Command:**
```bash
# Check if pods are running
kubectl get pods

# Check logs to confirm port
kubectl logs -l app=<your-app-label>

# Describe ingress to see backend health
kubectl describe ingress <ingress-name>
```
