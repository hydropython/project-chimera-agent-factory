from typing import Dict, Any

def fetch_trends(request: Dict[str, Any]) -> Dict[str, Any]:
    """Minimal stub for TrendFetcher used by tests.

    Returns an empty but valid response shape expected by the harness/tests.
    """
    return {
        "request_id": request.get("request_id", "stub"),
        "status": "success",
        "data": {
            "trends": []
        }
    }
