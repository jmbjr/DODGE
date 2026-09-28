#!/usr/bin/env python3
"""Validate DODGE documents/contracts and Digitropolis cross-references."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from tools.dodge.runtime import resolve_dodge


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def validate(instance: dict, schema_path: Path) -> None:
    validator = Draft202012Validator(load(schema_path))
    errors = sorted(validator.iter_errors(instance), key=lambda error: list(error.path))
    if errors:
        raise ValueError("\n".join(f"{'.'.join(map(str, error.path))}: {error.message}" for error in errors))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("document", type=Path)
    parser.add_argument("--contract", action="append", type=Path, default=[])
    args = parser.parse_args()
    document = load(args.document)
    validate(document, ROOT / "schemas/dodge.schema.v0.1.json")
    for contract_path in args.contract:
        validate(load(contract_path), ROOT / "schemas/dodge-export-contract.schema.v0.1.json")

    resolved = resolve_dodge(args.document, ROOT)
    print(f"OK: DODGE {document['dodge_version']}; {len(resolved.cards)} ordered cards; {len(args.contract)} contracts")


if __name__ == "__main__":
    main()
