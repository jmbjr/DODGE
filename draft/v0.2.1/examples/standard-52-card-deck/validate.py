#!/usr/bin/env python3
"""Validate schemas plus semantic invariants for the 52-card reference example."""
from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator

from resolve import DEFAULT_DODGE, ROOT, resolve

SCHEMA_ROOT = ROOT.parents[1] / "schemas"


def validate_file(instance_path: Path, schema_name: str) -> None:
    instance = json.loads(instance_path.read_text(encoding="utf-8"))
    schema = json.loads((SCHEMA_ROOT / schema_name).read_text(encoding="utf-8"))
    Draft202012Validator(schema).validate(instance)


def main() -> None:
    validate_file(DEFAULT_DODGE, "dodge.schema.v0.2.1.json")
    for path in sorted((ROOT / "export-contracts").glob("*.json")):
        validate_file(path, "dodge-export-contract.schema.v0.2.1.json")
    resolved = resolve()
    suits = {card["suit"] for card in resolved["cards"]}
    ranks = {card["rank"] for card in resolved["cards"]}
    assert suits == {"clubs", "diamonds", "hearts", "spades"}
    assert ranks == {"ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "jack", "queen", "king"}
    assert all(sum(card["suit"] == suit for card in resolved["cards"]) == 13 for suit in suits)
    print("standard-52-card-deck: schemas valid; 52 unique cards; 4 suits x 13 ranks")


if __name__ == "__main__":
    main()
