# Namespace decisions (Phase 2)

- Code: `src/namespace/canonical.py`, `src/namespace/mapping.py`
- Reviewable data files:
  - `config/namespace/aliases.csv`
  - `config/namespace/non_neuronal_names.csv`
  - `config/namespace/cengen_types.csv`
- Generated artifacts (deterministic, committed), in `data/interim/namespace/`:
  - `canonical_neurons.csv`
  - `mapping_<source>.csv`
  - `mapping_taylor2021_cengen_types.csv`
  - `exclusions.csv`
  - `needs_review.csv`
  - `coverage.csv`
- Rebuild with: `python -m src.namespace.mapping`

Calls marked **PROVISIONAL** were made by Claude after the owner asked, on
2026-10-12, not to be asked further questions. Each one is listed with its
alternatives in `docs/decisions.md` → "Provisional resolutions", and each is
switchable in `config/pipeline.json` where a switch makes sense.

## 1. The canonical list (single source of truth)

**The canonical list is the 302 hermaphrodite neurons, in WormAtlas
nomenclature.** wormatlas.org is blocked, so the list comes from the acquired
copies, and the build **fails** if they ever disagree:

- The names in `IndividualNeurons.csv` (OpenWorm's copy of WormAtlas
  NeuronNames.htm; its first line cites it), restricted to those that
  `C. elegans Cell List - WormBase.csv` marks in "Neurons (no male-specific
  cells)". That column marks exactly 302 names, which equals its own totals
  row.
- That set must equal exactly:
  - `Cells.py` PREFERRED_HERM_NEURON_NAMES (ConnectomeToolbox);
  - owmeta `neurons.csv`;
  - the neuron entries of the NemaNode cell table.

  It does, for all three.
- Style of the list: unpadded ventral-cord numbering (VB1, not VB01); AWCL
  and AWCR; CANL and CANR included; all 20 pharyngeal neurons included.

**Neuron classes** come from NemaNode's `classes` field. It yields exactly
118 classes over the 302 names, White et al.'s count, and 14 over the 20
pharyngeal neurons. Numbered motor neurons fall in classes such as ASn, DAn
and VBn.

**Extension identities AWCON / AWCOFF (PROVISIONAL).**

- AWC is left/right asymmetric by *function*. In each animal one AWC becomes
  ON (str-2 expressing) and the other OFF, at random with respect to L/R.
- The Randi atlas (NeuroPAL-based) and CeNGEN name AWC by function. The
  anatomical connectomes name it by position, AWCL/AWCR.
- A one-to-one mapping between the two would assert a correspondence that is
  not fixed biologically. So AWCON and AWCOFF are kept as two extra canonical
  identities (class AWC, `is_extension=1`), next to AWCL/AWCR, and are never
  silently identified with them.
- How the merged table joins them to anatomy is the `awc_policy` setting in
  §4.

## 2. Mapping rules, in order of application

1. **alias**: explicit entries in `config/namespace/aliases.csv`. There are
   three:
   - `randi2023` `AWCOF` → `AWCOFF`. The h5 stores ids as 5-byte strings and
     truncates "AWCOFF". The package's own `neuron_ids.txt` spells AWCOFF.
   - `white1986` `avfl` → `AVFL` and `avfr` → `AVFR`. One lower-case record
     in Varshney's `NeuronConnect.xls`; every other record of that pair is
     upper case.
2. **exact**: the name is canonical, extensions included.
3. **strip_whitespace**: the name with surrounding spaces removed is
   canonical.
4. **vnc_zero_padding**: `^(AS|DA|DB|DD|VA|VB|VC|VD)0(\d)$`, so VB01 → VB1.
   This is the only pattern rule. It applies to Fenyves (64 names) and
   Ripoll-Sánchez (64 names).

There is **no fuzzy or similarity matching**. Every mapping produced by a
rule other than `exact` is written to `needs_review.csv` for the owner's
review: 152 entries.

**CeNGEN cell types (Taylor 2021)** are class-level, so they map one-to-many.

- A type whose name equals a canonical class maps to that class's members.
- All other types are listed explicitly in `config/namespace/cengen_types.csv`
  with a reason each:
  - individual neurons: ASEL, ASER, DA9, DB01→DB1, VA12, VB01→VB1,
    VB02→VB2;
  - functional AWC: AWC_ON→AWCON, AWC_OFF→AWCOFF;
  - split classes: IL2_DV / IL2_LR, RMD_DV / RMD_LR, RME_DV / RME_LR, VC_4_5;
  - the pooled VD_DD;
  - remainders: DA, DB, VA, VB, VC, which are the class minus the separately
    profiled members. These are marked REVIEW, because they are inferred from
    the separate columns.

## 3. Exclusions (nothing is dropped silently)

`exclusions.csv` lists every name in every source file that does not map,
with its file(s), occurrence count and reason. Current contents:

| Source | Excluded names | Reason |
|---|---|---|
| white1986 | 35 | body wall muscles (NemaNode cell table type `b`) |
| white1986 | 9 | other non-neuronal cells (NemaNode type `u`: pharyngeal muscles, marginal cells, glia, etc.) |
| witvliet2021 | 32 | body wall muscles (type `b`) |
| witvliet2021 | 10 | other non-neuronal cells (type `u`) |
| witvliet2021 | 4 | unidentified neurite fragments `Fragment`, `NR_fragment`, `VAn`, `vncfrag` (`config/namespace/non_neuronal_names.csv`) |
| all other sources | 0 | — |

**No neuron-like name is unrecognised in any source.**

## 4. Policies (switchable in `config/pipeline.json`)

**`awc_policy` (PROVISIONAL default `unresolved`).**

