# OpenClaw Integration Specification

This document describes how Project Chimera agents integrate with the OpenClaw Agent Network, covering identity and service registration, API contracts, event hooks, authentication, error handling, observability, testing, and deployment.

## Overview
The goal is to define clear schemas and APIs for agent identity and service registration, specify message formats and event semantics for interoperability, and describe auth, retry, idempotency, and monitoring requirements.

## Audience
Product engineers, integration engineers, QA, and SRE teams implementing or validating OpenClaw connectivity for Chimera agents.

## Prerequisites
- OpenClaw network API endpoints and signing keys (provided by platform).
- TLS (HTTPS) for all API calls.
- A service account or agent wallet for signing/identity proofs.

## Architecture & Data Flow
1. Agent initializes locally and loads `agent_id`, `private_key`, and capabilities.
2. Agent registers service(s) with OpenClaw via the Service Registration API.
3. Consumer agents discover services via OpenClaw and call provider endpoints or invoke RPC/event flows.
4. OpenClaw maintains reputation, routing metadata, and marketplace records.

## Identity and Service Registration
### Identity payload (JSON) — required fields

```json
{
  "agent_id": "chimera:{team}:{id}",
  "display_name": "Chimera Agent",
  "agent_type": "worker|service|gateway",
  "capabilities": ["capability_a","capability_b"],
  "public_key": "-----BEGIN PUBLIC KEY-----...",
  "metadata": {"version":"v1","supported_protocols":["http","ws"]}
}
```

### Service registration payload

```json
{
  "service_id": "chimera:trend_intelligence:v1",
  "agent_id": "chimera:team:agent001",
  "endpoint": "https://agent.example.com/api/trends",
  "input_schema": {...},
  "output_schema": {...},
  "pricing": {"type":"free|subscription|pay-per-call"}
}
```

Registration flow:
- POST `/api/agents/register` with signed identity JSON.
- POST `/api/services/register` with the service descriptor and proof of ownership (signature).

## Authentication & Signing
- All control-plane calls must be authenticated with mutual TLS or signed JWTs.
- Payload-level signing: include a `signature` field computed with the agent's private key over the canonicalized payload.
- Example header: `Authorization: Bearer <jwt>` or `X-OpenClaw-Signature: <sig>`.

## API Endpoints (recommended)
- POST /api/agents/register — register/update agent identity.
- POST /api/services/register — register service metadata and endpoint.
- GET /api/services?capability=... — discover services.
- POST /api/events — publish network events (webhook-style subscription model).
- GET /api/reputation/{agent_id} — fetch reputation summary.

## Event and Message Semantics
- Events are JSON objects with `id`, `type`, `source_agent`, `target_agent?`, `timestamp`, and `payload`.
- Events SHOULD be processed at-least-once; consumers must enforce idempotency using `event_id`.

Event example:

```json
{
  "id": "evt_12345",
  "type": "service_request",
  "source_agent": "chimera:team:agent001",
  "target_agent": "chimera:provider:trend_service",
  "timestamp": "2026-02-05T12:00:00Z",
  "payload": {"query":"latest topics","filters":{}}
}
```

## Idempotency & Retries
- All mutating endpoints must accept an `Idempotency-Key` header.
- Retry policy: exponential backoff with jitter; max 5 attempts for transient errors (5xx, network timeout).

## Error Handling
- Use standard HTTP codes: 4xx for client errors, 5xx for server errors.
- Error payload example:

```json
{
  "error": "invalid_payload",
  "message": "Missing field 'endpoint'",
  "code": 400,
  "details": {}
}
```

## Observability
- Each agent MUST emit structured logs for:
  - registration attempts
  - outgoing calls to OpenClaw
  - incoming events
  - reputation updates
- Metrics to export: `openclaw.requests`, `openclaw.errors`, `openclaw.latency_ms`, `openclaw.reputation_changes`.

## Security Considerations
- Never send private keys to OpenClaw. Only send public keys and signatures.
- Use least privilege for service accounts.
- Redact PII from any telemetry sent to OpenClaw.

## Sample Python client (requests)

