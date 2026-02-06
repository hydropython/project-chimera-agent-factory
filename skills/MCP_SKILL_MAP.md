MCP ↔ Skills Mapping
====================

This document explains how the \"brain\" (MCP / developer tooling) relates
to the runtime \"hands\" (skills).

## MCP tooling (developer side)

| MCP module / script              | Responsibility                                               | Related skills / assets                     |
|----------------------------------|--------------------------------------------------------------|---------------------------------------------|
| `src.mcp.spec_kit`              | Developer CLI for specs, skill validation, and tests        | Uses `make spec-check`, `pytest`, contracts |
| `src.mcp.validate_skill_contracts` | Validates JSON skill contracts against shared schemas    | Reads `skills/*.json`, `specs/schemas/*`    |
| `scripts/validate_specs.py`     | Validates `specs/schemas/*.json` and `specs/openapi.yaml`   | All skills via shared schemas               |
| `scripts/run_skill.py`          | Thin runner for invoking a named skill with JSON input      | Any skill in `skills/*` via `skills.loader` |
| `skills/loader.py`              | Discovers skills, validates input, loads `handler.py`       | `skills/<name>/manifest.yaml`, schemas, handlers |

## Runtime skills (agent side)

| Skill directory                  | Purpose                                                      | Canonical runtime interface                  |
|----------------------------------|--------------------------------------------------------------|----------------------------------------------|
| `skills/content-generation/`     | Generate multi-turn content given prompt and style params   | `handler.handle(input_data)`                 |
| `skills/fetch-trends/`          | Call OpenClaw `trends/fetch` and normalize results          | `handler.handle(input_data)`                 |
| `skills/register-service/`      | Register or update a service with OpenClaw                  | `handler.handle(input_data)`                 |
| `src.skills.trend_fetcher`      | Python-level TrendFetcher implementation used by tests/MCP  | `fetch_trends(request: dict) -> dict`        |

## Mental model

- **MCP (`src.mcp`, `scripts/`)**: decides *what* should be validated or run and orchestrates workflows.
- **Skills (`skills/`, `src.skills/`)**: implement the concrete behavior; they do not need to know *who* is calling them.

