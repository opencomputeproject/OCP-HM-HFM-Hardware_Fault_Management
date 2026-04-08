
#!/usr/bin/env python3
import json
import sys
import re
import argparse
from jsonschema import Draft202012Validator, validate

# -------------------------------
# PascalCase utilities
# -------------------------------
PASCAL_RE = re.compile(r'^[A-Z][A-Za-z0-9]*$')

def is_pascal_case(s: str) -> bool:
    """Return True if string is PascalCase (starts with A-Z, alnum thereafter)."""
    return bool(PASCAL_RE.match(s))

def to_pascal_case(s: str) -> str:
    """
    Convert a string to PascalCase.
    - Splits on non-alphanumerics and transitions from lower-to-upper boundaries.
    - Works reasonably for camelCase, snake_case, kebab-case, and 'mixed Stuff'.
    """
    if not s:
        return s
    # If already PascalCase, return as-is
    if is_pascal_case(s):
        return s

    # Break on non-alnum boundaries
    parts = re.split(r'[^A-Za-z0-9]+', s)
    parts = [p for p in parts if p]  # drop empties

    # If that yields nothing (unlikely), fall back to simple capitalize
    if not parts:
        return s[:1].upper() + s[1:]

    # Handle camelCase within tokens (e.g., "firmwareVersion" -> ["firmware", "Version"])
    normalized = []
    for p in parts:
        # Split on transitions from lower-to-upper (e.g., "lastUpdated" -> "last", "Updated")
        split = re.findall(r'[A-Z]+(?=[A-Z][a-z0-9])|[A-Z]?[a-z0-9]+|[A-Z]+', p)
        normalized.extend(split)

    return ''.join(seg[:1].upper() + seg[1:] for seg in normalized)

def collect_non_pascal_keys(obj, path=""):
    """
    Walk the object and collect keys that are not PascalCase.
    Returns a list of (path, key) pairs.
    """
    issues = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            if not is_pascal_case(k):
                issues.append((path or "$", k))
            child_path = f'{path or "$"}.{k}'
            issues.extend(collect_non_pascal_keys(v, child_path))
    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            child_path = f'{path or "$"}[{i}]'
            issues.extend(collect_non_pascal_keys(item, child_path))
    return issues

def convert_keys_to_pascal(obj):
    """
    Recursively convert all dict keys to PascalCase; leave values untouched.
    """
    if isinstance(obj, dict):
        return {to_pascal_case(k): convert_keys_to_pascal(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_keys_to_pascal(item) for item in obj]
    else:
        return obj

# -------------------------------
# I/O helpers
# -------------------------------
def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")

# -------------------------------
# Validation workflow
# -------------------------------
def validate_json(schema_path, json_path, strict=False, rewrite=False, out_path=None):
    schema = load_json(schema_path)
    instance = load_json(json_path)

    # Check schema validity first
    Draft202012Validator.check_schema(schema)

    # Optionally enforce PascalCase BEFORE validation
    if strict:
        issues = collect_non_pascal_keys(instance)
        if issues:
            print("❌ Non-PascalCase keys detected in instance:")
            for where, key in issues[:50]:  # cap output for readability
                print(f"   - {where}: '{key}'")
            if len(issues) > 50:
                print(f"   ...and {len(issues) - 50} more.")
            print("Hint: use --rewrite to auto-convert keys to PascalCase.")
            sys.exit(1)

        # If strict and no issues, validate directly
        instance_to_validate = instance

    elif rewrite:
        instance_to_validate = convert_keys_to_pascal(instance)
        # Write back if requested
        if out_path:
            save_json(out_path, instance_to_validate)
            print(f"✍️ Rewrote instance with PascalCase keys to: {out_path}")
        else:
            print("✍️ Rewrote instance (PascalCase) in-memory; no file was saved. Use --out to save.")

    else:
        # Default: attempt validation as-is (assumes upstream has already converted)
        instance_to_validate = instance

    # Perform schema validation
    try:
        validate(instance=instance_to_validate, schema=schema)
        print(f"✅ '{json_path}' is valid according to the schema.")
    except Exception as e:
        print(f"❌ Validation failed: {e}")
        sys.exit(1)

# -------------------------------
# CLI
# -------------------------------
def parse_args():
    parser = argparse.ArgumentParser(
        description="Validate JSON against a JSON Schema with optional PascalCase enforcement."
    )
    parser.add_argument("schema", help="Path to JSON Schema file (PascalCase properties).")
    parser.add_argument("json", help="Path to JSON instance file.")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--strict", action="store_true",
                       help="Fail if any non-PascalCase keys exist in the instance.")
    group.add_argument("--rewrite", action="store_true",
                       help="Auto-convert instance keys to PascalCase before validation.")
    parser.add_argument("--out", help="Output file path when using --rewrite (optional).")
    return parser.parse_args()

def main():
    args = parse_args()
    validate_json(
        schema_path=args.schema,
        json_path=args.json,
        strict=args.strict,
        rewrite=args.rewrite,
        out_path=args.out
    )

if __name__ == "__main__":
    main()
``
