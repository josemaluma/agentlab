from fastapi import FastAPI
from pydantic import BaseModel, Field

from .config import app_description, app_name, app_version
from .openai_client import AgentLabOpenAIClient


class AskRequest(BaseModel):
    prompt: str = Field(min_length=1)


class AskResponse(BaseModel):
    answer: str


app = FastAPI(
    title=app_name,
    version=app_version,
    description=app_description,
)


@app.get("/")
def read_root() -> dict[str, str]:
    """Return the API status and current version."""
    return {
        "message": "AgentLab API is running",
        "version": app_version,
    }


@app.post("/ask", response_model=AskResponse)
def ask(request: AskRequest) -> AskResponse:
    """Send a prompt to the configured AgentLab OpenAI client."""
    client = AgentLabOpenAIClient()
    return AskResponse(answer=client.ask(request.prompt))
