Handler placeholder

This skill's runtime handler is intentionally not implemented in this repository.

Contract expectations for the runtime implementer:
- Entrypoint name: `handle(input: dict) -> dict`
- Input: Must match `skills/content-generation/schema/input.json`.
- Output: Must match `skills/content-generation/schema/output.json`.
- Error handling: return JSON with `error` property on failure.
- Idempotency / retries: caller will handle retries; handler should be idempotent when possible.

Deployment notes:
- The runtime should load the skill's `manifest.yaml` to determine requirements.
- Credentials (LLM API keys) must be provided via environment variables or a secrets provider.
- The handler should validate input against the input schema before processing.

TODO: implement runtime-safe wrapper and tests in the runtime project.
