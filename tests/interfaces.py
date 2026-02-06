"""Test-side interfaces that define skill contracts.

These abstract base classes describe the behavior MCP \"brain\" code
expects from runtime \"skills\" without coupling tests to concrete
implementations.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict


class TrendFetcherInterface(ABC):
    """Contract for a trend fetching skill."""

    @abstractmethod
    def fetch_trends(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Fetch trends for the given request payload."""
        raise NotImplementedError


__all__ = ["TrendFetcherInterface"]

