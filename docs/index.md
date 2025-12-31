# Event-Driven GCP - GKE Extension

This documentation covers the **GKE Standard Cluster** extension of the Event-Driven GCP project.

## Overview

We have extended the platform to support a production-grade Kubernetes environment using **GKE Standard**. This replaces or augments the Cloud Run setup for workloads requiring long-running processes, stateful sets, or complex orchestration.

## Key Features

*   **VPC-Native Cluster**: Integrated directly with your GCP VPC for performance and security.
*   **Cost-Optimized Node Pools**: Separate node pools with support for Spot/Preemptible instances.
*   **Automated DNS**: Cloud DNS management for your domain (`templatejojotest.com`).
*   **Global Ingress**: Google Cloud Global Load Balancer with managed SSL certificates.
*   **Infrastructure as Code**: Everything is defined in Terraform modules.