| Value | Effect on the merged table | Trade-off |
|---|---|---|
| `unresolved` (default) | Randi's AWCON/AWCOFF rows get **no** anatomical, polarity or extrasynaptic values. Those columns are null and the row is flagged `awc_identity_unresolved` | Asserts nothing false. Loses all wired/wireless information for the 750 ordered pairs that involve AWCON or AWCOFF |
| `authors_convention` | AWCOFF is read as AWCL and AWCON as AWCR, as the authors' analysis code does (pumpprobe `Funatlas.approximate_ids`) | Reproduces how Randi et al. compared function with anatomy. Wrong for about half of the animals in any given pair. The arbitrariness is mild because AWCL/AWCR wiring is nearly symmetric, but it is not zero |

**`bilateral_policy` (PROVISIONAL default `split`).**

- `split` (implemented): one row per individual neuron pair. No information is
  lost, and every statistic stays as the authors computed it. Every row
  carries `pre_class`/`post_class`, so class-level summaries of anatomical,
  polarity and extrasynaptic columns can be derived by grouping.
- `collapse` (not implemented by design): merge L/R (and D/V) members into
  classes. The authors' own loader warns that averaging q-values across
  merged neurons "is not mathematically accurate … Do not use q values like
  this". A valid class-level q needs re-running their KS/TOST statistics on
  trial-level data with their null distributions. The null distributions are
  **not** in the released h5. A collapsed table would therefore have no valid
  measured statistics. If the owner wants collapse, the honest version is
  class-level counts of member pairs (tested / connected / confidently
  absent) rather than a merged q. That is a scoping decision for the owner.

**`head_set` (PROVISIONAL `randi_head188_plus_rmhr`).** The row universe is:

- the authors' 188-neuron head set (`aconnectome_ids_ganglia.json` "head",
  with AWCON/AWCOFF in place of AWCL/AWCR, as their code does);
- **plus RMHR**. RMHR is a ventral-ganglion head neuron that the authors'
  ganglia file omits through a duplicated RMHL entry. It has no measurements,
  so it enters as never tested.

The head set is **not** NemaNode's `inhead` flag. That flag marks neurons
with processes in the head, such as ALM, PVC and CAN, and omits the pharynx
and the retrovesicular-ganglion motor neurons (AS1, DA1, DB1, DB2, DD1, VA1,
VB1, VB2, VD1, VD2, SAB, AVG). Randi's ganglion-based set is the atlas's own
coverage definition.

## 5. Coverage (from `coverage.csv`)

| Source / file | Distinct names | Mapped | Excluded (non-neuronal) | Unrecognised | Canonical 302 covered |
|---|---|---|---|---|---|
| randi2023 atlas ids (both releases) | 300 | 300 | 0 | 0 | 298 (98.7%) + AWCON/AWCOFF |
| randi2023 ganglia "head" | 188 | 188 | 0 | 0 | 188 |
| white1986 N2U (`_A`) | 221 | 180 | 41 | 0 | 180 (59.6%) |
| white1986 JSH (`_L4`) | 215 | 178 | 37 | 0 | 178 (58.9%) |
| white1986 whole (Varshney + pharynx) | 309 | 300 | 9 | 0 | 300 (99.3%) |
| witvliet2021 dataset 7 (published) | 224 | 181 | 43 | 0 | 181 (59.9%) |
| witvliet2021 dataset 8 (published) | 221 | 180 | 41 | 0 | 180 (59.6%) |
| fenyves2020 sign predictions (sheet 5) | 297 | 297 | 0 | 0 | 297 (98.3%) |
| fenyves2020 receptor expression (sheet 3) | 302 | 302 | 0 | 0 | 302 (100%) |
| ripollsanchez2023, each matrix | 302 | 302 | 0 | 0 | 302 (100%) |
| bentley2016 monoamine | 237 | 237 | 0 | 0 | 237 (78.5%) |
| bentley2016 neuropeptide | 239 | 239 | 0 | 0 | 239 (79.1%) |
| taylor2021 CeNGEN types (one-to-many) | 128 types | 128 | 0 | 0 | 300 (99.3%) + AWCON/AWCOFF |

Coverage below 100% reflects each dataset's scope, not mapping failures:

- the N2U/JSH series and Witvliet's datasets reconstruct the head/nerve ring
  only;
- Fenyves excludes the five neurons without chemical synapses (CANL, CANR,
  M5, PLML, PLMR);
- Bentley's layers include only neurons with known ligand or receptor
  expression;
- Randi lacks CANL/CANR and names AWC functionally.

## 6. Non-obvious calls, one by one

- **AWCOF → AWCOFF**: an explicit alias (§2). It is evidence-based, not a
  guess: the package's own id list and its loader both show the truncation.
- **avfl / avfr → AVFL / AVFR**: an explicit alias. One record of the pair is
  lower case, and the same record exists upper case on the send side.
- **Zero padding (VB01 → VB1)**: the only pattern rule. It is applied only
  when the unpadded name is canonical.
- **DVB vs PVT**: NemaNode renames Durbin's head "DVB" processes to PVT, a
  published correction. The pipeline never reads Durbin's neurodata.txt for
  the table, so no rename is applied. If Durbin data are ever used, this needs
  an explicit alias.
- **AWCL/AWCR vs AWCON/AWCOFF**: never mapped onto each other in the
  namespace. Only the merge-time `awc_policy` can join them (§4).
- **CeNGEN remainder types (DA, DB, VA, VB, VC)**: inferred from the
  separately profiled members. REVIEW.
- **CANL/CANR**: canonical. They are absent from Randi, so they do not enter
  the head row universe.
- **Muscles, glia and other cells** (BWM-*, pm*, mc*, e*, hmc, CEPsh, GLR,
  excgl, …) are excluded, never mapped to neurons.
