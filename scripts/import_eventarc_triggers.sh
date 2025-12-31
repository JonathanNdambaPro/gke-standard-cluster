#!/bin/bash
set -e

# Arguments
NAMESPACE="$1"
FILTER_ENV="$2"

if [ -z "$NAMESPACE" ] || [ -z "$FILTER_ENV" ]; then
  echo "Usage: $0 <NAMESPACE> <FILTER_ENV>"
  echo "Environment variables GCP_PROJECT_ID and GCP_ZONE must be set."
  exit 1
fi

PIPELINE_KEY="ingest"

# Determine expected Trigger Name
if [ "$NAMESPACE" == "default" ]; then
   TRIGGER_NAME="trigger-${PIPELINE_KEY}"
else
   TRIGGER_NAME="trigger-${PIPELINE_KEY}-${NAMESPACE}"
fi

# Define Terraform address and GCP Resource ID
TF_ADDRESS="module.eventarc[\"${PIPELINE_KEY}\"].google_eventarc_trigger.gke_trigger"
RESOURCE_ID="projects/${GCP_PROJECT_ID}/locations/${GCP_ZONE}/triggers/${TRIGGER_NAME}"

echo "Checking import for $TF_ADDRESS ($RESOURCE_ID)..."

# 1. Check if resource exists in GCP
exists_in_gcp=$(gcloud eventarc triggers list --location=${GCP_ZONE} --format="value(name)" --filter="name:$TRIGGER_NAME")

if [ -n "$exists_in_gcp" ]; then
  echo "Resource $TRIGGER_NAME exists in GCP."

  # 2. Check if resource exists in Terraform State
  # Note: Assumes we are running from repo root implies -chdir=infra/terraform
  if terraform -chdir=infra/terraform state list | grep -Fq "$TF_ADDRESS"; then
    echo "Resource is already in Terraform state. Skipping import."
  else
    echo "Resource is NOT in Terraform state. Importing..."
    terraform -chdir=infra/terraform import -var-file="tfvars/main.tfvars" \
      -var "eventarc_trigger_namespace=${NAMESPACE}" \
      -var "eventarc_environment_filter=${FILTER_ENV}" \
      "$TF_ADDRESS" "$RESOURCE_ID"
  fi
else
  echo "Resource $TRIGGER_NAME does not exist in GCP. Terraform will create it."
fi
