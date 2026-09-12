"""Domain models for AgentLab research."""

from pydantic import BaseModel, Field


class ResearchRequest(BaseModel):
    """Describe a research task requested by a user."""

    question: str = Field(min_length=1)
    context: str | None = None


class ResearchReport(BaseModel):
    """Structured result for a research task."""

    question: str
    summary: str
    findings: list[str] = Field(default_factory=list)
    limitations: list[str] = Field(default_factory=list)
