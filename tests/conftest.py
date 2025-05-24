import pytest
from utils.api import StellarBurgersAPI
from utils.generators import generate_random_email, generate_random_string
from yourapi.client import APIClient

@pytest.fixture
def api_client():
    import pytest
    import requests

    @pytest.fixture
    def api_client():
        base_url = "https://your-api-url.com"
        session = requests.Session()
        session.headers.update({"Content-Type": "application/json"})
        return session