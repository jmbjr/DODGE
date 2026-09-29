# DODGE 0.2.1 working draft

This is a complete candidate release derived from `official/v0.2.0/` and informed by the structured Wretched Demesne GDD sidecar.

It remains under `draft/` until the Wretched Demesne implementation has exercised and corrected the inferred rule vocabulary.

## Added candidate concepts

- game profiles and supported player counts/modes
- typed resources, tracks, statuses, and state variables
- actions with costs, requirements, procedures, and effects
- ordered phases and procedures
- declarative conditions and effects with prose fallbacks
- priority-based AI profiles
- concrete map topology and connection rules
- scenarios, objectives, setup, and end conditions
- campaign phases, locations, persistence, and progression loops
- timing anchors, deterministic effect lifetimes, scheduled effects, and usage limits
- explicit actor/player/party/expedition/location/scenario/campaign ownership
- deterministic transformation transactions with consumption, placement, identity, and state-transfer policy
- unresolved topology generation and materialized runtime topology snapshots
- neutral resumable runtime snapshots for clocks, bindings, active effects, and scheduled effects
- normative physical component dimensions and explicit exporter-scaling rules
- selectable representations of semantic state with export-profile selection

## Deliberate limits

The schema does not promote inspirations, design pillars, candidate mechanics, prototype recommendations, or unresolved questions into executable rules. Those remain metadata or adjacent sidecar information.

This vocabulary is intentionally declarative and conservative. It can preserve the WD sidecar's structured intent, but it is not yet a complete rules engine or expression language.

Issue #21 drove the timing, ownership, transformation, and topology-materialization semantics in this revision.

Issue #23 clarified that explicit component dimensions are authoritative physical facts, established exact-size print-and-play behavior, and kept target-specific layout and digital scaling outside the neutral document.

Issue #25 introduced the minimum neutral vocabulary for alternate state representations while keeping the underlying value/resource definition authoritative. Export contracts select one candidate without moving game rules into target configuration.

## Structure

- `DODGE_SPEC.md` — complete candidate specification
- `schemas/dodge.schema.v0.2.1.json` — document schema
- `schemas/dodge-export-contract.schema.v0.2.1.json` — target contract schema
- `examples/digitropolis-minimal.dodge.json` — compatibility example
- `examples/wretched-demesne-sidecar-promoted.dodge.json` — inferred WD rule-model example
- `examples/export-contracts/` — WD Health representation-laboratory selections
