"""Test devices."""

import pytest
import random
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


@pytest.fixture(scope="module")
def create_device_group_data():
    """Let's create the test data"""
    device_group = client.post(
        "/v1/device_groups/",
        json={
            "name": "nuevo abril device_group",
            "description": "creado por postman en abril",
            "devices": [],
            "employees": [],
        },
    )
    device_group = device_group.json()
    yield device_group
    client.delete(f"/v1/device_groups/{device_group['data']['id']}")


@pytest.fixture(scope="module", autouse=True)
def create_test_data(create_device_group_data):
    """Let's create the test data"""
    device = client.post(
        "/v1/devices/",
        json={
            "name": "nuevo abril",
            "location": "creado por postman en abril",
            "timezone": "GMT",
            "device_group_id": create_device_group_data["data"]["id"],
            "pin": True,
            "face": True,
        },
    )
    device = device.json()
    yield device
    client.delete(f"/v1/devices/{device['data']['id']}")


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
