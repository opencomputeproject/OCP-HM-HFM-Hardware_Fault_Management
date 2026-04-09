#!/usr/bin/env python3
"""Validate a CodeCurrency JSON instance against schema_updated.json.

Usage:
  python validate_codecurrency.py --schema schema_updated.json --instance example.json
  python validate_codecurrency.py --instance example.json   # defaults schema to ./schema_updated.json

Exit codes:
  0 = valid
  1 = invalid JSON or schema
  2 = validation failed

Requires:
  pip install jsonschema referencing
"""

import argparse
import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator
from referencing import Registry, Resource


def load_json(path: Path):
    try:
        with path.open('r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in {path}: {e}")


def build_registry(schema_path: Path, schema_obj: dict) -> Registry:
    """Build a local registry so in-document $ref can resolve without network access."""
    # Use file URI as a stable key
    schema_uri = schema_path.resolve().as_uri()
    resource = Resource.from_contents(schema_obj)
    reg = Registry().with_resource(schema_uri, resource)

    # Also register by $id if present
    schema_id = schema_obj.get('$id')
    if isinstance(schema_id, str) and schema_id:
        reg = reg.with_resource(schema_id, resource)

    return reg


def main():
    ap = argparse.ArgumentParser(description='Validate CodeCurrency JSON against a JSON Schema (Draft 2020-12).')
    ap.add_argument('--schema', default='schema_updated.json', help='Path to JSON Schema (default: schema_updated.json)')
    ap.add_argument('--instance', required=True, help='Path to JSON instance to validate')
    ap.add_argument('--show-all', action='store_true', help='Show all validation errors (default shows first 20)')
    args = ap.parse_args()

    schema_path = Path(args.schema)
    inst_path = Path(args.instance)

    if not schema_path.exists():
        print(f"Schema file not found: {schema_path}", file=sys.stderr)
        return 1
    if not inst_path.exists():
        print(f"Instance file not found: {inst_path}", file=sys.stderr)
        return 1

    try:
        schema_obj = load_json(schema_path)
        inst_obj = load_json(inst_path)
    except ValueError as e:
        print(str(e), file=sys.stderr)
        return 1

    try:
        registry = build_registry(schema_path, schema_obj)
        validator = Draft202012Validator(schema_obj, registry=registry)
    except Exception as e:
        print(f"Failed to initialize validator: {e}", file=sys.stderr)
        return 1

    errors = sorted(validator.iter_errors(inst_obj), key=lambda e: list(e.path))
    if not errors:
        print("VALID ✅")
        return 0

    print("INVALID ❌")
    limit = len(errors) if args.show_all else min(len(errors), 20)
    for i, err in enumerate(errors[:limit], 1):
        path = '$'
        for p in err.absolute_path:
            if isinstance(p, int):
                path += f"[{p}]"
            else:
                path += f".{p}"
        print(f"{i}. {path}: {err.message}")

    if not args.show_all and len(errors) > 20:
        print(f"... and {len(errors) - 20} more. Re-run with --show-all to see everything.")

    return 2


if __name__ == '__main__':
    raise SystemExit(main())
