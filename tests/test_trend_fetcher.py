import pytest
from pathlib import Path

# New:
from trend_fetcher import fetch_trends  # noqa: F401

def test_trend_schema_present():
    """Spec check: ensure the trend_request.json schema exists in specs/schemas."""
    p = Path('specs/schemas/trend_request.json')
    assert p.exists(), f'spec missing: {p}'


def test_trend_fetcher_implements_fetch():
    """Failing test: there should be a trend_fetcher implementation that provides `fetch_trends`.

    This test is expected to fail until the TrendFetcher is implemented.
    """
    # the implementation is intentionally missing; importing should fail until implemented
    from src.trend_fetcher import fetch_trends  # noqa: F401
    assert callable(fetch_trends)
