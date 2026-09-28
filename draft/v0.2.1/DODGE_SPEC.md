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

Resources declare scope, optional bounds/defaults, and optional threshold rules. A threshold rule contains a condition and ordered effect references or inline effects.

Resource definitions do not imply ownership. Runtime state binds scoped resource IDs to concrete players, actors, scenes, objects, or campaigns.

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

A topology defines concrete logical space independently of rendering. It contains nodes and edges.

A node MAY declare object/terrain tags, capacity, state, and discovery visibility. An edge declares endpoints, directionality, connection kind, costs, requirements, and state.

Connection kinds are semantic project IDs such as `passage`, `door`, `rail`, or `road`. Page coordinates, pixels, and TTS transforms remain target-owned.

Procedural-generation candidates or recommendations are not concrete topology. They remain metadata/sidecar information until expressed as a formal generator in a future version.

## 9. Scenarios

A scenario binds game semantics into a playable scope. It MAY declare:

- a setup `scene_ref`;
- a `topology_ref`;
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

Events are named semantic occurrences with optional payload. Conditions can match events; effects can emit them. Event names are project IDs unless standardized by a later DODGE version.

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
