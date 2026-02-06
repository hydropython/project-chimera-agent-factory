"""Legacy shim for skill contract validation.

The canonical implementation lives in `src.mcp.validate_skill_contracts`.
This wrapper preserves the historical module path.
"""

from mcp.validate_skill_contracts import (  # type: ignore F401
    main,
    validate_skill,
)


if __name__ == "__main__":
    main()

