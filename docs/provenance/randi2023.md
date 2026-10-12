# randi2023: Neural signal propagation atlas (WT and unc-31)

- Paper: Randi F, Sharma AK, Dvali S, Leifer AM. *Neural signal propagation
  atlas of Caenorhabditis elegans.* Nature 623, 406–414 (2023).
  doi:10.1038/s41586-023-06683-4. Preprint arXiv:2208.04790.
- Module: `src/acquire/randi2023.py`
- Status: **SECONDARY — primary comparison PENDING (blocks Phase 4 freeze)**
- Retrieval dates (UTC), from `data/raw/randi2023/MANIFEST.json`:
  - 2026-10-11: wheel members, i.e. the date the wheel was downloaded;
  - 2026-10-12: `funatlas_release-2023-06-14.h5`.
- Verified independently: Phase 1 verification pass, 2026-10-12. Every count
  was recomputed from the raw files and agreed.

## Primary location (not reachable from this environment)

| Acquired file | Primary counterpart | Status |
|---|---|---|
| `funatlas.h5`, `funatlas_release-2023-06-14.h5` | FunCoNN interactive atlas (https://funconn.princeton.edu/); machine-readable datasets on OSF, doi:10.17605/OSF.IO/E2SYT (https://osf.io/e2syt/), per a search excerpt of the Nature data-availability statement | Which OSF file corresponds to which h5 is UNVERIFIED. Host blocked |
| `aconnectome_ids_ganglia.json` | none known (author package metadata). Byte-identical to `leiferlab/pumpprobe` @1dbc5e0a `pumpprobe/aconnectome_ids_ganglia.json`, the paper's analysis code | — |
| `neuron_ids.txt` | none known (author package metadata) | — |

Other unreachable candidate primaries, none byte-compared:

- Raw recordings, reportedly as NWB in DANDI dandiset 001075 (web-search
  excerpt; unverified).
- funsim.princeton.edu.
- Nature Source Data files, reportedly added by a January 2024 correction
  (content unverified).
- figshare 23057558, "Supplementary Spreadsheet 1" for arXiv v3 (content
  unverified).

Primary check to perform once reachable: download the atlas from FunCoNN/OSF
and compare `q`, `q_eq`, `dFF`, `dFF_all` and `occ1`, for both strains,
element by element against `funatlas.h5`.

## Files acquired

| File | Size (bytes) | SHA-256 | Distributor / URL | Integrity checks passed |
|---|---|---|---|---|
| `funatlas.h5` | 18,266,176 | `53a99055667b853e1d3d6be573ec2613d38c9f6989f302ec38ecd38dd50c7975` | PyPI `wormneuroatlas` 0.0.7.3 (F. Randi), uploaded 2023-06-29T11:26:33Z: `https://files.pythonhosted.org/packages/b3/dc/634b2a009739f692bad83325e5c0f8fd5b1323ac1a9ce11df7d4c8ac40db/wormneuroatlas-0.0.7.3-py3-none-any.whl#wormneuroatlas/data/funatlas.h5` | (1) archive size + SHA-256 match pin; (2) member size + SHA-256 match pin; (3) member matches the wheel's `RECORD`; (4) wheel SHA-256 equals PyPI's published digest, checked live. Also byte-identical to `francescorandi/wormneuroatlas` git 827e26b (blob fa122efd) |
| `funatlas_release-2023-06-14.h5` | 18,249,792 | `f84f1790a6cdf812375e2644122a08e101d7d7c15c99a44a7fb106f7bd1088d6` | GitHub `francescorandi/wormneuroatlas` @ df07176e2b369d13c683e2361651277fac5d0346 (first author's repository), `wormneuroatlas/data/funatlas.h5` | size + SHA-256 match pin; git blob `247c9d11f814c2e0c011634ed3ca4cda42056c58` matches the commit |
| `aconnectome_ids_ganglia.json` | 5,636 | `e754fcb703b39b5f0db977d0b654ba2ac5ce09111f4e19aef3a85fb09ee2e0a2` | same wheel, member `wormneuroatlas/data/aconnectome_ids_ganglia.json` | the same four checks as `funatlas.h5` |
| `neuron_ids.txt` | 2,645 | `e2c7e54af611c1e85aa0705588fcf096ede5f0c28f7fd1d5f0cbec5480b786cc` | same wheel, member `wormneuroatlas/data/neuron_ids.txt` | the same four checks as `funatlas.h5` |

**Which release later phases use.** `funatlas.h5` (2023-06-28) is the
release the merged table reads (`ATLAS_FILE` in the module). It reproduces
the Nature article and includes the authors' "fix in export script". See
decision D-013. The 2023-06-14 file is kept for version comparison and for the
preprint reproduction test.

## What each file contains

**`funatlas.h5` (both releases have the same layout)**

- Attributes: `time_compiled` (2023-06-28_19-52-14, or 2023-06-14_08-36-12)
  and `kernels_keys = g,factor,power_t,branch`.
- `neuron_ids`: 300 entries, dtype `|S5`, alphabetically sorted. AWC is
  stored as `AWCON` and `AWCOF` ("AWCOFF" truncated to 5 bytes). There is no
  AWCL/AWCR and no CANL/CANR.
- Per strain (`wt`, `unc31`), all 300×300 unless noted:
  - `dFF`: mean ΔF/F. It equals `mean(dFF_all)` exactly.
  - `dFF_all`: retained per-trial values, an object array.
  - `q`: q-value for "functionally connected". It is finite **if and only
    if** at least one trial was retained (`len(dFF_all) > 0`). This holds
    for every entry, in both strains and both releases.
  - `q_eq`: q-value of the equivalence (TOST) test for "functionally not
    connected".
  - `q_eq_th`: scalar, 1.2 for both strains. In the authors' code
    (pumpprobe `qvalues_map.py:79`, `funatlas_plot_intensity_map.py:136`),
    `tost_th=1.2` is passed to `get_kolmogorov_smirnov_q`, with TOST bounds
    = ±tost_th × SD of the control distributions. That is consistent with
    this field but UNVERIFIED for this file, because the h5 exporter is not
    public.
  - `occ1`: number of stimulation/response occurrences, **including trials
    later discarded**. occ1 ≥ len(dFF_all) everywhere. They differ in 11,067
    WT and 3,142 unc-31 entries.
  - `kernels`: fitted response kernels, an object array.
- **Orientation: `M[i, j]` is the response of neuron i (row, responding) to
  stimulation of neuron j (column, stimulated).** Four lines of evidence:
  1. The authors' code: pumpprobe's occ1 docstring reads "occ1[i,j] is the
     number of occurrences of the response of i following a stimulation of
     j", and `fig5_commands.txt` uses `-j:AVDR -i:AVDL`.
  2. The paper's named candidates AVDR→AVDL and M3L→URYVL appear at
     `[responding, stimulated]` and not transposed.
  3. head188 has 186 rows but only 168 columns with observations, matching
     "activity from 186 of 188 neurons".
  4. The Leifer-lab file in the Creamer et al. repository
     (`leifer_extrasynaptic_pairs.csv`) lists the 55 strict pairs' trial
     counts in row-major [resp, stim] order.

**`aconnectome_ids_ganglia.json`**

- The authors' assignment of neurons to ganglia.
- Its `head` key lists 7 ganglion groups with **189 entries, 188 unique**:
  `RMHL` is listed twice under "ventral ganglion", and `RMHR` is never
  listed. AWC is named `AWCL`/`AWCR`.
- Atlas ids absent from this file: AWCOF, AWCON, DB7, RMHR, VA11. DB7, VA11
  and RMHR have no data in either strain.
- Ids in this file absent from the atlas: AWCL, AWCR, CANL, CANR.
- 20 pharyngeal neurons.

**`neuron_ids.txt`**

- The package's 300-id list, with the pharynx last.
- Its order differs from the h5's `neuron_ids`, and it spells `AWCOFF` where
  the h5 has `AWCOF`, so the two id sets differ in that one spelling.
- The wormneuroatlas loader sorts these ids (`np.unique`) at construction.
  When it loads the h5 it compares against that sorted list and silently
  excuses the AWCOF/AWCOFF difference; no warning is printed for this file.

## Record counts

Counts come from `python -m src.acquire --counts randi2023`. Keys are prefixed
`release_<date>__`; the table shows the 2023-06-28 release unless stated.

- `head188` = the authors' head set, with the atlas's AWCON/AWCOF standing in
  for the ganglia file's AWCL/AWCR. This follows the authors' analysis code,
  which maps AWCOFF→AWCL and AWCON→AWCR (pumpprobe `Funatlas.py` 369–377);
  under it the code has no −1 indices.
- "Measured" = a finite q-value. This is the authors' definition
  (`Numbers_script.py` 81–87, run with `--no-merge-bilateral --inclall-occ
  --req-auto-response`). It includes the diagonal.

| Quantity | Definition | Count in acquired file | Paper reports | Where the paper reports it | Match |
|---|---|---|---|---|---|
| Measured head pairs, WT | finite `wt/q` in head188 | **23,433** (168 self) | 23,433 | Nature: "1,310 of the 23,433 measured neuron pairs, or 6%, pass our stringent criteria to be deemed functionally connected at q < 0.05" (web-search excerpt attributed to nature.com/articles/s41586-023-06683-4) | **YES** |
| Functionally connected, WT | `wt/q` < 0.05 in head188 | **1,310** (159 self) | 1,310 (6%) | same excerpt | **YES** |
| Inhibitory share of WT connections | sign of `wt/dFF` among head188 q<0.05 pairs | 150 negative, 1,159 positive, 1 NaN. 150/1,309 = **11.46%** under the authors' formula (inh/(inh+exc) at the q nearest 0.05, `Numbers_script.py` 207–220), applied here to the h5's mean dF/F; the authors applied it to a recomputed dF/F that this file does not contain | 11% | Nature: "11% of q < 0.05 functional connections are inhibitory" (domain-restricted web-search excerpt) | **YES** (rounds to 11% under either denominator) |
| Strict candidate purely extrasynaptic pairs | WT q<0.05 ∧ unc-31 q_eq<0.05 ∧ unc-31 q>0.05, off-diagonal | **53** (plus 2 self-pairs, 55 total) | 53 | Nature: "Fifty-three pairs of neurons met their criteria, and were therefore putative candidates for purely extrasynaptic signalling" (web-search excerpt). The authors' listing skips i==j (`wt_unc31_differences.py` 199–204) | **YES** |
| Measured head pairs (preprint figure) | finite `wt/q` in head188 | 23,433 in the acquired 2023-06-28 release; **23,427** in the 2023-06-14 release | 23,427 | arXiv:2208.04790: "imaged activity in response to stimulation for 23,427 neuron pairs (66% of all possible pairs in the head) at least once" (web-search excerpt; current version v3, revised 2023-05-22; the exact version holding the sentence is unconfirmed) | **NO — BLOCKER for the 2023-06-28 release; YES for the 2023-06-14 release.** Same definition; the difference is the data release. Resolved provisionally by D-013 |
| Measured head pairs, unc-31 | finite `unc31/q` in head188 | 9,228 (109 self); same in both releases | not found | — | **UNVERIFIED** |
| unc-31 connections | `unc31/q` < 0.05 in head188 | 430 (73 self); **324 in the 2023-06-14 release** | not found | — | **UNVERIFIED**. Release-sensitive |

Other counts recorded for later phases (2023-06-28 release):

- **Observed but not evaluated.** 1,057 WT head188 pairs (unc-31: 1,360)
  have occ1 > 0 but no q, because **all of their trials were discarded**
  (`dFF_all` is empty). The 2023-06-14 release has 1,061 such pairs.
  - In the authors' code this fits every trial failing the per-trial filter
    in `get_significance_features` (contiguous-NaN run or zero local SD).
  - The auto-response requirement acts before occ1 is counted, so it does
    not explain these pairs.
  - The exporter is not public, so the mechanism is UNVERIFIED.
- **Pairs measured in both strains.** 8,150 off-diagonal head188 pairs have a
  finite q in both strains (8,145 in the 2023-06-14 release).
- **Non-head neurons.** They add 642 finite WT q-values (all300 24,075 vs
  head188 23,433). None of them is q < 0.05.
- **The wormneuroatlas package does not reproduce the paper.** Its own
  `reduce_to_head()` maps AWCL/AWCR to index −1, which is the last sorted id,
  `VD9`, because its AWCOFF/AWCON mapping lines are commented out. It
  therefore yields 22,913 / 1,274 (head186).
- **Self-pairs in the 1,310.** All 159 are 0-hop "connections" (a neuron's
  response to its own stimulation).

## Candidates considered but not acquired

- `francescorandi/wormneuroatlas` earlier atlas releases:
  - 7a7c653 (2022-12-23, blob 55247b70);
  - 8c267c0 (2023-01-02, blob ba4b7a2b);
  - 5a55acf (2023-01-09, blob 7e3ad44f);
  - a31bb36 (2023-01-24, blob f337d907).

  All give head188 WT 9,742 measured / 1,084 at q < 0.05 (verifier's
  count). They are far earlier, partial-data releases that match no paper
  figure; not needed.
- PyPI `wormneuroatlas` 0.0.2–0.0.7.2 wheels and the 0.0.7.3 sdist. 0.0.7.1
  and 0.0.7.2 were uploaded 2023-06-20 and likely bundle the 2023-06-14
  atlas, which is acquired directly from git instead.
- `francescorandi/wormneuroatlas` HEAD (b2e13d8) copies of the three wheel
  members: byte-identical to the acquired files, so redundant.
- `leiferlab/worm-functional-connectivity` `atlas/wild-type.pickle` and
  `atlas/unc-31.pickle`, the FunCoNN app atlases. Pickle files can execute
  code when loaded, so they are not acquired.
- `leiferlab/pumpprobe` @1dbc5e0a `pumpprobe/aconnectome_ids.txt`: the
  authors' analysis id list with AWCL/AWCR naming. Used as evidence, not
  data.
- DANDI 001075 (raw NWB), funsim, Nature Source Data, figshare 23057558:
  hosts blocked; listed above as candidate primaries.

## Discrepancies, flags and open questions

- **P1-R1. Five evidence states per pair and strain, not four.** The states
  are: connected (q<0.05); confidently absent (q_eq<0.05); inconclusive;
  **observed but every trial discarded** (occ1 > 0, no q: 1,057 WT); and
  never observed. Q-002 covers all five.
- **P1-R2. Sign undefined for one connected pair.** URYDL (responding) ←
  ADER (stimulated) has q = 1.36e-16, q_eq = NaN, occ1 = 1 and
  `dFF_all = [nan]`. It is also the only WT pair with a finite q and a NaN
  q_eq. Phase 4 must carry it with an explicit flag, not drop it.
- **P1-R3. The pair-count target depends on the release (Q-001).**
  - The brief's 23,427 matches arXiv:2208.04790 and is reproduced exactly by
    the author's 2023-06-14 release (git df07176).
  - The 2023-06-28 release (git 827e26b, "updated data after fix in export
    script") reproduces Nature's 23,433 / 1,310 / 53.
  - Between the two releases every unc-31 q changed: unc-31 q<0.05 went
    324→430, q_eq<0.05 659→1,061, and strict candidates 33→55. Any
    unc-31-dependent result depends on the release.
  - Provisional resolution: D-013.
- **P1-R4. The authors' AWC convention.** The paper's analysis code
  (pumpprobe Funatlas.py 369–377) maps AWCOFF→AWCL and AWCON→AWCR. That is
  how head188 reproduces the paper. Adopting the convention for our
  namespace is Q-005; see its provisional resolution.
- **P1-R5. The authors' head list omits RMHR.**
  - RMHL is listed twice and RMHR never.
  - RMHR has zero finite q-values in either strain, so the omission changes
    no paper count. DB7 and VA11 are also atlas ids with no data and no
    ganglion entry.
  - Owner question: should RMHR be included in the head set with "never
    tested" status? See its provisional resolution in `docs/decisions.md`.
- **P1-R6. This copy's identity with the portal version is unproven.** The
  matching headline numbers are strong evidence, not proof. The element-wise
  primary comparison remains PENDING.
