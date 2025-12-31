terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 7.12.0"
    }
  }

  backend "gcs" {

  }
}


provider "google" {
  project = var.project
  region  = var.region
}
