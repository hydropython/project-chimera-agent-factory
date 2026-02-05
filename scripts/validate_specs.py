"""Validate JSON Schema files and the OpenAPI YAML for basic correctness.

Checks performed:
- Parse each JSON file in `specs/schemas/` and validate they are valid JSON Schema (Draft-07) using jsonschema.check_schema.
- Parse `specs/openapi.yaml` to ensure it's valid YAML and contains a top-level `openapi` key.

Exit code: 0 on success, non-zero on failure.
"""
import sys
import json
import glob
from pathlib import Path

try:
    import yaml
    import jsonschema
except Exception as e:
    print("Missing dependency:", e)
    print("Run: pip install pyyaml jsonschema")
    sys.exit(2)

root = Path(__file__).resolve().parents[1]
schemas_dir = root / "specs" / "schemas"
openapi_file = root / "specs" / "openapi.yaml"

errors = 0

print("Validating JSON schemas in:", schemas_dir)
for p in sorted(schemas_dir.glob('*.json')):
    print(f"- {p.name}", end='')
    try:
        with p.open('r', encoding='utf-8') as f:
            schema = json.load(f)
        jsonschema.Draft7Validator.check_schema(schema)
        print(" OK")
    except Exception as e:
        print(" FAIL")
        print("  ", e)
        errors += 1

print('\nValidating OpenAPI YAML:', openapi_file)
if not openapi_file.exists():
    print('  File not found')
    errors += 1
else:
    try:
        with openapi_file.open('r', encoding='utf-8') as f:
            spec = yaml.safe_load(f)
        if not isinstance(spec, dict) or 'openapi' not in spec:
            print('  Invalid OpenAPI document: missing top-level "openapi" key')
            errors += 1
        else:
            print('  OK (parsed, contains openapi key)')
    except Exception as e:
        print('  YAML parse error:', e)
        errors += 1

if errors:
    print(f"\nValidation finished: {errors} error(s) found")
    sys.exit(1)

print('\nAll validations passed')
sys.exit(0)
