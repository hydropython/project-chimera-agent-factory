Tooling & MCP Strategy for Project Chimera

Goal
- Provide a minimal, developer-focused MCP tooling stack that speeds iteration and enables safe automation for the co-pilot and developer workflows.

Sub-Task A — Developer Tools (MCP)

Selected MCP servers
- git-mcp
  - Purpose: version-control operations with safe, auditable commits and git metadata exposure to MCP clients.
  - Usage: run `git status`, create branches, stage/commit patches produced by the co-pilot. Configure to require small, focused commits and include commit message templates.
  - Security: require token-based auth; do not expose credentials in payloads.

- filesystem-mcp
  - Purpose: read/write project files, create patches, and preview diffs before committing.
  - Usage: provide read-only access to most flows; grant write access only after explicit plan and user approval.
  - Security: sandboxed file paths limited to workspace root; enforce file-type restrictions.

- run-python-mcp (or python-exec-mcp)
  - Purpose: execute lint, unit tests, validation scripts (e.g., `scripts/validate_specs.py`) in an isolated environment.
  - Usage: run test harnesses, run schema validation, safety checks. Return structured test results and logs.
  - Security: run in ephemeral containers; limit network egress.

- logging-mcp / telemetry-mcp
  - Purpose: capture structured logs from the co-pilot and MCP actions for audit, debugging, and AI-fluency triggers.
  - Usage: emit structured JSON logs, trigger the AI fluency tools when specific patterns are detected.

Configuration recommendations
- Each MCP should have an access control policy and audit logging enabled.
- For development, provide a local MCP stack (mock services) and CI-integrated MCP endpoints for automated validation.
- Require explicit confirmations for any write/commit operation initiated by the co-pilot.

Operational notes
- The co-pilot must always present a plan before performing file edits or commits (see `CLAUDE.md`).
- All MCP interactions must be signed and logged; keep a tamper-evident audit trail for critical ops.

Sub-Task B — Agent Skills (Runtime) (overview)
- Skills are capability packages the runtime can load and invoke. A Skill bundles input schema, outputs, runtime requirements (libraries, credentials), and error handling behavior.
- Skills are registered in the `skills/` folder and documented with I/O contracts and examples.

Next: create `skills/README.md` with three critical skill definitions and I/O contracts.
