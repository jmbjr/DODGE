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
- `entity_invocations`
- `rules`
- `representations`
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

### 4.1 Normative physical dimensions

When `component.dimensions` is present, it defines the normative finished physical dimensions of the component. These values are game-domain facts, not layout hints. For a cut component, width and height describe the finished cut or trim boundary; bleed MAY extend beyond that boundary but MUST NOT change it.

Physical unit conversion MUST be exact: 1 inch is 25.4 millimetres, and 1 point is 1/72 inch. Dimensions MUST be positive and geometrically compatible with the declared shape.

A print-and-play exporter MUST render a component at its declared physical dimensions when the artifact is printed at 100% scale. It MAY apply a different scale only when the selected target contract explicitly declares and documents the transformation. Such a transformation MUST state the scale factor, MUST be recorded in the build manifest or equivalent provenance record, and MUST cause the output to be identified as not dimensionally accurate at 100% print scale.

`size_class` is a semantic, project-defined classification. It does not have a universal DODGE measurement. When both `size_class` and explicit `dimensions` are present, `dimensions` is authoritative. A project MAY define a registry that maps size classes to expected dimensions; validators MAY report a mismatch between that registry and explicit dimensions, but exporters MUST NOT replace the explicit dimensions with the registry value.

When explicit dimensions are absent, a project or target contract MAY resolve a `size_class` to dimensions. That mapping MUST be deterministic and documented, and its identity SHOULD be preserved in export provenance. Exporters MUST NOT silently invent conflicting physical sizes for the same unresolved size class.

Digital targets MAY scale components freely for display or interaction. They SHOULD preserve the declared aspect ratio and neutral size semantics. A Tabletop Simulator exporter, for example, MAY map physical units to target units but MUST NOT redefine the component's neutral dimensions or `size_class`; the mapping belongs in its target contract or target-owned configuration.

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

### 7.5.1 Playable-object invocation bindings

An `invocation` is the neutral bridge from using a game object to executable rule semantics. It declares:

- a stable local `id`;
- a semantic trigger such as `play`, `use`, or `activate`;
- one or more ordered procedure steps referencing existing actions, procedures, or effects, or containing inline effects;
- optional subject-slot bindings that construct the execution context.

Invocations MAY be declared on a local object, on a collection member, or in top-level `entity_invocations` keyed by an externally referenced entity ID. This permits canonical entity catalogs to remain external while the DODGE document binds their entities to its normalized rule graph.

For a resolved playable occurrence, invocation resolution is deterministic:

1. a member-level `invocations` array overrides inherited invocation declarations for that member occurrence;
2. otherwise, an `object_ref` member inherits the referenced object's invocations;
3. otherwise, an `entity_ref` member inherits `entity_invocations[entity_ref]` when present;
4. a directly instantiated object uses its own invocations.

If no explicit invocation resolves, the object has no executable use binding. A runtime MUST NOT infer one from equality or similarity between object/entity IDs and action IDs.

Each invocation step uses the existing procedure-step vocabulary. An action step references its action with `kind: action` and `ref`. The referenced action remains authoritative for costs, requirements, target semantics, procedure, and effects. An invocation MUST NOT copy or override an action's cost. Therefore changing an action cost changes every object that invokes it without changing those objects.

An invocation MAY instead reference a procedure, reference effects, or contain inline effects. Direct effects retain their own conditions and timing. Ordered mixed sequences use multiple steps rather than target-specific runtime branches.

Subject bindings populate neutral execution-context slots. A binding declares a slot such as `source`, `target`, `current-actor`, or `location` and obtains its value from:

- `runtime-input`, identified by a stable input name;
- `using-object`, the concrete object/member occurrence that triggered the invocation;
- `context-subject`, an existing neutral subject selector.

Required runtime inputs MUST be supplied before execution. All steps then resolve ordinary subject selectors such as `{ "relative": "target" }` against that context. For example, a Sidearm-like object binds the `target` slot from runtime input `enemy-target`, then invokes Attack; the runtime does not test whether the object's ID is `sidearm`.

Invocation IDs MUST be unique within their declaring array, subject-binding slots MUST be unique within an invocation, referenced steps MUST resolve to definitions of the correct kind, and required subject slots used by those definitions MUST be bound by the invocation or already available in the surrounding execution context.

Multiple differently identified objects MAY invoke the same action. Renaming an object or entity does not change execution as long as its explicit invocation binding is preserved.

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

### 7.9 Selectable representations of semantic state

