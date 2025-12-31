#!/bin/bash
# ONLY IN LOCAL => GENERATE SERVICE_ACCOUNT AND HIS JSON KEYS FOR RUNNING CICD GITHUB ACTION

# Variables de configuration
SERVICE_ACCOUNT_NAME="event-driven-heevi-dataascode"
PROJECT_ID="dataascode"
SERVICE_ACCOUNT_EMAIL="${SERVICE_ACCOUNT_NAME}@${PROJECT_ID}.iam.gserviceaccount.com"
KEY_FILE="${SERVICE_ACCOUNT_NAME}-key.json"


echo "Création (ou vérification) du service-account ${SERVICE_ACCOUNT_NAME}…"
gcloud iam service-accounts create ${SERVICE_ACCOUNT_NAME} --display-name="Terraform bootstrap SA"

echo "Attribution des rôles IAM à ${SERVICE_ACCOUNT_NAME}…"
gcloud projects add-iam-policy-binding ${PROJECT_ID} \
    --member="serviceAccount:${SERVICE_ACCOUNT_EMAIL}" \
    --role="roles/iam.serviceAccountAdmin"

# Backend GCS (state Terraform)
echo "Backend GCS (state Terraform)"
gcloud projects add-iam-policy-binding ${PROJECT_ID} \
    --member="serviceAccount:${SERVICE_ACCOUNT_EMAIL}" \
    --role="roles/storage.admin"

# Artifact Registry
echo "Artifact Registry"
gcloud projects add-iam-policy-binding ${PROJECT_ID} \
    --member="serviceAccount:${SERVICE_ACCOUNT_EMAIL}" \
    --role="roles/artifactregistry.admin"

# IAM User (pour attacher les SA aux ressources)
echo "IAM Service Account User"
gcloud projects add-iam-policy-binding ${PROJECT_ID} \
    --member="serviceAccount:${SERVICE_ACCOUNT_EMAIL}" \
    --role="roles/iam.serviceAccountUser"

# IAM Token Creator (pour OIDC et autres needs)
echo "IAM Service Account Token Creator"
gcloud projects add-iam-policy-binding ${PROJECT_ID} \
    --member="serviceAccount:${SERVICE_ACCOUNT_EMAIL}" \
    --role="roles/iam.serviceAccountTokenCreator"

# Eventarc (pour gérer les triggers et secrets associés si besoin dans le module eventarc)
echo "Eventarc Admin"
gcloud projects add-iam-policy-binding ${PROJECT_ID} \
      --member="serviceAccount:${SERVICE_ACCOUNT_EMAIL}" \
      --role="roles/eventarc.admin"

# Gestion des IAM Members du projet (pour ajouter BigQuery, Run Invoker, etc.)
echo "Project IAM Admin (pour gérer les binding IAM via Terraform)"
gcloud projects add-iam-policy-binding ${PROJECT_ID} \
    --member="serviceAccount:${SERVICE_ACCOUNT_EMAIL}" \
    --role="roles/resourcemanager.projectIamAdmin"

# Pub/Sub (pour les topics et subs)
echo "Pub/Sub Admin"
gcloud projects add-iam-policy-binding ${PROJECT_ID} \
    --member="serviceAccount:${SERVICE_ACCOUNT_EMAIL}" \
    --role="roles/pubsub.admin"

# --- NOUVEAUX RÔLES AJOUTÉS POUR LEAST PRIVILEGE ---

# Network (VPC, Subnets, Firewall rules) via modules/network
echo "Compute Network Admin"
gcloud projects add-iam-policy-binding ${PROJECT_ID} \
    --member="serviceAccount:${SERVICE_ACCOUNT_EMAIL}" \
    --role="roles/compute.networkAdmin"

# Security (Cloud Armor policies) via modules/security
echo "Compute Security Admin"
gcloud projects add-iam-policy-binding ${PROJECT_ID} \
    --member="serviceAccount:${SERVICE_ACCOUNT_EMAIL}" \
    --role="roles/compute.securityAdmin"

# GKE Cluster via modules/gke-cluster
echo "Kubernetes Engine Admin"
gcloud projects add-iam-policy-binding ${PROJECT_ID} \
    --member="serviceAccount:${SERVICE_ACCOUNT_EMAIL}" \
    --role="roles/container.clusterAdmin"

# GKE Developer (pour déployer dans le cluster via kubectl/helm)
echo "Kubernetes Engine Developer"
gcloud projects add-iam-policy-binding ${PROJECT_ID} \
    --member="serviceAccount:${SERVICE_ACCOUNT_EMAIL}" \
    --role="roles/container.developer"

# Cloud DNS via modules/cloud-dns
echo "Cloud DNS Admin"
gcloud projects add-iam-policy-binding ${PROJECT_ID} \
    --member="serviceAccount:${SERVICE_ACCOUNT_EMAIL}" \
    --role="roles/dns.admin"

# Cloud Domains via modules/cloud-domains
echo "Cloud Domains Admin"
gcloud projects add-iam-policy-binding ${PROJECT_ID} \
    --member="serviceAccount:${SERVICE_ACCOUNT_EMAIL}" \
    --role="roles/domains.admin"


# Service Usage Admin (pour activer les APIs via modules/google-api)
echo "Service Usage Admin"
gcloud projects add-iam-policy-binding ${PROJECT_ID} \
    --member="serviceAccount:${SERVICE_ACCOUNT_EMAIL}" \
    --role="roles/serviceusage.serviceUsageAdmin"


# Monitoring Admin (pour gérer les alert policies et notification channels)
echo "Monitoring Editor"
gcloud projects add-iam-policy-binding ${PROJECT_ID} \
    --member="serviceAccount:${SERVICE_ACCOUNT_EMAIL}" \
    --role="roles/monitoring.editor"


# --- FIN DES AJOUTS ---

echo "Génération de la clé JSON pour ${SERVICE_ACCOUNT_NAME}…"
gcloud iam service-accounts keys create ${KEY_FILE} \
    --iam-account=${SERVICE_ACCOUNT_EMAIL} \
    --project=${PROJECT_ID} \
    --quiet

echo "✔ ${SERVICE_ACCOUNT_NAME} est prêt, clé générée : ${KEY_FILE}"
