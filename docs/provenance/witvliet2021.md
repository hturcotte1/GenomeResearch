# witvliet2021: Brain connectomes across development (adult datasets 7 and 8)

- Paper: Witvliet D, Mulcahy B, Mitchell JK, et al. *Connectomes across
  development reveal principles of brain maturation.* Nature 596, 257–261
  (2021). doi:10.1038/s41586-021-03778-8
- Module: `src/acquire/witvliet2021.py`
- Status: **SECONDARY — primary comparison PENDING (blocks Phase 4 freeze)**
- Retrieval date (UTC): 2026-10-11, for all 13 files, from
  `data/raw/witvliet2021/MANIFEST.json`

## Primary location (not reachable from this environment)

- **Journal:** https://www.nature.com/articles/s41586-021-03778-8, Supplementary
  Information. The supplementary tables, per a web-search excerpt (wording not
  confirmed on the page):
  - Supplementary Table 2: "synapse number connectivity matrix";
  - Supplementary Table 3: "synapse size matrix";
  - Supplementary Table 4: "physical contact matrix";
  - Supplementary Table 5: synapses onto spine-like protrusions.

  The ConnectomeToolbox (`cect/validation/WitvlietEtAl2021.md`) links
  `41586_2021_3778_MOESM4_ESM.xlsx` as "connectivity matrices … only contain
  the chemical connections". Which MOESM file is which table is unverified.
- **Data portal:** https://nemanode.org/, dataset ids `witvliet_2020_7` and
  `witvliet_2020_8`. Per a web-search excerpt of the paper's data
  availability statement: "Connectivity matrices for all datasets are
  available at http://www.nemanode.org and as Supplementary Tables."
- **WormWiring:** https://wormwiring.org/pages/witvliet.html. The toolbox
  says the per-dataset xlsx files came from here.
- **EM images and volumes:** https://bossdb.org/project/witvliet2020 (from the
  same excerpt). Not needed here.

Primary checks to perform once reachable:

1. Download the Nature ESM files. Compare `synapse_count_matrices.xlsx`,
   `synapse_list.csv`, `connection_classifications.csv` and `_neurons.csv`
   with the matching Supplementary Tables, byte for byte or cell for cell.
2. Download datasets 7 and 8 from nemanode.org and compare them with
   `nemanode_baf8ec8__*.json`.
3. Download the WormWiring xlsx and compare them with the toolbox copies.

How each acquired file relates to the primary copies:

| Acquired file | Corresponding primary copy |
|---|---|
| `aconnectome_witvliet_2020_{7,8}.csv` | none current. This is the 2020-05-22 NemaNode content, which the authors replaced; nemanode.org presumably no longer serves it (unverified) |
| `nemanode_baf8ec8__witvliet_2020_{7,8}.json`, `nemanode_baf8ec8__neurons.json` | nemanode.org datasets 7 and 8 and its cell table |
| `nemanode_859641e__witvliet_2020_{7,8}.json` | the superseded 2020-05-22 NemaNode content |
| `witvliet_2020_{7,8} adult.xlsx` | WormWiring spreadsheets |
| `synapse_count_matrices.xlsx`, `synapse_list.csv`, `connection_classifications.csv`, `_neurons.csv` | Nature Supplementary Tables (exact mapping unverified) |

## Files acquired

Four secondary distributions are used:

- **(A)** PyPI wheel `wormneuroatlas` 0.0.7.3, already declared project-wide.
  Its SHA-256 equals PyPI's published digest (checked live), and each member
  matches the wheel's `RECORD`.
