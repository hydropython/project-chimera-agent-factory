# Project Chimera — Agent Factory

Project Chimera is a spec-driven repository that scaffolds an autonomous AI influencer platform: trend ingestion, content generation, safety reviews, and service integration (OpenClaw). This repo contains the technical and functional specifications, schema contracts, skill definitions, test harnesses, CI, and infra scaffolding needed to develop, validate, and operate the agents.

Contents
- `specs/` — master specifications and integration contracts (meta, functional, technical, OpenClaw integration, schemas).
- `skills/` — skill manifests and input/output schemas (runtime handlers are intentionally omitted; see placeholders).
- `tests/` — TDD scaffolding (failing tests that define empty slots for implementers).
- `scripts/` — helper scripts (spec validation, skill runner stub).
- `alembic/` — migration scaffold and initial migration for video metadata DB.
- `.github/workflows/` — CI workflows: spec validation and test pipeline.
- `Dockerfile`, `Makefile` — container and developer automation.
- `CLAUDE.md`, `.coderabbit.yaml` — co-pilot rules and AI review policy.

Quick start

1. Install dependencies (recommended to use a virtualenv):

```bash
python -m venv .venv
source .venv/bin/activate    # or .\.venv\Scripts\activate on Windows
pip install -r requirements.txt
```

2. Run spec-check (validates JSON schemas and scans for leftover heredoc wrappers):

```bash
make spec-check
# or
python scripts/validate_specs.py
```

3. Run tests (TDD: some tests are intentionally failing to define empty slots):

```bash
make test
# or
python -m pytest -q
```

Notes on failing tests
- Tests under `tests/` are intentionally written to fail until implementations are provided. They create the "empty slot" that the agent runtime and engineers must fill (TrendFetcher, skill handlers).

Development workflow
1. Read the relevant spec files in `specs/` before making changes. The project enforces a Prime Directive: NEVER generate code without checking specs first. See `CLAUDE.md` for co-pilot rules.
2. Make small, focused changes and include/modify tests to codify expected behavior (TDD).
3. Run `make spec-check` then `make test` locally.
4. Push changes to a feature branch and open a PR. CI will run spec validation and tests automatically.

Skills and Runtime
- `skills/` contains skill manifests and JSON Schemas for inputs and outputs. Runtime handler implementations are deliberately omitted and documented by `HANDLER_PLACEHOLDER.md` files; implementers should provide handlers that conform to the schemas and the loader contract (`runtime/skill-loader/README.md`).

Database & Migrations
- The `specs/db_schema.md` contains the ERD and Postgres DDL for video metadata and related tables.
- Alembic scaffold and an initial migration are included under `alembic/`. To run migrations, configure your DB URL in `alembic.ini` (or set `sqlalchemy.url` via env) and run:

```bash
pip install alembic
alembic upgrade head
```

Containerization
- Build the project image (optional):

```bash
make build-image
```

CI / QA
- `/.github/workflows/specs-validation.yml` runs the spec validator on spec changes.
- `/.github/workflows/main.yml` runs `make spec-check` then `make test` on push/PR to `main`.

Security & Key Management
- The repository recommends using ECDSA (P-256) for payload signing and storing private keys in a managed KMS (AWS KMS, Azure Key Vault, GCP KMS). See `specs/technical.md` for a full recommendation and rotation policy.
- Never commit secrets. `.coderabbit.yaml` contains AI review rules to detect obvious secret leaks and insecure patterns.

Contributing
- Follow the Prime Directive (`CLAUDE.md`): link PRs to `specs/` sections and include a short plan and tests.
- Use small reviewable commits; include a test or validation step where possible.

Useful commands
- `make setup` — install dependencies
- `make spec-check` — validate specs
- `make test` — run pytest
- `make build-image` — build Docker image
- `python scripts/run_skill.py <skill> <json|file>` — run a skill via the loader (for runtime implementers)

Contact & License
- Repository owner: see Git history and remote `origin` for repo contact.
- License: see top-level `LICENSE` file for project license terms.

Appendix
- Important files:
  - `specs/_meta.md` — vision & constraints
  - `specs/functional.md` — user stories & acceptance criteria
  - `specs/technical.md` — API contracts, schemas, security
  - `specs/openclaw_integration.md` — OpenClaw integration guidance
  - `skills/*/HANDLER_PLACEHOLDER.md` — handler contract placeholders

---

This README is intended to be the canonical onboarding and operational summary for engineers and reviewers working on Project Chimera.

Architecture diagram

The repository includes a Mermaid diagram illustrating the high-level architecture at `diagrams/architecture.mmd`. Below is an embeddable Mermaid view:

```mermaid
flowchart LR
  subgraph External
    A["Social Platforms\n(Twitter, Reddit, YouTube, Google Trends)"]
    B["OpenClaw Network"]
    H["Human Reviewers"]
  end

  subgraph Chimera_Core
    TF["Trend Fetcher"]
    TA["Trend Analyzer"]
    CG["Content Generator"]
    SL["Safety Layer"]
    SK["Skills Runtime"]
    RG["Registry / Integration"]
    DB["Metadata DB"]
    CACHE["Cache / Vector DB"]
    OBS["Observability / Tracing"]
  end

  A -->|signals| TF
  TF --> TA
  TA --> DB
  TA --> CG
  CG --> SL
  SL -->|queue| H
  H -->|decision (approve/reject)| SL
  SL -->|publish| RG
  RG -->|register/discover| B
  RG --> SK
  SK --> CG
  CG --> DB
  DB --> CACHE
  TF --> OBS
  TA --> OBS
  CG --> OBS
  RG --> OBS

```

