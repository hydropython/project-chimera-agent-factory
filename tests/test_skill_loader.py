"""TDD-style goal posts for the skills.loader module.

These tests define how the Dev MCP "brain" is expected to see and use
runtime skills, without depending on their internal implementation.
"""

from typing import Any, Dict

import pytest

from skills import loader


def test_list_skills_includes_core_runtime_skills() -> None:
    """The loader should discover all core runtime skills by name."""
    discovered = set(loader.list_skills())

    for name in {"content-generation", "fetch-trends", "register-service"}:
        assert (
            name in discovered
        ), f"core skill {name!r} was not discovered by loader.list_skills()"


def test_invoke_skill_rejects_invalid_input_via_schema() -> None:
    """Goal post: invalid input must be rejected before hitting handlers.

    For content-generation, `prompt` is required by the JSON Schema. An
    empty dict should therefore fail validation and raise ValueError.
    """
    bad_input: Dict[str, Any] = {}

    with pytest.raises(ValueError):
        loader.invoke_skill("content-generation", bad_input)


def test_invoke_skill_accepts_valid_input_for_content_generation() -> None:
    """Minimal goal post: a valid input passes schema validation and runs."""
    good_input: Dict[str, Any] = {"prompt": "Hello, world"}

    result = loader.invoke_skill("content-generation", good_input)

    assert isinstance(result, dict)

