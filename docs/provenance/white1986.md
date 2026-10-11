# white1986: White et al. 1986 anatomical connectome, all reachable White-lineage variants

- Paper: White JG, Southgate E, Thomson JN, Brenner S. The structure of the nervous system of the nematode *Caenorhabditis elegans*. Phil Trans R Soc Lond B 314, 1–340 (1986). doi:10.1098/rstb.1986.0056
  - The files below also come from separate papers that re-compiled or re-annotated White's EM series. Each file is attributed to its own work:
    - Durbin 1987 (PhD thesis, Cambridge): `neurodata.txt`.
    - Varshney et al. 2011, PLoS Comput Biol 7:e1001066, doi:10.1371/journal.pcbi.1001066: `NeuronConnect.xls`, and the somatic part of `*_whole*`.
    - Albertson & Thomson 1976, doi:10.1098/rstb.1976.0085: the pharynx part of `*_whole*`.
    - Cook et al. 2019, Nature 571:63–71, doi:10.1038/s41586-019-1352-7: the three SI 5 workbooks.
    - Zhen lab (NemaNode, 2020): the muscle re-annotation in `*_A*`, `*_L4*`, `white_1986_jsh/n2u*`.
- Module: `src/acquire/white1986.py`
- Status: SECONDARY — primary comparison PENDING (blocks Phase 4 freeze)
- Retrieval date (UTC): 2026-10-11 (all 20 files; `data/raw/white1986/MANIFEST.json`)

This source answers no question by itself. It exists so the owner can settle **Q-007 ("which White")** with every candidate in hand. Nothing here picks one.

## Primary location (not reachable from this environment)

