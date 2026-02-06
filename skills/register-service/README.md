register-service skill
======================

Runtime skill for creating or updating a service registration with
OpenClaw. The Dev MCP orchestrates registration flows but only calls
this skill via the stable `handler.handle(input)` entrypoint.

## Contract

- Entrypoint: `handler.handle(input: dict) -> dict`
- Input schema: `skills/register-service/schema/input.json`
- Output schema: `skills/register-service/schema/output.json`

## Example

Input (shape only, see `specs/schemas/service.json` for full details):

```json
{
  "service": {
    "name": "example-service",
    "description": "Example service registered via Chimera",
    "endpoints": []
  },
  "agent_id": "agent-123"
}
```

Output:

```json
{
  "status": "ok",
  "service_id": "svc-123",
  "errors": []
}
```

