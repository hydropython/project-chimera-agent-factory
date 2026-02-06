from pathlib import Path
from typing import Any, Dict

from trend_fetcher import fetch_trends

from interfaces import TrendFetcherInterface


def test_trend_schema_present() -> None:
    """Spec check: ensure the trend_request.json schema exists in specs/schemas."""
    p = Path("specs/schemas/trend_request.json")
    assert p.exists(), f"spec missing: {p}"


class TrendFetcherAdapter(TrendFetcherInterface):
    """Adapter to treat the module-level function as a skill implementation."""

    def fetch_trends(self, request: Dict[str, Any]) -> Dict[str, Any]:
        return fetch_trends(request)


def test_trend_fetcher_satisfies_interface() -> None:
    """The concrete trend_fetcher must satisfy the TrendFetcherInterface contract."""
    impl = TrendFetcherAdapter()
    sample_request = {"request_id": "test-123"}

    result = impl.fetch_trends(sample_request)

    assert isinstance(result, dict)
    assert result.get("request_id") == "test-123"
    assert result.get("status") == "success"
    assert "data" in result and isinstance(result["data"], dict)
    assert "trends" in result["data"]
    assert isinstance(result["data"]["trends"], list)