Semantic state and its representation are separate. A value or resource definition owns its type, bounds, ownership, persistence, timing, thresholds, and rule behavior. A representation candidate only describes how that same state may be perceived or manipulated.

`representations` is an optional map of reusable candidates. Each candidate MUST declare:

- `state_ref`, resolving to exactly one `rules.values` or `rules.resources` definition;
- a neutral `kind`, such as `unit_tokens`, `numbered_track`, `marker_track`, `dial`, `numeric_display`, `status_marker`, or `target_native`;
- an `encoding`: `quantity`, `position`, `numeric`, or `presence`;
- whether interaction is `display-only` or `read-write`;
- zero or more neutral component requirements.

A component requirement references an ordinary DODGE object, assigns its representational role, and derives its required quantity using one of these bases:

- `fixed`, with an explicit non-negative quantity;
- `current`, from the selected state's current binding;
- `maximum`, from the selected state's maximum.

`per_binding` states whether the requirement is repeated for every resolved owner binding. A quantity derived from `current` or `maximum` is not a copied game value: it MUST resolve from the semantic definition or runtime binding. If the required value is unavailable in the selected export scope, the exporter MUST fail clearly or use a different explicitly selected candidate.

An export contract includes candidates with `representation_inclusions`. Each inclusion group declares one `state_ref`, one `mode`, and an ordered, unique `representation_refs` list:

- `selected` contains exactly one gameplay representation;
- `synchronized` contains two or more simultaneously active views or controls of the same state binding;
- `alternatives` contains two or more mutually alternative implementations bundled into one artifact for evaluation, prototyping, or review.

Omitting an inclusion group for a state means that profile includes no representation for that state. A target MAY therefore include one, several, or none of the available candidates according to its capability and purpose.

For every inclusion, the state and representation references MUST resolve, every candidate's `state_ref` MUST equal the inclusion's `state_ref`, every candidate kind MUST be listed in `accepts.representation_kinds`, and the mode MUST be listed in `accepts.representation_modes`. A standard contract MUST contain at most one inclusion group per state.

Every included candidate adds its component requirements to the resolved export inventory. Unincluded candidates contribute no components. Target-native candidates may have no neutral component requirements. An `alternatives` group adds all configured alternatives to one artifact but does not duplicate the base game inventory and does not imply that the alternatives are used simultaneously. A `synchronized` group requires the target to keep all included representations bound to the same semantic state during play.

Representation selection MUST NOT change or override current values, maximum values, defaults, ownership, persistence, reset timing, conditions, effects, or any other semantic rule. PDF coordinates, track graphics, TTS scripts/GUIDs/transforms, Web DOM/CSS, and equivalent implementation details remain target-owned.

An object's use as a representation component is established by the selected candidate, not by its physical form. World objects such as a corpse or chrysalis remain game objects even when physically token-shaped; they are not representations of a value unless a candidate explicitly uses them in that role.

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

When an export contract includes state representations, the resolver appends every included candidate's resolved component requirements in inclusion-group and candidate order. Those additions MUST retain provenance to the representation candidate, state definition, contract inclusion, and inclusion mode that caused them. Base scene inventory is resolved once; an alternatives bundle MUST NOT clone the rest of the game for each candidate.

### 13.1 Resolved target manifests

An exporter MUST be able to emit an explicit resolved target manifest conforming to `schemas/dodge-target-manifest.schema.v0.2.1.json`. The manifest is deterministic diagnostic output, not a new source of game truth. It identifies the exact DODGE document, export contract, resolution scope, and ordered target contents used for a build.

Each content entry exposes:

- a deterministic `content_id`;
- its source kind, reference, and JSON path;
- canonical and resolved quantity;
- inclusion status;
- inherited and effective component metadata when applicable;
- optional target grouping and presentation-variant identity;
- ordered provenance back to DODGE and contract inputs;
- field-level diagnostics showing inherited, derived, or overridden values and classifying them as canonical, presentation-only, or explicitly non-canonical playtest data.

When a resolved object/member has invocations, its target-manifest entry SHOULD include their ordered IDs in `invocation_ids`. A renderer may preserve or display this relationship without executing it; gameplay runtimes consume the full DODGE invocation definitions.

Content IDs use these deterministic forms within a resolution scope:

- scene instance: `scene/<scene-ref>/instance/<instance-id>`;
- collection member: append `/member/<zero-based-declared-index>` to its owning content ID;
- representation component: `representation/<representation-ref>/component/<zero-based-declared-index>`;
- presentation variant: append `/variant/<variant-id>` to the source content ID.

