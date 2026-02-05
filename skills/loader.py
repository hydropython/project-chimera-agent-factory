import os
import json
import importlib.util
from json import JSONDecodeError

try:
    import yaml
except Exception:
    yaml = None

try:
    import jsonschema
except Exception:
    jsonschema = None

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def skill_dir(skill_name):
    return os.path.join(BASE_DIR, skill_name)


def load_manifest(skill_name):
    p = os.path.join(skill_dir(skill_name), 'manifest.yaml')
    if not os.path.exists(p):
        return {}
    if yaml:
        with open(p, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f) or {}
    # fallback: return minimal manifest
    return {}


def _load_json_file(path):
    if not os.path.exists(path):
        return None
    with open(path, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except JSONDecodeError:
            return None


def _load_handler_module(skill_name, entrypoint='handler.py'):
    p = os.path.join(skill_dir(skill_name), entrypoint)
    if not os.path.exists(p):
        raise FileNotFoundError(f'Handler not found: {p}')
    spec = importlib.util.spec_from_file_location(f'skills.{skill_name}.handler', p)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def validate_input(skill_name, input_data):
    schema_path = os.path.join(skill_dir(skill_name), 'schema', 'input.json')
    schema = _load_json_file(schema_path)
    if schema is None:
        return True, None
    if jsonschema is None:
        raise RuntimeError('jsonschema package is required for input validation')
    try:
        jsonschema.validate(instance=input_data, schema=schema)
        return True, None
    except Exception as e:
        return False, str(e)


def invoke_skill(skill_name, input_data):
    manifest = load_manifest(skill_name)
    entry = manifest.get('entrypoint', 'handler.py')
    ok, err = validate_input(skill_name, input_data)
    if not ok:
        raise ValueError(f'Input validation failed: {err}')
    module = _load_handler_module(skill_name, entry)
    if not hasattr(module, 'handle'):
        raise AttributeError('Skill handler must expose a `handle(input)` function')
    return module.handle(input_data)


def list_skills():
    # list subdirectories of skills folder that contain a manifest or handler
    skills = []
    for name in os.listdir(BASE_DIR):
        p = os.path.join(BASE_DIR, name)
        if not os.path.isdir(p):
            continue
        if os.path.exists(os.path.join(p, 'handler.py')) or os.path.exists(os.path.join(p, 'manifest.yaml')):
            skills.append(name)
    return skills
