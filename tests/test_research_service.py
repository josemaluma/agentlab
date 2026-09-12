from agentlab.domain import ResearchReport, ResearchRequest
from agentlab.research_service import ResearchService


def test_valid_request_produces_research_report() -> None:
    report = ResearchService().research(ResearchRequest(question="What is AgentLab?"))

    assert isinstance(report, ResearchReport)


def test_report_copies_question_exactly() -> None:
    request = ResearchRequest(question="What is AgentLab?")

    report = ResearchService().research(request)

    assert report.question == request.question


def test_report_has_expected_summary() -> None:
    report = ResearchService().research(ResearchRequest(question="What is AgentLab?"))

    assert report.summary == "Research has not been executed yet."


def test_report_has_no_findings() -> None:
    report = ResearchService().research(ResearchRequest(question="What is AgentLab?"))

    assert report.findings == []


def test_report_has_expected_limitation() -> None:
    report = ResearchService().research(ResearchRequest(question="What is AgentLab?"))

    assert report.limitations == [
        "This report was generated without external research."
    ]


def test_equal_requests_produce_equal_reports() -> None:
    first = ResearchService().research(ResearchRequest(question="What is AgentLab?"))
    second = ResearchService().research(ResearchRequest(question="What is AgentLab?"))

    assert first == second


def test_request_with_context_keeps_defined_behavior() -> None:
    request = ResearchRequest(
        question="What is AgentLab?",
        context="A project context.",
    )

    report = ResearchService().research(request)

    assert report == ResearchReport(
        question="What is AgentLab?",
        summary="Research has not been executed yet.",
        findings=[],
        limitations=["This report was generated without external research."],
    )


def test_service_does_not_require_openai_api_key() -> None:
    report = ResearchService().research(ResearchRequest(question="Test question"))

    assert report.question == "Test question"
