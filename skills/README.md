Skills Catalog — Project Chimera

## Dev MCP vs Runtime Skills

- **Dev MCP (brain)** lives under `src/mcp/` and `scripts/`:
  - `src/mcp/spec_kit.py` – developer CLI for specs, skills, and tests.
  - `src/mcp/validate_skill_contracts.py` – validates JSON contracts against `specs/schemas`.
  - `scripts/run_skill.py` and `skills/loader.py` – generic runners/loaders.
- **Runtime skills (hands)** live under `skills/` and `src/skills/`:
  - `skills/<skill-name>/...` – manifests, schemas, and runtime entrypoints (`handler.py`).
  - `src/skills/...` – optional Python-level helpers/interfaces (e.g. `src/skills/trend_fetcher.py`).

The MCP \"brain\" never reaches into a skill’s internals directly – it only:

- validates requests/responses against schemas,
- invokes skills through a stable entrypoint (`handler.handle(...)` or a Python interface).

## Shared skill contract

All skills follow the same high-level contract:

- Entrypoint: `handler.handle(input: dict) -> dict`
- Input: must match `skills/<skill-name>/schema/input.json`
- Output: must match `skills/<skill-name>/schema/output.json`
- Errors: on failure, handlers should return a JSON object with an `error` property.

## Core skills

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
- Python helper: `src/skills/trend_fetcher.fetch_trends(request: dict) -> dict` (see `tests/interfaces.py`).

3. register-service
- Purpose: create or update a service registration with OpenClaw, including metadata and capabilities.
- Input contract: `schema/input.json` — fields: `service` (object matching `specs/schemas/service.json`), `agent_id` (string), `credentials` (object, optional)
- Output contract: `schema/output.json` — fields: `status` (string), `service_id` (string), `errors` (array)
- Runtime: HTTP client, idempotency key generation, retry logic.

## Directory layout

- `skills/<skill-name>/manifest.yaml` — metadata and runtime requirements
- `skills/<skill-name>/schema/input.json` — JSON Schema for input
- `skills/<skill-name>/schema/output.json` — JSON Schema for output
- `skills/<skill-name>/handler.py` — invocation entrypoint (runtime only)
- `skills/<skill-name>/README.md` — examples and operational notes
- `src/skills/<helper>.py` — optional Python helpers/interfaces for tests and MCP code

Note on handlers:

- Runtime `handler.py` implementations are intentionally not included in this repository.
- Each skill includes a `HANDLER_PLACEHOLDER.md` describing the expected entrypoint and I/O contract.
- The runtime project should implement the actual handlers and load them according to `manifest.yaml`.