Nested collection paths repeat the member segment. Decimal indexes MUST be emitted without leading zeroes. Exporters MUST preserve scene, member, representation-inclusion, component, and variant declaration order. The same inputs and selected scope MUST produce byte-equivalent ordered semantic manifest content after canonical JSON serialization; timestamps, random IDs, and machine paths MUST NOT participate.

### 13.2 Target content configuration and inheritance

An export contract MAY contain `content_configuration`. Its default is `inherit-resolved`: every resolved scene, collection-member, and included representation-component entry is included with canonical quantity and component metadata unless an exact `content_ref` entry changes it.

A designer-authored content entry MAY:

- inherit, include, or exclude the resolved item;
- assign a target grouping label;
- override dimensions or `size_class` for that target artifact;
- declare an explicit non-canonical playtest quantity with a reason;
- attach target notes;
- add presentation variants that replace or accompany the base rendering.

Overrides are applied only after neutral inventory and representation resolution. They MUST NOT mutate the DODGE document, its objects, semantic state, collection membership, or rules. Every override MUST appear in target-manifest diagnostics with its canonical and effective values. An overridden physical dimension is the documented scaling transformation allowed by section 4.1; the canonical DODGE dimension remains authoritative and the effective target size is presentation metadata.

An `include` override may restore an entry excluded earlier by the same target configuration, but it cannot create an unresolved game object. An `exclude` override retains a diagnostic manifest entry with `resolved_quantity: 0`. A quantity override MUST use classification `noncanonical-playtest` and state a reason. It changes only the artifact contents, never the canonical inventory or gameplay requirement.

### 13.3 Presentation variants versus semantic representations

A presentation variant is another rendering or packaging treatment of the same content identity: for example, standard and high-contrast art, alternate label treatments, or a target-sized playtest print. It MUST NOT change what state is represented, object behavior, rules, or semantic identity.

A semantic representation implements a value/resource through a different interaction model, such as Health tokens versus a numbered track. Those alternatives belong in DODGE `representations` and are included through `representation_inclusions`. If a proposed variant changes state encoding, gameplay interaction, component meaning, or rule behavior, it is not a presentation variant.

With `variant_policy: replace-base`, the base content remains in the manifest for provenance but is excluded from emitted artifact quantity while the variant entries are emitted. With `alongside-base`, both base and variant entries are emitted. Each variant inherits the base entry's effective quantity and component metadata unless it carries its own explicit override. Variant copies are presentation artifacts and MUST NOT be added to canonical game quantity.

## 14. Target boundary

DODGE owns neutral facts, logical topology, declarative rules, and scene/campaign composition. Targets own presentation and deployment details.

Normative physical component dimensions are neutral facts. Page imposition, margins, bleed, cut marks, typography, printer settings, digital transforms, TTS GUIDs, atlas indices, hosted URLs, engine node paths, and target save identifiers are target-owned.

Forbidden examples in a DODGE document include PDF coordinates, cut-mark geometry, font sizes, printer settings, TTS GUIDs, atlas indices, hosted URLs, engine node paths, and target save identifiers. Neutral dimensions do not become target-owned merely because an exporter consumes them.

A target contract MUST declare supported DODGE versions, object kinds, component forms, rule features, representation kinds when used, and required extensions. Any transformation that changes declared physical output size MUST also be explicit and documented in the contract. Unsupported required semantics MUST fail clearly rather than degrade silently.

Target grouping, notes, variant artwork, effective print size, and non-canonical playtest quantities belong in the export contract and resolved target manifest. Page coordinates, typography, page imposition, and renderer layout remain outside both DODGE and the neutral target manifest.

## 15. Semantic validation

In addition to schema validation, a 0.2.1 validator MUST check:

1. all required local and external references resolve;
2. object/archetype kinds and face slots agree;
3. collection nesting and procedure references are acyclic unless repetition is explicit;
4. quantities are coherent, and component dimensions are positive, geometrically valid, and expressed in supported units;
5. source hashes match;
6. scene instance and topology node IDs are unique in scope;
7. topology edges reference existing nodes;
8. rule references target definitions of the correct kind;
9. defaults satisfy types and bounds;
10. phase transitions and scenario end-condition evaluation are deterministic;
11. AI priorities have an executable action/effect/procedure or are marked prose-only;
12. a target contract supports all required normalized features.

