# Decisions log

A running record of every judgement call and its reasoning.

- An **engineering** decision may be made and noted here.
- A **biological or threshold** decision stays OPEN until the project owner
  rules on it.

Each entry: ID, date, phase, status (DECIDED / OPEN), decision or question, and
reasoning.

---

## Phase 0

### D-001 (2026-10-11, Phase 0, DECIDED, engineering)
**Use the authors' own code and data release as primary evidence for what Randi
et al. did, because the full text could not be reached.**

Reasoning: the container's egress policy blocks Nature, PMC, arXiv and the
citation indexes. `leiferlab/pumpprobe` holds the command behind every figure,
and `wormneuroatlas` 0.0.7.3 ships the atlas. That atlas reproduces the paper's
23,433 measured pairs and 1,310 at q < 0.05 exactly. This is stated as a
limitation in `docs/phase0-prior-work.md` §0.

### D-002 (2026-10-11, Phase 0, DECIDED, engineering)
**One-off inspection scripts stay in the session scratch directory, not in the
repository.**

Reasoning: Phase 0 is a no-code phase. The inspection was used only to check
facts about the published data, and the counting rule is described in prose
(phase0 §1.2). It will be re-implemented as a proper reproduction test in
Phase 3.

### OPEN questions raised in Phase 0 (owner decision required)

Full context for each is in `docs/phase0-prior-work.md` §5.

| ID | Question |
|---|---|
| Q-001 (F1) | Phase 3 pair-count target: 23,433 (Nature, reproduced) or 23,427 (brief / reportedly an arXiv version)? Are the 168 self-pairs in scope for the edge table? |
| Q-002 (F2) | Encode per-strain evidence as four states (connected q<0.05 / confidently absent q_eq<0.05 / inconclusive / untested) instead of a boolean `randi_tested`? |
| Q-003 (F3) | 617 of 1,151 WT connections have no unc-31 measurement. Confirm the data layer should carry an explicit "DCV-dependence undetermined" state. Its use in the rubric is deferred to the classification pass. |
| Q-004 (F5) | Category D (hop limit, sign composition, gap-junction handling, timing) must be frozen before E is inspected. Who owns that rubric, and when is it frozen? (Not for this repo, but it determines which anatomical path features the table must expose.) |
| Q-005 (F7) | AWC: keep AWCON/AWCOF, map to AWCL/AWCR, or collapse to AWC? |
| Q-006 (F8) | Bilateral policy given that the authors' averaged q-values are statistically invalid: split-only, or collapse with statistics recomputed from trial-level `dFF_all`? |
| Q-007 (F9) | Which "White 1986" version is `anat_chem_white`: White A/L4/whole as used by Randi, or NemaNode jsh/n2u as used by Creamer? |
| Q-008 (F10) | `predicted_sign` source: Fenyves 2020 primary, and whether to add the 2026 refinement, Wang 2024, or a CeNGEN threshold variant as separate columns. |
| Q-009 (F13) | `monoamine_edge` source: Bentley 2016 or the later monoamine connectome file? |
| Q-010 | Data access: approve secondary copies (the PyPI `wormneuroatlas` wheel, the ConnectomeToolbox GitHub repo) with SHA-256 recorded, or allowlist the primary hosts listed in phase0 §5 first? |

---

## Phase 1

### D-003 (2026-10-11, Phase 1, DECIDED by owner)
**Acquire from reachable secondary distributions now; verify against the
primary copies later.**

Answers Q-010. Every file is logged as SECONDARY with URL, SHA-256 and
retrieval date. Each provenance doc marks the primary comparison as PENDING,
and pending primary checks block the Phase 4 freeze until the primary hosts are
allowlisted. Distributions used:

- the PyPI `wormneuroatlas` 0.0.7.3 wheel (by Randi);
- the GitHub `openworm/ConnectomeToolbox` repository at commit
  `ffe570268b7cffb9329cd009a1bb37d60db2d465`.

### D-004 (2026-10-11, Phase 1, DECIDED, engineering)
**`data/raw/` contents are not committed to git; only the per-source
`MANIFEST.json` files are.**

