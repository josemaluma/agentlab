
from unittest.mock import Mock

import pytest

from agentlab import openai_client
from agentlab.domain import ResearchReport


def test_client_requires_api_key(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(openai_client, "OPENAI_API_KEY", None)

    with pytest.raises(RuntimeError, match="OPENAI_API_KEY is not configured"):
        openai_client.AgentLabOpenAIClient()


def test_client_is_created_with_test_api_key(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    sdk_client = object()
    openai_constructor = Mock(return_value=sdk_client)

    monkeypatch.setattr(openai_client, "OPENAI_API_KEY", "test-api-key")
    monkeypatch.setattr(openai_client, "OpenAI", openai_constructor)

    client = openai_client.AgentLabOpenAIClient()

    openai_constructor.assert_called_once_with(api_key="test-api-key")
    assert client.client is sdk_client


def test_client_keeps_configured_model(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(openai_client, "OPENAI_API_KEY", "test-api-key")
    monkeypatch.setattr(openai_client, "OPENAI_MODEL", "test-model")
    monkeypatch.setattr(openai_client, "OpenAI", Mock())

    client = openai_client.AgentLabOpenAIClient()

    assert client.model == "test-model"


def test_client_keeps_configured_research_model(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(openai_client, "OPENAI_API_KEY", "test-api-key")
    monkeypatch.setattr(
        openai_client,
        "RESEARCH_MODEL",
        "test-research-model",
    )
    monkeypatch.setattr(openai_client, "OpenAI", Mock())

    client = openai_client.AgentLabOpenAIClient()

    assert client.research_model == "test-research-model"


def test_ask_sends_prompt_and_returns_response_text(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    response = Mock(output_text="Test response")
    sdk_client = Mock()
    sdk_client.responses.create.return_value = response

    monkeypatch.setattr(openai_client, "OPENAI_API_KEY", "test-api-key")
    monkeypatch.setattr(openai_client, "OPENAI_MODEL", "test-model")
    monkeypatch.setattr(openai_client, "OpenAI", Mock(return_value=sdk_client))

    client = openai_client.AgentLabOpenAIClient()
    prompt = "Test prompt"

    result = client.ask(prompt)

    sdk_client.responses.create.assert_called_once_with(
        model=client.model,
        input=prompt,
    )
    assert result == response.output_text


def test_research_returns_structured_report(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    expected_report = ResearchReport(
        question="What is AgentLab?",
        summary="AgentLab is an AI research project.",
        findings=["It uses Python."],
        limitations=["No external sources were consulted."],
    )

    sdk_client = Mock()
    sdk_client.responses.parse.return_value = Mock(
        output_parsed=expected_report
    )

    monkeypatch.setattr(openai_client, "OPENAI_API_KEY", "test-api-key")
    monkeypatch.setattr(openai_client, "OPENAI_MODEL", "test-model")
    monkeypatch.setattr(
        openai_client,
        "RESEARCH_MODEL",
        "test-research-model",
    )
    monkeypatch.setattr(openai_client, "OpenAI", Mock(return_value=sdk_client))

    client = openai_client.AgentLabOpenAIClient()

    result = client.research(
        question="What is AgentLab?",
        context="A project built with Python.",
    )

    sdk_client.responses.parse.assert_called_once()

    call_arguments = sdk_client.responses.parse.call_args.kwargs

    assert call_arguments["model"] == "test-research-model"
    assert call_arguments["tools"] == [{"type": "web_search"}]
    assert call_arguments["text_format"] is ResearchReport
    assert "What is AgentLab?" in call_arguments["input"]
    assert "A project built with Python." in call_arguments["input"]
    assert result == expected_report


def test_research_raises_error_when_no_report_is_returned(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    sdk_client = Mock()
    sdk_client.responses.parse.return_value = Mock(output_parsed=None)

    monkeypatch.setattr(openai_client, "OPENAI_API_KEY", "test-api-key")
    monkeypatch.setattr(openai_client, "OpenAI", Mock(return_value=sdk_client))

    client = openai_client.AgentLabOpenAIClient()

    with pytest.raises(RuntimeError, match="did not return a valid research report"):
        client.research("What is AgentLab?")
