"""Test device groups."""
import random
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


def test_get_device_groups():
    """Test get device groups."""
    response = client.get("/v1/device_groups/")
    assert response.status_code == 200
    return response.json()


def test_get_device_random():
    """Test get device groups random."""
    data = test_get_device_groups()
    device_group = random.choice(data["data"])
    device_group_id = device_group["id"]
    response = client.get(f"/v1/device_groups/{device_group_id}")
    assert response.status_code == 200
