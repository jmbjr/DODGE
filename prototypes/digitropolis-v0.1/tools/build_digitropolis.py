#!/usr/bin/env python3
"""Build the first neutral Digitropolis DODGE scene from canonical inputs."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", required=True, type=Path)
    parser.add_argument("--selection", type=Path)
    parser.add_argument("--rules", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    dataset_raw = args.dataset.read_bytes()
    dataset = json.loads(dataset_raw)
    selection_raw = args.selection.read_bytes() if args.selection else None
    selection = json.loads(selection_raw) if selection_raw else None
    rules_text = args.rules.read_text(encoding="utf-8")
    deck_id = selection["deck_id"] if selection else "full-set"
    card_ids = selection["card_ids"] if selection else [card["id"] for card in dataset["cards"]]
    sources = {
        "cards": {"kind": "entity_catalog", "uri": str(args.dataset), "version": dataset["data_version"], "sha256": hashlib.sha256(dataset_raw).hexdigest()},
        "rules": {"kind": "rules", "uri": str(args.rules), "version": "research-v0.1", "sha256": hashlib.sha256(rules_text.encode()).hexdigest()},
    }
    if selection and selection_raw:
        sources["selection"] = {"kind": "selection_manifest", "uri": str(args.selection), "version": selection["manifest_version"], "sha256": hashlib.sha256(selection_raw).hexdigest()}
    document = {
        "dodge_version": "0.1.0",
        "document_id": f"digitropolis.{deck_id}",
        "game_id": "digitropolis",
        "title": f"Digitropolis {deck_id} scene",
        "description": "Target-neutral card collection and rules reference shared by every exporter.",
        "sources": sources,
        "archetypes": {
            "standard-card": {"kind": "token", "face_slots": [{"id": "front", "role": "front"}, {"id": "back", "role": "back"}], "description": "A two-sided standard card token."},
            "deck": {"kind": "collection", "description": "An ordered collection that may be shuffled and drawn without replacement."},
            "reference-token": {"kind": "token", "face_slots": [{"id": "reference", "role": "reference"}], "description": "A readable non-playing reference token."}
        },
        "objects": {
            "card-pool": {
                "kind": "collection", "archetype_ref": "deck", "name": deck_id,
                "source_ref": "selection" if selection else "cards",
                "members": [{"entity_ref": f"cards:{card_id}", "archetype_ref": "standard-card"} for card_id in card_ids],
                "behaviors": [{"type": "shuffle"}, {"type": "draw", "replacement": False, "destination": "player-hand"}]
            },
            "rules-reference": {
                "kind": "token", "archetype_ref": "reference-token", "name": "Digitropolis Rules",
                "faces": [{"slot": "reference", "content_ref": "rules"}]
            }
        },
        "scenes": {
            "starter-table": {
                "name": "Digitropolis starter table",
                "instances": [{"id": "deck-1", "object_ref": "card-pool"}, {"id": "rules-1", "object_ref": "rules-reference"}]
            }
        },
        "metadata": {"status": "draft", "limitations": ["No target layout", "No normalized game rules", "No general randomizer model"]}
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(document, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
