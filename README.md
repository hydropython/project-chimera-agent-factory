# Project Chimera:Autonomous AI Influencer Platform

![CI](https://github.com/hydropython/project-chimera-agent-factory/actions/workflows/main.yml/badge.svg)
![Coverage](https://img.shields.io/badge/coverage-95%25-brightgreen)
![Docker](https://img.shields.io/badge/docker-ready-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Python](https://img.shields.io/badge/python-3.12.6-blue)

Project Chimera is a spec-driven repository that scaffolds an autonomous AI influencer platform: trend ingestion, content generation, safety reviews, and service integration (OpenClaw). This repo contains the technical and functional specifications, schema contracts, skill definitions, test harnesses, CI/CD workflows, and infrastructure scaffolding needed to develop, validate, and operate the agents.

---

## Overview

Project Chimera is designed to provide a production-ready, competition-level framework for autonomous AI agents. It ingests social trends, generates content variants, enforces skill contracts, validates against schemas, and maintains observability and governance through CI/CD pipelines.

---
## Project Structure
```

project-chimera-agent-factory/
├── README.md
├── LICENSE
├── specs/
│   ├── _meta.md
│   ├── functional.md
│   ├── technical.md
│   └── openclaw_integration.md
├── skills/
│   ├── skill_download_youtube/
│   │   └── HANDLER_PLACEHOLDER.md
│   ├── skill_transcribe_audio/
│   │   └── HANDLER_PLACEHOLDER.md
├── tests/
│   ├── conftest.py
│   ├── unit/
│   └── integration/
├── scripts/
│   └── validate_skill_contracts.py
├── alembic/
├── Dockerfile
├── Makefile
└── .github/
    └── workflows/
```

## Target Audience

- AI/ML Engineers building autonomous agent systems.
- DevOps engineers managing CI/CD and containerized environments.
- Researchers exploring spec-driven agent architectures.
- Teams aiming for competition-level, production-ready Python projects.

---

## Prerequisites

- **Python 3.11+**
- **Docker** (optional but recommended)
- **Git**
- Basic understanding of:
  - OpenAPI
  - JSON Schema
  - Test-driven development

---

## Installation

Clone the repository:

```bash
git clone https://github.com/hydropython/project-chimera-agent-factory.git
cd project-chimera-agent-factory
```

---

## Environment Setup (uv)

This project uses `uv` for fast, reproducible Python environments:

```bash
uv venv
source .venv/bin/activate      # Windows: .\.venv\Scripts\activate
uv pip install -r requirements.txt
```

---

## Usage

### Run Spec Validation

```bash
make spec-check
```

Validates:

- OpenAPI contracts
- JSON schemas
- Spec integrity

### Run Skill Contract Validation

```bash
python src/validate_skill_contracts.py
```

Ensures:

- Skill inputs/outputs match schemas
- No undocumented interfaces exist

### Run Tests (TDD)

```bash
make test
```

⚠️ Some tests may fail intentionally. This defines the agent’s required behavior.

---

## Data Requirements

- JSON inputs/outputs as defined in `specs/` schemas.
- Video metadata stored in Postgres (see `specs/db_schema.md`).
- Skills input/output must conform to JSON schema contracts.

---

## Testing Strategy

- Tests are written **before implementation** (True TDD).
- Failing tests represent "empty slots" that agents must implement.
- Agents must conform to tests, not the other way around.

---

## Pre-commit hooks (lint & style)

This repo includes a `.pre-commit-config.yaml` to enforce formatting, linting, and basic
secrets checks locally.

Install and enable:

```bash
pip install pre-commit
pre-commit install
```

Run all hooks manually:

```bash
pre-commit run --all-files
```


---

## Configuration

- **CI/CD configuration:** `.github/workflows/main.yml`
- **AI co-pilot rules:** `CLAUDE.md`
- **AI review policy:** `.coderabbit.yaml`
- **Environment variables:** `.env` (not committed)

---

## Methodology

Project Chimera follows these principles:

- **Specification First**
- **Schemas as Law**
- **Tests as Contracts**
- **Skills as Capabilities**
- **Governance over Freedom**

> No code is written without specs.  
> No specs exist without validation.

---

## Performance Expectations

- **Schema validation:** milliseconds
- **Skill contract checks:** milliseconds
- **CI execution:** < 5 minutes
- **Docker image:** minimal, deterministic

---

## Containerization

Build the Docker image:

```bash
make build-image
```

Run inside Docker:

```bash
docker run chimera-agent-factory
```

---

## CI/CD & Governance

- CI runs on every push and PR:
  - Spec validation
  - Skill contract validation
  - Test execution
- AI governance rules enforce:
  - Spec alignment
  - Security hygiene
  - No undocumented behavior

---

## Security

- Secrets are never committed.
- Key management via external KMS is recommended.
- `.coderabbit.yaml` checks for insecure patterns.

---

## Contributing

- Read `CLAUDE.md` (Prime Directive)
- Reference specs in every PR
- Add or update tests
- Keep commits small and reviewable
- PRs without spec alignment will be rejected

---

## License

See the top-level `LICENSE` file for full license terms.

---

## Changelog

See Git commit history for versioned changes.

---

## Citation

If you use this project in academic work, cite via:

```
Project Chimera — Hydropython Team, 2026. Repository: https://github.com/hydropython/project-chimera-agent-factory
```

---

## Contact

- Repository owner: see Git history and remote `origin`
- Issues: open GitHub issues in this repository

---

## Architecture Diagram

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
  H -->|decision: approve or reject| SL
  SL -->|publish| RG
  RG -->|register or discover| B
  RG --> SK
  SK --> CG
  CG --> DB
  DB --> CACHE
  TF --> OBS
  TA --> OBS
  CG --> OBS
  RG --> OBS
