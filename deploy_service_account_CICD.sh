#!/bin/bash
# ONLY IN LOCAL => GENERATE SERVICE_ACCOUNT AND HIS JSON KEYS FOR RUNNING CICD GITHUB ACTION

# Variables de configuration
SERVICE_ACCOUNT_NAME="event-driven-dataascode"
PROJECT_ID="dataascode"
SERVICE_ACCOUNT_EMAIL="${SERVICE_ACCOUNT_NAME}@${PROJECT_ID}.iam.gserviceaccount.com"
KEY_FILE="${SERVICE_ACCOUNT_NAME}-key.json"


echo "Création (ou vérification) du service-account ${SERVICE_ACCOUNT_NAME}…"
gcloud iam service-accounts create ${SERVICE_ACCOUNT_NAME} --display-name="Terraform bootstrap SA"

echo "Attribution des rôles IAM à ${SERVICE_ACCOUNT_NAME}…"
gcloud projects add-iam-policy-binding ${PROJECT_ID} \
    --member="serviceAccount:${SERVICE_ACCOUNT_EMAIL}" \
    --role="roles/iam.serviceAccountAdmin"

gcloud projects add-iam-policy-binding ${PROJECT_ID} \
    --member="serviceAccount:${SERVICE_ACCOUNT_EMAIL}" \
    --role="roles/iam.serviceAccountKeyAdmin"

echo "Backend GCS (state Terraform)"
gcloud projects add-iam-policy-binding ${PROJECT_ID} \
    --member="serviceAccount:${SERVICE_ACCOUNT_EMAIL}" \
    --role="roles/storage.admin"

echo "Artifact Registry"
gcloud projects add-iam-policy-binding ${PROJECT_ID} \
    --member="serviceAccount:${SERVICE_ACCOUNT_EMAIL}" \
    --role="roles/artifactregistry.admin"

echo "Cloud Run v2"
gcloud projects add-iam-policy-binding ${PROJECT_ID} \
    --member="serviceAccount:${SERVICE_ACCOUNT_EMAIL}" \
    --role="roles/run.admin"
gcloud projects add-iam-policy-binding ${PROJECT_ID} \
    --member="serviceAccount:${SERVICE_ACCOUNT_EMAIL}" \
    --role="roles/iam.serviceAccountUser"

echo "Cloud Scheduler (création de job + OIDC Token)"
gcloud projects add-iam-policy-binding ${PROJECT_ID} \
    --member="serviceAccount:${SERVICE_ACCOUNT_EMAIL}" \
    --role="roles/cloudscheduler.admin"
gcloud projects add-iam-policy-binding ${PROJECT_ID} \
    --member="serviceAccount:${SERVICE_ACCOUNT_EMAIL}" \
    --role="roles/iam.serviceAccountTokenCreator"

echo "Secret Eventarc"
gcloud projects add-iam-policy-binding dataascode \
      --member="serviceAccount:${SERVICE_ACCOUNT_EMAIL}" \
      --role="roles/eventarc.admin"

echo "Secret Manager"
gcloud projects add-iam-policy-binding ${PROJECT_ID} \
    --member="serviceAccount:${SERVICE_ACCOUNT_EMAIL}" \
    --role="roles/secretmanager.admin"

echo "Gestion des IAM Members du projet (pour ajouter BigQuery, Run Invoker, etc.)"
gcloud projects add-iam-policy-binding ${PROJECT_ID} \
    --member="serviceAccount:${SERVICE_ACCOUNT_EMAIL}" \
    --role="roles/resourcemanager.projectIamAdmin"

echo "Ajout des droits BigQuery Admin pour créer des datasets"
gcloud projects add-iam-policy-binding ${PROJECT_ID} \
    --member="serviceAccount:${SERVICE_ACCOUNT_EMAIL}" \
    --role="roles/bigquery.admin"

echo "Ajout des droits Pub/Sub Editor pour créer des topics"
gcloud projects add-iam-policy-binding ${PROJECT_ID} \
    --member="serviceAccount:${SERVICE_ACCOUNT_EMAIL}" \
    --role="roles/pubsub.editor"

echo "Génération de la clé JSON pour ${SERVICE_ACCOUNT_NAME}…"
gcloud iam service-accounts keys create ${KEY_FILE} \
    --iam-account=${SERVICE_ACCOUNT_EMAIL} \
    --project=${PROJECT_ID} \
    --quiet

echo "✔ ${SERVICE_ACCOUNT_NAME} est prêt, clé générée : ${KEY_FILE}"
