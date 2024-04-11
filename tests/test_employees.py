"""Test employees."""
import random
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


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
