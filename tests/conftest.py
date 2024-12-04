import os
import pytest
from fastapi.testclient import TestClient
from app.main import app
from dotenv import load_dotenv

# Load test environment variables
load_dotenv(dotenv_path=".env.test")

@pytest.fixture(scope="module")
def test_client():
    with TestClient(app) as client:
        yield client