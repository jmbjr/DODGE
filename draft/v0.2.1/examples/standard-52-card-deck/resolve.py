#!/usr/bin/env python3
"""Resolve the standard-deck scene from DODGE as an exporter's sole domain input."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DEFAULT_DODGE = ROOT / "standard-52-card-deck.dodge.json"


class ResolutionError(ValueError):
    pass


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def resolve(dodge_path: Path = DEFAULT_DODGE) -> dict:
    dodge = load(dodge_path)
    if dodge.get("dodge_version") != "0.2.1":
        raise ResolutionError("This example requires DODGE 0.2.1")

    source = dodge["sources"]["cards"]
    catalog_path = (dodge_path.parent / source["uri"]).resolve()
    digest = hashlib.sha256(catalog_path.read_bytes()).hexdigest()
    if digest != source.get("sha256"):
        raise ResolutionError("Card catalog SHA-256 does not match the DODGE source declaration")

    catalog = load(catalog_path)
    if catalog.get("card_back", {}).get("id") != "standard-back":
        raise ResolutionError("Catalog must define cards:standard-back")
    by_id = {card["id"]: card for card in catalog["cards"]}
    if len(by_id) != len(catalog["cards"]):
        raise ResolutionError("The canonical catalog contains duplicate card IDs")

    scene = dodge["scenes"]["table"]
    instance = scene["instances"][0]
    deck = dodge["objects"][instance["object_ref"]]
    resolved_cards = []
    seen = set()
    for position, member in enumerate(deck["members"]):
        source_ref, card_id = member["entity_ref"].split(":", 1)
        if source_ref != "cards" or card_id not in by_id:
            raise ResolutionError(f"Unknown member reference: {member['entity_ref']}")
        if card_id in seen:
            raise ResolutionError(f"Duplicate deck member: {card_id}")
        seen.add(card_id)
        resolved_cards.append({"position": position, **by_id[card_id]})

    if len(resolved_cards) != 52 or seen != set(by_id):
        raise ResolutionError("Deck must contain every one of the 52 canonical cards exactly once")

    return {
        "format": "dodge-resolved-scene.v1",
        "dodge_version": dodge["dodge_version"],
        "document_id": dodge["document_id"],
        "document_sha256": hashlib.sha256(dodge_path.read_bytes()).hexdigest(),
        "scene_ref": "table",
        "deck_ref": instance["object_ref"],
        "catalog": {
            "id": catalog["catalog_id"],
            "version": catalog["catalog_version"],
            "sha256": digest,
        },
        "component": dodge["archetypes"]["playing-card"]["component"],
        "card_back": catalog["card_back"],
        "behaviors": deck["behaviors"],
        "cards": resolved_cards,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dodge", type=Path, default=DEFAULT_DODGE)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    text = json.dumps(resolve(args.dodge), indent=2, ensure_ascii=False) + "\n"
    if args.out:
        args.out.write_text(text, encoding="utf-8")
    else:
        print(text, end="")


if __name__ == "__main__":
    main()