Reasoning: the raw files total tens of MB, and every file is pinned by URL,
size and SHA-256 in `src/acquire/`, so a fresh clone can re-create
`data/raw/` with `python -m src.acquire` and verify it bit-for-bit. The risk
is that a distributor deletes a file. PyPI release files are immutable
(yank-only) and the GitHub URLs are commit-pinned, so the risk is low but not
zero. If the owner prefers, raw files can be committed or moved to LFS later
without changing any pin.

### D-005 (2026-10-11, Phase 1, DECIDED, engineering)
**Archive members are extracted, byte-identical, into
`data/raw/<source>/`; the archive itself is kept untouched in
`data/raw/_distributions/`.**

Every extracted member is checked against both its pin and the wheel's own
`RECORD`. Extraction copies bytes and never transforms them, so "raw is never
modified" holds for the archive and for each member.

### D-006 (2026-10-11, Phase 1, DECIDED, engineering)
**Raw files are made read-only after their hash is verified, and an existing
raw file whose bytes differ from its pin raises an error instead of being
overwritten.**

### D-007 (2026-10-11, Phase 1, DECIDED, engineering)
**Retrieval dates are recorded only in `data/raw/<source>/MANIFEST.json` and
`docs/provenance/`, never in interim or processed data** (Rule 4).

A date is set when bytes first arrive and is carried forward on re-runs. If a
manifest is lost, the date is written as "UNKNOWN" rather than guessed.

### D-008 (2026-10-11, Phase 1, DECIDED, engineering)
**Python dependencies are pinned exactly in `requirements.txt`** (Python
3.13).

### D-009 (2026-10-11, Phase 1, DECIDED, engineering)
**The canonical-neuron-list candidates are acquired as their own "source"
(`canonical_neurons`).**

Phase 2 needs a WormAtlas-standard list, and wormatlas.org is blocked. The
choice of which candidate is authoritative stays with the owner in Phase 2.

### D-010 (2026-10-11, Phase 1, DECIDED, engineering)
**When several reachable copies of the same dataset exist, all genuine
variants are acquired and their byte-level relationships documented; none is
picked as canonical in Phase 1.**

Examples: the White-lineage connectome variants, and the wheel vs toolbox
copies of Bentley 2016. Which variant feeds which Phase 4 column is the
owner's call (Q-007, Q-009).

### D-011 (2026-10-12, Phase 1, DECIDED, engineering)
**A file extracted from a distribution archive carries the archive's download
date as its `retrieved_utc_date`, not the date it was extracted.**

Archive downloads are recorded in `data/raw/_distributions/MANIFEST.json`.

Reasoning: the canonical_neurons build showed that wheel members extracted on
2026-10-12 were stamped 2026-10-12, although the wheel bytes were downloaded
from PyPI on 2026-10-11. Rule 5 asks for the date the bytes were retrieved.

The `_distributions` manifest was seeded once, by hand, with the wheel's date
2026-10-11. That date was taken from `randi2023/MANIFEST.json`: the wheel was
downloaded and those members extracted in the same run. A regression test
covers the rule.

### D-012 (2026-10-12, Phase 1, DECIDED, engineering)
**`connectome_toolbox_file()` percent-encodes repository paths itself and keeps
existing `%XX` escapes**, so raw and pre-encoded paths give the same URL.

Several build agents requested this. The per-module GitHub helpers (NemaNode,
the Fenyves, Ripoll-Sánchez and Witvliet author repositories) are left as
written because they work and are verified; consolidating them into one shared
helper is a later clean-up, not a Phase 1 change.

---

## Provisional resolutions (made by Claude, 2026-10-12)

On 2026-10-12 the owner wrote: "Continue. Keep going until you are fully done.
Don't ask me anything again unless you need permission". The open questions
below were therefore resolved provisionally rather than asked.

Rules applied to every resolution:

- prefer the choice that asserts nothing beyond the data;
- keep the alternatives available as switches in `config/pipeline.json` or as
  separate columns;
- never discard data.

**Every item here is PROVISIONAL and the owner may overturn it.** A switch
change plus `python -m src.build` regenerates everything.

