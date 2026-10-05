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
- export-profile inclusion modes for selected, synchronized, and bundled-alternative representations
- deterministic resolved target manifests with inherited-versus-overridden diagnostics
- target-owned PnP grouping, presentation variants, size overrides, and explicit playtest quantities
- neutral playable-object invocation bindings to actions, procedures, and effects
- explicit executable modes, player choices, requirements, and scoped modifiers
- neutral carried/equipped lifecycle, slots, capabilities, parameters, and equipped modifiers
- data-driven location entry, exit, access, interaction, and search outcomes

## Deliberate limits

The schema does not promote inspirations, design pillars, candidate mechanics, prototype recommendations, or unresolved questions into executable rules. Those remain metadata or adjacent sidecar information.

This vocabulary is intentionally declarative and conservative. It can preserve the WD sidecar's structured intent, but it is not yet a complete rules engine or expression language.

Issue #21 drove the timing, ownership, transformation, and topology-materialization semantics in this revision.

Issue #23 clarified that explicit component dimensions are authoritative physical facts, established exact-size print-and-play behavior, and kept target-specific layout and digital scaling outside the neutral document.

Issue #25 introduced the minimum neutral vocabulary for alternate state representations while keeping the underlying value/resource definition authoritative. Export contracts include candidates without moving game rules into target configuration.

Issue #27 generalized export profiles so Beta artifacts can bundle several alternative implementations without duplicating the game, while stable profiles can select one and capable targets can synchronize redundant views.

Issue #29 defined designer-authored target content configuration and deterministic resolved target manifests. Target overrides remain traceable artifact decisions and never mutate DODGE semantics.

Issue #32 added explicit invocation bindings between usable objects and normalized actions/procedures/effects, including runtime subject inputs. Action costs remain authoritative and object-ID dispatch is non-conforming.

Issues #34–#36 completed a shared rule layer for choices, requirement waivers, equipment lifecycle, and location-bound outcomes without game-specific flags or room-ID dispatch.

## Structure

- `DODGE_SPEC.md` — complete candidate specification
- `schemas/dodge.schema.v0.2.1.json` — document schema
- `schemas/dodge-export-contract.schema.v0.2.1.json` — target contract schema
- `schemas/dodge-target-manifest.schema.v0.2.1.json` — resolved target-manifest schema
- `examples/digitropolis-minimal.dodge.json` — compatibility example
- `examples/wretched-demesne-sidecar-promoted.dodge.json` — inferred WD rule-model example
- `examples/playable-object-bindings.dodge.json` — neutral invocation and target-binding example
- `examples/requirements-equipment-locations.dodge.json` — choices, waivers, equipment, and location semantics
- `examples/export-contracts/` — WD Health representation-laboratory selections
- `examples/target-manifests/` — resolved content and provenance examples
