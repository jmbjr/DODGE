# Architecture

## Core principle

Digitropolis separates **what the game is** from **how it is rendered or played**.

The canonical layer contains neutral facts and rules. Target layers transform those facts into a printable artifact, a Tabletop Simulator package, simulation inputs, or a digital client. A target may cache generated files, but those files are disposable and must be reproducible from the canonical layer.

## Layers

### 1. Canonical definition

- `data/cards/`: card instances and printed facts
- `schemas/`: allowed structure, types, and enumerations
- Future `data/rules/`: normalized timing, placement, scoring, and effect definitions
- Future `data/variants/`: explicit patches layered over the original game

Every researched field should carry provenance or point to a source record. Unknown facts remain `null`; they are not guessed merely to satisfy an exporter.

### 2. Domain tooling

- Importers convert research sources into canonical records.
- Validators enforce schema and cross-record invariants.
- Future selectors build legal card pools or historically plausible randomized products.
- Future rules engines interpret normalized mechanics without depending on a user interface.

### 3. Targets

Each directory under `targets/` owns only target-specific code and configuration:

- page size, bleed, and typography for print-and-play;
- deck-sheet coordinates and object manifests for Tabletop Simulator;
- experiment definitions and result formats for simulation;
- storage, networking, and UI adapters for digital play.

Target code may read canonical data. Canonical data must never import or depend on a target.

### Neutral scene interchange: DODGE

DODGE sits between canonical domain data and target exporters when a build needs
to describe a set of objects and their relationships. It references canonical
entities; it does not duplicate their facts. DODGE owns neutral archetypes,
collections, behaviors, and scene membership. Target contracts map those
concepts into target output and enumerate the deployment fields the target adds.

DODGE is required export orchestration, not a new source of card truth. PnP and
TTS accept a DODGE scene as their sole domain input and resolve its hash-pinned
canonical sources through one shared runtime. See `docs/dodge.md` and
`schemas/dodge.schema.v0.1.json`.

## Original game and variants

The original researched game should remain immutable in meaning. A redesign is expressed as a named variant containing only deliberate differences: setup changes, card overrides, scoring changes, pack recipes, or new cards.

A future resolved build should be conceptually:

```text
original definition + ordered variant patches + target configuration = exported artifact
```

This allows the project to generate faithful proxies, family-friendly rules, experimental balance builds, and simulation scenarios from the same evidence base without confusing historical facts with redesign decisions.

## Stable identifiers

Dataset IDs such as `base-001` are project-local identifiers, not original collector numbers. Exporters and variants should refer to IDs rather than names. IDs must remain stable once published; corrected names or statistics should not create a new ID unless the physical card identity changes.

## Generated files

Generated artifacts should eventually live in a target's ignored `build/` directory. Small manifests and reproducibility metadata may be committed; rendered PDFs, image atlases, TTS packages, simulation result batches, and application builds generally should not be.
