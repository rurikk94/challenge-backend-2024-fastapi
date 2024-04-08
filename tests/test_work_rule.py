import random
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


def test_work_rules():
    response = client.get("/v1/work_rules/")
    assert response.status_code == 200
    return response.json()

def test_work_rule_random():
    data = test_work_rules()
    work_rule = random.choice(data["data"])
    work_rule_id = work_rule["work_rule_id"]
    response = client.get(f"/v1/work_rules/{work_rule_id}")
    assert response.status_code == 200


