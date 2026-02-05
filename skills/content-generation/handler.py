from typing import Dict, Any

def handle(input_payload: Dict[str, Any]) -> Dict[str, Any]:
    """Minimal content-generation handler stub.

    Returns a single empty variant to satisfy interface checks.
    """
    return {
        "content_id": input_payload.get("content_id", "stub"),
        "platform": input_payload.get("platform", "unknown"),
        "content_type": "text_post",
        "primary_content": {"text": "", "character_count": 0, "readability_score": 0},
        "variants": [],
        "metadata": {"generated_by": "stub-handler"},
    }
