# randi2023: Neural signal propagation atlas (WT and unc-31)

- Paper: Randi F, Sharma AK, Dvali S, Leifer AM. *Neural signal propagation
  atlas of Caenorhabditis elegans.* Nature 623, 406–414 (2023).
  doi:10.1038/s41586-023-06683-4
- Module: `src/acquire/randi2023.py`
- Status: **SECONDARY — primary comparison PENDING (blocks Phase 4 freeze)**
- Retrieval date (UTC): 2026-10-11, from `data/raw/randi2023/MANIFEST.json`

## Primary location (not reachable from this environment)

- FunCoNN atlas portal: https://funconn.princeton.edu/
- Raw recordings on OSF: https://osf.io/e2syt/ (linked from the OpenWorm
  ConnectomeToolbox Randi_2023 page). The Creamer et al. 2026 repository
  README points to https://osf.io/qxhjd/ for "the data from Randi et al 2023";
  which OSF node holds what is unverified.
- No journal supplementary file holds the full atlas, as far as I could
  determine; the paper points readers to the portal.

Primary check to perform once reachable: download the atlas from FunCoNN/OSF
and compare `q`, `q_eq`, `dFF` and `occ1` for WT and unc-31 against
`funatlas.h5`, element by element.

## Files acquired

All three are members of the PyPI wheel `wormneuroatlas-0.0.7.3-py3-none-any.whl`.

- Wheel SHA-256: `166289031784c9565f6b9205e30dc718bafbc092db3b46f1aef73d93dc4d1325`
- Wheel URL: https://files.pythonhosted.org/packages/b3/dc/634b2a009739f692bad83325e5c0f8fd5b1323ac1a9ce11df7d4c8ac40db/wormneuroatlas-0.0.7.3-py3-none-any.whl
- Uploaded to PyPI on 2023-06-29 by the first author's package.

| File | Size (bytes) | SHA-256 | Integrity checks passed |
|---|---|---|---|
| `funatlas.h5` | 18,266,176 | `53a99055667b853e1d3d6be573ec2613d38c9f6989f302ec38ecd38dd50c7975` | wheel SHA-256 equals PyPI's published digest (checked live); member matches pin; member matches wheel `RECORD` |
| `aconnectome_ids_ganglia.json` | 5,636 | `e754fcb703b39b5f0db977d0b654ba2ac5ce09111f4e19aef3a85fb09ee2e0a2` | same three checks |
| `neuron_ids.txt` | 2,645 | `e2c7e54af611c1e85aa0705588fcf096ede5f0c28f7fd1d5f0cbec5480b786cc` | same three checks |

## What each file contains

**`funatlas.h5`**

- Attributes: `time_compiled = 2023-06-28_19-52-14` and
  `kernels_keys = g,factor,power_t,branch`.
- `neuron_ids` is 300 entries, dtype `|S5`, alphabetically sorted. AWC is
  stored as `AWCON` and `AWCOF`; the second is "AWCOFF" truncated to 5 bytes.
  There is no AWCL/AWCR, and CANL/CANR are absent.
- Per strain (`wt`, `unc31`), all 300×300 unless noted:
  - `dFF`: mean ΔF/F over the response window, averaged over trials;
  - `dFF_all`: per-trial values, object array;
  - `q`: q-value for "functionally connected";
  - `q_eq`: q-value of the equivalence (TOST) test for "functionally not
    connected";
  - `q_eq_th`: scalar, equal to 1.2 for both strains. Its meaning is not yet
    confirmed from the Methods;
  - `occ1`: number of observations;
  - `kernels`: fitted response kernels, object array.
- **Orientation: `M[i, j]` is the response of neuron i (row, responding) to
  stimulation of neuron j (column, stimulated).** The authors' code reads this
  way ("pair i<-j"; x-axis "stimulated", y-axis "responding"). It is confirmed
  in the data: the paper's named candidate extrasynaptic pairs AVDR→AVDL and
  M3L→URYVL appear at `[responding, stimulated]` and not transposed. See the
  `orientation_*` counts.

**`aconnectome_ids_ganglia.json`**

- The authors' assignment of neurons to ganglia.
- Its `head` key lists 7 ganglion groups: anterior ganglion, anterior
  pharyngeal bulb, dorsal ganglion, lateral ganglion, ventral ganglion,
  posterior pharyngeal bulb, retrovesicular ganglion. Together they hold 188
  neurons, including 20 pharyngeal neurons.
- It names AWC as **AWCL/AWCR**, which do not occur in the atlas.

**`neuron_ids.txt`**

- The package's 300-name id list. **Its order differs from the h5's
  `neuron_ids`**: the txt puts the pharynx last, the h5 is alphabetical.
- Matrices must be indexed with the h5's own `neuron_ids`.
- The authors' loader prints a warning about this mismatch and then uses a
  sorted list, which agrees with the h5.

