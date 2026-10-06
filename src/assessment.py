"""Deterministic validation and governance scoring for AI use-case proposals."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


ALLOWED_DATA_CLASSES = {"public", "internal", "confidential", "personal"}
ALLOWED_IMPACT = {"assistive", "recommendation", "automated-action"}


@dataclass(frozen=True)
class UseCase:
    title: str
    business_goal: str
    data_classification: str
    decision_impact: str
    human_approval: bool
    owner: str


def validate_payload(payload: dict[str, Any]) -> UseCase:
    """Validate untrusted JSON before any model or platform call."""
    if not isinstance(payload, dict):
        raise ValueError("Request body must be a JSON object.")

    required = {
        "title",
        "business_goal",
        "data_classification",
        "decision_impact",
        "human_approval",
        "owner",
    }
    missing = required - payload.keys()
    if missing:
        raise ValueError(f"Missing fields: {', '.join(sorted(missing))}.")

    for field in ("title", "business_goal", "owner"):
        if not isinstance(payload[field], str) or not payload[field].strip():
            raise ValueError(f"{field} must be a non-empty string.")
        if len(payload[field]) > 500:
            raise ValueError(f"{field} is too long.")

    if payload["data_classification"] not in ALLOWED_DATA_CLASSES:
        raise ValueError("Unsupported data_classification.")
    if payload["decision_impact"] not in ALLOWED_IMPACT:
        raise ValueError("Unsupported decision_impact.")
    if not isinstance(payload["human_approval"], bool):
        raise ValueError("human_approval must be a boolean.")

    return UseCase(**{field: payload[field] for field in required})


def assess(use_case: UseCase) -> dict[str, Any]:
    """Return an explainable readiness decision without an AI dependency."""
    risk_points = 0
    checks: list[dict[str, str]] = []

    if use_case.data_classification in {"confidential", "personal"}:
        risk_points += 3 if use_case.data_classification == "personal" else 2
        checks.append({"status": "required", "control": "privacy-and-data-owner-review"})
    else:
        checks.append({"status": "passed", "control": "data-classification"})

    if use_case.decision_impact == "automated-action":
        risk_points += 3
        checks.append({"status": "required", "control": "execution-boundary-review"})
    elif use_case.decision_impact == "recommendation":
        risk_points += 1
        checks.append({"status": "required", "control": "output-quality-evaluation"})
    else:
        checks.append({"status": "passed", "control": "assistive-use-only"})

    if not use_case.human_approval and use_case.decision_impact != "assistive":
        risk_points += 3
        checks.append({"status": "blocked", "control": "human-approval"})
    else:
        checks.append({"status": "passed", "control": "human-approval"})

    if any(check["status"] == "blocked" for check in checks):
        recommendation = "blocked"
    elif risk_points >= 4:
        recommendation = "controlled-poc"
    elif risk_points >= 2:
        recommendation = "limited-pilot"
    else:
        recommendation = "prototype"

    return {
        "use_case": asdict(use_case),
        "risk_points": risk_points,
        "recommendation": recommendation,
        "checks": checks,
        "next_step": {
            "blocked": "Add human approval and review the execution boundary.",
            "controlled-poc": "Run a time-boxed PoC with privacy, security and owner sign-off.",
            "limited-pilot": "Define success metrics and test with a restricted user group.",
            "prototype": "Build a small measurable prototype with synthetic data.",
        }[recommendation],
    }
