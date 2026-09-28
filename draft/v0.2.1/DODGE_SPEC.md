# DODGE Specification 0.2.1

**Status:** Working draft  
**Version:** 0.2.1  
**Name:** Declarative Object Description for Game Engines

## 1. Purpose

DODGE is a target-neutral interchange format describing a game's canonical references, component inventory, scenes, and optionally the declarative rules needed to interpret them.

```text
canonical catalogs + rules + selections + adjacent sidecars
                              |
                         DODGE document
                 _____________|_____________
                |             |             |
          component       rule graph     scenarios
          inventory       and state      and campaign
                |             |             |
                +-------------+-------------+
                              |
                    shared resolver/runtime
                    /          |           \
                 PnP          TTS       digital/sim
```

DODGE is authoritative for neutral composition and for any normalized semantics it explicitly contains. External sources remain authoritative for facts merely referenced by DODGE. Generated target artifacts MUST NOT become independent definitions.

## 2. Compatibility

0.2.1 includes all 0.2.0 concepts unchanged except the required `dodge_version`. The following new top-level sections are optional:

- `game_profile`
- `rules`
- `topologies`
- `scenarios`
- `campaigns`
- `runtime_states`

The revision responding to issue #21 also makes timing, ownership, transformation, and runtime topology materialization normative within those sections.

A 0.2.0 document migrates by changing `dodge_version` to `0.2.1`. No other change is required.

## 3. Conformance

The words **MUST**, **MUST NOT**, **SHOULD**, **SHOULD NOT**, and **MAY** are normative.

A conforming document MUST:

1. validate against `schemas/dodge.schema.v0.2.1.json`;
2. resolve all local references required by a selected scene/scenario/campaign;
3. resolve one deterministic component inventory;
4. preserve declared rule/procedure order;
5. reject reference cycles where cycles are forbidden;
6. contain no target-owned presentation or deployment fields.

## 4. Stable 0.2.0 core

The following 0.2.0 semantics remain normative:

- `sources` reference versioned external catalogs, rules, selections, scenarios, assets, or sidecars and may be SHA-256 pinned.
- source `authority` distinguishes `authoritative`, `derived`, `provisional`, and `reference` inputs.
- `sidecars` losslessly preserve information outside the normalized core.
- `archetypes` describe reusable token, collection, and experimental randomizer shapes.
- neutral `component` profiles describe form, size class, shape, dimensions, sides, and shared backs without target layout.
- `objects` populate faces, semantic regions, members, behaviors, and relationships.
- collection and instance quantities multiply during inventory resolution.
- `scenes` instantiate objects with initial state and semantic locations.
- target contracts declare capabilities, mappings, target-owned additions, outputs, and forbidden fields.
- namespaced `extensions` allow declared experiments without redefining the core.

The detailed JSON shapes for this core are normative in the 0.2.1 schema.

## 5. Identity and references

Local identifiers match `^[a-z0-9][a-z0-9._:-]*$`.

References ending in `_ref` name a local definition of the corresponding kind unless explicitly documented as external content. Arrays ending in `_refs` preserve order. Resolvers MUST reject missing references required by the selected execution scope.

## 6. Game profile

`game_profile` identifies broad play constraints without defining mechanics:

- minimum and maximum players;
- supported modes such as cooperative, competitive, solo, or team;
- optional genre, setting, and tags.

Inspirations and design pillars are non-executable design intent. They MAY remain in metadata or a sidecar but SHOULD NOT control runtime behavior.

## 7. Rules graph

The optional `rules` object contains named dictionaries:

- `values`
- `resources`
- `actions`
- `conditions`
- `effects`
- `procedures`
- `phases`
- `ai_profiles`

The graph is declarative. Definitions are reusable and referenced by stable ID.

### 7.1 Values and state

A value definition declares a typed state value:

- `number`, optionally bounded;
- `integer`, optionally bounded;
- `boolean`;
- `string`;
- `enum`, with declared values.

