from fastapi.testclient import TestClient

from agentlab.main import app


client = TestClient(app)


def test_read_root() -> None:
    response = client.get("/")

    assert response.status_code == 200
    assert "AgentLab API is running" in response.json()["message"]
    assert response.json()["version"] == "0.1.0"
