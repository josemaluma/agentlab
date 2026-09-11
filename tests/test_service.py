from unittest.mock import Mock

from agentlab.service import AgentLabService


def test_ask_delegates_to_client_and_returns_its_answer() -> None:
    openai_client = Mock()
    openai_client.ask.return_value = "Test answer"
    service = AgentLabService(client=openai_client)

    result = service.ask("Test prompt")

    openai_client.ask.assert_called_once_with("Test prompt")
    assert result == "Test answer"