It MAY define a default and scope. Scopes include `game`, `campaign`, `scenario`, `round`, `turn`, `player`, `actor`, `object`, and `location`.

Values cover health, ammunition, fed state, incapacitation, counters, and other state not best modeled as a spendable resource.

### 7.2 Resources, tracks, and statuses

A resource has a `kind`:

- `currency`: gained and spent quantities such as scrap or ammunition;
- `track`: a bounded value whose thresholds may drive effects, such as threat or noise;
- `status`: a named state such as fed, suppressed, or incapacitated;
- `capacity`: a bounded allowance such as actions remaining or hand size;
- `inventory`: a counted carried or pooled item category.

Resources declare ownership, persistence, optional bounds/defaults, and optional threshold rules. A threshold rule contains a condition and ordered effect references or inline effects.

Every resource declares two separate concepts:

- `owner_scope`: which kind of subject owns one binding (`actor`, `player`, `party`, `expedition`, `location`, `scenario`, `campaign`, `object`, or `game`);
- `persistence_scope`: the boundary through which that binding survives (`turn`, `round`, `scenario`, `expedition`, `campaign`, or `game`).

`scope` is retained temporarily as a deprecated draft alias and MUST NOT be used when `owner_scope` is present. A binding selects the concrete owner. Thus one Health binding can belong to one crew actor, one hand/deck to one player or crew context, Ammo to the current expedition, Threat to the scenario, and Scrap or Knowledge to the campaign.

An optional `reset_at` timing anchor declares when a resource resets. Ownership never implies reset or persistence.

### 7.3 Conditions

A condition is either:

- a structured predicate; or
- an explicitly marked prose predicate when the source is not yet formal enough.

Structured predicates support:

- comparison: `eq`, `ne`, `lt`, `lte`, `gt`, `gte`;
- Boolean composition: `all`, `any`, `not`;
- state/resource lookup by reference and optional subject;
- existence and containment tests;
- event matching.

Prose predicates preserve intent but are not automatically executable. A runtime MUST NOT claim executable support for a prose-only condition.

### 7.4 Effects

An effect is either structured or prose-only. Structured effect operations include:

- `set`, `add`, `subtract` on a value/resource;
- `add_status`, `remove_status`;
- `create`, `remove`, `move`, or `transform` an object/instance;
- `draw`, `discard`, or `shuffle` a collection;
- `advance` a phase, procedure, track, or turn;
- `emit` a semantic event;
- `choose` among declared options.

Effects MAY have conditions. Effects execute in declared order unless a rule explicitly marks them simultaneous.

### 7.4.1 Timing anchors

A timing anchor identifies a deterministic boundary:

- `scope`: `phase`, `turn`, `round`, `scenario`, `expedition`, or `campaign`;
- `boundary`: `start` or `end`;
- optional `ref`: the named phase, procedure, scenario, or campaign;
- optional `subject`: whose boundary is meant;
- `occurrence`: `current`, `next`, or a positive ordinal;
- optional `offset` in boundary occurrences.

For example, “until your next turn” expires at the start of the next turn owned by the affected actor. “Hatch during the next End phase” schedules an effect at the specified boundary of the next referenced End phase.

### 7.4.2 Effect timing and lifetime

An effect MAY declare `timing`:

- `apply`: `immediate` or `scheduled`;
- `at`: required timing anchor for scheduled application;
- `expires_at`: timing anchor that removes the effect;
- `cancel_condition_refs`: conditions that cancel it before application or expiration;
- `recheck_condition_refs`: conditions evaluated at scheduled execution time;
- `duration`: an integer number of named boundary occurrences;
- `usage`: a usage-limit definition.

A scheduled effect is queued with stable identity, source/cause traceability, resolved subject bindings, and its resolved anchor. Crossing the anchor executes it once unless cancelled. Runtimes MUST serialize pending scheduled effects as neutral state so saves and targets agree.

A temporary effect with neither `expires_at`, `duration`, nor consuming `usage` is invalid.

