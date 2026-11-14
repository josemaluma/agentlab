from unittest.mock import Mock

import pytest
from fastapi.testclient import TestClient

import agentlab.main as main
from agentlab.domain import ResearchReport, ResearchRequest

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

def test_research_endpoint_returns_report(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    service_instance = Mock()
    service_instance.research.return_value = ResearchReport(
        question="What is AgentLab?",
        summary="Test summary",
        findings=["Finding 1"],
        limitations=["Limitation 1"],
    )

    service_constructor = Mock(return_value=service_instance)
    client_constructor = Mock()

    monkeypatch.setattr(main, "ResearchService", service_constructor)
    monkeypatch.setattr(main, "AgentLabOpenAIClient", client_constructor)

    response = client.post(
        "/research",
        json={"question": "What is AgentLab?"},
    )

    assert response.status_code == 200
    assert response.json() == {
        "question": "What is AgentLab?",
        "summary": "Test summary",
        "findings": ["Finding 1"],
        "limitations": ["Limitation 1"],
        "sources": [],
    }

    client_constructor.assert_called_once_with()
    service_constructor.assert_called_once_with(client=client_constructor.return_value)

    service_instance.research.assert_called_once()
    request = service_instance.research.call_args.args[0]
    assert isinstance(request, ResearchRequest)
    assert request.question == "What is AgentLab?"


def test_research_endpoint_validates_missing_question() -> None:
    response = client.post("/research", json={})

    assert response.status_code == 422


def test_research_endpoint_validates_empty_question() -> None:
    response = client.post(
        "/research",
        json={"question": ""},
    )

    assert response.status_code == 422