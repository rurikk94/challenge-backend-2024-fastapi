"""Test devices."""
import random
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


def test_get_devices():
    """Test get devices."""
    response = client.get("/v1/devices/")
    assert response.status_code == 200
    return response.json()


def test_get_device_random():
    """Test get device random."""
    data = test_get_devices()
    device = random.choice(data["data"])
    device_id = device["id"]
    response = client.get(f"/v1/devices/{device_id}")
    assert response.status_code == 200
