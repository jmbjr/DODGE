#!/usr/bin/env python3
"""Prove that PnP and TTS artifacts resolved the identical DODGE source."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


IDENTITY_FIELDS = (
    "dodge_version",
    "dodge_sha256",
    "dataset_sha256",
    "rules_sha256",
    "deck_id",
    "card_count",
    "card_ids",
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("pnp_manifest", type=Path)
    parser.add_argument("tts_manifest", type=Path)
    args = parser.parse_args()
    pnp = json.loads(args.pnp_manifest.read_text(encoding="utf-8"))
    tts = json.loads(args.tts_manifest.read_text(encoding="utf-8"))
    mismatches = [field for field in IDENTITY_FIELDS if pnp.get(field) != tts.get(field)]
    if mismatches:
        raise ValueError(f"cross-target DODGE identity mismatch: {mismatches}")
    print(
        f"OK: PnP and TTS share DODGE {pnp['dodge_version']} "
        f"{pnp['dodge_sha256'][:12]} with {pnp['card_count']} ordered cards"
    )


if __name__ == "__main__":
    main()