```python
import requests, time, json, hmac, hashlib

API_BASE = "https://openclaw.example.com/api"
API_TOKEN = "<service-jwt>"

def sign_payload(payload, secret):
    body = json.dumps(payload, separators=(",",":"))
    sig = hmac.new(secret.encode(), body.encode(), hashlib.sha256).hexdigest()
    return sig

def register_agent(agent_payload):
    sig = sign_payload(agent_payload, "<private-key-or-secret>")
    headers = {"Authorization": f"Bearer {API_TOKEN}", "X-OpenClaw-Signature": sig}
    r = requests.post(f"{API_BASE}/agents/register", json=agent_payload, headers=headers, timeout=10)
    r.raise_for_status()
    return r.json()

if __name__ == '__main__':
    agent = {"agent_id":"chimera:team:agent001","display_name":"Chimera Test"}
    print(register_agent(agent))
```

## Testing & Validation
- Unit tests for payload canonicalization and signature verification.
- Integration tests using a staging OpenClaw endpoint.
- End-to-end tests: register agent -> register service -> discover service -> call service -> validate reputation update.

## Deployment Notes
- Agents should expose health and readiness endpoints for orchestration.
- Graceful shutdown: complete in-flight OpenClaw interactions or mark agent as `draining` before stopping.

## Monitoring & Alerts
- Alert on repeated registration failures, high latency to OpenClaw, or sudden reputation drops.

## Open Questions
- What exact signing algorithm and key format does OpenClaw require? (RSA, ECDSA, raw HMAC)
- Is there a sandbox/staging OpenClaw instance available for integration tests?

---

### Architecture & Data Flow Details

This section provides step-by-step integration sequences, component responsibilities, and message examples for core flows.

1) Agent Boot & Registration (sequence)
   - Agent loads config (agent_id, public_key, private_key reference, capabilities).
   - Agent performs a local self-check and opens TLS connection to OpenClaw control-plane.
   - Agent POSTs signed identity to `/api/agents/register`.
   - OpenClaw verifies signature, stores agent metadata, returns `agent_status: registered`.
   - Agent registers one or more services by POSTing to `/api/services/register` with service descriptors and ownership signature.

2) Service Discovery and Invocation
   - Consumer queries `/api/services?capability=trend_analysis` or receives an event listing available providers.
   - OpenClaw returns best-matched providers with endpoint URLs and routing metadata (latency score, reputation).
   - Consumer selects provider and calls the provider endpoint directly (HTTPS) including `X-OpenClaw-Trace` and `Idempotency-Key` headers.
   - Provider processes request, emits events to OpenClaw `/api/events` for billing/reputation, and returns response.

3) Reputation Update Flow
   - After service completion, consumer sends a signed reputation event to `/api/reputation/update` including `service_id`, `quality_score`, and `latency_ms`.
   - OpenClaw aggregates scores, updates the `reputation_score` for the provider, and emits `reputation_changed` events to subscribers.

4) Event Subscribe / Webhook Model
   - Providers may register a webhook with OpenClaw to receive `service_request` events.
   - Webhook messages include `event_id` to support deduplication and `signature` for authenticity.

5) Failure Modes and Recovery
   - Signature verification failure: OpenClaw rejects registration (400). Agent must log, alert, and retry after key/format fix.
   - Reputation loss threshold: OpenClaw may auto-suspend services; providers should implement a `drain` endpoint and a recovery workflow.
   - Network partition: Agent should operate in `local_mode` with limited functionality until connectivity is restored; queue outbound events and reconcile after reconnect.

Message canonicalization rules
- Canonicalize JSON with stable key ordering and no whitespace before signing.
- Use UTF-8 encoding and ISO 8601 UTC timestamps.

Example: Signed registration payload (pseudo)

```json
{
  "payload": {"agent_id":"chimera:team:agent001","public_key":"..."},
  "signature": "base64(ecdsa_sign(canonical(payload), private_key))",
  "timestamp": "2026-02-05T12:00:00Z"
}
```

Observability notes for flows
- Trace: add `trace_id` and `span_id` to all control and data-plane requests.
- Logs: include `event_id`, `request_id`, and `agent_id` for correlation.
- Metrics: increment counters for `registration.attempt`, `registration.success`, `service.call`, `service.error`.

Security follow-ups
- Establish a rotation policy for keys used to sign payloads; expose an endpoint `/api/agents/rotate-key` that accepts a signed key-rotation request.
- Define allowed ciphers and minimum TLS versions in the integration guide.

Performance considerations
- Use service metadata hints for preferred routing to reduce cross-region latency.
- Allow pre-warming of model caches based on predicted demand from OpenClaw's routing hints.

---
