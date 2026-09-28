# DODGE Specification 0.2.0

**Status:** Draft for review  
**Version:** 0.2.0  
**Name:** Declarative Object Description for Game Engines

## 1. Purpose

DODGE is a target-neutral interchange format for describing the game objects required by a scene, how those objects are grouped, and the basic interactions they advertise.

A DODGE document sits between canonical game information and target exporters:

```text
canonical catalogs + rules + selections + adjacent sidecars
                              |
                         DODGE scene
                              |
                    shared resolver/inventory
                    /          |           \
                 PnP          TTS       other targets
```

DODGE is the source of truth for scene composition and resolved component inventory. It is not necessarily the source of truth for every game fact. Canonical catalogs and rules may remain external and be referenced by stable identity.

Generated target artifacts MUST NOT become independent definitions of the game.

## 2. Design principles

1. **Neutrality.** DODGE describes game meaning and component identity, not PDF coordinates, TTS GUIDs, atlas slots, hosted URLs, or engine-specific transforms.
2. **Single composition source.** All exporters for a build MUST consume the same DODGE document and resolve the same ordered objects and quantities.
3. **Reference rather than duplication.** Canonical facts SHOULD remain in canonical sources. DODGE references them.
4. **Traceability.** Sources MAY be versioned and SHA-256 pinned. Production pipelines SHOULD verify every supplied hash.
5. **Lossless evolution.** Design information that DODGE cannot express MAY remain in a declared adjacent sidecar. A tool MUST NOT silently discard or invent such information.
6. **Target ownership.** Each target owns its deployment and presentation details.
7. **Explicit uncertainty.** Provisional interpretations and authoritative facts SHOULD be distinguishable through source authority and metadata.

## 3. Conformance language

The key words **MUST**, **MUST NOT**, **SHOULD**, **SHOULD NOT**, and **MAY** are normative.

A conforming 0.2.0 document:

- validates against `schemas/dodge.schema.v0.2.0.json`;
- uses `dodge_version` equal to `0.2.0`;
- resolves all local references;
- resolves every referenced source required by an exported scene;
- produces deterministic collection order and quantities;
- contains no target-owned fields.

Schema validity alone is insufficient. The semantic validation rules in this specification are also normative.

## 4. Document model

A DODGE document contains:

| Field | Meaning |
|---|---|
| `dodge_version` | Format version; exactly `0.2.0` |
| `document_id` | Stable identifier for this document |
| `game_id` | Stable identifier for the game or product |
| `title`, `description` | Human-readable identification |
| `sources` | External canonical data, rules, selections, assets, or sidecars |
| `sidecars` | Declared adjacent sources preserved outside the normalized core |
| `archetypes` | Reusable neutral object shapes and capabilities |
| `objects` | Reusable tokens, collections, or randomizers |
| `scenes` | Named sets of object instances |
| `metadata` | Non-normative project information |
| `extensions` | Namespaced experimental information |

Dictionary keys are local identifiers. They are referenced by those keys inside the same document.

## 5. Identifiers and references

Local identifiers MUST match:

```text
^[a-z0-9][a-z0-9._:-]*$
```

The following reference forms are used:

- `archetype_ref`, `object_ref`, `source_ref`, and scene relationship targets refer to local dictionary keys.
- `entity_ref` refers to an entity in an external source, conventionally as `<source-key>:<entity-id>`.
- `content_ref` refers to a source or source fragment understood by the resolver.
- Source `uri` values MAY include URI fragments such as JSON Pointers.

Resolvers MUST reject unresolved references needed by the selected scene.

## 6. Sources and authority

Each source declares:

- `kind`: its broad role;
- `uri`: its location, relative to a resolver-defined root unless absolute;
- `version`: its source version;
- optional `sha256`: the lowercase hexadecimal digest of the retrieved bytes;
- optional `media_type`;
- optional `authority`.

Known source kinds are:

- `entity_catalog`
- `selection_manifest`
- `rules`
- `text`
- `asset_catalog`
- `scenario`
- `sidecar`

Authority values are:

- `authoritative`: governing source information;
- `derived`: reproducibly produced from authoritative inputs;
- `provisional`: an explicit prototype interpretation or assumption;
- `reference`: informative material that does not govern resolution.

If `sha256` is present, a resolver MUST verify it before using the source. A mismatch is fatal.

## 7. Adjacent sidecars

