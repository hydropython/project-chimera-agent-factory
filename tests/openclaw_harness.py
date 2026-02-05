"""Simple test harness for OpenClaw registration and trend fetch flows.

Environment variables:
- OPENCLAW_URL: base URL for OpenClaw API (e.g. https://openclaw.example.com/api)
- API_TOKEN: bearer token for auth
- SHARED_SECRET: HMAC secret for payload signing (for testing only)

Run:
python tests/openclaw_harness.py
"""
import os
import json
import time
import hmac
import hashlib
import requests

OPENCLAW_URL = os.environ.get('OPENCLAW_URL', 'https://openclaw.example.com/api')
API_TOKEN = os.environ.get('API_TOKEN', '')
SHARED_SECRET = os.environ.get('SHARED_SECRET', 'test-secret')

HEADERS = {'Authorization': f'Bearer {API_TOKEN}'} if API_TOKEN else {}


def sign_payload(payload: dict, secret: str) -> str:
    body = json.dumps(payload, separators=(',', ':'), sort_keys=True)
    sig = hmac.new(secret.encode(), body.encode(), hashlib.sha256).hexdigest()
    return sig


def register_agent(agent_payload: dict) -> dict:
    sig = sign_payload(agent_payload, SHARED_SECRET)
    headers = {**HEADERS, 'X-OpenClaw-Signature': sig}
    url = f"{OPENCLAW_URL}/agents/register"
    r = requests.post(url, json=agent_payload, headers=headers, timeout=10)
    r.raise_for_status()
    return r.json()


def register_service(service_payload: dict) -> dict:
    sig = sign_payload(service_payload, SHARED_SECRET)
    headers = {**HEADERS, 'X-OpenClaw-Signature': sig}
    url = f"{OPENCLAW_URL}/services/register"
    r = requests.post(url, json=service_payload, headers=headers, timeout=10)
    r.raise_for_status()
    return r.json()


def fetch_trends(request_payload: dict) -> dict:
    url = f"{OPENCLAW_URL}/trends/fetch"
    headers = {**HEADERS, 'Idempotency-Key': str(time.time())}
    r = requests.post(url, json=request_payload, headers=headers, timeout=15)
    r.raise_for_status()
    return r.json()


if __name__ == '__main__':
    agent = {
        "agent_id": "chimera:team:agent001",
        "display_name": "Chimera Test Agent",
        "public_key": "-----BEGIN PUBLIC KEY-----...",
        "capabilities": ["trend_fetch","content_generate"]
    }

    service = {
        "service_id": "chimera:trend_intelligence:v1",
        "agent_id": agent['agent_id'],
        "endpoint": "https://agent.example.com/api/trends",
        "input_schema": {},
        "output_schema": {},
        "pricing": {"type": "free"}
    }

    trend_request = {
        "request_id": "req_test_001",
        "sources": ["twitter"],
        "categories": ["technology"],
        "time_range": "last_24_hours",
        "limit": 10
    }

    print('Registering agent...')
    try:
        resp = register_agent(agent)
        print('Agent registered:', json.dumps(resp, indent=2))
    except Exception as e:
        print('Agent registration failed:', e)

    print('\nRegistering service...')
    try:
        resp = register_service(service)
        print('Service registered:', json.dumps(resp, indent=2))
    except Exception as e:
        print('Service registration failed:', e)

    print('\nFetching trends...')
    try:
        resp = fetch_trends(trend_request)
        print('Trends fetched:', json.dumps(resp, indent=2))
    except Exception as e:
        print('Trend fetch failed:', e)
