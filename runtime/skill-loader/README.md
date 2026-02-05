Runtime Skill Loader — Interface spec

Purpose
- Describe the expected behavior and contract for the runtime skill-loader that will load skills from `skills/` and execute them.

Responsibilities
- Discover skills under the `skills/` directory by reading `manifest.yaml` files.
- Validate input payloads against `schema/input.json` before invoking the skill.
- Provide a secure execution environment for skill handlers (e.g., sandbox, container, or dedicated process).
- Supply environment variables and secrets to the handler via an established secrets provider.
- Capture and normalize outputs, validating them against `schema/output.json`.

Entrypoints and API
- `load_skill(path: str) -> SkillMeta` — load manifest and schemas, return metadata.
- `invoke_skill(name: str, input: dict) -> dict` — validate, call handler, validate output, and return result.

Handler contract
- Handlers must expose a single function: `handle(input: dict) -> dict`.
- Handlers should avoid long-running CPU work and must be interruptible.

Security
- Secrets should never be stored in plaintext in the repo.
- Enforce least privilege; only provide secrets required by the skill.

Observability
- Emit structured logs for each invocation: skill name, request id, duration, success/failure, and error details.

Errors and retries
- The loader must classify errors as transient or permanent. Transient errors may be retried with backoff by the caller.

Next steps
- Implement the loader in the runtime repo (separate project). Add unit tests to verify schema validation and loading logic.
