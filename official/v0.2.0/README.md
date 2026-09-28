# Official DODGE 0.2.0 draft

This directory contains the first common specification drafted from both prototype families:

- `prototypes/digitropolis-v0.1/`
- `prototypes/wretched-demesne-v0.1/`

## Files

- `DODGE_SPEC.md` — normative human-readable specification
- `schemas/dodge.schema.v0.2.0.json` — document structure
- `schemas/dodge-export-contract.schema.v0.2.0.json` — target capability-contract structure
- `examples/` — small examples demonstrating both prototype families

## Scope decision

Version 0.2.0 formalizes the shared object/scene model, source traceability, adjacent sidecars, neutral physical components, quantities, relationships, deterministic inventory resolution, and exporter boundaries.

It intentionally does not promote the broader Wretched Demesne sidecar semantics for turns, resources, AI, topology, progression, or scenario logic. Those are reserved for the planned 0.2.1 design pass.

## Compatibility

The 0.2.0 core retains every 0.1.0 field used by the Digitropolis and Wretched Demesne DODGE documents. Migration requires updating `dodge_version`; all new core fields are optional.
