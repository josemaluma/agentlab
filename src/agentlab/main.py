from fastapi import FastAPI
from pydantic import BaseModel, Field

from agentlab.domain import ResearchReport, ResearchRequest
from agentlab.research_service import ResearchService
from agentlab.service import AgentLabService


app = FastAPI(
    title="AgentLab API",
    description="Minimal API for the AgentLab project.",
)


class AskRequest(BaseModel):
    prompt: str = Field(min_length=1)


class AskResponse(BaseModel):
    answer: str


@app.get("/")
def read_root() -> dict[str, str]:
    """Return the API status and current version."""
    return {
        "message": "AgentLab API is running",
        "version": "0.1.0",
    }


@app.post("/ask", response_model=AskResponse)
def ask(request: AskRequest) -> AskResponse:
    """Answer a direct user prompt."""
    service = AgentLabService()
    answer = service.ask(request.prompt)
    return AskResponse(answer=answer)


@app.post("/research", response_model=ResearchReport)
def research(request: ResearchRequest) -> ResearchReport:
    """Run a research request."""
    service = ResearchService()
    return service.research(request)