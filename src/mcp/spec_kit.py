#!/usr/bin/env python3
"""Developer CLI for working with specs, skills, and tests.

This is the canonical MCP-facing entrypoint; the legacy `src/spec_kit.py`
module now delegates to this implementation.
"""

import subprocess
import sys


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: spec_kit <command>")
        print("Commands: validate, skills, test")
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "validate":
        print("🔹 Running spec validation...")
        subprocess.run(["make", "spec-check"], check=True)
    elif cmd == "skills":
        print("🔹 Validating skill contracts...")
        subprocess.run(["python", "src/validate_skill_contracts.py"], check=True)
    elif cmd == "test":
        print("🔹 Running tests...")
        subprocess.run(["make", "test"], check=True)
    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)


if __name__ == "__main__":
    main()

