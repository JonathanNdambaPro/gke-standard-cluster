"""
Locust load testing for event-driven API.

Usage:
    # Install locust first
    uv add locust --dev

    # Run against local
    locust -f scripts/locustfile.py --host=http://localhost:8000

    # Run against GKE
    locust -f scripts/locustfile.py --host=https://templatejojotest.com

    # Headless mode (no web UI)
    locust -f scripts/locustfile.py --host=http://localhost:8000 --headless -u 100 -r 10 -t 60s
"""

from locust import HttpUser, between, task


class EventDrivenUser(HttpUser):
    """Simulated user for load testing the event-driven API."""

    wait_time = between(0.5, 2)  # Wait between 0.5 and 2 seconds between tasks

    @task(1)
    def health_check(self):
        """Test the root health endpoint."""
        self.client.get("/")

    @task(3)
    def temporal_hello(self):
        """Test the temporal_hello endpoint with a JSON payload."""
        payload = {"name": "LoadTest", "lastname": "User"}
        self.client.post("/api/v1/temporal_hello", json=payload)

    # Uncomment to test ingest_event (requires Eventarc CloudEvent format)
    # @task(2)
    # def ingest_event(self):
    #     """Test the ingest_event endpoint with CloudEvent format."""
    #
    #
    #             "data": encoded_data
