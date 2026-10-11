# DODGE 0.2.1 Implementation Guide

**Status:** Adoption guidance for the DODGE 0.2.1 working draft  
**Audience:** Game implementers, tool authors, reviewers, and integration teams  
**Normative source:** `DODGE_SPEC.md` and the 0.2.1 JSON Schemas remain authoritative

This guide answers one practical question:

> Given a game design and DODGE 0.2.1, what sequence should an implementer follow to produce a conforming, executable, testable implementation without letting runtime or target code become a second source of game truth?

It exists because schema examples and a normative format specification are necessary but not sufficient onboarding material. A conforming implementation is a **toolchain**, not merely a JSON file.

The recommended implementation path is:

```text
authoritative source / GDD / rules
        |
        v
canonical game + scenario data
        |
        v
DODGE 0.2.1 document
        |
        v
core validation
        |
        v
game/application semantic validation
        |
        v
target-neutral resolution
        |
        v
resolved-game validation
        |
        v
shared runtime / execution evidence
        |
        v
target adapters
```

Target generation MUST remain downstream of the validation and resolution gates required by section 15 of the specification.

---

## 1. What this guide is, and is not

This guide:

- gives a portable adoption sequence for a new game;
- makes the validation lifecycle operational for implementers;
- distinguishes source authority from normalized DODGE semantics;
- gives a concrete workflow for sidecars, extensions, and candidate specification gaps;
- defines non-normative implementation maturity labels so teams can describe progress precisely;
- describes the evidence expected before a prototype concept should be proposed upstream.

This guide does **not**:

- add new DODGE 0.2.1 schema fields;
- change the normative conformance rules in `DODGE_SPEC.md`;
- require every game to use the same runtime, programming language, directory layout, or targets;
- make every prose rule executable;
- require Web, PnP, TTS, or any other particular target.

When this guide and the specification differ, the specification and schemas win.

---

## 2. Non-normative implementation maturity gates

These labels are implementation guidance only. They are **not DODGE document fields** and are not added to the 0.2.1 schema.

They are useful for reviews because words such as "prototype" or "working" can hide whether validation, resolution, and runtime execution actually exist.

| Gate | Meaning |
|---|---|
| **G0 - Scaffold** | Source layout, authority notes, compatibility audit, and initial DODGE work exist. No conformance claim yet. |
| **G1 - Schema-valid** | The candidate document validates against the exact DODGE 0.2.1 schema. |
| **G2 - Core-valid** | The implementation passes the complete generic DODGE core checks required by section 15.3, not only JSON Schema. |
| **G3 - Semantic-valid** | Every required game/application semantic profile passes at its declared source stage. |
| **G4 - Resolved** | One target-neutral resolver produces a resolved model and all required resolved-game validation passes. |
| **G5 - Executable** | At least one bounded mechanic executes from the resolved model with deterministic or inspectable evidence. |
| **G6 - Targeted** | At least one target consumes the same resolved/runtime semantics without owning game rules. |
| **G7 - Reference** | The implementation has enough validation, perturbation, runtime, replay/evidence, and target experience to serve as a conformance reference. |

A project SHOULD state which gate it has actually reached.

A green repository workflow is not evidence of G1-G7 unless that workflow executed the relevant checks against the candidate game.

---

## 3. Step 0 - Select the exact DODGE version

Before modeling the game:

1. choose the exact DODGE version;
2. read that version's specification;
3. use that version's schemas;
4. record the selected version in the document;
5. do not mix fields inferred from another draft or later branch.

For this guide the selected version is exactly `0.2.1`.

A version string in JSON is not proof of conformance. The candidate must be validated against the corresponding schema and lifecycle.

---

## 4. Step 1 - Establish source authority before normalization

Start by identifying what is authoritative.

Possible inputs include:

- a GDD;
- a rules PDF;
- canonical catalogs;
- spreadsheets;
- issue decisions;
- prototype data;
- generated selections;
- previously normalized sources.

For each input, record whether it is:

- **authoritative**;
- **derived**;
- **provisional**;
- **reference**.

Do not silently reconcile contradictions between sources.

When important semantics cannot yet be normalized into DODGE, preserve them in a declared source or adjacent sidecar rather than dropping them.

