"""Application service for deterministic research reports."""

from .domain import ResearchReport, ResearchRequest


class ResearchService:
    """Create a research report without external research."""

    def research(self, request: ResearchRequest) -> ResearchReport:
        """Return a deterministic placeholder report for a research request."""
        return ResearchReport(
            question=request.question,
            summary="Research has not been executed yet.",
            findings=[],
            limitations=["This report was generated without external research."],
        )