### 7.4.3 First, next, and once-per-X limits

A usage limit declares:

- `count`: allowed or consumable uses;
- `mode`: `first`, `next`, or `up-to`;
- `period`: a timing scope and owner subject for reset;
- `consume_on`: `attempt`, `resolve`, `success`, or a named event;
- optional event/action/tag matching;
- optional `expires_at` independent of consumption.

“Your next attack this turn” is a `next` use matching Attack, consumed at the declared point, with end-of-current-turn expiration. “First firearm attack each turn” is `first`, count 1, matching the firearm tag, reset per actor turn. “Once per turn” is `up-to`, count 1, with the same period.

### 7.4.4 Neutral runtime timing state

A resumable implementation MUST serialize normalized timing state rather than reconstruct it from target code. A `runtime_states` snapshot contains:

- the selected scene/scenario/campaign;
- current round/turn counters, phase reference, and active subject;
- concrete value/resource bindings and owners;
- active effects with remaining uses and resolved expiration anchors;
- scheduled effects with resolved application anchors, captured subjects, and causes;
- the current materialized topology reference;
- optional ordered semantic event records for traceability.

Runtime-state IDs, active-effect IDs, and scheduled-effect IDs are stable within the snapshot. Target saves MAY wrap this state, but they MUST NOT replace its neutral meaning.

### 7.5 Actions

An action declares:

- name and description;
- actor kinds or tags allowed to take it;
- costs, expressed as resource/value deltas;
- requirement condition references;
- target constraints;
- an ordered procedure or effect list;
- tags.

An action definition does not automatically place the action in every turn. Phases and scenarios determine availability.

### 7.6 Procedures

A procedure is an ordered list of steps. A step may:

- reference an action, condition, effect, procedure, phase, or AI profile;
- perform an inline condition/effect;
- create a choice;
- repeat while/until a condition holds;
- preserve an unresolved prose instruction.

Procedures model attack resolution, enemy activation, end-turn checks, expedition resolution, and campaign loops without hard-coding them into exporters.

### 7.7 Phases and turn structures

A phase declares available action references, an optional procedure, entry/exit effects, and an optional next phase.

A turn/round structure is represented as a procedure whose ordered steps reference phases. Macro structures such as Ship Phase and Expedition Phase use the same mechanism at a broader scope.

Phase order is normative. A phase cycle MUST terminate through a declared transition, scenario end condition, or externally controlled repetition.

### 7.8 AI profiles

An AI profile contains ordered priorities. Each priority has:

- a condition;
- an action, procedure, or effect;
- optional target-selection guidance;
- optional fallback text.

Priorities are evaluated in order; the first satisfied executable priority is selected unless `evaluation` states otherwise.

This supports WD's Detect → Move → Act procedure and differentiated Small/Large/Alpha Spider priorities while remaining generic.

## 8. Topologies

A topology defines logical space independently of rendering. It has a `resolution` of `unresolved`, `partially-materialized`, or `materialized`.

An unresolved topology declares a `generation_procedure_ref`, optional component/object pools, constraints, hidden-state policy, and stable-ID policy. It does not pretend that unknown nodes or edges already exist.

A materialized topology contains concrete nodes and edges plus a `materialization` record:

- `source_topology_ref` pointing to the unresolved/template topology;
- stable `generation_id`;
- optional seed and generator version;
- generation-procedure reference;
- ordered decisions/events sufficient for replay when available;
- stable node/edge ID policy;
- source hash or state revision when persisted.

Materialization creates or updates neutral DODGE runtime state, not a target-owned save format. Web, TTS, simulation, and other stateful targets consume the same materialized topology snapshot. PnP MAY export the generation procedure and unresolved component pool when topology is intentionally generated during physical play.

A node MAY declare object/terrain tags, capacity, state, and discovery visibility. An edge declares endpoints, directionality, connection kind, costs, requirements, and state.

Connection kinds are semantic project IDs such as `passage`, `door`, `rail`, or `road`. Page coordinates, pixels, and TTS transforms remain target-owned.