### 4.1 External rules references

A DODGE source may identify an external rules document without reproducing its prose.

For implementations that need rule explanations, teaching mode, or resolution traces, projects SHOULD maintain stable source locators such as:

```text
external source ID/version
        +
page / section / rule locator
        +
local semantic rule ID
        +
runtime procedure/action ID
```

The exact locator representation is project-owned unless standardized by DODGE. A locator must not be confused with normalized executable semantics.

---

## 5. Step 2 - Perform a bounded compatibility audit

Before substantial implementation, classify every mechanic or requirement that the intended scenario needs.

Use at least these categories:

1. **Expressible in DODGE 0.2.1**  
   Model it using existing DODGE semantics.

2. **Canonical game/scenario fact**  
   Keep it in an authoritative or provisional canonical source and reference/resolve it through DODGE.

3. **Not cleanly expressible in DODGE 0.2.1**  
   Preserve it in a declared sidecar or namespaced extension as permitted by the specification. Record it as a candidate gap. Do not hide it in a target.

4. **Legitimate runtime algorithm**  
   Keep the algorithm in implementation code, but drive it from neutral semantic inputs. Algorithms must not invent game facts.

5. **Target presentation/deployment detail**  
   Keep it in the target contract, renderer, exporter, packaging, or deployment layer.

The output SHOULD be a finite checklist tied to the first executable scenario.

Do not begin by designing every feature a full ruleset might eventually need. Model the smallest scenario that can prove the architecture.

---

## 6. Step 3 - Define a bounded executable scenario

A first scenario SHOULD be intentionally small but mechanically meaningful.

Define at minimum:

- setup and selected scene;
- actors and player-count scope;
- mutable state/resources used by the scenario;
- available actions;
- procedure/phase ordering;
- objects or collections used by play;
- objective and end conditions;
- every mechanic the scenario claims to exercise.

Prose is allowed where the source is not yet executable, but an implementation MUST NOT claim that a prose-only condition/procedure is executable.

### 6.1 Maintain an executable-claims matrix

During implementation, maintain a project-owned matrix such as:

| Claimed mechanic | Canonical source | DODGE binding | Runtime implementation | Test/evidence |
|---|---|---|---|---|
| ordinary skill check | scenario/rules | action/procedure | yes/no | yes/no |
| interaction | scenario | invocation/action | yes/no | yes/no |
| attack | rules | action/procedure | yes/no | yes/no |
| defensive reaction | rules/proto | procedure/extension | yes/no | yes/no |
| injury/state change | rules | effect/procedure | yes/no | yes/no |

This matrix is not a DODGE file format. It is an implementation audit tool.

Its purpose is to distinguish:

> "the scenario describes this mechanic"

from:

> "the resolved runtime actually executes this mechanic."

---

## 7. Step 4 - Create one canonical authority path for each fact

Prefer derivation and references over duplicated authored facts.

Bad:

```text
canonical scenario: DX = 11
DODGE scene state:  DX = 11
runtime default:    DX = 11
```

The values agree today but there are three authorities.

Better:

```text
canonical scenario: DX = 11
        |
        v
DODGE references/selects the canonical actor
        |
        v
resolver
        |
        v
runtime sees DX = 11
```

If duplication is unavoidable, the owning semantic validator MUST enforce the relationship.

A mature implementation SHOULD contain perturbation tests proving the authority path. For example:

1. change canonical DX from 11 to 12 in a test fixture;
2. resolve again;
3. assert the resolved/runtime value is 12;
4. fail if a historical literal still produces 11.

This is stronger evidence than a snapshot test that today's duplicated values happen to match.

---

## 8. Step 5 - Build the DODGE document and pass schema validation

Create the smallest DODGE document that correctly describes the selected scope.

The first hard gate is:

> The candidate document validates against `schemas/dodge.schema.v0.2.1.json`.

Do not rely on:

- a repository-wide green workflow that validates some other game;
- a similar document from another DODGE revision;
- visual inspection;
- a renderer successfully loading the JSON.

Schema validation is necessary but is only G1.

The schema defines exact required fields and allowed vocabulary. For example, 0.2.1 value definitions require the fields declared by the 0.2.1 schema; an implementation must not infer field shapes from memory or another draft.

