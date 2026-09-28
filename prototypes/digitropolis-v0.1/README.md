# Digitropolis DODGE prototype v0.1

This folder preserves the latest Digitropolis implementation of DODGE as one coherent prototype snapshot.

## Provenance

- Source repository: `jmbjr/digitropolis`
- Source pull request: [#4](https://github.com/jmbjr/digitropolis/pull/4)
- Source commit: `aae9a1b00d49634828cdc80e1c2870e37656cd5d`
- DODGE document version: `0.1.0`
- Snapshot date: 2026-09-28

The earlier Digitropolis draft is not copied separately because this commit supersedes it while retaining the same DODGE format version.

## Contents

- `docs/`: the human-readable DODGE description and architectural placement
- `schemas/`: machine-enforced scene and exporter-contract schemas
- `contracts/`: Print-and-Play and Tabletop Simulator capability contracts
- `tools/`: builder, shared resolver, validator, and cross-target parity checker
- `examples/`: one 60-card selected scene and one complete-set scene

The two example scenes are not different DODGE versions. They demonstrate the same format with and without a separate selection manifest.

## Important boundary

DODGE is required export orchestration, but it is not the canonical source of game facts. The examples reference Digitropolis datasets, rules, and selection manifests that remain in the source game repository and are deliberately not duplicated here.

The tools are preserved verbatim as prototype evidence. Their repository-root assumptions and referenced game files mean they should be run from the original Digitropolis layout unless they are generalized in a future DODGE implementation.
