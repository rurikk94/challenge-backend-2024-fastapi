import random
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


def test_schedule_desviation_rules():
    response = client.get("/v1/schedule_desviation_rules/")
    assert response.status_code == 200
    return response.json()


def test_schedule_desviation_rules_random():
    data = test_schedule_desviation_rules()
    schedule_desviation_rule = random.choice(data["data"])
    schedule_desviation_rule_id = schedule_desviation_rule["schedule_desviation_rule_id"]
    response = client.get(f"/v1/schedule_desviation_rules/{schedule_desviation_rule_id}")
    assert response.status_code == 200

