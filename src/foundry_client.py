"""Optional Microsoft Foundry response client using keyless Entra ID auth."""

from __future__ import annotations

import os
from typing import Any


def configured() -> bool:
    return bool(os.getenv("AZURE_OPENAI_ENDPOINT") and os.getenv("AZURE_OPENAI_DEPLOYMENT"))


def summarize_assessment(assessment: dict[str, Any]) -> str | None:
    """Create a short stakeholder summary when Azure configuration is available."""
    if not configured():
        return None

    from azure.identity import DefaultAzureCredential, get_bearer_token_provider
    from openai import OpenAI

    endpoint = os.environ["AZURE_OPENAI_ENDPOINT"].rstrip("/") + "/openai/v1/"
    deployment = os.environ["AZURE_OPENAI_DEPLOYMENT"]
    token_provider = get_bearer_token_provider(
        DefaultAzureCredential(),
        "https://ai.azure.com/.default",
    )
    client = OpenAI(base_url=endpoint, api_key=token_provider)
    response = client.responses.create(
        model=deployment,
        instructions=(
            "You summarize AI governance assessments for business and IT stakeholders. "
            "Use only the supplied JSON. Do not add legal conclusions or invented facts. "
            "Return at most three short sentences."
        ),
        input=str(assessment),
    )
    return response.output_text.strip()
