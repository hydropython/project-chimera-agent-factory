content-generation skill
========================

Runtime skill (\"hands\") for generating multi-turn content. The Dev MCP
(\"brain\") never calls this directly; it goes through the stable
`handler.handle(input)` entrypoint or higher-level orchestrators.

## Contract

- Entrypoint: `handler.handle(input: dict) -> dict`
- Input schema: `skills/content-generation/schema/input.json`
- Output schema: `skills/content-generation/schema/output.json`

## Example

Input:

```json
{
  "prompt": "Write a short welcome email for a new user."
}
```

Output:

```json
{
  "content": "Write a short welcome email for a new user.",
  "usage": { "tokens": 7 }
}
```