## Record counts

Counts come from `python -m src.acquire --counts randi2023`.

- `head188` = the ganglia head set, with AWCON/AWCOF standing in for
  AWCL/AWCR.
- `head186` = the ganglia head set with AWC dropped.
- "Measured" = a finite q-value. This is the authors' definition, from their
  `Numbers_script.py`, which counts non-NaN q-values in the head submatrix.

| Quantity | Definition | Count in acquired file | Paper reports | Where the paper reports it | Match |
|---|---|---|---|---|---|
| Measured head pairs, WT | finite `wt/q` in head188 | **23,433** (168 of them self-pairs) | 23,433 | Nature article: "1,310 of the 23,433 measured neuron pairs, or 6%, pass our stringent criteria to be deemed functionally connected at q < 0.05" (excerpt via web search of nature.com/articles/s41586-023-06683-4) | **YES** |
| Functionally connected, WT | `wt/q` < 0.05 in head188 | **1,310** (159 self) | 1,310 (6%) | same excerpt | **YES** |
| Inhibitory share of WT connections | `wt/dFF` < 0 among the 1,310 | 150 / 1,310 = **11.45%** | 11% | Nature article excerpt via web search: "11% of q < 0.05 functional connections are inhibitory" | **YES**. Note: 1 of the 1,310 has NaN `dFF`, so its sign is undefined |
| Measured head pairs (preprint figure) | — | no count in this file equals 23,427. head188 has 24,490 pairs with `occ1` > 0 and 23,433 with finite q | 23,427 | arXiv:2208.04790 (a preprint version), via web search: "imaged activity in response to stimulation for 23,427 neuron pairs (66% of all possible pairs in the head) at least once" | **NOT COMPARABLE**. This is a preprint figure; the published (Nature) figure is 23,433 and is reproduced exactly. This is where the brief's 23,427 comes from |
| Measured head pairs, unc-31 | finite `unc31/q` in head188 | 9,228 (109 self) | not found | — | **UNVERIFIED** (paper text not reachable) |
| unc-31 connections | `unc31/q` < 0.05 in head188 | 430 (73 self) | not found | — | **UNVERIFIED** |
| Candidate purely extrasynaptic pairs | WT q<0.05 ∧ unc-31 q_eq<0.05 ∧ unc-31 q>0.05, all 300 | 55 (53 off-diagonal + 2 self) | not found as a number in reachable text | The rule is the authors' (`wt_unc31_differences.py`). The Creamer et al. repository's `leifer_extrasynaptic_pairs.csv` has exactly 55 entries | **UNVERIFIED** against the paper; consistent with an independent author-side file |

Other counts recorded for later phases:

- head188 WT pairs with observations (`occ1` > 0) but **no q-value: 1,057**;
  for unc-31: 1,360. These are a fifth evidence state, beyond
  connected / confidently absent / inconclusive / never observed. See flag P1-R1.
- Off-diagonal head188 pairs with a finite q in **both** strains: 8,150.
- The non-head neurons carry 642 additional finite WT q-values
  (all300 24,075 vs head188 23,433). None is q < 0.05: all300 also has 1,310.
- The wormneuroatlas package's own `reduce_to_head()` maps AWCL/AWCR to index
  −1, which is the last id, `VD9`. It therefore yields 22,913 / 1,274 and does
  **not** reproduce the paper. Including AWCON/AWCOF (head188) reproduces it
  exactly.

## Discrepancies, flags and open questions

- **P1-R1. Five evidence states, not four.** The four in Phase 0 flag F2 were
  connected (q<0.05), confidently absent (q_eq<0.05), inconclusive and
  untested. To these add **"observed but not evaluated"**: `occ1` > 0 but q is
  NaN, 1,057 WT head pairs. These are probably pairs that failed the authors'
  NaN-fraction or auto-response filters; that is unverified. Owner question
  Q-002 should cover all five.
- **P1-R2. Sign undefined for one connected pair.** One WT pair with
  q < 0.05 has NaN mean ΔF/F. Phase 4's `measured_sign_wt` needs a rule for
  it; it must not be silently dropped.
- **P1-R3. Pair-count target (Q-001).** The brief's 23,427 is a preprint
  figure. The published 23,433 is reproduced exactly by this file, which was
  compiled 2023-06-28 and published to PyPI on 2023-06-29, before the
  November 2023 Nature publication.
- **P1-R4. The AWC naming affects reproduction.** Only the AWCON/AWCOF
  stand-in reproduces the paper's counts. That is evidence about what the
  authors did, not a decision about our namespace (Q-005 remains open).
- **P1-R5. This copy's identity with the portal version is unproven.** The
  matching headline numbers are strong evidence, not proof. The element-wise
  primary comparison remains PENDING.