`sidecars` formally declares lossless or experimental information that remains outside the normalized DODGE core. Each declaration references one entry in `sources` and states its purpose.

A sidecar declaration does not make every sidecar field part of DODGE. Exporters MUST NOT silently treat sidecar fields as normalized DODGE semantics. Promotion requires a later specification or a declared namespaced extension understood by the consumer.

This mechanism preserves the Wretched Demesne GDD-sidecar boundary without prematurely standardizing turn rules, AI, progression, topology, or campaign semantics in 0.2.0.

## 8. Archetypes

An archetype describes reusable neutral shape and capabilities. Its `kind` is one of:

- `token`: one discrete object with one or more faces;
- `collection`: an ordered or unordered group of members;
- `randomizer`: an object advertising outcome selection. General randomizer semantics remain experimental in 0.2.0.

An archetype MAY declare face slots, a component profile, tags, and a description.

Objects MUST have the same `kind` as their referenced archetype.

## 9. Neutral component profile

The optional `component` profile describes physical identity shared by exporters. It does not describe target layout.

It may contain:

- `form`: `card`, `token`, `tile`, `board`, `reference_sheet`, `tracker`, `die`, `standee`, or `custom`;
- `size_class`: a project-defined semantic name such as `standard-card` or `small-token`;
- `shape`: `rectangle`, `circle`, `hex`, `custom`, or `none`;
- `dimensions`: physical width, height, diameter, and/or thickness with a unit;
- `two_sided`: whether front/back distinction is physically meaningful;
- `shared_back_ref`: a neutral content reference for components sharing one back;
- `tags`.

Allowed dimension units are `mm`, `cm`, `in`, and `pt`.

An object MAY override its archetype's component profile. Resolution performs a shallow field merge with object fields taking precedence. Exporters MUST use the resolved profile when determining component inventory and physical form.

Page placement, cut marks, printer margins, pixels, atlas coordinates, and virtual-table transforms are not component-profile fields.

## 10. Faces and semantic regions

Archetypes declare face slots such as `front`, `back`, `side`, `outcome`, or `reference`. Objects populate those slots with faces.

A face contains either direct `text`, a `content_ref`, or named `regions`. A region describes semantic content such as `title`, `art`, `rules`, `stats`, `connections`, or `icon`. Regions do not contain coordinates in DODGE 0.2.0.

The same resolved face content can therefore drive vector PnP output and rasterized TTS assets without placing PDF or atlas geometry in DODGE.

## 11. Objects

Every object declares:

- `kind`;
- `archetype_ref`;
- optional `name` and `description`;
- optional `source_ref`;
- optional `component` override;
- optional `faces`, `members`, `behaviors`, and `relationships`.

Kind-specific rules:

- A `token` SHOULD contain faces and MUST NOT contain members.
- A `collection` MAY contain members and behaviors.
- A `randomizer` MAY contain members or outcome faces, but consumers MUST declare support before exporting it.

## 12. Collection members and quantities

A collection member refers to exactly one of:

- an external canonical entity through `entity_ref`, normally accompanied by `archetype_ref`; or
- another local object through `object_ref`.

`quantity` defaults to `1` and MUST be a positive integer.

Array order is normative. `ordering` defaults to `declared`. A collection explicitly marked `unordered` allows a consumer to choose an order only when no behavior or target requires stable order.

Collections MAY be nested through `object_ref`. Cycles are invalid.

## 13. Behaviors

Core advertised behaviors are:

- `shuffle`
- `draw`
- `return`
- `select_uniform`

A behavior advertises capability; it is not a complete game-rules language. `replacement`, `destination`, and namespaced parameters refine it.

For `draw`, omitted `replacement` means `false`. A destination is a semantic identifier, not a target container ID.

## 14. Relationships

Objects and instances MAY declare typed relationships. A relationship has:

- `type`: a semantic relationship name;
- exactly one of `target_object_ref` or `target_instance_ref`;
- optional `role` and `properties`.

Relationships cover neutral facts such as a marker tracking another object, a token belonging to a supply, or a component referencing a track. Target-specific attachment mechanisms remain outside DODGE.

## 15. Scenes and instances

A scene is a named set of instances. Each instance declares:

- a scene-unique `id`;
- an `object_ref`;
- optional `quantity`, defaulting to `1`;
- optional initial `state`;
- optional `location_ref` for a semantic game location;
- optional relationships.

