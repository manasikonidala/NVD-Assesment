import pytest
from backend.app import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_list_cves(client):
    response = client.get("/cves/list")
    assert response.status_code == 200
    assert isinstance(response.json, list)

def test_get_cve(client):
    response = client.get("/cves/CVE-TEST-1234")
    assert response.status_code in [200, 404]
