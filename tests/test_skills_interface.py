from pathlib import Path


def test_skill_manifests_exist():
    """Ensure each skill has a manifest and schema dir (structural sanity)."""
    skills = ['content-generation', 'fetch-trends', 'register-service']
    for s in skills:
        manifest = Path('skills') / s / 'manifest.yaml'
        input_schema = Path('skills') / s / 'schema' / 'input.json'
        output_schema = Path('skills') / s / 'schema' / 'output.json'
        assert manifest.exists(), f'manifest missing for {s}'
        assert input_schema.exists(), f'input schema missing for {s}'
        assert output_schema.exists(), f'output schema missing for {s}'


def test_skill_handlers_present():
    """Failing test: runtime handlers must be present at `handler.py` — intentionally failing now.

    This test defines the empty slot the runtime must fill.
    """
    handler = Path('skills') / 'content-generation' / 'handler.py'
    assert handler.exists(), 'skill handler missing: content-generation/handler.py'
