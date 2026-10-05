# DODGE Example Games Hub

The repository root is a GitHub Pages teaching surface for DODGE reference implementations. Examples form a semantic ladder from reusable components to complete games and are explicitly classified as an Example Game, Component Example, or Specification Lab.

## Release model

- Canonical sources and a DODGE document resolve once into a neutral model.
- Web, Print-and-Play, and Tabletop Simulator targets consume that same resolved identity and ordered inventory.
- The normal game route opens the latest build.
- Released Web builds and downloads are immutable and source-SHA addressed.
- `versions.json` preserves the build catalog.
- `build.json` records exact source identity, resolved-model identity, target hashes, executable semantics, and unsupported semantics.
- Generated artifacts live under `examples/`; they are outputs, not game-authoring sources.

The first vertical slice is the Standard 52-card deck. It provides a functional generic Web deck, a duplex-aligned poker-size PnP PDF, and an explicit TTS metadata placeholder that preserves source identity and ordered card IDs without claiming a playable package.

## Local build

```sh
pip install -r draft/v0.2.1/examples/standard-52-card-deck/requirements.txt reportlab
python draft/v0.2.1/examples/standard-52-card-deck/validate.py
python tools/build_example_hub.py --source-sha "$(git rev-parse HEAD)"
```

Serve the repository root over HTTP to exercise the Hub and Web example. Opening files directly with `file://` will prevent browser `fetch()` calls.

## Automation

`.github/workflows/example-hub.yml` validates the DODGE source and contracts, builds all targets, checks ordered identity parity, and performs a canonical-data perturbation test. On a push to `master`, it commits a new immutable generated release. Changes containing only generated `examples/**` files do not retrigger the workflow.
