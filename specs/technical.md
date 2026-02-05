# Technical Specifications

This document provides a concise, engineering-focused technical specification for Project Chimera's core services (trend ingestion, trend analysis, content generation, safety review) and integration with external platforms (including OpenClaw). It includes API contracts, JSON Schemas, OpenAPI fragments, security, observability, testing, and deployment guidance.

## System Overview
- Components:
  - Trend Fetcher: collects signals from external sources (Twitter, Reddit, YouTube, Google Trends).
  - Trend Analyzer: deduplicates, ranks, and predicts trend trajectories.
  - Content Generator: produces platform-optimized content variants.
  - Safety Layer: automated checks and human review workflow.
  - Registry/Integration Layer: service registration and discovery (OpenClaw integration).
  - Data Layer: Vector DB for embeddings, SQL for metadata, Cache for hot lookups.

## High-Level Data Flow
1. Fetcher ingests raw signals and stores interim records in the data layer.
2. Analyzer normalizes and consolidates into canonical trend objects.
3. Consumer (internal or external) requests content generation using trend IDs.
4. Content is passed to Safety Layer before publication; safety results update reputation/metrics.

## API Contracts (Summary)
- POST /api/v1/trends/fetch — request aggregated trends.
- GET /api/v1/trends/{id} — fetch trend details.
- POST /api/v1/content/generate — request content variants for a trend.
- POST /api/v1/safety/check — run safety checks on candidate content.

Full request/response examples were in the previous draft; below we add precise JSON Schemas and an OpenAPI fragment for engineering use.

## JSON Schemas

Agent identity schema (agent.json):

```json
{
  "$id": "https://example.com/schemas/agent.json",
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["agent_id","public_key"],
  "properties": {
    "agent_id": {"type":"string","pattern":"^chimera:[^:]+:[^:]+$"},
    "display_name": {"type":"string"},
    "agent_type": {"type":"string","enum":["worker","service","gateway"]},
    "capabilities": {"type":"array","items":{"type":"string"}},
    "public_key": {"type":"string"},
    "metadata": {"type":"object"}
  }
}
```

Service descriptor schema (service.json):

```json
{
  "$id": "https://example.com/schemas/service.json",
  "type": "object",
  "required":["service_id","agent_id","endpoint"],
  "properties":{
    "service_id":{"type":"string"},
    "agent_id":{"type":"string"},
    "endpoint":{"type":"string","format":"uri"},
    "input_schema":{"type":"object"},
    "output_schema":{"type":"object"},
    "pricing":{"type":"object"}
  }
}
```

Trend fetch request schema (trend_request.json):

```json
{
  "$id":"https://example.com/schemas/trend_request.json",
  "type":"object",
  "required":["request_id","sources"],
  "properties":{
    "request_id":{"type":"string"},
    "sources":{"type":"array","items":{"type":"string"}},
    "categories":{"type":"array","items":{"type":"string"}},
    "time_range":{"type":"string"},
    "geo_location":{"type":"string"},
    "limit":{"type":"integer","minimum":1}
  }
}
```

Content generation request schema (content_request.json):

```json
{
  "$id":"https://example.com/schemas/content_request.json",
  "type":"object",
  "required":["trend_id","platform"],
  "properties":{
    "trend_id":{"type":"string"},
    "platform":{"type":"string"},
    "content_type":{"type":"string"},
    "constraints":{"type":"object"},
    "context":{"type":"object"}
  }
}
```

## OpenAPI fragment (YAML) — core endpoints

```yaml
openapi: 3.0.3
info:
  title: Chimera Core APIs
  version: 1.0.0
paths:
  /api/v1/trends/fetch:
    post:
      summary: Fetch aggregated trends
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: 'https://example.com/schemas/trend_request.json'
      responses:
        '200':
          description: successful response
          content:
            application/json:
              schema:
                type: object
  /api/v1/content/generate:
    post:
      summary: Generate content variants
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: 'https://example.com/schemas/content_request.json'
      responses:
        '200':
          description: generation result
          content:
            application/json:
              schema:
                type: object
```

## Security
- Use mutual TLS or OAuth2/JWT for control-plane operations (service/agent registration).
- Use payload signing (ECDSA/RSA) for ownership proofs. Store private keys securely (hardware module or OS-protected key store).
- Sanitize and escape any user-provided input before using in downstream prompts or renderers.

## Signing & Key Management Recommendation

- Recommended algorithm: ECDSA (P-256) for payload signing to balance security and compact signatures. Use RSA-2048/3072 only where required for compatibility.
- Key Storage: store private keys in a managed Key Management Service (KMS) such as AWS KMS, Azure Key Vault, or GCP KMS; never store raw private keys in the repo or environment variables.
- Signing flows:
  - Control-plane registrations: create a signing key per agent or per team stored in KMS; agents request signing operations via a short-lived credential or use a hardware-backed key on the host.
  - Payloads: canonicalize JSON (stable key ordering, UTF-8) and include `timestamp` and `nonce` in the signed body to prevent replay attacks.
- Verification: OpenClaw (or counterpart) must expose public keys and key-ids to verify signatures; include `key_id` in registration payloads.
- Rotation policy: rotate keys every 90 days (or according to org policy). Support a `rotate-key` endpoint that accepts a signed rotation request from the existing key to publish a new public key.
- Auditing: log KMS key usage events and signing operations; ensure key access is gated by IAM roles and MFA for high-privilege operations.

## Observability & Monitoring

## Observability & Monitoring
- Logs: structured JSON logs including `component`, `operation`, `agent_id`, `request_id`.
- Metrics: `chimera.trends.fetch.count`, `chimera.content.generate.latency_ms`, `chimera.safety.failures`.
- Tracing: propagate `trace_id` in HTTP headers for distributed tracing.

## Reliability & Operational Considerations
- Idempotency: all mutating endpoints accept `Idempotency-Key`.
- Retries: exponential backoff for transient errors, max 5 attempts.
- Circuit Breaker: open on sustained 5xx error rate; fallback to degraded mode.

## Testing
- Unit tests for canonicalization/signature logic and schema validation.
- Integration tests against a staging API; include negative tests for malformed payloads, auth failures, and safety checks.
- E2E tests: register agent -> register service -> discover -> fetch -> generate -> safety.

## Performance & Scaling
- Horizontal scaling for fetchers and analyzers; shared cache for hot queries.
- Batch requests where possible; use async workers for long-running analysis.
- SLOs: 95th percentile trend fetch latency < 500ms (local cache), content generation 95p < 2s (model-dependent).

## Deployment
- Expose `/health` and `/ready` endpoints.
- Use rolling updates with connection draining; mark agent `draining` in registry prior to shutdown.

## Security & Compliance Notes
- PII: redact or avoid sending PII to 3rd-party integrations; document retention policy.
- Auditing: keep immutable audit logs for registration and reputation-related events.

---

Next steps I can take: generate standalone JSON Schema files under `specs/schemas/`, produce a full `openapi.yaml`, or scaffold a small test harness to validate registration flows — which would you like me to do next?
