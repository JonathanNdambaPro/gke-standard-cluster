from functools import lru_cache

from google.cloud import secretmanager


@lru_cache
def get_secret_from_gcp(project_id: str, secret_name: str, version: str = "latest") -> str:
    """
    Récupère un secret depuis Google Secret Manager.

    Args:
        project_id: ID du projet GCP
        secret_name: Nom du secret
        version: Version du secret (par défaut "latest")

    Returns:
        La valeur du secret en tant que string
    """
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_name}/versions/{version}"

    response = client.access_secret_version(request={"name": name})
    return response.payload.data.decode("UTF-8")
