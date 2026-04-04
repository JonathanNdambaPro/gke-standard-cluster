"""Script to generate a Fernet encryption key and store it in GCP Secret Manager."""

from cryptography.fernet import Fernet
from google.cloud import secretmanager

PROJECT_ID = "dataascode"
SECRET_NAME = "FERNET_ENCRYPTION_KEY"  # noqa: S105  # nosec B105


def create_or_add_secret_version(project_id: str, secret_name: str, secret_value: bytes) -> None:
    """Create a secret (if it doesn't exist) and add a new version with the given value.

    Args:
        project_id: GCP project ID.
        secret_name: Name of the secret in Secret Manager.
        secret_value: The secret payload as bytes.
    """
    client = secretmanager.SecretManagerServiceClient()
    parent = f"projects/{project_id}"
    secret_path = f"{parent}/secrets/{secret_name}"

    # Create the secret if it doesn't already exist.
    try:
        client.get_secret(request={"name": secret_path})
        print(f"Secret '{secret_name}' already exists — adding a new version.")
    except Exception:
        client.create_secret(
            request={
                "parent": parent,
                "secret_id": secret_name,
                "secret": {"replication": {"automatic": {}}},
            }
        )
        print(f"Secret '{secret_name}' created.")

    # Add a new version with the generated key.
    response = client.add_secret_version(
        request={
            "parent": secret_path,
            "payload": {"data": secret_value},
        }
    )
    print(f"New secret version added: {response.name}")


if __name__ == "__main__":
    key = Fernet.generate_key()
    print(f"Generated Fernet key: {key.decode()}")
    create_or_add_secret_version(PROJECT_ID, SECRET_NAME, key)
    print("Done — key successfully stored in Secret Manager.")
