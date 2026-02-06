"""Top-level compatibility shim for the TrendFetcher skill.

Tests and tooling may import `trend_fetcher.fetch_trends` directly.
The canonical implementation lives in `src.skills.trend_fetcher`.
"""

from typing import Any, Dict

from src.skills.trend_fetcher import fetch_trends  # type: ignore F401

__all__ = ["fetch_trends"]

