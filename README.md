# Per-edge channel attribution in the C. elegans head connectome: data layer

This repository builds a frozen, provenance-tracked table with one row per
ordered head-neuron pair (pre, post). The table lines up three kinds of data
for each pair:

- the signal propagation measured by Randi et al. 2023 (WT and unc-31);
- the anatomical connectome;
- predicted synapse polarity, the neuropeptide and monoamine connectomes, and
  single-neuron expression.

Classifying pairs into channels (categories A–E) is a later, separate pass and
is deliberately **not** done here.

## Status

| Phase | State |
|---|---|
| 0. Prior work | Verdict PROCEED, approved: `docs/phase0-prior-work.md` |
| 1. Acquisition | In progress: `docs/provenance/` |
| 2. Canonical namespace | not started |
| 3. Reproduction tests | not started |
| 4. Merged edge table | not started |

## Layout

```
data/raw/        downloaded bytes, never modified; pinned by SHA-256 (not committed; see MANIFEST.json per source)
data/interim/    per-source normalized tables
data/processed/  the frozen merged artifact
src/acquire/     one module per source; python -m src.acquire
src/namespace/   canonical neuron naming
src/merge/       table construction
tests/           integrity and reproduction tests
docs/            decisions.md, provenance/, phase reports
logs/
```

## Reproduce

```
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/python -m src.acquire            # download and verify every source
.venv/bin/python -m src.acquire --verify   # re-hash raw files offline
.venv/bin/python -m src.acquire --counts   # record counts per source
.venv/bin/python -m pytest
```

Every source is currently acquired from a **secondary** distribution, because
the primary hosts are blocked in the build environment. The primary comparison
is pending; see `docs/provenance/README.md`.
