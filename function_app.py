"""Azure Functions Python v2 HTTP entry point."""

from __future__ import annotations

import json
import logging
import uuid

import azure.functions as func

from src.assessment import assess, validate_payload
from src.foundry_client import summarize_assessment


app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)


@app.route(route="assess", methods=["POST"])
def assess_use_case(req: func.HttpRequest) -> func.HttpResponse:
    correlation_id = req.headers.get("x-correlation-id", str(uuid.uuid4()))
    try:
        use_case = validate_payload(req.get_json())
        result = assess(use_case)
        result["ai_summary"] = summarize_assessment(result)
        result["correlation_id"] = correlation_id
        logging.info(
            "assessment_complete recommendation=%s correlation_id=%s",
            result["recommendation"],
            correlation_id,
        )
        return func.HttpResponse(
            json.dumps(result, ensure_ascii=False),
            status_code=200,
            mimetype="application/json",
        )
    except (ValueError, TypeError, json.JSONDecodeError) as exc:
        logging.warning("invalid_request correlation_id=%s", correlation_id)
        return func.HttpResponse(
            json.dumps({"error": str(exc), "correlation_id": correlation_id}),
            status_code=400,
            mimetype="application/json",
        )
    except Exception:
        logging.exception("assessment_failed correlation_id=%s", correlation_id)
        return func.HttpResponse(
            json.dumps({"error": "internal_error", "correlation_id": correlation_id}),
            status_code=500,
            mimetype="application/json",
        )
