from fastapi import FastAPI

from .config import app_description, app_name, app_version


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
