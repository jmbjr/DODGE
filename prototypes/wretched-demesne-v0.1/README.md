# Wretched Demesne — DODGE interpretation used by the prototype

**Status:** historical prototype record, not a proposed replacement for the official DODGE specification  
**DODGE target:** 0.1.0  
**Source implementation:** `jmbjr/TheFountain`  
**Purpose:** preserve exactly how the Wretched Demesne prototype interpreted DODGE before the specification is formalized further.

## What we treated as DODGE

For Wretched Demesne, DODGE was treated as a **target-neutral object/scene manifest** sitting between canonical game/design information and deploy targets.

The working pipeline was:

```text
GDD / canonical game semantics
        |
DODGE scene + GDD sidecar
        |
Scenario 01 executable MVP data
        |
shared runtime / resolver
   /         |          \
Web       PnP PDF      TTS
```

The important architectural rule was that Web, PnP, and TTS were not allowed to become independent definitions of the game.

## DODGE v0.1 concepts actually used

The Wretched document used these top-level concepts:

- **sources** — references to external rules/entity catalogs.
- **archetypes** — reusable descriptions of broad object forms.
- **objects** — target-neutral game objects.
- **members** — entities contained by collection objects, with quantities.
- **behaviors** — generic interactions such as shuffle and draw.
- **scenes** — collections of object instances used to establish a playable/setup state.
- **instances** — occurrences of objects in a scene, optionally with state.

The prototype used these archetype kinds:

- `token`
- `collection`

The broader DODGE v0.1 work also contemplated `randomizer`, but Wretched did not require it in this document.

## Archetypes used by Wretched

### standard-card

A two-sided token with `front` and `back` face slots.

### deck

A collection intended to support shuffle and draw-without-replacement behavior.

### reference-token

A readable one-sided/reference object used to expose rules material.

### board-token

A neutral one-sided physical marker. Wretched used this for Spider Corpse and Chrysalis.

## Objects represented

The prototype DODGE scene represented:

1. **Security Starter Deck**
   - collection/deck
   - 2 Sidearm
   - 2 Move
   - 2 Take Cover
   - 2 Reload
   - 1 Suppressive Fire
   - 1 Security Training
   - shuffle behavior
   - draw-without-replacement behavior

2. **Prototype Rules / GDD**
   - reference token
   - points to the adjacent GDD sidecar

3. **Spider Corpse**
   - board token
   - supply object

4. **Chrysalis**
   - board token
   - supply object

The Scenario 01 scene instantiated those four objects.

## What DODGE did *not* represent

This was the most important limitation of the Wretched experiment.

We explicitly treated DODGE 0.1 as **not yet capable of normalizing**:

- game rules and effect semantics
- turn phases and action economy
- resources
- enemy AI
- progression
- map topology
- campaign state
- scenario logic
- design intent
- unresolved design questions

Those concepts were preserved in the adjacent sidecar instead of being discarded or forced into target-specific renderers.

## Sidecar convention

The sidecar was called `dodge-adjacent-gdd-sidecar`.

Its contract was:

> Preserve source design information losslessly when DODGE cannot yet express it. Do not discard, resolve, normalize away, or invent design information merely to make it fit the current schema.

It contains two layers:

- `structured_extensions` — machine-readable concepts that may eventually migrate into formal DODGE.
- `source_transcription` — complete parsed GDD text as a fidelity fallback.

This sidecar is included beside this document as:

`wretched-demesne.gdd.sidecar.v0.1.json`

## Later executable MVP layer

After the lossless import, TheFountain added a separate Scenario 01 MVP dataset containing provisional executable choices needed to make the game playable. This distinction matters:

- **GDD:** design authority.
- **Sidecar:** lossless preservation of GDD semantics DODGE 0.1 could not represent.
- **DODGE:** neutral object/scene representation.
- **Scenario MVP data:** executable prototype interpretation, including explicitly marked assumptions.
- **Renderers/exporters:** presentation/platform adapters only.

The MVP data was not intended to silently redefine DODGE.

## What the PnP experiment exposed

The first Wretched PnP exporter produced a reference-style text PDF rather than a true cuttable game. That exposed a gap in this interpretation of DODGE.

The game semantics were largely available, but DODGE did not adequately specify the **physical component model** needed by multiple targets. In particular, the prototype lacked a formal neutral way to describe:

- component type (card, tile, token, board/reference sheet, tracker)
- physical size/size class
- component quantity/supply requirements
- fronts, backs, and shared backs
- presentation/content regions on a component
- room connection geometry
- token/status relationships
- printable tracks and counters
- component grouping into decks/supplies
- enough resolved component information for PnP and TTS to produce equivalent inventories

This is a finding from the Wretched prototype, **not an assertion that these fields belong in any particular future DODGE schema**.

A useful future architecture to investigate is:

```text
canonical gameplay semantics
          |
   DODGE resolved scene
          |
neutral component inventory
     /              \
PnP presentation   TTS presentation
```

The key requirement is that the PnP and TTS exporters should agree on the same resolved objects and quantities rather than independently deciding what physical components the game contains.

## Files in the original implementation

TheFountain used:

- `game/wretched-demesne.dodge.v0.1.json` — the actual DODGE document.
- `game/wretched-demesne.gdd.sidecar.v0.1.json` — lossless adjacent semantics.
- `game/wretched-demesne.scenario-01.mvp.v0.1.json` — later executable prototype assumptions/data.
- `game/WRETCHED_DODGE_IMPORT.md` — import rationale.

This Markdown file intentionally records the **interpretation and architecture**, while the JSON files are the concrete data.

## Formalization questions raised by Wretched

The prototype suggests several questions for the formal DODGE work:

1. Where is the boundary between game semantics and physical component semantics?
2. Should size/layout be an archetype capability, a presentation contract, or a separate layer?
3. How should one neutral component inventory drive both physical PnP pieces and virtual TTS objects?
4. How should quantities be resolved when they depend on player count or scenario setup?
5. How should tokens, counters, tracks, state markers, and stateful objects relate?
6. How should map/room topology and connection geometry be represented?
7. Which structured sidecar concepts are generic enough to promote into DODGE?
8. How should DODGE distinguish authoritative source facts from provisional prototype assumptions?

Those questions are intentionally left open here for the specification work to resolve.
