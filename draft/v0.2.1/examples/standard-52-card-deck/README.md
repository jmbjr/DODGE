# Standard 52-card deck reference implementation

This folder is a small, complete DODGE 0.2.1 implementation for a joker-free French-suited deck. It follows the useful boundary demonstrated by Wretched Demesne: canonical facts live in a referenced source, the DODGE document supplies neutral composition and physical semantics, one resolver verifies and resolves that input, and target contracts describe only target capabilities and additions.

## Contents

- `data/standard-52-card-catalog.json` — canonical identities, ranks, suits, colors, labels, and deterministic ordering.
- `standard-52-card-deck.dodge.json` — one poker-card archetype, one ordered 52-member collection, neutral shuffle/draw behavior, and one scene.
- `resolve.py` — target-neutral resolution with version, hash, reference, uniqueness, completeness, and ordering checks.
- `export-contracts/` — illustrative PnP and Tabletop Simulator boundaries consuming the same resolved scene.
- `generate.py` — deterministic source generator; it also hash-pins the catalog in the DODGE document.
- `validate.py` — schema validation plus 52-card semantic invariants.

The example intentionally does not define rules for poker, bridge, solitaire, or any other game. A standard deck is reusable component data. A game can reference this catalog or copy the pattern, then add its own actions, procedures, setup, and win conditions.

## Data flow

```text
canonical card catalog
          ↓ referenced and SHA-256 pinned by
      DODGE scene
          ↓ resolved once by
   target-neutral resolver
       ↙             ↘
 PnP contract     TTS contract
```

Both exporters should consume `resolve.py` output (or equivalent conforming resolver output), never independently reconstruct the ranks, suits, membership, or ordering.

## Try it

From this directory:

```sh
python3 -m pip install jsonschema
python3 generate.py
python3 validate.py
python3 resolve.py --out /tmp/standard-52-card-deck.resolved.json
```

`generate.py` uses the declared order clubs, diamonds, hearts, spades, with ace through king inside each suit. That declared order is an identity and reproducibility aid; the deck's `shuffle` behavior permits runtime randomization.

## Exporter responsibilities

The DODGE document owns the 52-card membership, order, dimensions, two-sidedness, shared-back identity, and neutral behaviors. Exporters own typography, visual styling, layout, rasterization, platform identifiers, transforms, hosting, and other target mechanics.
