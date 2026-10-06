# Operations checklist

## Before deployment

- assign a named business owner and technical owner;
- define data classification and retention;
- use managed identity and least-privilege RBAC;
- keep secrets out of source control and local settings examples;
- define latency, error-rate and cost alerts;
- confirm that model output cannot bypass deterministic controls;
- run automated tests and dependency review.

## Monitoring signals

- request count and response status;
- validation failure rate;
- model-call latency and failure rate;
- recommendation distribution;
- correlation ID for incident investigation;
- dependency availability and throttling.

## Incident response

1. Disable the optional model integration without disabling deterministic assessment.
2. Use correlation IDs to isolate affected requests.
3. Review Application Insights errors without logging request bodies.
4. Escalate privacy, security and data-quality issues to the named owners.
