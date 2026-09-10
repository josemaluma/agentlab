"""Small OpenAI client wrapper for AgentLab."""

from openai import OpenAI

from agentlab.config import OPENAI_API_KEY, OPENAI_MODEL


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
