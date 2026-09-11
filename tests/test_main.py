from unittest.mock import Mock

from fastapi.testclient import TestClient

from agentlab import main


client = TestClient(main.app)


def test_read_root() -> None:
    response = client.get("/")

    assert response.status_code == 200
    assert "AgentLab API is running" in response.json()["message"]
    assert response.json()["version"] == "0.1.0"


def test_ask_returns_service_answer(monkeypatch) -> None:
    service_instance = Mock()
    service_instance.ask.return_value = "Test answer"
    service_constructor = Mock(return_value=service_instance)
    monkeypatch.setattr(main, "AgentLabService", service_constructor)

    response = client.post("/ask", json={"prompt": "Test prompt"})

    assert response.status_code == 200
    assert response.json() == {"answer": "Test answer"}
    service_instance.ask.assert_called_once_with("Test prompt")


def test_ask_requires_prompt() -> None:
    response = client.post("/ask", json={})

    assert response.status_code == 422


def test_ask_rejects_empty_prompt() -> None:
    response = client.post("/ask", json={"prompt": ""})

    assert response.status_code == 422
