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

## Deliberate limits

The schema does not promote inspirations, design pillars, candidate mechanics, prototype recommendations, or unresolved questions into executable rules. Those remain metadata or adjacent sidecar information.

This vocabulary is intentionally declarative and conservative. It can preserve the WD sidecar's structured intent, but it is not yet a complete rules engine or expression language.

## Structure

- `DODGE_SPEC.md` — complete candidate specification
- `schemas/dodge.schema.v0.2.1.json` — document schema
- `schemas/dodge-export-contract.schema.v0.2.1.json` — target contract schema
- `examples/digitropolis-minimal.dodge.json` — compatibility example
- `examples/wretched-demesne-sidecar-promoted.dodge.json` — inferred WD rule-model example
