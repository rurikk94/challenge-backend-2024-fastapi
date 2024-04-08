import random
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


def test_overtime_rules():
    response = client.get("/v1/overtime_rules/")
    assert response.status_code == 200
    return response.json()


def test_overtime_rules_random():
    data = test_overtime_rules()
    overtime_rule = random.choice(data["data"])
    overtime_rule_id = overtime_rule["overtime_rule_id"]
    response = client.get(f"/v1/overtime_rules/{overtime_rule_id}")
    assert response.status_code == 200

