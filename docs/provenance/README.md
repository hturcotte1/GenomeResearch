# Provenance records

There is one file per source, `docs/provenance/<source>.md`, matching
`src/acquire/<source>.py`.

## Status of every source: SECONDARY, primary check pending

The primary hosts (journal supplements, author portals, nemanode.org,
cengen.org, wormatlas.org) are blocked by this environment's network policy. On
2026-10-11 the project owner approved acquiring from reachable secondary
distributions, on these conditions (`docs/decisions.md` D-003):

- each file is logged as SECONDARY, with URL, SHA-256 and retrieval date;
- the comparison against the primary copy is recorded as PENDING;
- **pending primary checks block the Phase 4 freeze** until the primary hosts
  are allowlisted and each file is compared.

The reachable secondary distributions are:

| Distribution | Pinned as | Integrity checks performed at acquisition |
|---|---|---|
| PyPI `wormneuroatlas` 0.0.7.3 wheel, by F. Randi (Leifer lab) | file URL + SHA-256 | SHA-256 equals PyPI's published digest (fetched live); each extracted member matches the wheel's own `RECORD` |
| GitHub `openworm/ConnectomeToolbox` | commit `ffe570268b7cffb9329cd009a1bb37d60db2d465` | each file's git blob id matches the blob the commit records for its path |

These checks prove the bytes are exactly what the distributor published. They
do **not** prove the distributor's copy equals the journal or portal copy.
That is the pending primary check.

## Template for a source document

```markdown
# <source id>: <short title>

- Paper: <full citation, DOI>
- Module: `src/acquire/<source>.py`
- Status: SECONDARY — primary comparison PENDING (blocks Phase 4 freeze)
- Retrieval date (UTC): <from data/raw/<source>/MANIFEST.json>

## Primary location (not reachable from this environment)
<URL(s) of the journal supplement / author portal, and what file there corresponds to each acquired file>

## Files acquired
| File | Size (bytes) | SHA-256 | Distributor / URL | Integrity checks passed |
|---|---|---|---|---|

## What each file contains
<sheets / columns / matrix layout, orientation, units, naming quirks noticed>

## Record counts
| Quantity | Definition | Count in acquired file | Paper reports | Where the paper reports it | Match |
|---|---|---|---|---|---|

Match is one of:
- YES;
- NO — BLOCKER;
- NOT COMPARABLE (with the reason);
- UNVERIFIED (the paper text could not be reached; give the closest evidence).

Counts are produced by `python -m src.acquire --counts <source>`.

## Discrepancies, flags and open questions
<anything that looks wrong, every alternative version found, and decisions that belong to the owner>
```

Rules for every entry:

- A paper-reported number appears here only with a citation to where it was
  read. That can be a quoted excerpt with its URL, or a file in the
  distribution that states it.
- A number that could not be found is written as UNVERIFIED, never estimated.
- A count mismatch is a blocker. It is reported, not tolerated or explained
  away.
