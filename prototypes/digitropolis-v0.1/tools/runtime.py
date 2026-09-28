#!/usr/bin/env python3
"""Resolve a DODGE scene into verified canonical inputs for exporters."""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from pathlib import Path


@dataclass(frozen=True)
class ResolvedDodge:
    path: Path
    document: dict
    document_sha256: str
    dataset: dict
    dataset_path: Path
    dataset_sha256: str
    selection: dict | None
    selection_path: Path | None
    rules_text: str
    rules_path: Path
    rules_sha256: str
    cards: list[dict]
    card_ids: list[str]
    deck_id: str


def _read_verified_source(root: Path, source: dict) -> tuple[Path, bytes]:
    path = root / source["uri"]
    raw = path.read_bytes()
    actual = hashlib.sha256(raw).hexdigest()
    expected = source.get("sha256")
    if expected and actual != expected:
        raise ValueError(f"DODGE source hash mismatch for {source['uri']}: {actual} != {expected}")
    return path, raw


def resolve_dodge(path: Path, root: Path) -> ResolvedDodge:
    """Load one DODGE scene and verify every canonical source and card reference."""
    path = path.resolve()
    raw_document = path.read_bytes()
    document = json.loads(raw_document)
    if document.get("dodge_version") != "0.1.0":
        raise ValueError(f"unsupported DODGE version: {document.get('dodge_version')}")

    sources = document["sources"]
    dataset_path, dataset_raw = _read_verified_source(root, sources["cards"])
    dataset = json.loads(dataset_raw)
    rules_path, rules_raw = _read_verified_source(root, sources["rules"])

    scene_instances = [
        instance
        for scene in document["scenes"].values()
        for instance in scene["instances"]
    ]
    collections = [
        document["objects"][instance["object_ref"]]
        for instance in scene_instances
        if document["objects"][instance["object_ref"]]["kind"] == "collection"
    ]
    if len(collections) != 1:
        raise ValueError(f"DODGE scene must instantiate exactly one card collection, found {len(collections)}")
    deck = collections[0]
    refs = [member["entity_ref"] for member in deck["members"]]
    if len(refs) != len(set(refs)):
        raise ValueError("DODGE deck contains duplicate entity references")
    prefix = "cards:"
    if any(not ref.startswith(prefix) for ref in refs):
        raise ValueError("DODGE deck contains a non-card entity reference")
    card_ids = [ref.removeprefix(prefix) for ref in refs]
    by_id = {card["id"]: card for card in dataset["cards"]}
    missing = [card_id for card_id in card_ids if card_id not in by_id]
    if missing:
        raise ValueError(f"DODGE deck references unknown cards: {missing}")

    selection = None
    selection_path = None
    if "selection" in sources:
        selection_path, selection_raw = _read_verified_source(root, sources["selection"])
        selection = json.loads(selection_raw)
        if card_ids != selection["card_ids"]:
            raise ValueError("DODGE deck order differs from its selection manifest")
        deck_id = selection["deck_id"]
    else:
        deck_id = document["document_id"].split(".")[-1]

    return ResolvedDodge(
        path=path,
        document=document,
        document_sha256=hashlib.sha256(raw_document).hexdigest(),
        dataset=dataset,
        dataset_path=dataset_path,
        dataset_sha256=hashlib.sha256(dataset_raw).hexdigest(),
        selection=selection,
        selection_path=selection_path,
        rules_text=rules_raw.decode("utf-8"),
        rules_path=rules_path,
        rules_sha256=hashlib.sha256(rules_raw).hexdigest(),
        cards=[by_id[card_id] for card_id in card_ids],
        card_ids=card_ids,
        deck_id=deck_id,
    )