---

## 9. Step 6 - Run full DODGE core validation

After JSON Schema passes, execute the generic semantic checks required by `DODGE_SPEC.md` section 15.3.

Core validation includes more than syntax. It covers generic concerns such as:

- required references;
- object/archetype consistency;
- collection/procedure cycles;
- source hashes;
- uniqueness;
- rule-reference kinds;
- defaults and bounds;
- topology reference integrity;
- deterministic phase/end-condition structure;
- invocation binding correctness;
- representation and target-contract constraints when used.

A project reaches G2 only when the candidate itself has passed these checks.

If the DODGE repository does not provide a single ready-made validator for a required core rule, the implementation still owns satisfying the normative rule. Missing tooling does not waive conformance.

---

## 10. Step 7 - Declare and implement game/application semantic validation

DODGE cannot know the meaning of every game-specific declaration.

If the implementation has domain contracts that are not derivable or enforceable by DODGE core, it MUST provide the semantic validation needed to enforce them as required by specification section 15.

Typical examples:

- "searchable" implies executable Search behavior;
- an encounter marked as a combat tutorial must actually bind to the required combat procedure;
- a domain capability implies a corresponding invocation;
- two independently authored domain fields must agree;
- a scenario requires a complete set of domain entities.

### 10.1 Validation declaration pattern

The 0.2.1 schema supports a semantic-validator source and required validation profiles.

Illustrative shape:

```json
{
  "sources": {
    "my-game-validator": {
      "kind": "semantic_validator",
      "uri": "tools/validate_my_game.py",
      "version": "0.1.0",
      "authority": "authoritative"
    }
  },
  "validation": {
    "core_profile": {
      "profile_id": "dodge-core",
      "version": "0.2.1"
    },
    "required_profiles": [
      {
        "profile_id": "my-game",
        "version": "0.1.0",
        "kind": "game",
        "stages": [
          "source",
          "resolved-game"
        ],
        "validator_source_ref": "my-game-validator"
      }
    ]
  }
}
```

Use the exact 0.2.1 schema when constructing the declaration.

If a profile is declared, missing, unavailable, version-mismatched, or failing validation is a hard failure.

Target generation must not continue.

---

## 11. Step 8 - Resolve once into a target-neutral model

After source/core/domain validation passes, resolve the selected game scope exactly once.

A resolver SHOULD:

1. start from the DODGE document;
2. follow declared source references;
3. preserve source authority/provenance;
4. resolve the selected scenario/scene;
5. resolve required collections, components, rules, and bindings;
6. expose unresolved semantics explicitly instead of inventing defaults;
7. produce one neutral model consumed by runtime and targets.

Web, PnP, TTS, simulations, and other targets MUST NOT each reconstruct the game independently.

The resolver is allowed to implement deterministic algorithms. It is not allowed to become another authored game definition.

---

## 12. Step 9 - Validate the exact resolved model

Resolved-game validation is a separate gate.

Per section 15.4, it must verify that resolution did not:

- drop required semantics;
- duplicate semantics;
- weaken executable requirements;
- invent semantics;
- leave required bindings ambiguous;
- omit selected scenario/scene content.

Every required profile that declares the `resolved-game` stage must run against the exact model supplied downstream.

A project reaches G4 only after this passes.

---

## 13. Step 10 - Implement one executable vertical mechanic

Do not wait until the entire game is normalized.

Choose the thinnest meaningful mechanic that crosses the intended architecture:

```text
canonical fact
    ->
DODGE binding
    ->
resolved model
    ->
runtime action/procedure
    ->
state/result evidence
```

Examples:

- draw and resolve one card;
- make one skill check;
- perform one attack;
- enter one hazard location;
- buy/equip/use one item.

This step exists to prove that the source/validation/resolution model is executable, not merely descriptive.

A project reaches G5 only when at least one declared mechanic actually executes from the resolved model.

---

## 14. Step 11 - Add deterministic, negative, and perturbation evidence

A robust implementation SHOULD use all three test classes.

### Deterministic evidence

Given the same declared inputs and random evidence/seed, reproduce the same result and state transition.

If randomness matters to the scenario, preserve enough evidence to reproduce or inspect it. The exact replay format is project-owned unless DODGE standardizes it.