Procedural-generation candidates or recommendations are not concrete topology. They remain metadata/sidecar information until expressed as a formal generator in a future version.

Hidden is orthogonal to unresolved: a materialized node may exist with a stable ID while remaining unrevealed to players. Revealing it changes visibility/state, not identity.

## 9. Scenarios

A scenario binds game semantics into a playable scope. It MAY declare:

- a setup `scene_ref`;
- a `topology_ref`;
- optional `materialized_topology_ref`, bound after runtime generation;
- player constraints;
- initial state/resource bindings;
- available actions;
- a turn procedure;
- ordered objectives;
- win, loss, retreat, and other end conditions;
- end effects;
- target duration metadata;
- source authority and assumption notes.

Objectives contain a completion condition and optional effects. End conditions are evaluated according to declared order/priority.

Retreat is modeled as an end condition and outcome, not assumed to be victory or defeat.

## 10. Campaigns and progression

A campaign MAY declare:

- persistent values/resources/statuses;
- named locations or regions;
- macro phases/procedures;
- a progression procedure;
- scenario references or selection rules;
- terminal conditions.

Persistence MUST be explicit. Scenario state does not automatically become campaign state.

The WD loop—select destination, explore, gain resources/information, return or retreat, upgrade, unlock—can be preserved as an ordered campaign procedure even when individual steps remain prose-only.

## 11. Events and subject addressing

Rules operate on semantic subjects. A subject selector MAY reference a concrete instance, actor/object tag, current actor/player, target, source, location, scenario, or campaign.

Selectors also include `party` and `expedition`. `party` means the participating group identity; `expedition` means the shared state container for the current outing. They are not synonyms: a campaign party may undertake multiple expeditions, and expedition-owned resources normally end or transfer explicitly when that expedition ends.

Every state/resource lookup and mutation MUST resolve to exactly one binding unless the operation explicitly allows a set. Ambiguous selectors are validation/runtime errors.

Events are named semantic occurrences with optional payload. Conditions can match events; effects can emit them. Event names are project IDs unless standardized by a later DODGE version.

### 11.1 Deterministic transformation

An effect with `op: transform` MUST include a `transformation` transaction containing:

- `subject`: the object, entity, or instance being replaced;
- `replacement_object_ref` or `replacement_entity_ref`;
- `consume`: zero or more independently selected objects/entities consumed by the transformation;
- `placement`: `same-location`, an explicit `location_ref`, or a subject selector;
- `identity_policy`: `preserve-instance-id` or `new-instance-id`;
- `state_transfer`: `none`, `all`, `only`, `except`, or an explicit field map;
- optional relationship-transfer policy;
- optional `cause_ref` and event payload;
- optional effect timing, including scheduled transformation.

The runtime resolves the subject and consumed items first, validates them, removes or consumes them atomically, creates the replacement at the resolved placement, transfers only the declared state and relationships, and emits a traceable transformation event. Partial transformation is invalid.

For WD pupation, the spider is the transformation subject; corpse tokens are separate consumed inputs; the Chrysalis is the replacement; placement is the spider's location. The corpse is not itself transformed into the Chrysalis.

## 12. Authority and assumptions

Normalized rules MAY still be provisional. Every major rule definition MAY include:

- `source_ref`;
- `authority`;
- `assumptions`;
- `notes`.

Exporters and runtimes MUST preserve these fields in traceability output. They MUST NOT present provisional rules as authoritative without an explicit project policy.

## 13. Component inventory

The 0.2.0 deterministic inventory algorithm remains unchanged:

1. visit scene instances in order;
2. resolve objects and archetypes;
3. multiply instance and nested member quantities;
4. resolve entity and object members recursively;
5. reject cycles and missing references;
6. preserve stable identity, order, component profile, faces, state, relationships, and provenance.

