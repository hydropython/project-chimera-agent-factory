Running skills locally

Use the `scripts/run_skill.py` helper to invoke a skill by name.

Examples:

Run the `content-generation` skill with an inline JSON input:

```bash
python scripts/run_skill.py content-generation '{"prompt":"Hello world"}'
```

Or pass a file containing JSON:

```bash
python scripts/run_skill.py fetch-trends tests/sample_trend_request.json
```

Notes:
- Install dependencies first: `pip install -r requirements.txt`
- The loader will validate input against `skills/<skill>/schema/input.json` if present.