- **(B)** GitHub `openworm/ConnectomeToolbox` @ `ffe570268b7cffb9329cd009a1bb37d60db2d465`.
- **(C)** GitHub `zhenlab-ltri/NemaNode`, the Zhen lab's source repository for
  nemanode.org, declared in the module. Two commits are pinned:
  - `859641e20748f5313a99eaa862227ae9f6d369ca` (2020-05-22, "Renamed datasets
    to be consistent with manuscript");
  - `baf8ec877455890d089d965d1a0b3ea0db110e9f` (2021-03-15, by
    daniel.witvliet@gmail.com, "Updated witvliet datasets after paper
    revision").

  The repository's master head `6b7ca03f6d68c4ea1af3c120d1a47681edc74a90`
  (2022-03-16) has the same blobs as `baf8ec8`. Only these two commits ever
  touched `connections/witvliet_2020_{7,8}.json` (`git log --all`).
- **(D)** GitHub `dwitvliet/nature2021`, the first author's figure-generation
  repository, which the paper's code-availability statement names (web-search
  excerpt). Pinned at its master head
  `0646af9d25896ae660f97d462eab2d67282f5625` (2021-06-01, "Fixed stats for
  publication"); declared in the module. The `tables/` files were added in
  commits titled "Added export functions for supplementary tables"
  (2021-02-10), "Added supplementary tables" and "Added missing supplementary
  info" (2021-02-11), and "Fixed edge classification export table…"
  (2021-02-12).

Every GitHub file is fetched from `raw.githubusercontent.com/<repo>/<commit>/<path>`.
Its git blob id is checked against the id recorded at that commit.

| File | Size (bytes) | SHA-256 | Distributor / URL | Integrity checks passed |
|---|---|---|---|---|
| `aconnectome_witvliet_2020_7.csv` | 55,102 | `1370d2a7e26a17e0765edfa834c95ca59ab44d8587efb5fda330432233074165` | (A) member `wormneuroatlas/data/aconnectome_witvliet_2020_7.csv` | wheel = PyPI digest; pin; wheel RECORD |
| `aconnectome_witvliet_2020_8.csv` | 55,153 | `530a6d6b1c0c621d70a019e478ac79c8107cde475b55e79f225582f77b342ce4` | (A) member `…_8.csv` | same |
| `witvliet_2020_7 adult.xlsx` | 53,165 | `d0fd2dd32adbe5f04ce90a2e5b74c01c9a831876527b0a2b8bd5b94edc86b037` | (B) `cect/data/witvliet_2020_7 adult.xlsx` (URL-encoded `%20`) | pin; git blob `9cec72011ebfb1052631fbb7f86d6bf3190ed421` |
| `witvliet_2020_8 adult.xlsx` | 53,143 | `fdead89606257c1b26e57069fbe1de14c7696633b75b59b79e74c0bcc3497e62` | (B) `cect/data/witvliet_2020_8 adult.xlsx` | pin; git blob `b03bdbeddab70a0d70f6e430e8cdc584c46725c1` |
| `nemanode_baf8ec8__witvliet_2020_7.json` | 854,336 | `350b247214763fe6b5a89b76a95cc018f7551c0446ad6501bd9c4774fb05fbae` | (C) @`baf8ec8` `src/server/populate-db/raw-data/connections/witvliet_2020_7.json` | pin; git blob `201d50cd208f265d7b2819a87145cb2bcf718230` |
| `nemanode_baf8ec8__witvliet_2020_8.json` | 887,526 | `465aeb3c1f42d84273023cef8e5f5d8ebbcf63248550b2219db68fccb9787033` | (C) @`baf8ec8` `…/connections/witvliet_2020_8.json` | pin; git blob `135b1806872eea14a5f7bb667901285d269df720` |
| `nemanode_baf8ec8__neurons.json` | 58,575 | `c780e0b7cab28b311a7e0916a7b8e37b9cf72de152712bd4a5eb29fd9d595492` | (C) @`baf8ec8` `…/raw-data/neurons.json` | pin; git blob `81da4572b20674dcc852cfa9fd041e66a3c7a73c` |
| `nemanode_859641e__witvliet_2020_7.json` | 897,485 | `caff48ff6cde87983d616a67d1d5d1967871548a965f86722ab2b666fe0315c3` | (C) @`859641e` `…/connections/witvliet_2020_7.json` | pin; git blob `8ec3eab48416e4ea390fbcdf6be2085c14333f8d` |
| `nemanode_859641e__witvliet_2020_8.json` | 932,228 | `c13c42b5ba662e0bddcb1060693e0f75d579d85ee5c81ca539c620271819b07a` | (C) @`859641e` `…/connections/witvliet_2020_8.json` | pin; git blob `c156b36c7d9efb28d7cc048cbe173f6bc651ee39` |
| `synapse_count_matrices.xlsx` | 764,283 | `bd725d1f6121abeb8ec08d0b80edad94d9e0fea954a8704ee07c7f4be7cebfe6` | (D) `tables/synapse_count_matrices.xlsx` | pin; git blob `e2c29655de6932b1d9e9d968b16f7ed318d3e7e3` |
| `synapse_list.csv` | 1,287,223 | `36c431f25e72cd82946239a2eb555c1ed4494a2036092105bd37eb161ecf9340` | (D) `tables/synapse_list.csv` | pin; git blob `80fc81032f996e75349397c2dec505cd462ca48c` |
| `connection_classifications.csv` | 92,737 | `da94863507a64da8d85d75a280ceff538d30f98a746390a7d0090607b0870f08` | (D) `tables/connection_classifications.csv` | pin; git blob `960ce494eee0352320bde8a3bc82a59fede4d713` |
| `_neurons.csv` | 2,223 | `2189e2ee262a1d1a81f1139fcc95c4b886681cfdd706dc5f77bd8cda2a49491d` | (D) `tables/_neurons.csv` | pin; git blob `bef93bfd871caa8c3fbea910741d01bc9c960ac8` |

Re-running acquisition is idempotent. A second run re-verified all 13 files.
It downloaded nothing, left their modification times unchanged, and rewrote
`MANIFEST.json` with identical content. `--verify` reports OK. `--counts` is
byte-identical across runs.

### Byte-level relationships between copies

- **NemaNode `baf8ec8` and the first author's repository.**
  `nemanode_baf8ec8__witvliet_2020_{7,8}.json` have the same git blob ids
  (`201d50cd…`, `135b1806…`) as `data/nemanode/witvliet_2020_{7,8}.json` in
  `dwitvliet/nature2021` @`0646af9`. They are therefore byte-identical. They
  were written by that repository's `src/export/export_json.py`
  (`export_nemanode_connections`, added 2021-03-15), so the NemaNode files
  are the paper code's own export.
- **`neurons.json`** is one blob (`81da4572…`) at all three NemaNode commits.
- **Wheel CSV and toolbox xlsx** are different formats, so no byte
  comparison is possible. Their content differs; see "What each file
  contains". Both have the header `pre, post, type, synapses`.
- **Wheel CSV and NemaNode `859641e`: identical content.** Every chemical
  (pre, post, weight) matches, and every gap junction matches as an
  unordered pair with weight. The CSV weight is `len(syn)`. Only row order
  differs, and the CSV keeps one orientation per gap junction.
- **Toolbox xlsx and NemaNode `baf8ec8`: identical content**, except that
  the xlsx omit the gap junctions to the non-cell names `NR_fragment`,
  `vncfrag`, `Fragment` and `VAn`:
  - dataset 7: 3 pairs omitted;
  - dataset 8: 4 pairs omitted.

  The xlsx list each gap junction once, with pre ≤ post as strings.
- **Paper tables and NemaNode `baf8ec8`.**
  - `synapse_count_matrices.xlsx`, sheets Dataset7 and Dataset8, equals the
    `baf8ec8` chemical edges exactly: 2,202 cells summing to 7,467, and 2,186
    cells summing to 7,970.
  - `synapse_list.csv`, datasets 7 and 8, equals `baf8ec8` in edge counts.
    Its `syn_id` sets equal NemaNode's chemical connector-id sets.

## What each file contains

### Common facts (all versions)

- **Orientation.**
  - Chemical rows are pre → post.
  - `synapse_count_matrices.xlsx` is laid out **[post row, pre column]**:
    row 3 holds the pre names, column 3 the post names, and rows 1–2 and
    columns 1–2 hold "Pre"/"Post" and type labels. It has 180 pre columns
    (types Sensory, Inter, Motor, Modulatory) and 224 named post rows (the
    same plus Muscle and Other).
  - Electrical rows have no direction.
- **Weight.** A connection's weight is the number of (synapse, postsynaptic
  partner) records. NemaNode code `populate-connections.js` uses
  `synapseCount = syn.length`, and the CSV/xlsx `synapses` column equals it.
  - A polyadic synapse adds 1 to every partner's edge. Hence 7,467 weight
    vs 3,562 distinct presynaptic connector ids in dataset 7 (post-revision).
  - 49 (dataset 7) and 59 (dataset 8) chemical entries list one connector id
    twice. These are two postsynaptic contacts on the same partner cell.
- **Names.**
  - AWC is `AWCL`/`AWCR` (not AWCON/AWCOFF).
  - Muscles are `BWM-DL01` … `BWM-VR08` (32, zero-padded).
  - Glia: `CEPshDL/DR/VL/VR`, `GLRDL/DR/L/R/VL/VR` (not all present).
  - `excgl` (excretory gland) appears in the pre-revision data only.
  - `CANR` appears in dataset 7 only; there is no CANL.
  - Non-cell fragment names in post-revision gap junctions: `NR_fragment`,
    `vncfrag` (dataset 7); `Fragment`, `VAn` (dataset 8).
- **No pharyngeal neurons.** Witvliet's "brain" is the nerve ring plus the
  ventral ganglion region. The toolbox summary reads: "nerve ring, ventral
  ganglion and neuropil anterior of the ventral sub-lateral commissures";
  this is not checked against the paper text.

### Per-file notes

- **Wheel CSVs.**
  - Tab-separated despite `.csv`. ASCII, LF line endings, **no trailing
    newline**.
  - One row per chemical (pre, post) and one per gap-junction unordered pair,
    in mixed orientation. Self pairs are included.
  - Randi's loader (`NeuroAtlas._get_aconnectome_witvliet`) builds
    `chem[post, pre]` and `gap[b, a]`, then symmetrises gap junctions with
    `max(gap[i,j], gap[j,i])`.
- **Toolbox xlsx.**
  - LibreOffice 6.0.7.3 files; the zip entries are dated 2022-09-20. One
    sheet, named like the file. Data cells are str, str, str, int. No
    creation date in `docProps/core.xml`.
- **NemaNode JSON.**
  - A list of entries `{pre, post, typ, syn, ids, pre_tid, post_tid}`. `typ`
    0 = chemical, 2 = electrical.
  - Gap junctions are listed in both directions, except those to fragment
    names, which appear in one direction only.
  - Pre-revision files hold 4 chemical `syn` values of 2 per dataset. In
    dataset 7 these sit on `RIVL→BWM-VR07`, `RMER→BWM-DL04` and
    `RMGR→BWM-DR06`. The post-revision files have only 1s.
- **`nemanode_baf8ec8__neurons.json`.**
  - 447 cells with `classes`, `typ` (s/i/m/n codes; `b` = muscle;
    `u` = unknown), `nt`, `emb`, `inhead` and `intail`.
  - It types CEPsh, GLR, CANR and excgl as `u`.
  - Its `nt` transmitter codes are NemaNode annotations. Do not use them as a
    transmitter or polarity source without an owner decision.
- **`synapse_list.csv`.**
  - Columns: `dataset, pre, post, syn_id, sections, size, post_is_branch`.
    Datasets 1–8, 32,105 rows.
  - **Dataset 7 has `size = -1` (missing) on all 7,467 rows.** The authors'
    code also gives Dataset7 no size and no contact data.
- **`connection_classifications.csv`.**
  - Columns `pre, post, classification`, 3,676 rows. Values: variable 1,995;
    stable 829; post-embryonic brain integration 554; developmentally dynamic
    (strengthened) 278; developmentally dynamic (weakened) 20.
- **`_neurons.csv`.**
  - The paper's brain cell classes: 90 classes, 222 members.
  - Members by type: sensory 65, inter 44, modulatory 29, motor 42,
    muscle 32, glia 10.
  - Classes by integration: embryonic 80, post-embryonic 10.
  - It omits CAN; `tables.py` skips it explicitly.

### Exact differences, pre-revision (wheel CSV = NemaNode `859641e`) vs published (NemaNode `baf8ec8` = xlsx = paper tables)

**Dataset 7.**

- Chemical:
  - the pre-revision version has 2 extra edges, `RIVL→excgl:1` and
    `SMBVL→excgl:1`;
  - 3 weights differ: `RIVL→BWM-VR07` 14 vs 15, `RMER→BWM-DL04` 14 vs 15,
    `RMGR→BWM-DR06` 6 vs 8.

  The 3 weight differences are exactly the pre-revision `syn` = 2 entries.
  Weighted by the sum of `syn` values, the two versions differ only by the
  two `excgl` edges (`cmp_d7_…_weight_sum_syn_*`).
- Gap junctions: the pre-revision version has 5 extra pairs (`ASGL–CEPshVL`,
  `GLRR–RMEL`, `GLRVL–RMEV`, `GLRVR–RMEV`, `SIBVL–SMBVL`), and `RIPL–RIPR`
  is 2 vs 1. The post-revision JSON adds 3 fragment pairs.

**Dataset 8.**

- Chemical: this is a real re-annotation.
  - 15 edges exist only in the pre-revision version, among them 5 self-loops
    (ADEL, IL2DR, RMDDR, RMEL, URBL), 3 `excgl` edges, `RIFL→AVAL`,
    `RIFL→AVDR` and `URYDR→OLLR`.
  - 7 edges exist only in the published version: `ADFL→AIYL`,
    `AIML→RMGL`, `AIZL→SMBDR`, `RIBR→AWBR`, `RIFR→HSNR`, `RMDL→RMDVL`,
    `RMFL→RMDVL`.
  - 50 weights differ: 24 by +1, 25 by −1 and one by +3 (`ASHL→AVDR` 7→10).
  - Net, the published version has 11 fewer synapses (7,981 → 7,970).
- Gap junctions: identical as unordered pairs. The post-revision JSON adds 4
  fragment pairs.

## Record counts

From `python -m src.acquire --counts witvliet2021`. Key names are
`<version>_d<dataset>_<quantity>`. Definitions are in the `record_counts`
docstring. The full printed output (1,322 lines) has SHA-256
`57a954b3f814f4850aafb49110a61ba712ab37846939d53bee32d5db71dc3288`, and it
was identical on repeated runs.

Cells are partitioned two ways, both taken from distributor files with no
judgment added:

- by NemaNode `neurons.json` `typ`;
- by the paper's `_neurons.csv` type, via NemaNode's `classes` field.

| Quantity | Definition | Count in acquired file | Paper reports | Where the paper reports it | Match |
|---|---|---|---|---|---|
| D7 chemical connections / synapses, published version | nonzero cells / sum in the paper's count matrix, vs edges / weight sum in the file | NN baf8ec8 and xlsx: 2,202 / 7,467 | 2,202 / 7,467 | `synapse_count_matrices.xlsx` sheet Dataset7 (the author's Supplementary-table export, (D) @0646af9; identity with the Nature ESM unverified) | **YES** |
| D8 chemical connections / synapses, published version | same | NN baf8ec8 and xlsx: 2,186 / 7,970 | 2,186 / 7,970 | same file, sheet Dataset8 | **YES** |
| D7 chemical connections / synapses, **wheel CSV (Randi's input)** | same | 2,204 / 7,465 | 2,202 / 7,467 | same file | **NO — BLOCKER**: the wheel CSV is the superseded pre-revision version; owner must choose the version (Q-W1) |
| D8 chemical connections / synapses, **wheel CSV (Randi's input)** | same | 2,194 / 7,981 | 2,186 / 7,970 | same file | **NO — BLOCKER**: as above |
| D7 / D8 synapse records and distinct synapse ids | rows and distinct `syn_id` in `synapse_list.csv` vs NN baf8ec8 weight sum and connector ids | 7,467 & 3,562 / 7,970 & 3,674 | same numbers; id sets equal | `synapse_list.csv` ((D), "Added missing supplementary info") | **YES** (published version) |
| Adult total chemical synapses | — | one-to-one records: 7,467 (d7), 7,970 (d8); distinct presynaptic ids: 3,562, 3,674 | "~8,000" (and "~1,300" at birth) | WebSearch excerpt (search summary of nature.com/articles/s41586-021-03778-8, escholarship.org/content/qt6hf5q104/qt6hf5q104.pdf, biorxiv 2020.04.30.066209v3): "from roughly 1,300 at birth to roughly 8,000 in adults (Fig.1e) … ~1300 at birth to ~8000 in adults" | **NOT COMPARABLE**: rounded figure, and the counting unit is not given in the excerpt. One-to-one records are consistent (d1 = 1,296 in `synapse_list.csv`); distinct presynaptic sites are not |
| Mean synapses per connection, birth → adult | — | all edges: d1 1,296/775 = 1.67; d7 3.39; d8 3.65. Birth-edges only in adult: d7 5.17, d8 5.60 (scratch) | 1.7 → 6.9 | WebSearch excerpt (same sources): "The mean rose from 1.7 at birth to 6.9 in adults, a 4.6-fold increase" | **NOT COMPARABLE**: the paper's connection set for 6.9 is not reachable. No definition I tried gives 6.9; check against the full text |
| Connections classified (stable / variable / dynamic) | — | `connection_classifications.csv`: 3,122 rows not "post-embryonic" (3,112 non-self); 3,676 total | 3,113 | Only a secondary paraphrase: ConnectomeToolbox `docs/Witvliet_2021.md` (pinned clone) and openworm.org/ConnectomeToolbox/Witvliet_2021/ ("3,113 connections (averaging 1,292 per dataset) were assigned as stable, variable or developmentally dynamic"). Paper text not reached | **UNVERIFIED**. The author's table gives 3,122, not 3,113; resolve against the paper text |
| Connections per dataset, average | — | classified connections present per dataset (d1–d8: 775, 986, 1,012, 1,106, 1,402, 1,394, 1,847, 1,867), sum 10,389 over 8 datasets (mean 1,298.6); all chemical edges, mean 1,417.1 | 1,292 | same secondary paraphrase | **UNVERIFIED** (no definition tried gives 1,292) |
| Brain neurons / muscles | members by paper type | 180 neurons and 32 muscles present in both adult datasets (all versions) | 180 (65+44+29+42) / 32 | `_neurons.csv` (D) | **YES** for the published cell list. Glia (10 in the table; 9 and 7 cells with synapses in d7 and d8) is NOT COMPARABLE: the table lists the brain's cell set, not cells with annotated synapses per dataset |
| Gap junctions per dataset | — | see the per-version summary below | none reported. Gap junctions "were partially annotated … but because they could not be mapped in completion, they were excluded from further analyses" | WebSearch excerpt attributed to a preprint version (biorxiv 2020.04.30.066209); another version: "gap junctions were not subjected to the consensus scoring process due to limitations of current sample preparation methods" | **NOT COMPARABLE** (no paper count exists) |

### Per-version summary for datasets 7 and 8 (d7 / d8)

All values come from `--counts`; this table has no paper column.

| Quantity | Definition | wheel CSV (= NN 859641e) | NN 859641e JSON | NN baf8ec8 JSON | toolbox xlsx |
|---|---|---|---|---|---|
| rows | stored rows/entries | 2,500 / 2,504 | 2,790 / 2,806 | 2,781 / 2,802 | 2,493 / 2,496 |
| cells | distinct names | 224 / 220 | 224 / 220 | 224 / 221 | 222 / 219 |
| neurons (paper type sensory+inter+motor+modulatory) | `cells_by_paper_type` | 180 / 180 | 180 / 180 | 180 / 180 | 180 / 180 |
| muscles (paper type muscle; NemaNode `b`) | | 32 / 32 | 32 / 32 | 32 / 32 | 32 / 32 |
| glia (paper type glia) | | 10 / 7 | 10 / 7 | 9 / 7 | 9 / 7 |
| no paper type | names | CANR, excgl / excgl | CANR, excgl / excgl | CANR, NR_fragment, vncfrag / Fragment, VAn | CANR / — |
| chemical edges | ordered (pre, post) rows | 2,204 / 2,194 | 2,204 / 2,194 | **2,202 / 2,186** | **2,202 / 2,186** |
| chemical self-edges | pre = post | 11 / 5 | 11 / 5 | 11 / 0 | 11 / 0 |
| chemical synapses (weight sum) | Σ `synapses` = Σ len(syn) | 7,465 / 7,981 | 7,465 / 7,981 | **7,467 / 7,970** | **7,467 / 7,970** |
| chemical, Σ syn values | JSON only | — | 7,469 / 7,985 | 7,467 / 7,970 | — |
| distinct presynaptic connector ids | JSON only | — | 3,562 / 3,681 | 3,562 / 3,674 | — |
| chemical edges, both ends NemaNode neuron-coded | | 1,944 / 1,936 | 1,944 / 1,936 | 1,944 / 1,933 | 1,944 / 1,933 |
| … their synapse sum | | 6,587 / 7,108 | 6,587 / 7,108 | 6,587 / 7,099 | 6,587 / 7,099 |
| gap-junction rows | stored | 296 / 310 | 586 / 612 | 579 / 616 | 291 / 310 |
| gap unordered pairs | incl. self | 296 / 310 | 296 / 310 | 294 / 314 | 291 / 310 |
| gap self pairs | a = a | 6 / 8 | 6 / 8 | 6 / 8 | 6 / 8 |
| gap weight sum | Σ over unordered pairs | 406 / 430 | 406 / 430 | 403 / 434 | 400 / 430 |
| distinct gap connector ids | JSON only | — | 406 / 430 | 403 / 434 | — |

All web-search excerpts above are search-engine renderings of the listed
pages. Their exact wording and page location are unconfirmed because
nature.com, bioRxiv and escholarship are blocked here.

## Discrepancies, flags and open questions

**Headline finding.** Two versions of datasets 7 and 8 are in circulation.

- The files Randi et al. 2023 loaded are the wheel CSVs. They equal the
  **pre-revision** data the Zhen lab put on NemaNode on 2020-05-22.
- On 2021-03-15 the first author replaced that data on NemaNode ("Updated
  witvliet datasets after paper revision").
- The replacement equals the paper's own published tables. It also equals the
  WormWiring spreadsheets carried by the ConnectomeToolbox.

All three published-version copies agree edge for edge on chemical synapses.
The wheel CSVs do not. Choosing the version is an owner decision (Q-W1). Until
then, the wheel CSVs' counts are a mismatch against the published paper and are
logged as a blocker.

- **P1-W1. Randi used the superseded version** (BLOCKER until Q-W1 is
  decided).
  - The wheel CSVs equal NemaNode's 2020-05-22 data.
  - The published paper's tables, NemaNode since 2021-03-15, and the
    WormWiring xlsx all equal the revised data.
  - The wheel files are 2,204/7,465 (d7) and 2,194/7,981 (d8). The published
    files are 2,202/7,467 and 2,186/7,970.
  - Reproducing Randi's anatomy comparisons needs the wheel version; using
    "Witvliet 2021 as published" needs the revised version. They are not
    interchangeable for dataset 8 (22 edge set changes and 50 weight
    changes).
- **P1-W2. Randi's compiled anatomical connectome folds unmatched names into
  VD9.** This is a cross-source flag for randi2023 and Phase 2.
  - `wormneuroatlas` `NeuroAtlas.ids_to_ai` returns −1 for any name not in
    `neuron_ids.txt`, and `_get_aconnectome_witvliet` then indexes
    `chem[-1, …]`. Unmatched names include AWCL/AWCR, all BWM muscles,
    CEPsh, GLR, excgl and CANR.
  - Every synapse involving those names is therefore added to the **last
    neuron, VD9**.
  - I reproduced the wheel's `aconnectome_default.h5`
    (`time_compiled 2023-01-24_13-21-59`) exactly. It is the sum of the four
    CSVs (`white_1986_whole`, `white_1986_L4`, `witvliet_2020_7`,
    `witvliet_2020_8`) under this rule. Scratch script:
    `…/scratchpad/agent_witvliet2021/scripts/repro_default.py`.
  - The h5's VD9 row holds 4,141 incoming chemical synapses, of which 974
    come from Witvliet 7 and 978 from Witvliet 8. **AWCON and AWCOFF have
    zero anatomical synapses** in that file.
  - This project must build its anatomy from the raw files, never from
    `aconnectome_default.h5`. Whether the paper's analyses used this file is
    unverified.
- **P1-W3. `41586_2021_3284_MOESM5_ESM.xlsx` is not a Witvliet file.**
  - 41586_2021_3284 is Brittin et al. 2021, Nature 591:105, doi
    10.1038/s41586-021-03284-x. The toolbox's
    `cect/validation/Brittin2021.md` calls it "Supplementary data file 3 …
    containing the M^δ, C^δ and G^δ reference graphs".
  - Sheets: `restricted_cells` (173 cells); `M` (2,955 contact rows);
    `C` (1,474 chemical rows); `G` (389 gap rows). Each has columns
    `cell_1, cell_2, weight, delta`.
  - Its `docProps/core.xml` says created 2024-11-11 and modified
    2024-11-11 by "Microsoft Office User" (Excel for Mac). It was re-saved
    after publication, so it is probably not byte-identical to the Nature
    ESM.
  - Not acquired here; a separate source if the owner wants a contactome
    (Q-W9).
- **P1-W4. Gap junctions and an `anat_gap` column.**
  - Witvliet states gap junctions were only partially annotated, were not
    consensus-scored, and were excluded from the paper's analyses (excerpts
    above). The paper's own tables carry no gap junctions.
  - The files that do carry them are NemaNode, the CSV and the xlsx. There
    are 403–434 gap-junction ids per adult dataset, against 3,562–3,674
    chemical synapse ids.
  - Consequences for `anat_gap`:
    1. A missing Witvliet gap junction is not evidence of absence. It must
       be encoded as "not annotated", not 0.
    2. Witvliet gap-junction counts are not comparable in completeness with
       White/Cook gap junctions. Randi's loader sums all four sources.
    3. Self gap junctions exist: 6 (d7: IL1DR, IL1VL, IL1VR, RIBL, RIBR,
       SDQL) and 8 (d8: AIAL, AIAR, AIZR×2, AQR, RIBR, RIGL, RIPL, RIPR).
    4. The post-revision export has gap junctions to unidentified fragments.
       These come from a filter in the authors' `get_gapjunctions` that
       tests `n1` twice and never `n2`. The authors' raw
       `data/synapses/Dataset{7,8}_gapjunctions.json` hold the same gap-id
       sets as NemaNode `baf8ec8`, plus one Fragment–Fragment junction in
       dataset 8, so NemaNode loses nothing for real cells.
    5. Orientation is meaningless, and storage differs by copy: both
       directions in JSON, one in CSV/xlsx.
- **P1-W5. Coverage of the head set.**
  - 34 of Randi's 188 head neurons (`randi2023/aconnectome_ids_ganglia.json`)
    never occur in either adult Witvliet dataset:
    - the 20 pharyngeal neurons;
    - AVG;
    - AS1, DA1, DB1, DB2, DD1, SABD, SABVL, SABVR, VA1, VB1, VB2, VD1, VD2.
  - Pairs involving them are "outside the reconstructed volume", not
    "0 synapses". (Scratch check; it uses a randi2023 file, so it is not in
    `record_counts`.)
  - Cross-source: the ganglia file lists `RMHL` twice in "ventral ganglion"
    and never lists `RMHR`, so RMHR is missing from Randi's head set.
    Witvliet has RMHR.
- **P1-W6. Polyadic counting.** Edge weights count (synapse, partner)
  records: 7,467 records vs 3,562 distinct presynaptic sites in d7. Which
  unit `anat_chem_witvliet` uses is Q-W2.
- **P1-W7. Dataset 7 has no synapse sizes.** `size = -1` on all rows, and
  there is no contact data. If synapse size is ever used as a weight, only
  dataset 8 has it among the adults.
- **P1-W8. CAN.** CANR is present in d7 only, typed `u` by NemaNode, and
  omitted from the paper's `_neurons.csv`. Randi's atlas has no CAN.
- **P1-W9. Self-loops in chemical data.** d7 has 11 in both versions
  (ADEL, AIMR, ASER, ASHL, RMDDL, RMDDR×2, RMED, RMEL, RMER, RMGL, SDQL).
  d8 has 5 pre-revision and 0 published.
- **P1-W10. The paper's headline numbers are not yet reproduced:** 3,113
  connections, 1,292 per dataset, and 6.9 synapses per connection. The first
  two rest only on a secondary paraphrase. The author's own classification
  table gives 3,122. Check against the paper text before Phase 4.
- **P1-W11. The toolbox's "NemaNode exports".** The toolbox calls the xlsx
  WormWiring spreadsheets. They are LibreOffice files, so the export tool is
  unknown. Their content equals the post-revision NemaNode data minus
  fragment gap junctions.
- **Available but not acquired** (no silent drops):
  - **Datasets 1–6 (L1–L3).**
    - Toolbox `cect/data/witvliet_2020_{1..4} L1.xlsx`,
      `witvliet_2020_5 L2.xlsx` and `witvliet_2020_6 L3.xlsx` (blobs
      `961275d9…`, `44bb6852…`, `2296913f…`, `92d5f930…`, `c6e4ee54…`,
      `ddd71487…`).
    - NemaNode `connections/witvliet_2020_{1..6}.json` at both commits.
    - `dwitvliet/nature2021` `data/nemanode/` (same blobs as NemaNode
      `baf8ec8`).
    - The acquired `synapse_list.csv` and `synapse_count_matrices.xlsx`
      already contain datasets 1–6 but are only summarised here.
    - Owner decides if juvenile data matter (Q-W7).
  - **Upstream author data** in `dwitvliet/nature2021`:
    - `data/synapses/Dataset{1..8}_{synapses,gapjunctions}.json` (raw
      CATMAID exports);
    - `data/skeletons/`, `data/physical_contact/` (no Dataset7);
    - `tables/synapse_size_matrices.xlsx` and `tables/contact_matrices.xlsx`.

    These are not needed for edge-level counts, and the gap-junction
    contents were checked equal to NemaNode in scratch.
  - **NemaNode `annotations/head.annotations.json`** (last changed
    2020-05-19). This is a pre-revision connection classification:
    stable 823, variable 1,987, increase 280, decrease 23,
    postembryonic 552. It is superseded by `connection_classifications.csv`.
    NemaNode `trajectories/`: not needed.
  - **NemaNode `white_1986_{jsh,n2u,whole,jse}.json`.** These belong to the
    white1986 source (Phase 0 flag F9). The Zhen-lab muscle annotations of
    JSH/N2U live there.
  - **Wheel `aconnectome_default.h5`.** A composite of four sources with the
    P1-W2 defect; it belongs to randi2023 if wanted at all.
  - **Nature ESM files for Witvliet** (e.g. `41586_2021_3778_MOESM4_ESM.xlsx`):
    host blocked.
  - **Brittin MOESM5:** see P1-W3.

### Owner questions

- **Q-W1. Which version is canonical for `anat_chem_witvliet`?**
  - The published version: NemaNode `baf8ec8`, equal to the paper tables and
    the WormWiring xlsx.
  - Randi's pre-revision input: the wheel CSV, equal to NemaNode `859641e`.
  - Or both as separate columns: one to reproduce Randi, one to represent
    Witvliet 2021.
- **Q-W2. Weight unit.** One-to-one (synapse, partner) records (NemaNode,
  CSV, paper matrices), or distinct presynaptic sites? For the pre-revision
  data, `len(syn)` or the sum of `syn`?
- **Q-W3. Combining datasets 7 and 8.** Sum (Randi), mean, union, or require
  both? Combine with White as well (F9)?
- **Q-W4. `anat_gap`.** Use Witvliet gap junctions at all, given partial
  annotation and their exclusion from the paper? If so, how to encode
  "not annotated" versus 0, self gap junctions, and fragment partners?
- **Q-W5. Cell scope.** Muscles (32 BWM), glia (CEPsh, GLR), excgl, CANR and
  fragment names: keep in the raw edge table, or drop with exclusion-log
  entries?
- **Q-W6. Coverage.** The 34 head neurons absent from Witvliet (P1-W5) need
  a "not covered" state.
- **Q-W7. Juvenile datasets 1–6:** needed?
- **Q-W8. Edge-level attributes.** Use Witvliet's stable/variable/dynamic
  classification (`connection_classifications.csv`) as an edge attribute?
  Use synapse size (dataset 8 only)?
- **Q-W9. Brittin 2021** (MOESM5 contactome and C/G graphs): a separate
  source?