### Negative evidence

Remove or corrupt a required semantic fact and prove validation fails before runtime/target generation.

Examples:

- missing invocation;
- missing rule ref;
- invalid canonical entity;
- unresolved required domain capability.

### Perturbation evidence

Change one authoritative input and prove the resolved/runtime result follows it.

This catches copied constants and shadow authorities.

A mature reference implementation should not rely only on expected-value snapshots.

---

## 15. Step 12 - Add the first target only after the neutral boundary works

A target adapter owns presentation, interaction adaptation, serialization, packaging, and deployment details.

It does not own:

- canonical rule values;
- collection membership;
- scenario objectives;
- domain completeness fixes;
- target-specific fallback rules.

The first target may be intentionally small. It does not need to be Web, PnP, or TTS.

For a new rules-heavy implementation, a debug UI or command-line harness can be the best first consumer because it exposes the resolved semantics and execution trace directly.

A project reaches G6 when at least one target consumes the same resolved/runtime semantics.

---

## 16. Step 13 - Target contracts and manifests

When a target uses the DODGE export-contract/manifest model:

1. validate the target contract against the exact 0.2.1 export-contract schema;
2. resolve target contents from the same neutral model;
3. emit a deterministic resolved target manifest;
4. validate that manifest against `dodge-target-manifest.schema.v0.2.1.json`;
5. preserve validation evidence required by the manifest schema.

A 0.2.1 resolved target manifest requires `validation_evidence` for:

- core validation;
- required profiles;
- resolved-game validation.

Only passing evidence can appear in a release manifest because failures stop the pipeline.

A target artifact SHOULD be verifiable against its resolved manifest where practical.

---

## 17. Step 14 - Treat candidate DODGE gaps as hypotheses first

A compatibility audit may identify many likely format gaps.

Do not promote them all immediately.

Use three project-level states:

```text
suspected
    ->
exercised
    ->
candidate
```

### Suspected

The source/rules suggest DODGE may need a new neutral concept.

### Exercised

The bounded scenario actually requires the concept and the implementation has reached the point where the missing contract blocks or distorts the neutral model.

### Candidate

A target-neutral representation has been implemented, exercised through resolver/runtime behavior, and supported by deterministic/negative/perturbation evidence. Its vocabulary is plausibly reusable beyond the originating game.

Only candidate-level concepts SHOULD become upstream DODGE specification proposals.

This prevents speculative ruleset inventories from turning into premature core vocabulary.

---

## 18. Namespaced extensions and sidecars are bridges, not hiding places

DODGE 0.2.1 permits sidecars and namespaced extensions.

Use them deliberately.

A sidecar or extension MAY:

- preserve unsupported source semantics;
- prototype a candidate neutral contract;
- carry implementation metadata allowed by the schema.

It MUST NOT become an excuse to:

- bypass core validation;
- avoid defining the owning semantic profile;
- hide target-specific game logic;
- duplicate authoritative facts without validation;
- claim unsupported prose is executable.

If an extension becomes executable authority, its shape and implications SHOULD be validated by the owning semantic profile.

---

## 19. CI/release requirements

For a multi-game repository, CI SHOULD discover and validate the candidate game itself.

A green workflow that only checks an existing reference game proves nothing about a newly added game.

A conforming release pipeline for a selected game/scenario should make these results explicit:

```text
candidate game / scenario
  schema validation           PASS
  DODGE core validation       PASS
  required source profiles    PASS
  resolver                    PASS
  required resolved profiles  PASS
  target contract/manifest    PASS (when used)
  runtime/acceptance tests    PASS (project-defined)
```

If a stage is not implemented yet, report that state explicitly instead of allowing an unrelated green check to imply maturity.

The normative DODGE requirement remains: target generation must stop when an applicable required validation stage fails.

---

## 20. Review checklist for a new implementation

Before calling a new game implementation DODGE-conforming or release-ready, ask:

### Source and authority

- [ ] Exact DODGE version selected.
- [ ] Authoritative/provisional/reference sources identified.
- [ ] Unsupported source semantics preserved rather than discarded.
- [ ] No important executable fact has multiple unguarded authorities.

### Core document