When representations are present or included, a validator MUST additionally check that state and object references resolve; inclusion state matches every candidate state; candidate kinds and inclusion modes are supported by the contract; mode cardinality is valid; component quantities can be resolved for the export scope; candidate references are unique within a group; and a standard profile contains at most one inclusion group per state.

When target content configuration is present, a validator MUST check that every `content_ref` resolves exactly once in the pre-override manifest, configuration entries do not repeat a `content_ref`, presentation-variant IDs are unique within an entry, quantity overrides are explicitly non-canonical and justified, component overrides are valid, and no override changes semantic identity or rules. A resolved manifest MUST preserve excluded entries and every inherited/derived/overridden diagnostic required to explain the effective artifact contents.

When invocations are present, a validator MUST also check invocation-ID and subject-slot uniqueness, resolution precedence, referenced step kinds, required execution-context inputs, and action availability/cost semantics. An object/entity ID matching an action ID is not a binding and MUST NOT satisfy validation.

A validator MAY additionally compare explicit dimensions with a project-defined `size_class` registry and report mismatches. Such a diagnostic MUST treat the explicit dimensions as authoritative.

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
| alternate Health tokens/tracks/HUDs | representation candidates + export-contract selection |
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

## 19. Issue #25 adoption requirements

This revision separates selectable state representation into three normative layers:

| Concern | Normative location |
|---|---|
| Health current/max, owner, persistence, and rules | `rules.values.health` and runtime bindings |
| token, track, marker-card, HUD, or target-native alternative | `representations` candidate |
| included alternative(s) for one export | target contract `representation_inclusions` |

The Wretched Demesne example defines one Health value and multiple candidates. The accompanying contracts select individual tokens, a numbered track, a crew-card marker track, or a Web numeric display without cloning or overriding Health. Spider Corpse and Chrysalis remain contrasting world objects in scene/rule inventory rather than state representations.

The same pattern applies without new rule definitions to Ammo, Threat, Actions, and Scrap through quantity, position, or numeric encodings; and to Fed or Incapacitated through presence or status-marker encodings. The candidate chosen for any of them may differ by target and experiment. A physical Spider Corpse or Chrysalis, by contrast, has identity, location, relationships, and lifecycle in the game world, so it remains an object even if a target renders it with the same physical material as a representational token.

## 20. Issue #27 adoption requirements

Export profiles distinguish capability from inclusion policy:

| Concern | Contract field |
|---|---|
| supported candidate forms | `accepts.representation_kinds` |
| supported inclusion behavior | `accepts.representation_modes` |
| included candidates and their purpose | `representation_inclusions` |

The WD PnP Beta contract uses `alternatives` to place all three Health experiments in one PDF while resolving the game inventory once. Stable PnP, Web, and TTS profiles use `selected`. A TTS Beta profile demonstrates an alternatives bundle, and a separate TTS contract schema-tests `synchronized` views bound to the same Health state. These are export decisions only; none may clone or override Health semantics.

## 21. Issue #29 adoption requirements

The target-manifest pipeline is:

1. resolve the selected DODGE scope and canonical inventory;
2. append components from representation inclusions;
3. assign deterministic content IDs and provenance;
4. apply exact target content-configuration entries;
5. expand presentation variants;
6. emit the ordered resolved target manifest;
7. render the artifact from that manifest.

The WD PnP Beta example demonstrates inherited entries, a target-only dimension override, grouping and notes, presentation variants, and an explicitly non-canonical playtest quantity. The accompanying resolved manifest preserves both canonical and effective values so a reviewer can distinguish DODGE facts from target decisions without a Wretched-specific extension.

## 22. Issue #32 adoption requirements

The playable-object execution chain is:

1. resolve the concrete object or collection member;
2. resolve its explicit invocation declaration using the precedence in section 7.5.1;
3. collect required runtime subject inputs;
4. execute invocation steps in order;
5. for an action step, evaluate the referenced action's requirements and consume its declared costs;
6. resolve action/procedure/effect subjects through the constructed neutral execution context.

The neutral example demonstrates two differently identified movement cards invoking the same Move action, an attack card binding a runtime-selected target before invoking Attack, a reload card invoking Reload, and a direct-effect object. Object-ID switches, action-ID equality assumptions, embedded `sidearm` defaults, and engine-coded uniform action costs are explicit anti-patterns when invocation bindings and action costs are available.

All invocation fields are optional additions. Existing valid 0.2.1 documents remain valid and gain no inferred executable behavior.
