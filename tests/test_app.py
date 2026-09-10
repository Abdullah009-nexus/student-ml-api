from app import app


def test_health():
    client = app.test_client()
    response = client.get("/health")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "wrong"
    assert data["application"] == "student-ml-api"
    assert data["version"] == "1.0.0"


def test_predict_success():
    client = app.test_client()
    response = client.post("/predict", json={"value": 10})
    assert response.status_code == 200
    data = response.get_json()
    assert data["input"] == 10
    assert data["prediction"] == 20


def test_predict_missing_input():
    client = app.test_client()
    response = client.post("/predict", json={})
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data
    assert "value" in data["error"]


def test_predict_invalid_input():
    client = app.test_client()
    response = client.post("/predict", json={"value": "not-a-number"})
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data
    assert "Invalid" in data["error"]
