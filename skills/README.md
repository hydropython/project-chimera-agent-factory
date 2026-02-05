Skills Catalog — Project Chimera

Overview
- Each skill is a self-contained capability the agent can invoke at runtime.
- Skills must include: `manifest.yaml`, `schema/input.json`, `schema/output.json`, `handler.py` (or equivalent), and `README.md` with examples.

Core Skills (initial three)
1. content-generation
- Purpose: generate multi-turn content (e.g., task instructions, email drafts, or code snippets) given a prompt and style parameters.
- Input contract: `schema/input.json` — fields: `prompt` (string), `context` (object, optional), `max_tokens` (int, optional), `temperature` (float, optional)
- Output contract: `schema/output.json` — fields: `content` (string), `usage` (object), `debug` (object, optional)
- Runtime: requires network access to LLM API and credentials stored securely (prefer system-managed secrets).

2. fetch-trends
- Purpose: call OpenClaw `trends/fetch` endpoint and normalize results for downstream consumption.
- Input contract: `schema/input.json` — fields: `query` (string), `time_window` (string ISO interval, optional), `filters` (object, optional)
- Output contract: `schema/output.json` — fields: `trends` (array of {topic, score, samples}), `meta` (object)
- Runtime: HTTP client, signing support (HMAC or RSA), configurable endpoint and credentials.

3. register-service
- Purpose: create or update a service registration with OpenClaw, including metadata and capabilities.
- Input contract: `schema/input.json` — fields: `service` (object matching `specs/schemas/service.json`), `agent_id` (string), `credentials` (object, optional)
- Output contract: `schema/output.json` — fields: `status` (string), `service_id` (string), `errors` (array)
- Runtime: HTTP client, idempotency key generation, retry logic.

Directory layout
- `skills/<skill-name>/manifest.yaml` — metadata and runtime requirements
- `skills/<skill-name>/schema/input.json` — JSON Schema for input
- `skills/<skill-name>/schema/output.json` — JSON Schema for output
- `skills/<skill-name>/handler.py` — invocation entrypoint
- `skills/<skill-name>/README.md` — examples and operational notes

Next: scaffold `skills/content-generation`, `skills/fetch-trends`, and `skills/register-service` with minimal manifests and schema files.

Note on handlers:
- Runtime `handler.py` implementations are intentionally not included in this repository. Each skill includes a `HANDLER_PLACEHOLDER.md` describing the expected entrypoint and I/O contract. The runtime project should implement the actual handlers and load them according to `manifest.yaml`.
