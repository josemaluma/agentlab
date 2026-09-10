"""Basic application configuration."""

import os

app_name = "AgentLab API"
app_version = "0.1.0"
app_description = "Minimal API for the AgentLab project."

# Keep secrets outside the source code.  An unset key remains None.
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL") or "gpt-4.1-mini"
