from unittest.mock import Mock

import pytest

from agentlab import openai_client


def test_client_requires_api_key(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(openai_client, "OPENAI_API_KEY", None)

    with pytest.raises(RuntimeError, match="OPENAI_API_KEY is not configured"):
        openai_client.AgentLabOpenAIClient()


def test_client_is_created_with_test_api_key(monkeypatch: pytest.MonkeyPatch) -> None:
    sdk_client = object()
    openai_constructor = Mock(return_value=sdk_client)
    monkeypatch.setattr(openai_client, "OPENAI_API_KEY", "test-api-key")
    monkeypatch.setattr(openai_client, "OpenAI", openai_constructor)

    client = openai_client.AgentLabOpenAIClient()

    openai_constructor.assert_called_once_with(api_key="test-api-key")
    assert client.client is sdk_client


def test_client_keeps_configured_model(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(openai_client, "OPENAI_API_KEY", "test-api-key")
    monkeypatch.setattr(openai_client, "OPENAI_MODEL", "test-model")
    monkeypatch.setattr(openai_client, "OpenAI", Mock())

    client = openai_client.AgentLabOpenAIClient()

    assert client.model == "test-model"


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
