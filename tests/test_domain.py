import pytest
from pydantic import ValidationError

from agentlab.domain import ResearchReport, ResearchRequest


def test_research_request_accepts_valid_question() -> None:
    request = ResearchRequest(question="What is AgentLab?")

    assert request.question == "What is AgentLab?"
    assert request.context is None


def test_research_request_rejects_empty_question() -> None:
    with pytest.raises(ValidationError):
        ResearchRequest(question="")


def test_research_report_can_be_built_with_question_and_summary() -> None:
    report = ResearchReport(
        question="What is AgentLab?",
        summary="AgentLab is an AI-powered research agent.",
    )

    assert report.question == "What is AgentLab?"
    assert report.summary == "AgentLab is an AI-powered research agent."


def test_research_report_defaults_to_empty_lists() -> None:
    report = ResearchReport(question="What is AgentLab?", summary="A research agent.")

    assert report.findings == []
    assert report.limitations == []


def test_research_report_instances_do_not_share_default_lists() -> None:
    first_report = ResearchReport(question="First question", summary="First summary.")
    second_report = ResearchReport(question="Second question", summary="Second summary.")

    first_report.findings.append("Finding")
    first_report.limitations.append("Limitation")

    assert second_report.findings == []
    assert second_report.limitations == []
