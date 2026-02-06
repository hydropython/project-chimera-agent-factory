"""Compatibility shim for the TrendFetcher skill.

The canonical runtime implementation now lives in `src.skills.trend_fetcher`.
This module re-exports `fetch_trends` so existing imports keep working:

- `from src.trend_fetcher import fetch_trends`
"""

from typing import Any, Dict

from .skills.trend_fetcher import fetch_trends  # noqa: F401

__all__ = ["fetch_trends"]