| ID | Question | Provisional resolution | Alternatives kept | Reasoning |
|---|---|---|---|---|
| Q-001 / D-013 | Pair-count target and atlas release | Use the 2023-06-28 atlas release (`randi_release`); the Phase 3 test asserts 23,433 for it and also 23,427 for the 2023-06-14 release (both acquired) | `randi_release: "2023-06-14"` | 2023-06-28 reproduces the Nature article (23,433 / 1,310 / 53) and is the authors' "fix in export script" release. The brief's 23,427 is the preprint figure and is reproduced by the earlier release |
| Q-001b | Self-pairs in the edge table | Excluded (`include_self_pairs: false`); written to the exclusions log with counts | `include_self_pairs: true` | A neuron's response to its own stimulation is not a signalling edge between two neurons, so categories A–E do not apply |
| Q-002 | Evidence encoding | Per-strain five-state column `randi_state_wt/unc31` ∈ {connected, absent_confident, inconclusive, observed_all_trials_discarded, not_observed}; `randi_tested` = WT pair observed at least once (occ1 > 0) | raw q, q_eq, occ1 and n_trials columns are all carried | Keeps "tested, no response" apart from "never tested", and also separates confident absence from inconclusive |
| Q-003 | No unc-31 data for a pair | `randi_state_unc31 = not_observed` and `unc31_delta` null; nothing is imputed | — | Rule 2 |
| Q-004 | Category D rubric | Out of scope for this repository. The table exposes the inputs a rubric needs (pre/post classes; per-dataset anatomical weights; predicted sign; WT kernel peak and rise times), but computes no paths and no categories | — | The brief: "Do NOT classify anything into categories A–E" |
| Q-005 | AWC | `awc_policy: "unresolved"`: AWCON/AWCOFF rows get no anatomical, polarity or extrasynaptic values, and are flagged | `"authors_convention"` (OFF=AWCL, ON=AWCR) | The per-animal L/R ↔ ON/OFF correspondence is random, so any fixed mapping asserts something false for about half of the animals |
| Q-006 | Bilateral policy | `bilateral_policy: "split"`, with `pre_class` / `post_class` columns provided | `collapse` is documented but not implemented (see namespace-decisions §4) | Collapsing invalidates the measured statistics, and the null distributions needed to recompute them are not released |
| Q-007 | Which "White 1986" | `anat_chem_white` = NemaNode N2U (the adult White animal, `white_primary: "n2u"`). JSH (L4) and "whole" (the Varshney 2011 + pharynx compilation Randi actually loaded) are separate columns | `white_primary: "jsh"` or `"whole"` | N2U is the original adult reconstruction. The Randi Methods describe individual animals; Randi's code used the compilation. All three are kept |
| Q-W1 | Witvliet version | Published revision (NemaNode baf8ec8, which equals the first author's Feb-2021 tables in dwitvliet/nature2021; their identity with the Nature ESM is UNVERIFIED) | the pre-revision data Randi used (NemaNode 859641e content, = the wheel CSVs) and the 2020-05-14 original (8a50236) are acquired and documented in provenance | It is the authors' latest release, served by NemaNode, and the ConnectomeToolbox's ESM-derived counts (2,202 / 2,186 edges) agree with it. Caveat (witvliet2021 P1-W10): the only paper-text figures found, 3,113 classified connections and 1,292 per dataset, are reproduced exactly by the PRE-revision data, not by these tables. Which version the published text describes is unverified; reading the paper settles it |
| Q-W3 | Combining Witvliet datasets 7 and 8 | `anat_chem_witvliet = d7 + d8` (summed, as Randi's code sums sources), plus per-dataset columns | `witvliet_combination` | Per-dataset values are never lost |
| Q-W4 / gap | Gap-junction source | `anat_gap` = White N2U gap-junction count per unordered pair (single-counted); JSH and whole as separate columns; Witvliet gap junctions not used | `gap_primary` | Witvliet gap junctions were partially annotated and excluded from that paper's own analyses |
| Q-W6 | Neurons outside a dataset's volume | Anatomical value null, plus flag `<dataset>_not_covered`, when either neuron never occurs in that dataset; 0 only when both occur | — | 0 would assert absence where there was no reconstruction |
| Q-008 / FEN-2/6/7 | Predicted sign | Fenyves 2020 journal version (sheet 5 of the PLOS file): `+`→excitatory, `-`→inhibitory, `complex`→complex, `no pred`→unknown. Null when Fenyves's connectome has no chemical connection for the pair. The basis column lists the presynaptic transmitter(s), the matched receptor classes and the postsynaptic genes in those classes | preprint-version calls, Szilágyi 2026 and Wang 2024 not used | Fenyves 2020 is the brief's source, and the journal version reproduces the paper's published counts |
| Q-RS-1/2 | Neuropeptide version | `np_edge_short/mid/long` = the 08062023 matrices (they reproduce Table S6 exactly; the authors' README names them as the figure data). The 01022024 post-publication update is in `np_edge_*_v2024` | 07072022 (preprint-era) acquired but not tabulated | Matches the published supplementary table |
| Q-RS-5 | Neuropeptide edge value | Number of NPP–GPCR pairs supporting the edge (integer; 0 = no edge) | — | The matrices' own weights |
| Q-009 / Q-B3 | Monoamine source | `monoamine_edge` = Bentley 2016 (the brief's source): the sorted, ';'-joined ligands supporting the edge, the string `none` when there is no edge (Bentley's network spans all 302 neurons, so `none` is a real absence; null only for unresolved AWC rows); `monoamine_edge_rs2023` = the Ripoll-Sánchez 08062023 monoamine matrix weight | — | Bentley 2016 reproduces its paper's totals exactly. Neither file reproduces Ripoll-Sánchez's quoted 0.0236 |
| latency | `measured_latency_wt` | Effective rise time of the atlas's mean kernel for the pair: the authors' `get_effective_rise_time` algorithm (peak of abs(kernel) on a 0–200 s / 1,000-point axis; Brent root of kernel = peak/e before the peak), applied to the h5 kernels. `measured_peak_time_wt` is also carried | `kernel_time_axis_s` | The authors computed rise times per trial on fitted responses, which are not in the release. This is the closest reproducible quantity, and it is labelled as such |
| CeNGEN | Expression in the table | Not tabulated. The brief's column list has no expression column, and `predicted_sign_basis` uses the receptor expression Fenyves used (sheet 3 of their file), so the basis matches the call. Taylor 2021 is acquired, verified and mapped (`mapping_taylor2021_cengen_types.csv`), ready for the classification pass | — | Adding a CeNGEN-thresholded column would be a new biological call (threshold choice) that the brief reserves to the owner |
| head | Row universe | Randi head188 + RMHR = 189 neurons, 189 × 188 = 35,532 ordered pairs | `head_set` | RMHR is a head neuron omitted by a typo in the authors' list; it is included as never tested |

### D-013 (2026-10-12, Phase 1, PROVISIONAL)
**Atlas release.** The 2023-06-28 release is the table's source; the
2023-06-14 release is kept for comparison. See the table above (Q-001).

## Phase 4

### D-014 (2026-10-12, Phase 4, DECIDED, engineering)
**Every neuron pair that a source contributes but the table has no place for
is counted in `data/processed/merged_edges_exclusions.csv`, per source file
and reason.**

The reasons are:
- `out_of_head_scope`: Rule 6, head only;
- `awc_identity_unresolved`: AWCL/AWCR pairs under `awc_policy=unresolved`;
- `self_pair`: excluded by `include_self_pairs=false`.

Reasoning: before this, only name-level exclusions were logged, together with
the Randi WT measurements outside the head. Edges of the anatomical,
polarity, neuropeptide and monoamine sources that leave the head were not
logged, which Rule 3 forbids. `tests/test_merged_table.py` now checks, for
every White export and every 2023 neuropeptide range, that the pairs present
in the table plus the logged pairs equal the source's distinct neuron pairs.

The table itself is unchanged by this (same CSV and Parquet hashes). Only the
exclusion log and `SHA256SUMS` changed.