| Acquired file(s) | Primary copy | What the primary is |
|---|---|---|
| `wna__aconnectome_white_1986_A.csv`, `white_1986_n2u.csv`, `cect__aconnectome_white_1986_A.csv`, `nemanode_da8ca7e__white_1986_n2u.json` | nemanode.org connectivity download, dataset id `white_1986_n2u` ("White et al., 1986, N2U (adult)") | NemaNode export of Durbin's N2U compilation, with Zhen-lab muscle annotation |
| `wna__aconnectome_white_1986_L4.csv`, `white_1986_jsh.csv`, `cect__aconnectome_white_1986_L4.csv`, `nemanode_da8ca7e__white_1986_jsh.json` | nemanode.org, dataset id `white_1986_jsh` ("White et al., 1986, JSH (L4)") | same, for JSH |
| `wna__aconnectome_white_1986_whole.csv`, `cect__aconnectome_white_1986_whole.csv`, `nemanode_da8ca7e__white_1986_whole.json` | nemanode.org, dataset id `white_1986_whole` ("White et al., 1986 compilation (adult)") | Varshney 2011 somatic compilation plus Albertson & Thomson 1976 pharynx |
| `nemanode_da8ca7e__neurons.json` | nemanode.org cell table | NemaNode annotation |
| `neurodata.txt` | https://www.wormatlas.org/neurodata.txt (readme https://www.wormatlas.org/neurodata_readme.txt) | Durbin 1987 thesis data file |
| `neurodata_updated.txt` | none | OpenWorm edit of `neurodata.txt` (three edits listed in the toolbox's `cect/validation/WhiteEtAl1986.md`) |
| `NeuronConnect.xls` | https://www.wormatlas.org/images/NeuronConnect.xls | Varshney et al. 2011 data (per the toolbox's `cect/validation/VarshneyEtAl2011.md`) |
| `41586_2019_1352_MOESM9_ESM.xlsx` | https://static-content.springer.com/esm/art%3A10.1038%2Fs41586-019-1352-7/MediaObjects/41586_2019_1352_MOESM9_ESM.xlsx | Nature supplement SI 5 |
| `SI 5 Connectome adjacency matrices.xlsx` | https://wormwiring.org/si/SI%205%20Connectome%20adjacency%20matrices.xlsx | WormWiring copy |
| `SI 5 Connectome adjacency matrices, corrected July 2020.xlsx` | https://wormwiring.org/si/SI%205%20Connectome%20adjacency%20matrices,%20corrected%20July%202020.xlsx | WormWiring corrected copy |
| `aconnectome.json` | none found | Undocumented matrix in the Leifer-lab code |
| `aconnectome_ids.txt` | https://github.com/leiferlab/pumpprobe (the authors' repository is the only copy) | Index for `aconnectome.json` |

The nemanode.org export URLs above are given by dataset id. The exact download URL format was not checked, because the host is blocked. The NemaNode source data in the Zhen lab's GitHub repository was reachable and was acquired; see below.

## Files acquired

Distributor abbreviations:

- **PyPI-wheel**: `https://files.pythonhosted.org/packages/b3/dc/634b2a009739f692bad83325e5c0f8fd5b1323ac1a9ce11df7d4c8ac40db/wormneuroatlas-0.0.7.3-py3-none-any.whl#wormneuroatlas/data/<member>` (F. Randi, uploaded 2023-06-29).
- **Toolbox**: `https://raw.githubusercontent.com/openworm/ConnectomeToolbox/ffe570268b7cffb9329cd009a1bb37d60db2d465/cect/data/<file>`, with spaces and commas percent-encoded.
- **NemaNode**: `https://raw.githubusercontent.com/zhenlab-ltri/NemaNode/da8ca7e2fc0eece4b21c30625880b41f39961c76/src/server/populate-db/raw-data/<path>` (Zhen lab; commit by D. Witvliet, 2020-05-22, "Added dataset information to help"). The same blobs are at master head `6b7ca03` (2022-03-16).
- **pumpprobe**: `https://raw.githubusercontent.com/leiferlab/pumpprobe/1dbc5e0a2b609d54bc9b1c90c73d4e3bf183d3c7/pumpprobe/aconnectome_ids.txt` (Leifer lab, 2023-09-20).

Integrity checks:

- **W** (wheel members): size and SHA-256 equal the pin; SHA-256 and size equal the wheel's own `RECORD`; the archive SHA-256 equals the digest PyPI publishes, fetched live.
- **G** (GitHub files): size and SHA-256 equal the pin; the git blob SHA-1 equals the blob the pinned commit records for that path.

| File | Size (bytes) | SHA-256 | Distributor / URL | Integrity checks passed |
|---|---|---|---|---|
| `wna__aconnectome_white_1986_whole.csv` | 64492 | `768d2b16557d768b51f81548f630adb45d76c1f99586e8fd4c90279293cc9dae` | PyPI-wheel, member `aconnectome_white_1986_whole.csv` | W |
| `wna__aconnectome_white_1986_L4.csv` | 39065 | `afe7a37a5bae62630a773b5e7815a408e3a72063caf0ed49ecc91e213077fb12` | PyPI-wheel, member `aconnectome_white_1986_L4.csv` | W |
| `wna__aconnectome_white_1986_A.csv` | 41889 | `6b63f6c0281b7bbc3be75fa3962e26caa020ddf3756bfc8dd9aad6577655fc16` | PyPI-wheel, member `aconnectome_white_1986_A.csv` | W |
| `aconnectome.json` | 902866 | `8d45df9db673ec2a03bd0ab1bd3980d16b6305920adf2332dc80b4cb5f5fb29e` | PyPI-wheel, member `aconnectome.json` | W |
| `aconnectome_ids.txt` | 2641 | `bfcde4c0ccaadce2f69f44c858caddd7c6f5b27aaac878975042b19fa3f7442d` | pumpprobe, blob `1bb809e9eeee15926c0cb850f3dc1ca05e051d80` | G |
| `nemanode_da8ca7e__white_1986_n2u.json` | 284796 | `ba949e1e1766020009d0db38aa3182b245aa6242bb0359a253cd65d0a6b9a5d4` | NemaNode `connections/white_1986_n2u.json`, blob `6aafc974cd97be8cc43653bde6b81935a8266858` | G |
| `nemanode_da8ca7e__white_1986_jsh.json` | 271999 | `ac251c32cfbc3f3ee5add0f4f566c3006b715553e822210cc4ec9f1fc9816dd4` | NemaNode `connections/white_1986_jsh.json`, blob `3f54979ca00c210b37f205c77e69cab4810a464e` | G |
| `nemanode_da8ca7e__white_1986_whole.json` | 375599 | `fe7ff4a6529ccb9d13183e665644e30ad8aded887c64b24732808757bddae41d` | NemaNode `connections/white_1986_whole.json`, blob `75a28a2706b0834dca9420343f57213e83ce3894` | G |
| `nemanode_da8ca7e__neurons.json` | 58575 | `c780e0b7cab28b311a7e0916a7b8e37b9cf72de152712bd4a5eb29fd9d595492` | NemaNode `neurons.json`, blob `81da4572b20674dcc852cfa9fd041e66a3c7a73c` | G |
| `white_1986_jsh.csv` | 39065 | `afe7a37a5bae62630a773b5e7815a408e3a72063caf0ed49ecc91e213077fb12` | Toolbox `white_1986_jsh.csv`, blob `15577df82afdc9c842ae2a661bbd2ad55651dece` | G |
| `white_1986_n2u.csv` | 41889 | `6b63f6c0281b7bbc3be75fa3962e26caa020ddf3756bfc8dd9aad6577655fc16` | Toolbox `white_1986_n2u.csv`, blob `945003a9949c73c98bd2ad90003ac5fd16f693d8` | G |
| `cect__aconnectome_white_1986_whole.csv` | 67453 | `c8aac78756b71f6337629951e5f4211448e85d148f6db9b367b2cd0450bb403a` | Toolbox `aconnectome_white_1986_whole.csv`, blob `3b96800baa602180a6a49f704695df37df775586` | G |
| `cect__aconnectome_white_1986_L4.csv` | 40834 | `f2b709afa7b7997dff7482999af189971f79203f9df1db184a37ced86cb0127d` | Toolbox `aconnectome_white_1986_L4.csv`, blob `aadcc1ff705708af4b8248e18486f75d8863d329` | G |
| `cect__aconnectome_white_1986_A.csv` | 43790 | `09284a374c3c30f6c806ea4dbbbb33da2e735d1891893a3f1fd65ada1e565123` | Toolbox `aconnectome_white_1986_A.csv`, blob `442f160c9a10830c7d75a238528a2ed1f648f467` | G |
| `neurodata.txt` | 223795 | `e4cd6f02499a8cce7b780fa11076645b443ba509001782ae5844ff0b4d27b56c` | Toolbox `neurodata.txt`, blob `b137a51be4011b138dc81e3b40fd5153b5e42a6c` | G |
| `neurodata_updated.txt` | 226307 | `d420e9472e2cd2d62b3ed78211cc3e56a90e1e6ccbb00fab442b464bd30c1f37` | Toolbox `neurodata_updated.txt`, blob `da9ff80371b713f1609e2967064c44bb6c0b23ba` | G |
| `NeuronConnect.xls` | 518144 | `b5e32612967ff277c91ba37463bd03a85678bd8e65a4861abc6516323b6ff5f3` | Toolbox `NeuronConnect.xls`, blob `898ba5408669a4c27467554591dd69c73b571b41` | G |
| `41586_2019_1352_MOESM9_ESM.xlsx` | 4172457 | `86d3f24c77752b1f7df4b26cdf9583461fe7e8fc76f86d2d81b3879cdaa0e389` | Toolbox `41586_2019_1352_MOESM9_ESM.xlsx`, blob `b7a225693bde9aa198f39c69561c37e6a53b3892` | G |
| `SI 5 Connectome adjacency matrices.xlsx` | 4367796 | `559989daa02cd9a76e9266537a6b80bfd47d338cb5d397d11296288629df364a` | Toolbox, same name, blob `9e4f34968eb0f9436ab351c44c34a13a06379d07` | G |
| `SI 5 Connectome adjacency matrices, corrected July 2020.xlsx` | 4188190 | `1f4fdbf84746b69b49a8da0816f52787860ce349b638dce37924ba80f90c70c9` | Toolbox, same name, blob `4d53c16e9a07c1ecfd068a02b39ccffd6b8a3eaa` | G |

Re-running `python -m src.acquire white1986` verified all 20 files without re-downloading any of them. Data-file mtimes were unchanged and `MANIFEST.json` was rewritten byte-identically.

### Byte-level relationships between copies

These are computed by `record_counts` (`_relationships`) unless marked (scratch).

| Copies | Relationship |
|---|---|
| `wna__aconnectome_white_1986_L4.csv` = `white_1986_jsh.csv` | **identical bytes** (same SHA-256, same git blob `15577df8`) |
| `wna__aconnectome_white_1986_A.csv` = `white_1986_n2u.csv` | **identical bytes** (same SHA-256, same git blob `945003a9`) |
| same two, vs `Nondairy-Creamer/Creamer_LDS_2026@bba43302` `anatomical_data/worm_connectomes/white_1986_{jsh,n2u}.csv` (not acquired) | identical git blobs (scratch: `git ls-tree`). That README says: "Connectome data was downloaded from [NemaNode](https://nemanode.org/) on November 1st, 2025." So a 2025 NemaNode download is byte-identical to the copy Randi shipped in 2023. |
| wheel `aconnectome_white_1986_{whole,A,L4}.csv`, `aconnectome.json` vs `leiferlab/pumpprobe@1dbc5e0a` `pumpprobe/` (not acquired) | identical SHA-256 (scratch) |
| `cect__aconnectome_white_1986_whole.csv` vs `wna__…_whole.csv` | identical after CRLF→LF. The toolbox copy uses CRLF line endings (+2961 bytes); neither ends with a newline. |
| `cect__aconnectome_white_1986_L4.csv` vs `wna__…_L4.csv` | identical after CRLF→LF (+1769 bytes) |
| `cect__aconnectome_white_1986_A.csv` vs `wna__…_A.csv` | not identical after CRLF→LF. Line 1 (the header) is `pre post type synapses` with spaces instead of tabs, and the toolbox copy adds a final CRLF. All 1899 data lines are identical. |
| NemaNode JSON (`nemanode_da8ca7e__white_1986_{n2u,jsh,whole}.json`) → wheel CSVs | **NemaNode's own export rules, applied to the JSON, reproduce each wheel CSV exactly** (`nemanode_json_export_equals_csv`: all true). The rules are `populate-connections.js` (weight = `len(syn)`, electrical reverse duplicates skipped) and `db/download-data.js` (keep names in `neurons.json`). The pre-da8ca7e blobs (`859641e`, not acquired) do not reproduce them: n2u differs in 2 chemical rows (ADEL→RMGL 3 vs 1; ADER→RMGR 2 vs absent), and jsh in 5 rows that the CSV lacks (ADLL→ASHL 3, AIAL→ASKL 1, AIAR→ASKR 1, DVA→AIZL 1, DVA→AIZR 1). |
| `neurodata_updated.txt` vs `neurodata.txt` | content edit: 1 record removed (`ADAL ADAR Gap_junction` with no series); 20 records added (that record with series N2U, plus 19 reverse-direction gap junctions); 1 changed (`RIML AVAR Gap_junction JSH` 5 → 6). Comment and blank lines added. |
| `41586_2019_1352_MOESM9_ESM.xlsx` vs `SI 5 Connectome adjacency matrices.xlsx` | different bytes. All three hermaphrodite sheets have identical labels and values. Male sheets: ray structural cells renamed `R*st*` → `R*sh*` (7 chemical columns; 11 gap rows/columns), and chemical row `RMFL` relabelled `RMFR`, which duplicates the `RMFR` label. |
| `SI 5 … .xlsx` vs `SI 5 …, corrected July 2020.xlsx` | different bytes and content. Hermaphrodite chemical: column `hmc` added, no value changes. Hermaphrodite gap: row/column `int` added; 11 symmetric-sheet and 13 asymmetric-sheet label pairs changed; sheets renamed `herm gap jn …` → `hermaphrodite gap jn …`. Male: `R*sh*` → `R*st*` restored, `RMFL` restored, `int` added, 9 (symmetric) and 8 (asymmetric) gap changes. Symmetric-sheet changes (scratch listing): added PVDL↔hmc 400 and PVDR↔hmc 400; removed BDUL↔PLML 23 and BDUR↔PLMR 23; DD06↔PDB, ALA↔exc_gl and VA09↔PVCR made symmetric. These agree with the toolbox's `cect/validation/CookEtAl2019.md`. |

## What each file contains

**NemaNode exports** (`wna__*`, `cect__*`, `white_1986_{jsh,n2u}.csv`)

- Tab-separated despite the `.csv` suffix. Header `pre post type synapses`. One row per (pre, post, type); `type` is `chemical` or `electrical`; `synapses` is an integer > 0.
- Chemical rows are oriented pre → post.
- **Gap junctions: each unordered pair is listed once, in arbitrary orientation (first-seen in the JSON).** Self-pairs exist: RIBL–RIBL and RIBR–RIBR in A and L4; M4, M5, RIBL, RIBR, RID and VA8 in whole.
- Summing `synapses` over electrical rows gives the single-counted total. A symmetric matrix built from them sums to 2×total − self.
- Randi's loader (`_get_aconnectome_witvliet`, used for all White CSVs) symmetrises the gap matrix with `max(gap[i,j], gap[j,i])`.
- Names are not zero-padded (VA1). AWCL/AWCR are used.

Per-file contents:

- **`_A` / `white_1986_n2u`** (N2U, adult, head): 221 names, of which 186 are plain A-Z0-9. The rest are 32 `BWM-[DV][LR]0n` muscles and `CEPshDR/VL/VR` glia.
- **`_L4` / `white_1986_jsh`** (JSH, L4, head): 215 names (181 plain; 32 BWM, CEPshVL/VR).
- **`_whole`**: 309 names (306 plain, plus `LegacyBodyWallMuscles`, `pm1`, `pm4`). It covers the whole animal, including the ventral cord, tail and pharynx. All NMJs go to the single pseudo-node `LegacyBodyWallMuscles`.

NemaNode's own help text describes these datasets. It is in the NemaNode repository at `da8ca7e`, `src/client/webpack-template.index.html` (https://github.com/zhenlab-ltri/NemaNode/blob/da8ca7e2fc0eece4b21c30625880b41f39961c76/src/client/webpack-template.index.html):

> "White et al., 1986, JSH and N2U — The two datasets were reconstructed by White et al., 1986 and compiled by Durbin, 1987. Individual muscle cells were not annotated by White et al., 1986. To allow comparison to other datasets, individual muscle cells (and synapses onto them) were annotated in scans of the original EM micrographs by the Zhen Lab. These synapses have been added to the datasets instead of the originally listed anonymous neuromuscular junctions."
>
> "White et al., 1986, compilation — This dataset is a compilation of multiple partially overlapping animals. The cells making up the somatic nervous system were reconstructed by White et al., 1986 and compiled by Varshney et al., 2011. The cells making up the pharyngeal nervous systems were reconstructed by Albertson and Thomson, 1976 and cleaned up by Nikhil Bhatla, developer of WormWeb.org. Non-neuronal cells were not annotated individually but are grouped by cell type (e.g. Body wall muscles)."

`datasets.json` in the same repository gives the `white_1986_whole` description "Whole adult compiled by Varshney et al., 2011". For `white_1986_n2u` it gives "Adult legacy dataset<br />Muscles: <i>Zhen lab, 2020</i>".

**How Randi et al. used these.** Both `leiferlab/pumpprobe@1dbc5e0a` `pumpprobe/Funatlas.py` and the wheel's `NeuroAtlas.py` declare:

```
{"type": "whiteA",  "fname": "aconnectome_white_1986_whole.csv"},
{"type": "whiteL4", "fname": "aconnectome_white_1986_L4.csv"},
{"type": "witvliet", "fname": "aconnectome_witvliet_2020_7.csv"},
{"type": "witvliet", "fname": "aconnectome_witvliet_2020_8.csv"}
```

- The source labelled `whiteA` loads **`_whole`**, the multi-animal compilation, not `_A` (N2U). `_A` is loaded by no code in either repository.
- The four sources are summed (`average=False`), then thresholded with `chem <= chem_th → 0` and `gap <= gap_th → 0`.
- `pumpprobe` defaults to `chem_th=3, gap_th=2`, and the wheel to `0, 0`. The paper scripts in `pumpprobe/scripts` (e.g. `Numbers_script.py`, `funatlas_vs_anatomy.py`) call `load_aconnectome_from_file(chem_th=0, gap_th=0)`.

**NemaNode JSON** (`nemanode_da8ca7e__*.json`)

- Lists of records `{pre, post, typ, syn[, ids, pre_tid, post_tid]}`. `typ` is 0 (chemical) or 2 (electrical).
- Gap junctions are listed in both directions (n2u 538 records, jsh 576, whole 1144, each with 2 or 6 self-records).
- n2u: the number of `syn` entries (5210) differs from the sum of `syn` values (5213). NemaNode counts entries.
- `whole` contains 10 names that are not in `neurons.json`: `DefecationMuscles`, `G1`, `G2`, `mc2`, `mc3`, `pm2`, `pm3`, `pm5`, `pm6`, `pm7`. The CSV export therefore drops 19 rows (weight 246) of pharyngeal neuron → pharyngeal muscle/gland connectivity. `pm1` and `pm4` survive.

**Durbin `neurodata.txt`**

- Whitespace-separated `name1 name2 type series count`.
- Types: `Send`, `Send_joint` (polyadic), `Receive`, `Receive_joint`, `Gap_junction`. Series: `N2U` or `JSH`.
- Send-type records are name1 → name2; Receive-type are name2 → name1. Each synapse was recorded from both partners, so send-side and receive-side totals are **alternatives, not additive** (N2U 4056 vs 3768; JSH 4000 vs 3714).
- Gap junctions are listed in both directions, with gaps: N2U has 16 records without a reverse, and JSH has 4, plus one pair with unequal weights (AVAR|RIML 6 vs 5).
- Pseudo-names: `mu_bod` (anonymous body-wall muscle, i.e. NMJ), `hyp` (hypodermis), and `CEPsh*`.
- One record (`ADAL ADAR Gap_junction <blank> 1`) has no series.
- The file includes retrovesicular/ventral-cord cells (DA1, DB1, SABD, SABVL, VA2, VB1, VB2, VC1–3, VD1) that the NemaNode versions drop.

**`neurodata_updated.txt`**: the toolbox's edited copy (see the relationship table). It is not a published dataset.

**Varshney `NeuronConnect.xls`**

- One sheet `NeuronConnect.csv`, 6417 rows, columns `Neuron 1, Neuron 2, Type, Nbr`.
- Types: S, Sp (send, polyadic), R, Rp (receive), EJ, NMJ.
- R+Rp mirrors S+Sp exactly, except one synapse whose receive record is written in lower case (`avfl avfr Rp 1` vs `AVFR AVFL Sp 1`).
- EJ is listed in both directions, fully symmetric, with 3 self-pairs (RIBL, RIBR, VA08).
- NMJ rows have `Neuron 2` = `NMJ`. 38 neurons have two NMJ rows.
- 3 rows have Nbr 0: `AVFL VB01 Sp 0`, `FLPR VB01 Sp 0`, `VB01 AVFL Rp 0`.
- Names are zero-padded (VA01). No pharynx.

**Cook 2019 SI 5** (three workbooks)

- Each sheet is a matrix: row 3 holds column labels from column D; column C holds row labels from row 4. Chemical sheets have rows as presynaptic and columns as postsynaptic cells.
- Row 1 / column A hold group labels (PHARYNX, SENSORY NEURONS, …). Row 2 / column B hold sub-group labels (layer numbers 6…1, HEAD/SUBLATERAL/BODY MOTOR NEURONS, BODYWALL MUSCLES, …). The last column and last row repeat the labels, with occasional disagreements (e.g. `vm2AL` vs `vm2aL`, `pm8` vs `pm9`, missing `CANL`/`CANR`/`exc_cell`).
- The legend sheet reads: "Weights in the body of the matrices are the total number of EM serial sections of connectivity, taking into account both the number of synapses and the sizes of synapses. To provide complete coverage of the entire nervous system, the data are assembled from multiple animals and include connections added by extrapolation in gaps where no data were available."
- **Weights are therefore not synapse counts.**
- The corrected 2020 legend adds: "for the gap junction tables, values across the diagonal should match and be consistent with the values in the asymmetric tables."
- Hermaphrodite chemical has 300 presynaptic rows (all 302 neurons except CANL/CANR) and 453 or 454 columns.
- In the original files, the gap "symmetric" sheets have 4 cells without an equal mirror, and the "asymmetric" sheets list 3 pairs in both directions. The corrected file fixes both.

**`aconnectome.json` + `aconnectome_ids.txt`**

- Keys `chemical` (300×300), `electrical` (300×300) and `chemical_sign` (300-vector: −1 for 26 ids, namely DD1–6, VD1–13, RME×4, AVL, DVB, RIS).
- Indexed by pumpprobe's `aconnectome_ids.txt` (AWCL/AWCR). `chemical[i][j]` is ids[i] → ids[j]; pumpprobe `Anatlas._load_aconnectome_white` transposes it.
- Scratch comparison against `NeuronConnect.xls`, after removing zero-padding (VA01→VA1) for the comparison only:
  - The **electrical matrix equals Varshney EJ** for all 1031 directed entries.
  - The **chemical matrix equals Varshney with each Sp row overwriting the S row of the same pair** instead of being added. All 2194 Varshney pairs agree with that rule (including two pairs zeroed by Nbr-0 Sp rows); only 1813 agree with S+Sp.
  - 84 extra pharyngeal pairs (sum 200) are present; only 7 of them equal `_whole`.
- It is not loaded by the published analysis: the `white` entry in `Funatlas.aconn_sources` is commented out.

**Scratch lineage comparisons** (one-off scripts in the session scratch dir; names compared after removing Varshney's zero-padding):

- **`_whole` vs Varshney.**
  - All 2194 Varshney S+Sp ordered pairs are in `_whole` with equal weight. `_whole` adds 78 pharyngeal chemical pairs (weight 144).
  - All 517 Varshney EJ unordered pairs (incl. self) are in `_whole` with equal weight. `_whole` adds 58, mostly pharyngeal, plus BDUL/R–PLML/R, GLR–RME and RID–RID.
  - `LegacyBodyWallMuscles` NMJ rows cover 114 neurons, weight 1405. Varshney's NMJ rows cover 115 neurons, weight 1410: **DVB's 5 NMJs are missing in `_whole`.**
- **NemaNode n2u/jsh vs Durbin N2U/JSH.**
  - Neuron→neuron chemical pairs present in both have equal weight to Durbin's send side (n2u 1409/1409; jsh 1285/1287). The exceptions are JSH IL1L→RMDDL (3 vs 2) and RMHL→RMDR (3 vs 2).
  - NemaNode renames the head processes of **DVB to PVT**. This is the DVB/PVT swap correction noted in Varshney 2011 and Cook 2019 per the toolbox docs.
  - NemaNode drops DA1, DB1, SABD, SABVL, VA2, VB1, VB2, VC1–3, VD1, `hyp` and `mu_bod`, and adds BWM-* muscle targets. JSH also gains RIGR→PLNR 1, SIAVR→SAADR 4 and URYVR→RMDL 1.
- **`_whole` vs `_A` on the 186 shared names.**
  - Every `_A` chemical pair is in `_whole` (1376/1414 with equal weight); `_whole` has 103 more.
  - Every `_A` gap pair is in `_whole` (261/270 equal); `_whole` has 25 more.
  - `_whole` vs `_L4` overlap far less: 834 shared chemical pairs, 234 equal.

## Record counts

All "count in acquired file" values come from `python -m src.acquire --counts white1986`. Three runs of the final module gave byte-identical output (sha256 of the printed JSON `c3351272ce5d6889c2a229105e4573f240e58c938749af6b411db122a43ae7dd`). The paper excerpts were obtained through the WebSearch tool, because the journal hosts are blocked; the excerpt text is quoted as the tool returned it.

| Quantity | Definition | Count in acquired file | Paper reports | Where the paper reports it | Match |
|---|---|---|---|---|---|
| White 1986 total chemical synapses / NMJs / gap junctions | approximate whole-animal estimates | not computed: no file holds White's own whole-animal tally | "about 5,000 chemical synapses, 2,000 neuromuscular junctions, and 600 gap junctions" (search-tool summary of the abstract via https://scholarhub.vn/publication/:slug/e37ad51d-aaea-4f34-bc62-4fbb89c6ad10). A second search returned "approximate figures of 2000 neuromuscular junctions, 5000 chemical synapses between neurons, and 700 gap junctions" (unattributed). | abstract (not reached directly) | UNVERIFIED: the two excerpts disagree (600 vs 700) and the text was not reached. NOT COMPARABLE in any case, since these are estimates for a typical animal and every file is a partial or compiled reconstruction. |
| White 1986 neuron count | 302 neurons, hermaphrodite | no file classifies neurons; see per-file name counts below | "the connectivity of each of the 118 classes of neurons in the 302-neuron nervous system of the adult of one sex, the hermaphrodite was published" (search excerpt of Emmons 2015 commentary, https://royalsocietypublishing.org/rstb/article/370/1666/20140309/22515/The-beginning-of-connectomics-a-commentary-on) | commentary, not the paper | NOT COMPARABLE (the neuron set is decided in Phase 2) |
| Varshney 2011 neurons | distinct plain A-Z0-9 names in S/Sp/R/Rp/EJ rows with Nbr > 0 (`NeuronConnect.xls`) | **279** (VC06 occurs only in an NMJ row; `avfl`/`avfr` lower-case tokens excluded) | "After excluding CANL/R and VC06, which make no synapses, it keeps the remaining 279 somatic neurons" (search-tool summary of arXiv:0907.2373v4, https://arxiv.org/html/0907.2373v4) | Varshney et al., Results (arXiv v4 author version) | YES (against the author preprint excerpt; PLoS text not reached) |
| Varshney 2011 chemical synapses | sum of Nbr over S+Sp rows (`chemical_S_plus_Sp.weight`); R+Rp mirrored gives the same | **6394** | "The v4 HTML reports 6393 chemical synapses, 890 gap junctions, and 1410 neuromuscular junctions" (search excerpt of https://arxiv.org/html/0907.2373v4). Also 2016 PLOS Comput Biol paper: "279 neurons with 6,393 chemical synapses and 890 electrical junctions" (https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1005084) | arXiv v4; repeated by later papers | **NO — BLOCKER** (off by 1; Varshney candidate only). The only internal inconsistency found is the AVFR→AVFL synapse whose receive-side record is written `avfr`/`avfl`; that may explain it but is unverified. |
| Varshney 2011 gap junctions | EJ weight summed once per unordered pair, self-pairs included (`EJ.weight_sum_over_unordered_pairs_taking_max_direction`) | **890** (summed over both listed directions: 1777) | 890 (same excerpts as above) | arXiv v4 | YES |
| Varshney 2011 gap-junction connections | unordered EJ pairs excluding self (`EJ.unordered_pairs_excl_self`) | **514** (517 incl. 3 self) | "The gap junction network that we analyze consists of 279 neurons and 514 gap junction connections, consisting of one or more junctions" (search excerpt, arXiv:0907.2373 / journal.pcbi.1001066) | Varshney et al., Results | YES |
| Varshney 2011 NMJs | sum of Nbr over NMJ rows | **1410** (153 rows, 115 neurons) | 1410 (same arXiv v4 excerpt) | arXiv v4 | YES |
| Varshney dataset directed chemical connections | ordered pairs with S+Sp > 0 | **2194** | "There are 2194 unique directed chemical synapses and 514 unique undirected gap junctions" (2026 PLOS Comput Biol paper using the Varshney dataset, https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1014152, via search excerpt) | a third-party paper, not Varshney 2011 | UNVERIFIED (agrees, but it is not the paper's own statement) |
| Cook 2019 hermaphrodite chemical edges | nonzero cells in sheet `hermaphrodite chemical` | **4879** in all three workbooks | "respective graphs have 4,887 chemical (or directed) edges and 1,447 gap junction (or undirected) edges in the hermaphrodite and 5,315 chemical and 1,755 gap junction edges in the male" (search excerpt attributed to https://www.nature.com/articles/s41586-019-1352-7 / PubMed 31270481 / ResearchGate) | Cook et al. 2019, main text | **NO — BLOCKER** (8 fewer; Cook candidate only). The workbook has no explicit zero cells and no stray cells. The analogous gap definition matches exactly (next row), so the cause is unexplained. |
| Cook 2019 hermaphrodite gap-junction edges | nonzero cells in the herm gap **asymmetric** sheet | **1447** (Nature, WormWiring original); **1450** (corrected 2020) | 1,447 (same excerpt) | main text | YES for the as-published files (the corrected file differs by +3) |
| Cook 2019 male chemical edges | nonzero cells in `male chemical` | **5306** | 5,315 (same excerpt) | main text | **NO — BLOCKER** (9 fewer; male, out of project scope but reported) |
| Cook 2019 male gap-junction edges | nonzero cells in male gap asymmetric sheet | **1755** (orig.), 1758 (corrected) | 1,755 (same excerpt) | main text | YES for the as-published files |
| Cook 2019 hermaphrodite nodes | union of labels over the three herm sheets | **473** (all occur in a nonzero cell); per sheet 453 (chemical) / 468 (gap) | "460 nodes (302 neurons, 132 muscles and 26 non-muscle end organs)" (toolbox `docs/Cook_2019.md` and search excerpt of the abstract) | abstract | NOT COMPARABLE: the label set includes cells the paper may group or count differently; splitting into neurons, muscles and end organs needs the Phase-2 cell classification |
| Durbin 1987 H-series totals | — | N2U send-side 1486 pairs / 4056; JSH 1350 / 4000; gap junctions over unordered pairs N2U 347, JSH 775 | "3,462 chemical synapses and 754 gap junctions among 183 neurons in one database" (search-tool summary of https://ftp.sanger.ac.uk/pub/resources/theses/durbin/chapter7.pdf; definition of the database not given) | thesis ch. 7 | UNVERIFIED (definition unknown; likely NOT COMPARABLE) |

Per-file counts with no paper counterpart (raw facts; definitions are in the module docstrings):

| File | Names (plain A-Z0-9) | Chemical: rows / weight | Chemical to muscle pseudo-nodes | Chemical, both names plain: rows / weight | Electrical as listed: rows / weight | Electrical unordered pairs (self) / weight once per pair |
|---|---|---|---|---|---|---|
| `wna__…_whole.csv` (= cect__ after CRLF→LF) | 309 (306) | 2386 / 7943 | 114 rows / 1405 to `LegacyBodyWallMuscles` | 2266 / 6509 | 575 / 971 (listed once) | 575 (6) / 971; mirrored matrix sum 1928 |
| `wna__…_A.csv` = `white_1986_n2u.csv` | 221 (186) | 1629 / 4538 | 205 / 788 to `BWM-*` | 1414 / 3740 | 270 / 337 | 270 (2) / 337; mirrored 672 |
| `wna__…_L4.csv` = `white_1986_jsh.csv` | 215 (181) | 1480 / 4340 | 176 / 620 to `BWM-*` | 1293 / 3704 | 289 / 763 | 289 (2) / 763; mirrored 1522 |
| `neurodata.txt` N2U | 202 | send 1486 / 4056; receive-mirrored 1429 / 3768 | 39 pairs / 270 to `mu_bod` | send 1433 / 3772 | 540 / 675 (both directions; 16 lack reverse) | 279 (2) / 347 |
| `neurodata.txt` JSH | 190 | send 1350 / 4000; receive-mirrored 1308 / 3714 | 41 / 280 to `mu_bod` | send 1295 / 3701 | 582 / 1537 (4 lack reverse; 1 unequal) | 294 (2) / 775 |
| `neurodata_updated.txt` | as above | as above | as above | as above | N2U 556 / 692; JSH 586 / 1546 (all reversed) | N2U 279 (2) / 347; JSH 294 (2) / 775 |
| `NeuronConnect.xls` | 283 tokens (279 plain in nonzero non-NMJ rows) | S+Sp 2194 pairs / 6394 | NMJ 153 rows / 115 neurons / 1410 | — | EJ 1031 / 1777 (both directions) | 517 (3) / 890 |
| `aconnectome.json` | 300 ids | 2276 nonzero / 5862 | — | — | 1096 nonzero / 1864 | 568 (5) / 963; 35 entries lack a mirror, 6 pairs unequal |
| Cook Nature = WW original (herm) | 300 rows × 453 cols (chem); 468 × 468 (gap) | 4879 cells / 28113 sections; 38 diagonal | — | post label also a row label: 3707 / 20905 | symmetric 2881 cells / 21801 (4 without equal mirror); asymmetric 1447 / 10923 | — |
| Cook corrected 2020 (herm) | 300 × 454; 469 × 469 | 4879 / 28113 | — | 3707 / 20905 | symmetric 2883 / 23313 (fully symmetric); asymmetric 1450 / 11680 | — |

Cross-checks against the toolbox's own derived counts (not paper counts; `cect/validation/*_expected_data.yaml` at the pinned commit) all agree:

- `White_whole`: Generic_CS 2386 / 7943 and Generic_GJ 1144 / 1928. The GJ figures equal this file's mirrored rows and weight.
- `DurbinN2U` 1486 / 4056 and GJ 556 / 692; `DurbinJSH` 1350 / 4000 and GJ 586 / 1546.
- `Cook2019Herm` (corrected) 4879 / 28113 and GJ 2883 / 23313.

## Discrepancies, flags and open questions

**Blockers (report, do not explain away)**

1. **Cook 2019 chemical edge counts do not match the paper:** 4879 vs 4,887 (herm) and 5306 vs 5,315 (male), in all three workbooks. Gap-edge counts match exactly under the analogous definition (asymmetric-sheet nonzero cells: 1447 / 1755), so the definitional mapping is probably right. The paper number was read only through a search excerpt and must be re-checked against the Nature text. This blocks only if Cook 2019 is chosen.
2. **Varshney 2011 chemical synapse total is 6394 in the file vs 6393 reported** (arXiv v4 excerpt and two later papers). It blocks only if Varshney/`_whole` is chosen; `_whole` reproduces Varshney's 6394 exactly.

**Flags for the owner**

3. **Randi's "whiteA" is not White N2U.** The search excerpt of Randi's Methods says: "considered a neuron directly anatomically connected if the connectomes of any of the four L4 or adult individuals in refs. 1 and 6 contained at least one synaptic contact" (search-tool rendering of the Methods of https://www.nature.com/articles/s41586-023-06683-4; verbatim wording not verified, since the text was not reached). The code instead loads `_whole`, a multi-animal compilation that is Varshney 2011 plus pharynx, under the label `whiteA`. The N2U individual (`_A`) is shipped but never loaded.
   - On the 186 names `_A` and `_whole` share, `_whole` contains every `_A` chemical and gap pair and adds 103 chemical and 25 gap pairs.
   - Reproducing Randi means `_whole + _L4`. Following the Methods text means `_A + _L4`. **Owner decision.**
4. **Gap-junction encoding differs by file** (see "What each file contains"). Any "total gap junctions" figure must state single- vs double-counting and whether self-pairs (RIBL–RIBL etc.) are kept. **Owner decision** for `anat_gap`: weight convention, and whether to apply Randi's max-symmetrisation.
5. **NemaNode N2U/JSH ≠ Durbin N2U/JSH.**
   - NemaNode renames head DVB → PVT (a correction).
   - It drops retrovesicular/ventral-cord cells and `hyp`, and replaces `mu_bod` with Zhen-lab BWM annotations.
   - It changes 2 JSH weights and adds 3 JSH edges.
   - Durbin's file is closer to White's notebooks; NemaNode's is curated. **Owner decision**, including which name, DVB or PVT, to trust for those edges.
6. **`_whole` loses pharyngeal targets on export** (19 rows, weight 246, to `DefecationMuscles`, `G1`, `G2`, `mc2`, `mc3`, `pm2/3/5/6/7`). It also lacks DVB's 5 NMJs relative to Varshney. Irrelevant to neuron→neuron head edges, but `_whole` is not a lossless copy of the NemaNode data.
7. **Cook 2019 weights are EM serial-section counts (size-weighted), not synapse counts.** They are not comparable with White/Durbin/Varshney/NemaNode counts. There are three versions; the corrected 2020 file changes 11 hermaphrodite gap-junction cells, including two 400-section PVD–hmc entries and removal of two 23-section BDU–PLM entries. **Owner decision** on which version, if Cook is used.
8. **`neurodata_updated.txt` is an OpenWorm edit, not a published dataset.** Use `neurodata.txt` if Durbin is chosen, and decide how to treat the 20 one-directional gap-junction records.
9. **`aconnectome.json` looks like a processing artefact.** Its chemical matrix equals Varshney with S overwritten by Sp (S counts lost wherever both exist). It has no documented provenance and Randi's published analysis does not use it. It is acquired only so the owner can see it. Recommend not using it; that is the owner's call.
10. Naming quirks to resolve in Phase 2, without changing raw data:
    - Varshney `avfl`/`avfr` lower-case; zero-padded names in Varshney and Cook.
    - Cook male `R*st*`/`R*sh*` and a duplicate `RMFR`.
    - Cook echo-label disagreements (`vm2AL`/`vm2aL`, `pm8`/`pm9`).
    - NemaNode n2u: 3 `syn` entries whose value is not 1 (5213 vs 5210).
11. AWC: every file here uses AWCL/AWCR, while the atlas uses AWCON/AWCOF (Q-005 applies).

**Open questions** (proposed for `docs/decisions.md`; not decided here)

- Q-007 (refined): which White variant feeds `anat_chem_white` / `anat_gap`? The candidates are:
  - (a) Randi's exact inputs, `_whole` ("whiteA") + `_L4`;
  - (b) the NemaNode individuals `_A` (N2U) + `_L4` (JSH), as Randi's Methods describe and as Creamer used;
  - (c) Durbin `neurodata.txt` N2U/JSH, with send- or receive-side counts;
  - (d) Varshney 2011;
  - (e) Cook 2019, in one of three versions;
  - (f) separate columns per individual.
- Gap-junction weight convention and self-pairs (flag 4).
- DVB vs PVT for head edges (flag 5).
- Whether the Cook 2019 and Varshney 2011 count mismatches (blockers 1–2) need resolving before either can be used.

**Not acquired** (and why)

- Wheel `aconnectome_default.h5`: Randi's precompiled sum of `_whole` + `_L4` + Witvliet 7 + 8. It is not a White variant; it belongs with the combined Randi connectome (randi2023 / witvliet2021 owners).
- NemaNode `white_1986_{n2u,jsh}.json` at `859641e` (and older `b6dfd28`, `8a50236`): superseded on 2020-05-22. Their differences are listed above. The wheel and the 2025 NemaNode download both equal the later version.
- NemaNode `white_1986_jse.json`: JSE adult tail series (Hall & Russell 1991 compilation); no head edges.
- Creamer_LDS_2026 and pumpprobe copies: byte-identical to acquired files (same blob or SHA-256), cited as evidence only.
- Toolbox `NeuronConnectFormatted.xlsx`: OpenWorm reformat of `NeuronConnect.xls` (de-padded names, some rows re-oriented); not read by the Varshney reader.
- Toolbox `CElegansNeuronTables.xls`: reader says "legacy dataset (based on White_whole) used in the past in OpenWorm. Only included here for reference! Do not use!"
- Toolbox `herm_full_edgelist*.csv`: "legacy dataset (based on Cook et al. 2019) … Do not use!"
- Toolbox `CeConnMtrcs_170626.mat`: Haspel & O'Donovan 2011 ventral-cord model; no head data.
- Toolbox `cect/cache/*.json`: toolbox-processed caches.
- Cook et al. 2019 per-series re-annotation of N2U/JSH on WormWiring: NOT FOUND in any reachable distribution (wormwiring.org blocked).
- All primary copies (nemanode.org, wormatlas.org, nature.com/springer, wormwiring.org): hosts blocked.
