from fastapi import FastAPI


app = FastAPI(
    title="AgentLab API",
    description="Minimal API for the AgentLab project.",
)


@app.get("/")
def read_root() -> dict[str, str]:
    """Return the API status and current version."""
    return {
        "message": "AgentLab API is running",
        "version": "0.1.0",
    }
