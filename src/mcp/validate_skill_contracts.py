"""Validate skill JSON contracts against shared schemas.

This module is the canonical MCP-side validator. The legacy
`src/validate_skill_contracts.py` shim delegates here.
"""

import json
import os

from jsonschema import ValidationError, validate

SKILLS_DIR = "skills"
SCHEMAS_DIR = "specs/schemas"


def load_json(file_path: str):
    with open(file_path, "r") as f:
        return json.load(f)


def validate_skill(skill_path: str) -> bool:
    skill = load_json(skill_path)
    skill_name = os.path.basename(skill_path)

    # Validate input
    input_schema_file = os.path.join(SCHEMAS_DIR, skill.get("input_schema", ""))
    if os.path.exists(input_schema_file):
        input_example = skill.get("example_input", {})
        schema = load_json(input_schema_file)
        try:
            validate(instance=input_example, schema=schema)
        except ValidationError as e:
            print(f"[ERROR] Skill {skill_name} input does not match schema: {e}")
            return False
    else:
        print(f"[WARN] Input schema file not found for {skill_name}")

    # Validate output
    output_schema_file = os.path.join(SCHEMAS_DIR, skill.get("output_schema", ""))
    if os.path.exists(output_schema_file):
        output_example = skill.get("example_output", {})
        schema = load_json(output_schema_file)
        try:
            validate(instance=output_example, schema=schema)
        except ValidationError as e:
            print(f"[ERROR] Skill {skill_name} output does not match schema: {e}")
            return False
    else:
        print(f"[WARN] Output schema file not found for {skill_name}")

    print(f"[OK] Skill {skill_name} input/output validated")
    return True


def main() -> None:
    skills_files = [
        os.path.join(SKILLS_DIR, f)
        for f in os.listdir(SKILLS_DIR)
        if f.endswith(".json")
    ]
    all_valid = True
    for skill_file in skills_files:
        if not validate_skill(skill_file):
            all_valid = False
    if not all_valid:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

