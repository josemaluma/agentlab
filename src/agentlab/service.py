"""Application service for AgentLab questions."""

from .openai_client import AgentLabOpenAIClient


class AgentLabService:
    """Delegate questions to the configured AgentLab OpenAI client."""

    def __init__(self, client: AgentLabOpenAIClient | None = None) -> None:
        self.client = AgentLabOpenAIClient() if client is None else client

    def ask(self, prompt: str) -> str:
        """Return the answer for a prompt from the configured client."""
        return self.client.ask(prompt)