- [ ] Candidate validates against the exact DODGE schema.
- [ ] Generic core semantic checks pass.
- [ ] References resolve.
- [ ] Prose-only semantics are not claimed as executable.

### Game semantic validation

- [ ] Domain-specific contracts are identified.
- [ ] Required semantic profiles are declared where needed.
- [ ] Source-stage semantic validation passes.
- [ ] Negative fixtures prove contradictions are rejected.

### Resolution

- [ ] One target-neutral resolver exists.
- [ ] Resolver preserves authority/provenance.
- [ ] Missing required semantics fail rather than silently default.
- [ ] Resolved-game validation passes on the exact downstream model.

### Execution evidence

- [ ] At least one bounded mechanic executes from resolved semantics.
- [ ] Deterministic/random evidence is inspectable where relevant.
- [ ] Perturbation tests prove canonical authority.
- [ ] Scenario claims are matched by executable bindings/tests.

### Targets

- [ ] At least one target consumes the resolved/runtime model.
- [ ] Target code does not redefine game semantics.
- [ ] Target contracts/manifests validate when used.
- [ ] Release manifests contain required validation evidence.

### Upstream gaps

- [ ] Suspected gaps are separated from exercised gaps.
- [ ] Only exercised, generic, evidence-backed concepts are proposed upstream.

---

## 21. Common failure modes

### "The JSON loads, therefore it is DODGE-compliant"

False. Loading JSON is below G1.

### "The schema passes, therefore the game is valid"

False. Schema validity does not prove generic core semantic validity, domain completeness, or resolved-game correctness.

### "CI is green"

Ask: **what exact candidate did it validate?**

A workflow validating another game is not evidence for this one.

### "The scenario says combat is supported"

Check the executable-claims matrix. A prose procedure is not executable combat.

### "The renderer knows how to do it"

If the renderer is the only place that knows the rule, the architecture is wrong.

### "The canonical file and DODGE both contain the same number"

That may be duplicated authority. Perturb the canonical value and prove the resolved/runtime result follows it.

### "This ruleset probably needs eleven new DODGE features"

Record suspected gaps, then implement the smallest scenario. Promote only what the scenario actually exercises.

---

## 22. Reference material in this draft

Use these examples for different parts of the lifecycle:

### Small complete component implementation

`examples/standard-52-card-deck/`

Shows canonical source, DODGE composition, validation, target-neutral resolution, and target contracts without game-specific rules complexity.

### Semantic validation lifecycle

`examples/validation-lifecycle/`

Shows a DODGE-core-valid document that is intentionally rejected by a game-owned semantic profile before resolution/target generation.

### Invocation and executable bindings

`examples/playable-object-bindings.dodge.json`

Shows the neutral bridge from playable objects to actions/procedures/effects.

### Requirements, equipment, and location semantics

`examples/requirements-equipment-locations.dodge.json`

Shows structured requirements/modifiers/equipment/location behavior that should not be replaced by game-specific runtime flags.

### Target contracts and manifests

`examples/export-contracts/` and `examples/target-manifests/`

Show target-boundary selection and resolved target-manifest concepts.

---

## 23. Recommended adoption sequence in one page

```text
0. Read the exact DODGE version + schema
1. Identify source authority
2. Preserve unsupported source semantics
3. Perform a bounded compatibility audit
4. Define a small executable scenario
5. Create canonical game/scenario data
6. Create the DODGE document
   GATE: exact schema passes
7. Run full DODGE core validation
   GATE: generic core checks pass
8. Define + run game semantic validation
   GATE: all required source profiles pass
9. Resolve once into a neutral model
10. Run resolved-game validation
    GATE: all required resolved profiles pass
11. Execute one vertical mechanic
    GATE: deterministic/negative/perturbation evidence passes
12. Complete the bounded scenario claims
13. Add one target consuming the resolved/runtime model
14. Add target contract/manifest validation where applicable
15. Run a whole-system convergence audit
16. Propose only exercised, generic gaps upstream
```

The intended result is not merely "valid JSON."

The intended result is a traceable toolchain in which:

> authoritative source becomes normalized DODGE semantics, validation rejects contradictions before runtime, one resolver produces one neutral executable model, and targets remain projections rather than independent game definitions.
