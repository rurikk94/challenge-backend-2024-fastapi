"""Test employees."""

import random
from fastapi.testclient import TestClient
import pytest
from src.main import app

client = TestClient(app)


@pytest.fixture(scope="module", autouse=True)
def create_employees():
    """Let's create the test data"""
    employee = client.post(
        "/v1/employees/",
        json={
            "dni": "15.723.569-9",
            "fullname": "Clark Brereton",
            "email": "c.b@mail.com",
        },
    )
    employee = employee.json()
    yield employee
    client.delete(f"/v1/employees/{employee['data']['id']}")


def test_get_employees():
    """Test get employees."""
    response = client.get("/v1/employees/")
    assert response.status_code == 200
    return response.json()


def test_get_employee_random():
    """Test get employee random."""
    data = test_get_employees()
    employee = random.choice(data["data"])
    employee_id = employee["id"]
    response = client.get(f"/v1/employees/{employee_id}")
    assert response.status_code == 200
