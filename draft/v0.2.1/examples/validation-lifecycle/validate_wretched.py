#!/usr/bin/env python3
"""Reference WD semantic-profile gate for DODGE issue #43."""

import json
from pathlib import Path

from jsonschema import Draft202012Validator


HERE = Path(__file__).resolve().parent
DRAFT = HERE.parents[1]
FIXTURE = HERE / "core-valid-domain-invalid.dodge.json"
SCHEMA = DRAFT / "schemas" / "dodge.schema.v0.2.1.json"


def wd_semantic_errors(document: dict) -> list[str]:
    errors: list[str] = []
    for object_id, obj in document.get("objects", {}).items():
        searchable = obj.get("extensions", {}).get("wretched-demesne:searchable") is True
        has_search = any(invocation.get("trigger") == "search" for invocation in obj.get("invocations", []))
        if searchable and not has_search:
            errors.append(
                f"objects.{object_id}: wretched-demesne:searchable requires an executable "
                "search invocation or an explicitly resolved inherited Search default"
            )
    return errors


def main() -> None:
    document = json.loads(FIXTURE.read_text(encoding="utf-8"))
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))

    Draft202012Validator.check_schema(schema)
    Draft202012Validator(schema).validate(document)

    errors = wd_semantic_errors(document)
    if not errors:
        raise SystemExit("expected WD semantic validation to reject the fixture")

    print("PASS: DODGE core accepted the fixture")
    print("PASS: wretched-demesne@0.1.0 rejected it before resolution")
    for error in errors:
        print(f"  - {error}")


if __name__ == "__main__":
    main()
