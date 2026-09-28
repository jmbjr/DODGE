# DODGE v0.1

DODGE means **Declarative Object Description for Game Engines**. It is a small,
target-neutral manifest describing which game objects exist in a scene, how they
are grouped, and which basic interactions they advertise.

DODGE does not replace canonical game data. A Digitropolis card's name, stats,
rarity, and researched rules remain in `data/cards/`. A DODGE member references
that identity as `cards:base-205` rather than copying its facts.

## v0.1 concepts

| Concept | Meaning |
|---|---|
| Source | Versioned external canonical data, selection, rules, or text |
| Archetype | Shape of an object, such as a two-faced token or collection |
| Object | Reusable neutral definition such as the starter deck or rules token |
| Member | Reference from a collection to a canonical entity and archetype |
| Behavior | Advertised operation such as shuffle or draw without replacement |
| Scene | Set of named object instances, without target layout |

The first document contains a 60-card deck collection and a rules-reference
token. Each deck member points to the canonical card catalog. Its order exactly
matches `starter-original-01.json`.

## Export boundary

```text
canonical catalogs + selections + rules
                    |
                 DODGE scene
                  /       \
       PnP contract         TTS contract
            |                    |
       PDF geometry       atlas, GUIDs, URLs,
       and cut marks      transforms, save JSON
```

The contracts are capabilities and mapping declarations, not implementation
configuration. They say what an exporter accepts, how neutral concepts map to
target concepts, what the target must add, and which target fields are forbidden
from DODGE.

## Why a die is deferred

DODGE v0.1 deliberately avoids deciding whether a die is fundamentally a
six-sided token or a collection of six outcomes. A later randomizer model should
separate outcome selection from presentation, allowing the same uniform,
replacement-based mechanic to appear as either a die or a shuffled outcome deck.

## Rebuild and validate

```bash
python -m pip install -r tools/dodge/requirements.txt
python tools/dodge/build_digitropolis.py \
  --dataset data/cards/base-set.v0.2.json \
  --selection data/decks/starters/starter-original-01.json \
  --rules docs/research/rules-and-dataset.v0.1.md \
  --output data/scenes/digitropolis-starter-original-01.dodge.v0.1.json

python tools/dodge/validate.py \
  data/scenes/digitropolis-starter-original-01.dodge.v0.1.json \
  --contract targets/print-and-play/dodge-contract.v0.1.json \
  --contract targets/tabletop-simulator/dodge-contract.v0.1.json
```

The validator checks both JSON Schemas, source hashes, canonical card
references, uniqueness, and ordered parity with a source selection manifest
when present. Both PnP and TTS then resolve this validated document through the
same runtime module; exporters do not independently choose datasets or cards.
