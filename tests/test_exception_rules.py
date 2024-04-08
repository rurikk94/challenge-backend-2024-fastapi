import random
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


def test_get_exception_rules():
    response = client.get("/v1/exception_rules/")
    assert response.status_code == 200
    return response.json()

def test_get_exception_rules_random():
    data = test_get_exception_rules()
    exception_rule = random.choice(data["data"])
    exception_rule_id = exception_rule["exception_rule_id"]
    response = client.get(f"/v1/exception_rules/{exception_rule_id}")
    assert response.status_code == 200