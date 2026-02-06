#!/usr/bin/env python3
"""Legacy shim for the spec_kit CLI.

The canonical implementation lives in `src.mcp.spec_kit`. This wrapper
exists to preserve backwards compatibility for any tooling that still
imports or executes `src/spec_kit.py` directly.
"""

from mcp.spec_kit import main  # type: ignore F401


if __name__ == "__main__":
    main()
