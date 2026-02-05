Handler placeholder

This skill's runtime handler is intentionally not implemented in this repository.

Contract expectations for the runtime implementer:
- Entrypoint name: `handle(input: dict) -> dict`
- Input: Must match `skills/register-service/schema/input.json`.
- Output: Must match `skills/register-service/schema/output.json`.
- Idempotency key support: runtime should pass `Idempotency-Key` header when calling remote APIs.

Deployment notes:
- The runtime should supply `OPENCLAW_URL` and credentials via environment variables or secrets manager.
- Input validation required prior to registration calls.

TODO: add examples of idempotency headers and expected HTTP response handling.
