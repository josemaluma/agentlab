
from unittest.mock import Mock

from agentlab.domain import ResearchReport, ResearchRequest
from agentlab.research_service import ResearchService


def test_research_returns_report_from_client() -> None:
    expected_report = ResearchReport(
        question="What is AgentLab?",
        summary="AgentLab is an AI research project.",
        findings=["It uses Python."],
        limitations=["No external sources were consulted."],
    )
    client = Mock()
    client.research.return_value = expected_report

    service = ResearchService(client=client)
    request = ResearchRequest(question="What is AgentLab?")

    result = service.research(request)

    assert result == expected_report


def test_research_forwards_question_and_context_to_client() -> None:
    client = Mock()
    client.research.return_value = ResearchReport(
        question="What is AgentLab?",
        summary="A research project.",
    )

    service = ResearchService(client=client)
    request = ResearchRequest(
        question="What is AgentLab?",
        context="A project built with Python.",
    )

    service.research(request)

    client.research.assert_called_once_with(
        question="What is AgentLab?",
        context="A project built with Python.",
    )


def test_research_forwards_missing_context_as_none() -> None:
    client = Mock()
    client.research.return_value = ResearchReport(
        question="Test question",
        summary="Test summary.",
    )

    service = ResearchService(client=client)
    request = ResearchRequest(question="Test question")

    service.research(request)

    client.research.assert_called_once_with(
        question="Test question",
        context=None,
    )
