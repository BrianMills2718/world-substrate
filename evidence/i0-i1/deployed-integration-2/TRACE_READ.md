# Production API preflight rejection — no model execution

The first HTTP request to /generate-world returned HTTP403 because the probe omitted the required application Origin header. The service rejected it before owner budget reservation or model execution. The exact request body and error are retained in protocol.jsonl; result.json and trace-ids.json report zero calls and no trace roots. No build or resident round occurred.

## Findings

Corrected the probe to supply the service-required application origin, keeping owner authentication, origin checking and budgets enabled. This is retained request-validation evidence, not I0/I1 acceptance. The earlier deployed-integration-1 preflight separately failed shell command quoting before any POST and is retained as result.json with zero calls.
