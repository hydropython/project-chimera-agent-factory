#!/usr/bin/env python3
import sys
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS_PKG = ROOT / 'skills'
sys.path.insert(0, str(SKILLS_PKG))

from skills import loader  # type: ignore


def main(argv):
    if len(argv) < 2:
        print('Usage: run_skill.py <skill-name> <json-input-or-path>')
        return 2
    skill = argv[0]
    raw = argv[1]
    # if raw is a path to a file, load it
    try:
        p = Path(raw)
        if p.exists():
            input_data = json.loads(p.read_text(encoding='utf-8'))
        else:
            input_data = json.loads(raw)
    except Exception as e:
        print('Failed to parse input JSON:', e)
        return 2

    try:
        out = loader.invoke_skill(skill, input_data)
        print(json.dumps(out, indent=2, ensure_ascii=False))
    except Exception as e:
        print('Skill invocation failed:', e)
        return 3
    return 0


if __name__ == '__main__':
    raise SystemExit(main(sys.argv[1:]))
