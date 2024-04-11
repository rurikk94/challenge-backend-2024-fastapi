"""Test device groups."""

import random
import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

@pytest.fixture(scope="module", autouse=True)
def create_device_group_data():
    """Let's create the test data"""
    device_group = client.post("/v1/device_groups/", json={
        "name": "nuevo abril device_group",
        "description": "creado por postman en abril",
        "devices": [],
        "employees": []
    })
    device_group = device_group.json()
    yield device_group
    client.delete(f"/v1/device_groups/{device_group['data']['id']}")

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