Instance state is initial scene state, not a normalized rules engine. Consumers MAY preserve unknown state keys but MUST NOT infer unspecified rules from them.

## 16. Resolved component inventory

For each scene, a conforming resolver constructs one deterministic component inventory:

1. Visit instances in declared order.
2. Resolve each `object_ref` and its archetype.
3. Multiply by the instance `quantity`.
4. For a collection, visit members in declared order.
5. Multiply member quantity by every containing quantity.
6. Resolve `entity_ref` members through their named source and archetype.
7. Resolve `object_ref` members recursively.
8. Reject cycles, missing references, non-positive quantities, or unsupported kinds.
9. Preserve stable identity, declared order, resolved component profile, faces, and source provenance for every inventory entry.

All exporters for the same build MUST consume this same resolved inventory. They MUST NOT independently choose component membership or quantity.

## 17. Target contracts

A target contract declares:

- supported DODGE versions and object/component kinds;
- neutral-to-target mappings;
- target-owned additions;
- output artifacts;
- fields forbidden from DODGE;
- limitations.

Contracts describe capabilities and boundaries, not target configuration.

Examples of target-owned information:

| PnP | TTS |
|---|---|
| page size and coordinates | GUIDs and transforms |
| typography and cut guides | atlas indices and hosted URLs |
| printer settings | table, sky, and save-specific IDs |

Both targets SHOULD emit build manifests containing DODGE version, document identity and hash, verified source hashes, scene ID, ordered resolved inventory identities and quantities, target version, and source-control revision. A parity verifier SHOULD fail when shared identity differs.

## 18. Extensions

`extensions` is an object whose keys MUST be namespaced identifiers, preferably reverse-domain names. Extension values are unrestricted JSON.

Extensions MUST NOT redefine core fields. A consumer that requires an extension for correctness MUST declare that requirement and MUST fail clearly when it is unsupported.

The extension mechanism is for experimentation, not for silently bypassing versioning.

## 19. Semantic validation

In addition to JSON Schema validation, a validator MUST check:

1. all local references resolve;
2. object and archetype kinds match;
3. face slots exist on the archetype and are not duplicated;
4. each member has exactly one referent;
5. each relationship has exactly one target;
6. scene instance IDs are unique;
7. collection nesting is acyclic;
8. supplied source hashes match;
9. entity references resolve when their source is available;
10. any declared selection manifest has exact ordered parity with its collection;
11. component dimensions are physically coherent;
12. the selected target contract supports every resolved kind and required extension.

## 20. Compatibility with the prototypes

### Digitropolis

0.2.0 preserves:

- hash-pinned catalogs, rules, and selection manifests;
- canonical entity references rather than copied card facts;
- ordered deck membership;
- shuffle and draw-without-replacement behaviors;
- shared resolution for PnP and TTS;
- target contracts and cross-target identity manifests.

### Wretched Demesne

0.2.0 preserves:

- tokens, reference material, decks, quantities, supplies, and initial state;
- the authoritative GDD / sidecar / provisional implementation distinction;
- lossless adjacent sidecars;
- neutral board-token and card component identities;
- a deterministic component inventory usable by PnP and TTS;
- relationships needed to associate markers, supplies, and stateful components.

0.2.0 intentionally does not normalize the broader Wretched sidecar's turn structure, resources, enemy AI, progression, map topology, campaign state, or scenario logic. Those are candidates for 0.2.1.

## 21. Migration from 0.1.0

A conforming 0.1.0 Digitropolis or Wretched document can migrate by:

1. changing `dodge_version` to `0.2.0`;
2. adding source `authority` values where known;
3. declaring adjacent sidecars through `sidecars` where applicable;
4. adding optional component profiles to archetypes or objects;
5. retaining existing sources, archetypes, objects, members, behaviors, scenes, state, and metadata.

No existing 0.1.0 core concept is removed. The 0.2.0 schema is therefore a structural superset after the required version-field update.

## 22. Explicit deferrals

The following are outside the normalized 0.2.0 core:

- full turn/action/rules semantics;
- resources and costs;
- enemy AI and activation logic;
- procedural map topology and room-connection rules;
- campaign progression and persistence;
- scenario objectives and triggers;
- generalized probability distributions and die presentation;
- target presentation coordinates and styling;
- a shared semantic icon/style vocabulary.

These deferrals prevent the first official common specification from inventing semantics not yet proven across implementations.
