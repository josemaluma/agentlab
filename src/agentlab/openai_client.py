"""Small OpenAI client wrapper for AgentLab."""

from openai import OpenAI

from agentlab.config import OPENAI_API_KEY, OPENAI_MODEL
from agentlab.domain import ResearchReport

class AgentLabOpenAIClient:
    """Keep the OpenAI client and AgentLab's default model together."""

    def __init__(self) -> None:
        if not OPENAI_API_KEY:
            raise RuntimeError("OPENAI_API_KEY is not configured.")

        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.model = OPENAI_MODEL

    def ask(self, prompt: str) -> str:
        response = self.client.responses.create(
            model=self.model,
            input=prompt,
        )
        return response.output_text
    def research(self, question: str, context: str | None = None) -> ResearchReport:
        """Generate a structured research report using OpenAI."""

        prompt = f"""
        Research question: {question}

        Additional context: {context or "No additional context provided."}

        Create a concise research report.
        Include a useful summary, key findings, and limitations.
        Do not invent facts or claim that external research was performed.
        """

        response = self.client.responses.parse(
            model=self.model,
            input=prompt,
            text_format=ResearchReport,
        )

        if response.output_parsed is None:
            raise RuntimeError("OpenAI did not return a valid research report.")

        return response.output_parsed