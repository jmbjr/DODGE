#!/usr/bin/env python3
"""Generate the canonical catalog and DODGE scene for a standard 52-card deck."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CATALOG_PATH = ROOT / "data" / "standard-52-card-catalog.json"
DODGE_PATH = ROOT / "standard-52-card-deck.dodge.json"

SUITS = (
    ("clubs", "black", "\u2663"),
    ("diamonds", "red", "\u2666"),
    ("hearts", "red", "\u2665"),
    ("spades", "black", "\u2660"),
)
RANKS = (
    ("ace", "A", 1),
    ("2", "2", 2),
    ("3", "3", 3),
    ("4", "4", 4),
    ("5", "5", 5),
    ("6", "6", 6),
    ("7", "7", 7),
    ("8", "8", 8),
    ("9", "9", 9),
    ("10", "10", 10),
    ("jack", "J", 11),
    ("queen", "Q", 12),
    ("king", "K", 13),
)


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def build_catalog() -> dict:
    cards = []
    for suit, color, symbol in SUITS:
        for rank, label, rank_order in RANKS:
            cards.append(
                {
                    "id": f"{rank}-of-{suit}",
                    "name": f"{rank.title()} of {suit.title()}",
                    "rank": rank,
                    "rank_label": label,
                    "rank_order": rank_order,
                    "suit": suit,
                    "suit_symbol": symbol,
                    "color": color,
                }
            )
    return {
        "catalog_version": "1.0.0",
        "catalog_id": "standard-52-card-deck",
        "description": "A deterministic, joker-free French-suited 52-card catalog.",
        "ordering": "clubs, diamonds, hearts, spades; ace through king within each suit",
        "card_back": {
            "id": "standard-back",
            "name": "Standard shared card back",
            "description": "Semantic identity only; target exporters supply the artwork.",
        },
        "cards": cards,
    }


def build_dodge(catalog_sha256: str, cards: list[dict]) -> dict:
    return {
        "dodge_version": "0.2.1",
        "document_id": "standard-52-card-deck.reference-example",
        "game_id": "standard-52-card-deck",
        "title": "Standard 52-card deck reference example",
        "description": "A game-neutral, joker-free French-suited deck demonstrating a canonical catalog, ordered collection, physical card profile, shared back, neutral behaviors, and one scene.",
        "sources": {
            "cards": {
                "kind": "entity_catalog",
                "uri": "data/standard-52-card-catalog.json",
                "version": "1.0.0",
                "sha256": catalog_sha256,
                "media_type": "application/json",
                "authority": "authoritative",
                "description": "Canonical identities and semantic playing-card facts.",
            }
        },
        "archetypes": {
            "playing-card": {
                "kind": "token",
                "face_slots": [
                    {"id": "front", "role": "front"},
                    {"id": "back", "role": "back"},
                ],
                "component": {
                    "form": "card",
                    "size_class": "poker",
                    "shape": "rectangle",
                    "two_sided": True,
                    "dimensions": {"unit": "in", "width": 2.5, "height": 3.5},
                    "shared_back_ref": "cards:standard-back",
                },
            },
            "deck": {"kind": "collection"},
        },
        "objects": {
            "standard-deck": {
                "kind": "collection",
                "archetype_ref": "deck",
                "name": "Standard 52-card deck",
                "description": "One card of every rank in each of four suits; no jokers.",
                "source_ref": "cards",
                "members": [
                    {"entity_ref": f"cards:{card['id']}", "archetype_ref": "playing-card"}
                    for card in cards
                ],
                "ordering": "declared",
                "behaviors": [
                    {"type": "shuffle"},
                    {"type": "draw", "replacement": False, "destination": "player-hand"},
                ],
                "tags": ["deck", "standard-52", "joker-free"],
            }
        },
        "scenes": {
            "table": {
                "name": "Standard deck table",
                "description": "A neutral starting scene containing one complete deck.",
                "instances": [{"id": "deck-1", "object_ref": "standard-deck"}],
            }
        },
    }


def main() -> None:
    catalog = build_catalog()
    write_json(CATALOG_PATH, catalog)
    digest = hashlib.sha256(CATALOG_PATH.read_bytes()).hexdigest()
    write_json(DODGE_PATH, build_dodge(digest, catalog["cards"]))
    print(f"wrote {len(catalog['cards'])} cards; catalog sha256={digest}")


if __name__ == "__main__":
    main()