A scenario's inventory is the inventory of its `scene_ref`, plus components created by explicit setup effects whose quantities can be resolved before export. Dynamic runtime creation that cannot be bounded is reported as a runtime requirement rather than silently omitted.

## 14. Target boundary

DODGE owns neutral facts, logical topology, declarative rules, and scene/campaign composition. Targets own presentation and deployment details.

Forbidden examples include PDF coordinates, cut marks, font sizes, TTS GUIDs, atlas indices, hosted URLs, engine node paths, and target save identifiers.

A target contract MUST declare supported DODGE versions, object kinds, component forms, rule features, and required extensions. Unsupported required semantics MUST fail clearly rather than degrade silently.

## 15. Semantic validation

In addition to schema validation, a 0.2.1 validator MUST check:

1. all required local and external references resolve;
2. object/archetype kinds and face slots agree;
3. collection nesting and procedure references are acyclic unless repetition is explicit;
4. quantities and component dimensions are coherent;
5. source hashes match;
6. scene instance and topology node IDs are unique in scope;
7. topology edges reference existing nodes;
8. rule references target definitions of the correct kind;
9. defaults satisfy types and bounds;
10. phase transitions and scenario end-condition evaluation are deterministic;
11. AI priorities have an executable action/effect/procedure or are marked prose-only;
12. a target contract supports all required normalized features.

## 16. WD sidecar mapping used for this draft

| WD sidecar concept | 0.2.1 candidate representation |
|---|---|
| players/modes/genre | `game_profile` |
| turn and macro phases | phases + ordered procedures |
| hand size/actions per crew | capacity resources |
| move/attack/search/interact/assist/recover | actions |
| action costs | action cost entries |
| attack resolution | procedure |
| noise/threat | track resources + thresholds/effects |
| health/ammunition/scrap/medical supplies | values/resources |
| fed/suppressed/incapacitated | status resources |
| Detect → Move → Act | AI activation procedure |
| spider behavior differences | ordered AI profiles |
| feeding/pupation/development tree | conditions, effects, and transformations |
| end-turn checks | procedure |
| rooms/passages/terrain | topology |
| objective/win/loss/retreat | scenario objectives and end conditions |
| ship/expedition loop | campaign phases/procedure |
| regions/unlocks/persistence | campaign locations and persistent state |
| design pillars/inspirations/open questions | metadata or sidecar; not executable |

## 17. Known uncertainties for WD review

The WD chat should validate at least these decisions:

1. whether actions remaining and hand size are resources or actor value definitions;
2. whether noise is scoped to actor, location, scenario, or multiple scopes;
3. whether threat is a scenario track, campaign track, or linked pair;
4. the exact event order for feeding, corpse removal, pupation, and hatching;
5. whether enemy evolution is object transformation or replacement;
6. how hidden rooms and exploration generation become concrete topology;
7. which retreat consequences persist to campaign state;
8. which GDD statements are authoritative versus candidate/provisional;
9. whether rules need simultaneous-effect groups or interrupt/reaction timing;
10. how deck-building acquisition and ship modification interact with campaign persistence.

These are explicit draft uncertainties, not silent assumptions.

## 18. Issue #21 adoption requirements

This revision intends to satisfy issue #21 as follows:

| Requirement | Normative mechanism |
|---|---|
| temporary deterministic expiration | effect `timing.expires_at` or duration |
| delayed/scheduled effects | `timing.apply: scheduled`, an `at` anchor, and pending-effect state |
| phase/turn/round anchors | timing-anchor scope, boundary, subject, and occurrence |
| first/next/once-per-X | usage limits with mode, count, period, matching, and consumption point |
| actor/player/shared ownership | `owner_scope`, `persistence_scope`, subject selectors, and concrete bindings |
| deterministic replacement | atomic `transformation` transaction |
| generated versus concrete topology | topology `resolution`, materialization record, and stable IDs |
| deterministic save/resume | neutral `runtime_states` bindings, active effects, schedules, clock, and topology reference |

These mechanisms are generic. WD-specific values and procedures belong in WD data, not this specification.
