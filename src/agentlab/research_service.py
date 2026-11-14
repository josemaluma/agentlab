
""""Application service for research operations."""

from .domain import ResearchReport, ResearchRequest
from .openai_client import AgentLabOpenAIClient


class ResearchService:
    """Handle research requests using the OpenAI client."""

    def __init__(self, client: AgentLabOpenAIClient) -> None:
        self.client = client

    def research(self, request: ResearchRequest) -> ResearchReport:
        """Generate a structured research report."""
        return self.client.research(
            question=request.question,
            context=request.context,
        )