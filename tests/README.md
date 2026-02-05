OpenClaw test harness

Setup

1. Create a virtualenv and install dependencies:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

2. Set environment variables (example):

```powershell
$env:OPENCLAW_URL = 'https://openclaw.example.com/api'
$env:API_TOKEN = 'your-token'
$env:SHARED_SECRET = 'test-secret'
python tests\openclaw_harness.py
```

What it does
- Registers a test agent
- Registers a test service
- Calls the trends fetch endpoint

Notes
- This harness uses HMAC for signing payloads for convenience in a test environment. Production should use proper key management and asymmetric signing.
