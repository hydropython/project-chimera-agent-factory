fetch-trends skill
==================

Runtime skill for fetching and normalizing trend data from OpenClaw. The
Dev MCP uses this skill via `handler.handle(input)` or via the Python
helper `src/skills/trend_fetcher.fetch_trends`.

## Contract

- Entrypoint: `handler.handle(input: dict) -> dict`
- Input schema: `skills/fetch-trends/schema/input.json`
- Output schema: `skills/fetch-trends/schema/output.json`

## Example

Input:

```json
{
  "query": "climate policy",
  "time_window": "P30D"
}
```

Output:

```json
{
  "trends": [
    { "topic": "carbon tax", "score": 0.82, "samples": ["...sample text..."] }
  ],
  "meta": { "source": "openclaw-mock" }
}
```

