import random
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


def test_rounding_rules():
    response = client.get("/v1/rounding_rules/")
    assert response.status_code == 200
    return response.json()


def test_rounding_rules_random():
    data = test_rounding_rules()
    rounding_rule = random.choice(data["data"])
    rounding_rule_id = rounding_rule["rounding_rule_id"]
    response = client.get(f"/v1/rounding_rules/{rounding_rule_id}")
    assert response.status_code == 200

