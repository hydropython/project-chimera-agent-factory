Handler placeholder

This skill's runtime handler is intentionally not implemented in this repository.

Contract expectations for the runtime implementer:
- Entrypoint name: `handle(input: dict) -> dict`
- Input: Must match `skills/fetch-trends/schema/input.json`.
- Output: Must match `skills/fetch-trends/schema/output.json`.
- Networking: runtime must supply `OPENCLAW_URL` and credentials via environment.
- Error handling: return JSON with `error` property on failure.

Deployment notes:
- The runtime should perform schema validation before invoking the skill code.
- Ensure request signing configuration is present if required by the environment.

TODO: implement HTTP client wrapper and retry/reconciliation logic inside runtime.
