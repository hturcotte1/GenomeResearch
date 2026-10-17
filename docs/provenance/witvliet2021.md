# witvliet2021: Brain connectomes across development (adult datasets 7 and 8)

- Paper: Witvliet D, Mulcahy B, Mitchell JK, et al. *Connectomes across
  development reveal principles of brain maturation.* Nature 596, 257–261
  (2021). doi:10.1038/s41586-021-03778-8
- Module: `src/acquire/witvliet2021.py`
- Status: **SECONDARY — primary comparison PENDING (blocks Phase 4 freeze)**
- Retrieval date (UTC), from `data/raw/witvliet2021/MANIFEST.json`:
  2026-10-11 for the 13 files of the first acquisition, and 2026-10-13 for
  the 13 files added by the Phase 1 fix (NemaNode `8a50236` datasets 7 and 8,
  NemaNode `859641e` datasets 1–6 and `head.annotations.json`, and four
  ConnectomeToolbox evidence files). 26 files in all.

## Primary location (not reachable from this environment)

- **Journal:** https://www.nature.com/articles/s41586-021-03778-8,
  Supplementary Information. The supplementary tables, per a web-search
  excerpt (wording not confirmed on the page):
  - Supplementary Table 1: content unverified. A search excerpt cites
    Supplementary Tables 1–5; it may be the cell list (cf. `_neurons.csv`),
    but that is a guess, not a finding;
  - Supplementary Table 2: "synapse number connectivity matrix";
  - Supplementary Table 3: "synapse size matrix";
  - Supplementary Table 4: "physical contact matrix";
  - Supplementary Table 5: synapses onto spine-like protrusions.

  The ConnectomeToolbox (`cect/validation/WitvlietEtAl2021.md`, acquired)
  links `41586_2021_3778_MOESM4_ESM.xlsx` as connectivity matrices that "only
  contain the chemical connections". Which MOESM file is which table is
  unverified.
- **Paper text** (needed for every paper figure in "Record counts"):
  nature.com; the NIH author manuscript PMC8756380
  (https://pmc.ncbi.nlm.nih.gov/articles/PMC8756380/, identified by a web
  search on 2026-10-13); the bioRxiv preprint 10.1101/2020.04.30.066209 (v1
  and v2 PDFs listed by the same search); a PDF at
  `ftp.wormatlas.org/papers/Witvliet et al 2021.pdf` (listed by a search).
  None was read: the proxy refuses pmc.ncbi.nlm.nih.gov, ftp.wormatlas.org,
  www.nature.com, www.biorxiv.org and escholarship.org (CONNECT 403, checked
  2026-10-13).
- **Data portal:** https://nemanode.org/, dataset ids `witvliet_2020_7` and
  `witvliet_2020_8` (proxy 403, checked 2026-10-13). Per a web-search excerpt
  of the paper's data availability statement: "Connectivity matrices for all
  datasets are available at http://www.nemanode.org and as Supplementary
  Tables."
- **Zenodo:** https://zenodo.org/records/5637219 (proxy 403, checked
  2026-10-13). Per a web search on 2026-10-13 (search-result text, not the
  page itself): the data release for this paper, "Published November 1, 2021 |
  Version v1", whose description points to a README, with files including
  `Adult_neuron_3d_models.zip` (1.1 GB) "with several associated archives".
  Whether it holds connectivity tables, and how they relate to the GitHub
  tables acquired here, is unknown.
- **WormWiring:** https://wormwiring.org/pages/witvliet.html (proxy 403,
  checked 2026-10-13). The toolbox says the per-dataset xlsx files came from
  here.
- **EM images and volumes:** https://bossdb.org/project/witvliet2020 (from the
  data-availability excerpt). Not needed here.

Primary checks to perform once reachable:

1. Download the Nature ESM files. Compare `synapse_count_matrices.xlsx`,
   `synapse_list.csv`, `connection_classifications.csv` and `_neurons.csv`
   with the matching Supplementary Tables, byte for byte or cell for cell.
2. Download datasets 7 and 8 from nemanode.org and compare them with
   `nemanode_baf8ec8__*.json`.
3. Download the WormWiring xlsx and compare them with the toolbox copies.
4. List Zenodo 5637219 and compare any connectivity table in it with the
   acquired files.
5. Read the paper text (Nature, or PMC8756380) for the figures 3,113, 1,292,
   1.7 → 6.9 and ~8,000, and establish which data version they were computed
   from (P1-W10).

How each acquired file relates to the primary copies:

| Acquired file | Corresponding primary copy |
|---|---|
| `aconnectome_witvliet_2020_{7,8}.csv`, `nemanode_859641e__witvliet_2020_{1..8}.json` | none current. This is the NemaNode repository content from 2020-05-18 (`b6dfd28`) to 2021-03-15 (`baf8ec8`), when the first author replaced it; nemanode.org presumably no longer serves it (unverified) |
| `nemanode_8a50236__{TEM,SEM}_adult.head.json` | none current. NemaNode repository root commit (2020-05-14), replaced four days later by `b6dfd28` |
| `nemanode_859641e__head.annotations.json` | NemaNode's connection annotations. Same blob from `8a50236` to the master head `6b7ca03`; whether nemanode.org serves it is unverified |
| `nemanode_baf8ec8__witvliet_2020_{7,8}.json`, `nemanode_baf8ec8__neurons.json` | nemanode.org datasets 7 and 8 and its cell table (presumably; unverified) |
| `witvliet_2020_{7,8} adult.xlsx` | WormWiring spreadsheets |
| `synapse_count_matrices.xlsx`, `synapse_list.csv`, `connection_classifications.csv`, `_neurons.csv` | Nature Supplementary Tables (exact mapping unverified) |
| `WitvlietDataReader{7,8}_expected_data.yaml`, `WitvlietEtAl2021.md`, `Witvliet_2021.md` | none: written by the ConnectomeToolbox itself (evidence only, not Witvliet data) |

## Files acquired

Four secondary distributions are used:

- **(A)** PyPI wheel `wormneuroatlas` 0.0.7.3, already declared project-wide.
  Its SHA-256 equals PyPI's published digest (checked live), and each member
  matches the wheel's `RECORD`.
- **(B)** GitHub `openworm/ConnectomeToolbox` @ `ffe570268b7cffb9329cd009a1bb37d60db2d465`:
  the two adult xlsx, plus four evidence files: the toolbox's expected values
  for its dataset-7 and dataset-8 readers
  (`cect/validation/WitvlietDataReader{7,8}_expected_data.yaml`), its note
  on what it read from where (`cect/validation/WitvlietEtAl2021.md`), and its
  paraphrase of the paper (`docs/Witvliet_2021.md`).
- **(C)** GitHub `zhenlab-ltri/NemaNode`, the Zhen lab's source repository for
  nemanode.org, declared in the module. `git log --all --follow` on a bare
  clone (2026-10-13) gives this history for datasets 7 and 8. All five
  commits are by daniel.witvliet@gmail.com.
  - `8a50236db4c5888e7fe0c1d018e5eff0729e4c88` (2020-05-14, the repository's
    root commit, "Initial commit after removing unpublished datasets") adds
    `src/server/db/populate-db/raw-data/connections/TEM_adult.head.json`
    (blob `fbe13f1e…`) and `SEM_adult.head.json` (blob `cf39c0d4…`).
    **Pinned** (datasets 7 and 8).
  - `b6dfd28` (2020-05-18, "Fixed bug in data where two synapses were counted
    only once") gives all eight datasets new content, among them
    `TEM_adult.head.json` → blob `8ec3eab4…` and `SEM_adult.head.json` →
    blob `c156b36c…`. Not pinned separately; these are the blobs pinned at
    `859641e`.
  - `a0ff6f3` (2020-05-18, "Cleaned up populate-database scripts") moves the
    folder to `src/server/populate-db/raw-data/` (R100, no content change).
  - `859641e20748f5313a99eaa862227ae9f6d369ca` (2020-05-22, "Renamed datasets
    to be consistent with manuscript") only renames the dataset files (R100,
    0 lines changed; the commit also edits code and `datasets.json`):
    `TEM_adult.head.json` → `witvliet_2020_7.json`,
    `SEM_adult.head.json` → `witvliet_2020_8.json`, and `SEM_L1_3`,
    `TEM_L1_5`, `SEM_L1_4`, `SEM_L1_2`, `SEM_L2_2`, `TEM_L3` (`.head.json`)
    → `witvliet_2020_1` … `_6.json`. **Pinned** (datasets 1–8 and
    `annotations/head.annotations.json`).
  - `baf8ec877455890d089d965d1a0b3ea0db110e9f` (2021-03-15, "Updated witvliet
    datasets after paper revision") gives all eight datasets new content.
    **Pinned** (datasets 7 and 8, `neurons.json`).

  The repository's master head `6b7ca03f6d68c4ea1af3c120d1a47681edc74a90`
  (2022-03-16) has the same blobs as `baf8ec8` for these paths.
  `head.annotations.json` (blob `dae8701a…`) was added in `8a50236`, only
  moved by `a0ff6f3`, and is unchanged through `6b7ca03`. `neurons.json` is
  one blob (`81da4572…`) at `8a50236`, `b6dfd28`, `a0ff6f3`, `859641e`,
  `baf8ec8` and `6b7ca03`. The first version of this record said "Only these
  two commits ever touched `connections/witvliet_2020_{7,8}.json`"; that came
  from a path-limited `git log` without `--follow` and was wrong.
- **(D)** GitHub `dwitvliet/nature2021`, the first author's figure-generation
  repository. An earlier web-search excerpt said the paper's code-availability
  statement names it; a search on 2026-10-13 did not re-confirm this, and the
  repository's README is empty. Pinned at its master head
  `0646af9d25896ae660f97d462eab2d67282f5625` (2021-06-01, "Fixed stats for
  publication"); declared in the module. The `tables/` files were added in
  commits titled "Added export functions for supplementary tables"
  (2021-02-10), "Added supplementary tables" and "Added missing supplementary
  info" (2021-02-11), and "Fixed edge classification export table…"
  (2021-02-12).

Every GitHub file is fetched from `raw.githubusercontent.com/<repo>/<commit>/<path>`.
Its git blob id is checked against the id recorded at that commit. For the 13
files added on 2026-10-13, the pinned blob ids were also checked against
`git ls-tree` of a bare NemaNode clone and of the ConnectomeToolbox clone at
`ffe5702`, and the pinned SHA-256 of the NemaNode files against
`git cat-file -p <blob> | sha256sum` of that bare clone.

| File | Size (bytes) | SHA-256 | Distributor / URL | Integrity checks passed |
|---|---|---|---|---|
| `aconnectome_witvliet_2020_7.csv` | 55,102 | `1370d2a7e26a17e0765edfa834c95ca59ab44d8587efb5fda330432233074165` | (A) member `wormneuroatlas/data/aconnectome_witvliet_2020_7.csv` | wheel = PyPI digest; pin; wheel RECORD |
| `aconnectome_witvliet_2020_8.csv` | 55,153 | `530a6d6b1c0c621d70a019e478ac79c8107cde475b55e79f225582f77b342ce4` | (A) member `…_8.csv` | same |
| `witvliet_2020_7 adult.xlsx` | 53,165 | `d0fd2dd32adbe5f04ce90a2e5b74c01c9a831876527b0a2b8bd5b94edc86b037` | (B) `cect/data/witvliet_2020_7 adult.xlsx` (URL-encoded `%20`) | pin; git blob `9cec72011ebfb1052631fbb7f86d6bf3190ed421` |
| `witvliet_2020_8 adult.xlsx` | 53,143 | `fdead89606257c1b26e57069fbe1de14c7696633b75b59b79e74c0bcc3497e62` | (B) `cect/data/witvliet_2020_8 adult.xlsx` | pin; git blob `b03bdbeddab70a0d70f6e430e8cdc584c46725c1` |
| `WitvlietDataReader7_expected_data.yaml` | 440 | `e68d150f07cf3c30164e78607a43768188e4154d471c64d70c456fd5a81c9a95` | (B) `cect/validation/WitvlietDataReader7_expected_data.yaml` | pin; git blob `879672e7f78b97dda2dc7b0fd0ad7d2d67821f50` |
| `WitvlietDataReader8_expected_data.yaml` | 435 | `1e99bfe82b5f1b4b1bf5f2d40360198aeac6c34739720fbdd496b83c2ba89bda` | (B) `cect/validation/WitvlietDataReader8_expected_data.yaml` | pin; git blob `041a0e3ef3e7e783001c568afea41f1464be6f8a` |
| `WitvlietEtAl2021.md` | 1,035 | `452c0977a771a3c08bb3e5ac0dbc7ae9e400cd46c359d0a9a455a3ec8ba73f6c` | (B) `cect/validation/WitvlietEtAl2021.md` | pin; git blob `7e5d091debb2ef06cf7f17ed4b31db0dd7df6a01` |
| `Witvliet_2021.md` | 3,263 | `4fad03369d8613eb4cae9745d6db556d35e4bc31f40e0af9d3cbae39b23eebc4` | (B) `docs/Witvliet_2021.md` | pin; git blob `0a8961df039d5adb0c5559b0ad62f871b255998b` |
| `nemanode_8a50236__TEM_adult.head.json` | 827,927 | `4b9b5392603c621f7e76bb69880d314f401baffe6ffe7417ddfc106792435ab7` | (C) @`8a50236` `src/server/db/populate-db/raw-data/connections/TEM_adult.head.json` | pin; git blob `fbe13f1e916cc9842c2877d3a7f4717e8e758283` |
| `nemanode_8a50236__SEM_adult.head.json` | 859,998 | `4de49ad034465df9cd1ff2e9d93a0a985e06ff1ca637b62adbdd365565f5bad7` | (C) @`8a50236` `…/connections/SEM_adult.head.json` | pin; git blob `cf39c0d4114bb0584b2bd51fdc1c496653c65837` |
| `nemanode_859641e__witvliet_2020_1.json` | 227,839 | `130f5b6cfefa824958374ec9f8f964202faf56baa8634f6b79d58e49962b84d0` | (C) @`859641e` `src/server/populate-db/raw-data/connections/witvliet_2020_1.json` | pin; git blob `7cdc94fd3fa57c8084b0df81344787198e3eeab4` |
| `nemanode_859641e__witvliet_2020_2.json` | 309,957 | `83ad7f2410eeec903a2454882b35fd5210e6dae48bc652902cf3dc32665389aa` | (C) @`859641e` `…/connections/witvliet_2020_2.json` | pin; git blob `e5ea2884d2a03fe364b082e86e4d1f7cde7472a0` |
| `nemanode_859641e__witvliet_2020_3.json` | 314,899 | `c2295e45df692a6d85004ebb70632b25f80fc2be59c4bec7ea3492912005c7c3` | (C) @`859641e` `…/connections/witvliet_2020_3.json` | pin; git blob `da46eb7d634a02fead622adb4284ac32a0b01215` |
| `nemanode_859641e__witvliet_2020_4.json` | 416,671 | `d5c50a6f4248842a3155ef0d12bbe3b24ca0444d25a847404d41cf12cf077b62` | (C) @`859641e` `…/connections/witvliet_2020_4.json` | pin; git blob `fe65dd81a6ab47bbb63fa0d84d0f6560fc6b001a` |
| `nemanode_859641e__witvliet_2020_5.json` | 596,438 | `879ae9ae44db9804b869841fd067e0d3eb584bf55faa2dd8c78c952d59269355` | (C) @`859641e` `…/connections/witvliet_2020_5.json` | pin; git blob `cda01e99b9ab3fa406eec704b26f9aeef9bf219b` |
| `nemanode_859641e__witvliet_2020_6.json` | 580,169 | `c31e90ab7d677b7a19fad18b57aaa81ff7b6d1b4b13a08c23b0393503ecc1423` | (C) @`859641e` `…/connections/witvliet_2020_6.json` | pin; git blob `e1e460f380ccc9cb910dcd616053769062f3b7ff` |
| `nemanode_859641e__witvliet_2020_7.json` | 897,485 | `caff48ff6cde87983d616a67d1d5d1967871548a965f86722ab2b666fe0315c3` | (C) @`859641e` `…/connections/witvliet_2020_7.json` | pin; git blob `8ec3eab48416e4ea390fbcdf6be2085c14333f8d` |
| `nemanode_859641e__witvliet_2020_8.json` | 932,228 | `c13c42b5ba662e0bddcb1060693e0f75d579d85ee5c81ca539c620271819b07a` | (C) @`859641e` `…/connections/witvliet_2020_8.json` | pin; git blob `c156b36c7d9efb28d7cc048cbe173f6bc651ee39` |
| `nemanode_859641e__head.annotations.json` | 156,426 | `65f1e2b629f6966312861be1f0b1455e7a5948e650dd388b0c5f6a1ac9124fdb` | (C) @`859641e` `src/server/populate-db/raw-data/annotations/head.annotations.json` | pin; git blob `dae8701a1ffc09152261ce840f842d9bfdd46ad5` |
| `nemanode_baf8ec8__witvliet_2020_7.json` | 854,336 | `350b247214763fe6b5a89b76a95cc018f7551c0446ad6501bd9c4774fb05fbae` | (C) @`baf8ec8` `src/server/populate-db/raw-data/connections/witvliet_2020_7.json` | pin; git blob `201d50cd208f265d7b2819a87145cb2bcf718230` |
| `nemanode_baf8ec8__witvliet_2020_8.json` | 887,526 | `465aeb3c1f42d84273023cef8e5f5d8ebbcf63248550b2219db68fccb9787033` | (C) @`baf8ec8` `…/connections/witvliet_2020_8.json` | pin; git blob `135b1806872eea14a5f7bb667901285d269df720` |
| `nemanode_baf8ec8__neurons.json` | 58,575 | `c780e0b7cab28b311a7e0916a7b8e37b9cf72de152712bd4a5eb29fd9d595492` | (C) @`baf8ec8` `…/raw-data/neurons.json` | pin; git blob `81da4572b20674dcc852cfa9fd041e66a3c7a73c` |
| `synapse_count_matrices.xlsx` | 764,283 | `bd725d1f6121abeb8ec08d0b80edad94d9e0fea954a8704ee07c7f4be7cebfe6` | (D) `tables/synapse_count_matrices.xlsx` | pin; git blob `e2c29655de6932b1d9e9d968b16f7ed318d3e7e3` |
| `synapse_list.csv` | 1,287,223 | `36c431f25e72cd82946239a2eb555c1ed4494a2036092105bd37eb161ecf9340` | (D) `tables/synapse_list.csv` | pin; git blob `80fc81032f996e75349397c2dec505cd462ca48c` |
| `connection_classifications.csv` | 92,737 | `da94863507a64da8d85d75a280ceff538d30f98a746390a7d0090607b0870f08` | (D) `tables/connection_classifications.csv` | pin; git blob `960ce494eee0352320bde8a3bc82a59fede4d713` |
| `_neurons.csv` | 2,223 | `2189e2ee262a1d1a81f1139fcc95c4b886681cfdd706dc5f77bd8cda2a49491d` | (D) `tables/_neurons.csv` | pin; git blob `bef93bfd871caa8c3fbea910741d01bc9c960ac8` |

Re-running acquisition is idempotent. After the Phase 1 fix, a further run
(2026-10-13) reported all 26 files present and verified. It downloaded
nothing, left the data files' modification times unchanged, and rewrote
`MANIFEST.json` with byte-identical content. `--verify` reports OK.
`--counts` is byte-identical across runs.

### Byte-level relationships between copies

- **NemaNode `baf8ec8` and the first author's repository.**
  `nemanode_baf8ec8__witvliet_2020_{7,8}.json` have the same git blob ids
  (`201d50cd…`, `135b1806…`) as `data/nemanode/witvliet_2020_{7,8}.json` in
  `dwitvliet/nature2021` @`0646af9`. They are therefore byte-identical. They
  were written by that repository's `src/export/export_json.py`
  (`export_nemanode_connections`, added 2021-03-15), so the NemaNode files
  are an export by the first author's figure code (D). The same holds for
  datasets 1–6 (`data/nemanode/witvliet_2020_{1..6}.json` = NemaNode
  `baf8ec8` blobs).
- **Wheel CSVs and Randi et al.'s analysis repository.** `leiferlab/pumpprobe`
  @ `1dbc5e0a2b609d54bc9b1c90c73d4e3bf183d3c7` holds
  `pumpprobe/aconnectome_witvliet_2020_{7,8}.csv` with blob ids `f312c4db…`
  and `b16614e2…`, the git blob ids of the two wheel CSVs: byte-identical
  copies. Not acquired separately.
- **`neurons.json`** is one blob (`81da4572…`) at every NemaNode commit named
  above.
- **NemaNode datasets 1–8 at `859641e`** are the blobs introduced by
  `b6dfd28` (2020-05-18); `a0ff6f3` and `859641e` only moved and renamed
  them. All eight changed again in `baf8ec8`.
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
- **Author's table export (D) and NemaNode `baf8ec8`.**
  - `synapse_count_matrices.xlsx`, sheets Dataset7 and Dataset8, equals the
    `baf8ec8` chemical edges exactly: 2,202 cells summing to 7,467, and 2,186
    cells summing to 7,970.
  - `synapse_list.csv`, datasets 7 and 8: its rows per (pre, post) equal the
    `baf8ec8` weights edge for edge, and its `syn_id` sets equal NemaNode's
    chemical connector-id sets.
- **NemaNode `8a50236`** equals none of the other versions; see "Exact
  differences".

## What each file contains

### Common facts (all versions)

- **Orientation.**
  - Chemical rows are pre → post.
  - `synapse_count_matrices.xlsx` is laid out **[post row, pre column]**:
    row 3 holds the pre names, column 3 the post names, and rows 1–2 and
    columns 1–2 hold "Pre"/"Post" and type labels. It has 180 pre columns
    (types Sensory, Inter, Motor, Modulatory) and 224 named post rows (the
    same plus 32 Muscle and 12 Other). The 12 "Other" post rows are `CANL`,
    `CANR`, `CEPshDL/DR/VL/VR` and `GLRDL/DR/L/R/VL/VR`: the matrices carry
    CAN although `_neurons.csv` omits it. The matrices have no `excgl` row
    or column.
  - Electrical rows have no direction.
- **Weight.** A connection's weight is the number of (synapse, postsynaptic
  partner) records. NemaNode code `populate-connections.js` uses
  `synapseCount = syn.length` (`weight = syn.length` at `8a50236`), and the
  CSV/xlsx `synapses` column equals it.
  - A polyadic synapse adds 1 to every partner's edge. Hence 7,467 weight
    vs 3,562 distinct presynaptic connector ids in dataset 7 (post-revision).
  - A connector id can also be repeated within one chemical entry. 49
    (dataset 7) and 59 (dataset 8) entries do so in every NemaNode version.
    The extra records (weight minus per-entry distinct ids,
    `chem_records_minus_unique_ids_per_edge`) number 67 in d7 at `8a50236`
    and `859641e`, 71 in d7 at `baf8ec8`, and 86 in d8 at all three commits.
    In d7 at `baf8ec8`, 4 ids occur three times, in the entries
    `RIVL→BWM-VR07`, `RMER→BWM-DL04` and `RMGR→BWM-DR06` (×2), the same
    entries that carry `syn` values of 2 at `859641e`.
  - At `859641e` and `baf8ec8`, the repeated records differ in `pre_tid` or
    `post_tid`, except one exact duplicate (same id, `pre_tid` and
    `post_tid`) at `859641e` d7: `ASEL→AIBL`, id 8415363, post_tid 8138259.
    At `8a50236` every repeated record is an exact duplicate (67 in d7, 86
    in d8). What a repeated id means (two contacts, or a duplicated record)
    is not established here.
- **Names.**
  - AWC is `AWCL`/`AWCR` (not AWCON/AWCOFF).
  - Muscles are `BWM-DL01` … `BWM-VR08` (32, zero-padded).
  - Glia: `CEPshDL/DR/VL/VR`, `GLRDL/DR/L/R/VL/VR` (not all present).
  - `excgl` (excretory gland) appears in the `8a50236` and pre-revision data
    only.
  - `CANR` appears in dataset 7 only; there is no CANL in either adult
    dataset file (the author's count matrices (D) list a CANL row, which is
    therefore all zero in Dataset7 and Dataset8).
  - Non-cell fragment names in post-revision gap junctions: `NR_fragment`,
    `vncfrag` (dataset 7); `Fragment`, `VAn` (dataset 8).
- **No pharyngeal neurons.** Witvliet's "brain" is the nerve ring plus the
  ventral ganglion region. The toolbox summary (`Witvliet_2021.md`) reads:
  "Brain was defined as the nerve ring, ventral ganglion and neuropil
  anterior of the ventral sub-lateral commissures"; this is not checked
  against the paper text.

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
    sheet, named like the file. Data cells are str, str, str, int (checked
    for every row by `record_counts`). No creation date in
    `docProps/core.xml`.
- **NemaNode JSON (all three commits).**
  - A list of entries `{pre, post, typ, syn, ids, pre_tid, post_tid}`. `typ`
    0 = chemical, 2 = electrical.
  - Gap junctions are listed in both directions, except those to fragment
    names, which appear in one direction only.
  - `859641e` files hold 4 chemical `syn` values of 2 per adult dataset. In
    dataset 7 these sit on `RIVL→BWM-VR07`, `RMER→BWM-DL04` and
    `RMGR→BWM-DR06`. The `8a50236` and `baf8ec8` files have only 1s.
  - Connector ids: `8a50236` uses small integers (d7 435–4,193; d8
    455–4,466); `859641e` and `baf8ec8` use ids from 8,230,351 upward.
- **`nemanode_baf8ec8__neurons.json`.**
  - 447 cells with `classes`, `typ` (s/i/m/n codes; `b` = muscle;
    `u` = unknown), `nt`, `emb`, `inhead` and `intail`.
  - It types CEPsh, GLR, CANR and excgl as `u`.
  - Its `nt` transmitter codes are NemaNode annotations. Do not use them as a
    transmitter or polarity source without an owner decision.
- **`nemanode_859641e__head.annotations.json`.** NemaNode's per-connection
  classification, `{category: [[pre, post], …]}`, cell-level names. Entries:
  stable 823, variable 1,987, increase 280, decrease 23, postembryonic 552
  (3,665 entries, 3,665 distinct pairs, no pair in two categories, no self
  pairs). Its content is unchanged since `8a50236`, so it is a
  pre-revision classification. Against the authors' Feb-2021
  `connection_classifications.csv` (non-post-embryonic pairs): 25 pairs only
  in the annotations, 34 only in the table
  (`cmp_nemanode_head_annotations__vs__paper_classifications_*`).
- **`nemanode_859641e__witvliet_2020_{1..6}.json`** (datasets 1–6,
  pre-revision). Acquired only for per-dataset counts (classified
  connections present; dataset-1 connections followed into the adults).
  Not used for edges.
- **`synapse_list.csv`.**
  - Columns: `dataset, pre, post, syn_id, sections, size, post_is_branch`.
    Datasets 1–8, 32,105 rows.
  - **Dataset 7 has `size = -1` (missing) on all 7,467 rows.** The authors'
    code also gives Dataset7 no size and no contact data.
- **`connection_classifications.csv`.**
  - Columns `pre, post, classification`, 3,676 rows, no duplicate
    (pre, post). Values: variable 1,995; stable 829; post-embryonic brain
    integration 554; developmentally dynamic (strengthened) 278;
    developmentally dynamic (weakened) 20.
- **`_neurons.csv`.**
  - The first author's table of brain cell classes (D; whether it is a
    Nature ESM table is unverified): 90 classes, 222 members.
  - Members by type: sensory 65, inter 44, modulatory 29, motor 42,
    muscle 32, glia 10.
  - Classes by integration: embryonic 80, post-embryonic 10.
  - It omits CAN; `tables.py` skips it explicitly.
- **Toolbox evidence files.**
  - `WitvlietEtAl2021.md` names `41586_2021_3778_MOESM4_ESM.xlsx`, says the
    WormWiring xlsx also hold electrical connectivity, and says: "The
    chemical connection weights below were read from the supplementary
    information spreadsheet, and the electrical connection weights were taken
    from the WormWiring spreadsheet."
  - `WitvlietDataReader{7,8}_expected_data.yaml`: 3 sampled chemical and 3
    sampled electrical weights per dataset, and `total_nonzero_conns`:
    chemical 2202 (d7) and 2186 (d8), electrical 576 and 612. The toolbox
    does not say where `total_nonzero_conns` came from (its `Validator.py`
    only compares it with its reader's nonzero-cell count). The values equal
    the nonzero cells of the toolbox's own xlsx: chemical 2,202 / 2,186,
    electrical 576 / 612 when each unordered pair fills both cells
    (`cect_xlsx_d<k>_*_nonzero_cells*`). The 3 sampled chemical weights are
    reproduced by every version, including the wheel CSV and the author's
    matrix (D), so they do not discriminate between versions.
  - `Witvliet_2021.md`: the toolbox's paraphrase of the paper, the only
    source reached for 3,113 and 1,292. It also states figures not checked
    here (1,647 connections averaging 323 per dataset; 1,466 connections
    pooled into 658 pair connections).

### Exact differences between the versions of datasets 7 and 8

**Root commit (NemaNode `8a50236`) vs pre-revision (`859641e` = wheel CSV).**

- Dataset 7, chemical: `859641e` has 2 extra edges (`ADLL→PVNL:1`,
  `ADLR→AVJL:1`) and 7 higher weights, all on ADL edges (`ADLL→AIBL` 11 vs
  13, `ADLL→ASHL` 2 vs 6, `ADLL→AVDR` 9 vs 10, `ADLR→AIAR` 8 vs 9,
  `ADLR→AIBR` 10 vs 11, `ADLR→ASHR` 1 vs 5, `ADLR→AVAR` 6 vs 8). Net
  7,448 → 7,465. Distinct connector ids 3,556 vs 3,562.
- Dataset 8, chemical: same edge set; 4 weights differ (`ADLL→ASKL` 6 vs 5,
  `ASKL→ADLL` 1 vs 2, `ASKL→AIBL` 5 vs 6, `ASKR→ADLR` 3 vs 2), net 0
  (7,981 both). Distinct connector ids 3,680 vs 3,681.
- Gap junctions: identical as unordered pairs in both datasets.

**Pre-revision (wheel CSV = NemaNode `859641e`) vs published (NemaNode
`baf8ec8` = xlsx = author's tables (D)).**

Dataset 7:

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

Dataset 8:

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
docstring. The full printed output (2,311 lines by `wc -l`) has SHA-256
`da11a59aa3ccc9d20bbca6f360016b9fbc398692700e823be6f09b6a1accdaaf`, and it
was identical under `PYTHONHASHSEED` 1, 12345 and random (2026-10-13).
`record_counts` reads only `data/raw/witvliet2021/`.

Cells are partitioned two ways, both taken from distributor files with no
judgment added:

- by NemaNode `neurons.json` `typ`;
- by the type in the first author's `_neurons.csv` (D), via NemaNode's
  `classes` field. "Paper type" below, and "paper" in key names
  (`paper_*`, `cells_by_paper_type`, `…_paper_matrix…`), refer to the first
  author's tables (D), not to verified Nature ESM tables.

"Paper reports" below is what the paper itself states. The paper text and
the Nature ESM were not reached, so no row is YES. Where the only reference
is the first author's GitHub table export (D) of Feb 2021, the row says so:
(D) was written by the same `data_manager` pipeline that later wrote NemaNode
`baf8ec8`, so agreement with it is an internal-consistency check, not
agreement with the paper.

| Quantity | Definition | Count in acquired file | Paper reports | Where the paper reports it | Match |
|---|---|---|---|---|---|
| D7 chemical connections / synapses, published version | edges / weight sum; for the matrix, nonzero cells / sum | NN `baf8ec8`, toolbox xlsx, `synapse_count_matrices.xlsx` sheet Dataset7, `synapse_list.csv`: 2,202 / 7,467 (all four equal, edge for edge) | not reached | Nature Supplementary Table (count matrix; which MOESM file is unverified). Closest evidence: the author's table export (D) gives 2,202 / 7,467; the toolbox yaml gives `total_nonzero_conns` 2202 (source not stated by the toolbox; equal to its xlsx) | **UNVERIFIED**: paper and ESM not reached; consistent across four files (three from the first author's pipeline, plus the toolbox/WormWiring xlsx, exporter unknown) |
| D8 chemical connections / synapses, published version | same | same four files: 2,186 / 7,970 | not reached | same; author export 2,186 / 7,970; toolbox yaml `total_nonzero_conns` 2186 | **UNVERIFIED**: as above |
| D7 chemical connections / synapses, **wheel CSV (Randi's input)** | same | 2,204 / 7,465 as stored. Like for like, on the matrix's cell set (pre among its 180 columns, post among its 224 rows; drops `RIVL→excgl`, `SMBVL→excgl`): 2,202 / 7,463 | the published-version count, 2,202 / 7,467, as given by the author's export (D); the paper itself not reached | `synapse_count_matrices.xlsx` sheet Dataset7 (D) | **NO — BLOCKER**: like for like the edge sets are equal, but the synapses are 7,463 vs 7,467 (`RIVL→BWM-VR07` 14 vs 15, `RMER→BWM-DL04` 14 vs 15, `RMGR→BWM-DR06` 6 vs 8). The wheel CSV is the superseded pre-revision version; the owner must choose the version (Q-W1) |
| D8 chemical connections / synapses, **wheel CSV (Randi's input)** | same | 2,194 / 7,981 as stored. On the matrix's cell set (drops `RIVL→excgl`, `SMBVL→excgl`, `SMBVR→excgl`): 2,191 / 7,977 | 2,186 / 7,970 per (D); paper not reached | sheet Dataset8 (D) | **NO — BLOCKER**: 2,191 / 7,977 vs 2,186 / 7,970 like for like (12 edges only in the wheel, 7 only in the matrix, 50 weight differences); same version question (Q-W1) |
| D7 / D8 synapse records and distinct synapse ids | rows and distinct `syn_id` in `synapse_list.csv`; NN `baf8ec8` weight sum and distinct chemical connector ids | 7,467 & 3,562 / 7,970 & 3,674 in both; id sets equal | not reached | — (closest: `synapse_list.csv` (D), "Added missing supplementary info") | **UNVERIFIED**: paper not reached; the two author-derived files agree |
| Adult total chemical synapses | — | one-to-one records: 7,467 (d7), 7,970 (d8); distinct presynaptic ids: 3,562, 3,674. Dataset 1: 1,296 records, 608 distinct ids, 775 connections (`synapse_list.csv`) | "~8,000" (and "~1,300" at birth) | WebSearch excerpts (search summaries of nature.com/articles/s41586-021-03778-8, escholarship.org/content/qt6hf5q104/qt6hf5q104.pdf, biorxiv 2020.04.30.066209v3; version not identified): "from roughly 1,300 at birth to roughly 8,000 in adults (Fig.1e)"; a 2026-10-13 search summary: at birth "~1300 synapses among ~800 connections" | **NOT COMPARABLE**: rounded figures from search paraphrases of unidentified versions. One-to-one records are consistent (1,296; 7,970); distinct presynaptic sites (608; 3,674) are not |
| Mean synapses per connection, birth → adult | — | all edges: d1 1,296/775 = 1.67, d7 7,467/2,202 = 3.39, d8 7,970/2,186 = 3.65 (`synapse_list.csv`). Dataset-1 connections still present in the adult: d8 4,343/634 = 6.85 (`synapse_list.csv`) and 4,331/630 = 6.87 (NN `859641e`); d7 4,010/633 = 6.33 and 3,996/631 = 6.33. Same sums over all 775 dataset-1 connections: d8 5.60 / 5.59, d7 5.17 / 5.16. NN `859641e` d1: 1,298/775 = 1.67 (`d1_edges_in_adult__*`) | 1.7 → 6.9 | 2026-10-13 WebSearch summary (sources listed: PMC8756380, bioRxiv v1/v2 PDFs, Harvard MCB news, openworm.org; version not identified): "the mean synapse number per connection increasing from 1.7 at birth to 6.9 at adulthood". The first version of this record quoted "a 4.6-fold increase" from an earlier excerpt; that wording was not found again and its version is unknown | **UNVERIFIED**: the paper's connection set for 6.9 is not reachable. Closest candidate: dataset-1 connections still present in dataset 8 give 6.85 (post-revision) or 6.87 (pre-revision), both 6.9 when rounded; dataset 1 gives 1.67 |
| Connections classified (stable / variable / developmentally dynamic) | pairs in every category except post-embryonic | Pre-revision NemaNode `head.annotations.json`: 823 + 1,987 + 280 + 23 = **3,113** distinct pairs (`nemanode_head_annotations_pairs_not_postembryonic`). Post-revision `connection_classifications.csv`: 3,122 rows not "post-embryonic brain integration" (10 of them self pairs); 3,676 rows in all | 3,113 | Only a secondary paraphrase: ConnectomeToolbox `docs/Witvliet_2021.md` (acquired; also openworm.org/ConnectomeToolbox/Witvliet_2021/): "3,113 connections (averaging 1,292 per dataset) were assigned as stable, variable or developmentally dynamic." Paper text not reached | **UNVERIFIED**: paper text not reached. If the paraphrase is faithful, it is reproduced exactly by the pre-revision classification, not by the authors' post-revision table (3,122) |
| Connections per dataset, average | classified pairs (as above) present as a chemical (pre, post) pair in each of datasets 1–8, summed, divided by 8 | Pre-revision (`head.annotations.json` pairs in NN `859641e` d1–d8): 775, 986, 1,006, 1,074, 1,391, 1,393, 1,839, 1,872; sum 10,336; **10,336 / 8 = 1,292.0**. Post-revision: `connection_classifications.csv` pairs in `synapse_list.csv` 10,389 / 8 = 1,298.6; `head.annotations.json` pairs in `synapse_list.csv` 10,355 / 8 = 1,294.4. All chemical edges in `synapse_list.csv`: 11,337 / 8 = 1,417.1 | 1,292 | same secondary paraphrase | **UNVERIFIED**: paper text not reached. Reproduced exactly (1,292.0) by the pre-revision data under this definition; the post-revision tables do not give it |
| Brain neurons / muscles | members by paper type | 180 neuron-type and 32 muscle-type cells present in both adult datasets, in all five versions | 180 (65+44+29+42) / 32 per `_neurons.csv`; paper not reached | — (closest: `_neurons.csv` (D)) | **UNVERIFIED**: paper not reached; the author's cell table and every version agree |
| Glia | members of paper type glia | 10 (d7) and 7 (d8) in `8a50236`, `859641e` and the wheel CSV; 9 and 7 in `baf8ec8` and the xlsx | 10 per `_neurons.csv`; paper not reached | — (closest: `_neurons.csv` (D)) | **NOT COMPARABLE**: the table lists the brain's cell set; the dataset files list cells with annotated synapses |
| Gap junctions per dataset | — | see the per-version summary below | none reported. Gap junctions "were partially annotated … but because they could not be mapped in completion, they were excluded from further analyses" | WebSearch excerpt attributed to a preprint version (biorxiv 2020.04.30.066209); another version: "gap junctions were not subjected to the consensus scoring process due to limitations of current sample preparation methods" | **NOT COMPARABLE**: no paper count exists |

### Per-dataset classification counts (datasets 1–8)

All values from `--counts` (`nemanode_859641e_by_dataset_*`,
`nemanode_head_annotations_not_postembryonic_present_in_*`,
`paper_synapse_list_*`, `paper_classified_connections_present_*`); sums and
means are arithmetic on them. Datasets 1–6 also changed in the revision.

| Dataset | NN `859641e` chemical edges | NN `859641e` synapse sum | `head.annotations` pairs present in NN `859641e` | `synapse_list.csv` (pre, post) pairs | `synapse_list.csv` rows | table-classified pairs present in `synapse_list.csv` | `head.annotations` pairs present in `synapse_list.csv` |
|---|---|---|---|---|---|---|---|
| 1 | 775 | 1,298 | 775 | 775 | 1,296 | 775 | 773 |
| 2 | 988 | 1,895 | 986 | 986 | 1,895 | 986 | 985 |
| 3 | 1,007 | 2,134 | 1,006 | 1,012 | 2,128 | 1,012 | 1,008 |
| 4 | 1,101 | 2,772 | 1,074 | 1,136 | 2,777 | 1,106 | 1,099 |
| 5 | 1,505 | 4,069 | 1,391 | 1,515 | 4,116 | 1,402 | 1,396 |
| 6 | 1,526 | 4,432 | 1,393 | 1,525 | 4,456 | 1,394 | 1,392 |
| 7 | 2,204 | 7,465 | 1,839 | 2,202 | 7,467 | 1,847 | 1,837 |
| 8 | 2,194 | 7,981 | 1,872 | 2,186 | 7,970 | 1,867 | 1,865 |
| sum / 8 | 11,300 / 8 = 1,412.5 | | **10,336 / 8 = 1,292.0** | 11,337 / 8 = 1,417.1 | | 10,389 / 8 = 1,298.6 | 10,355 / 8 = 1,294.4 |

### Per-version summary for datasets 7 and 8 (d7 / d8)

All values come from `--counts`; this table has no paper column.

| Quantity | Definition | wheel CSV (= NN 859641e) | NN 8a50236 JSON | NN 859641e JSON | NN baf8ec8 JSON | toolbox xlsx |
|---|---|---|---|---|---|---|
| rows | stored rows/entries | 2,500 / 2,504 | 2,788 / 2,806 | 2,790 / 2,806 | 2,781 / 2,802 | 2,493 / 2,496 |
| cells | distinct names | 224 / 220 | 224 / 220 | 224 / 220 | 224 / 221 | 222 / 219 |
| neurons (paper type sensory+inter+motor+modulatory) | `cells_by_paper_type` | 180 / 180 | 180 / 180 | 180 / 180 | 180 / 180 | 180 / 180 |
| muscles (paper type muscle; NemaNode `b`) | | 32 / 32 | 32 / 32 | 32 / 32 | 32 / 32 | 32 / 32 |
| glia (paper type glia) | | 10 / 7 | 10 / 7 | 10 / 7 | 9 / 7 | 9 / 7 |
| no paper type | names | CANR, excgl / excgl | CANR, excgl / excgl | CANR, excgl / excgl | CANR, NR_fragment, vncfrag / Fragment, VAn | CANR / — |
| chemical edges | ordered (pre, post) rows | 2,204 / 2,194 | 2,202 / 2,194 | 2,204 / 2,194 | **2,202 / 2,186** | **2,202 / 2,186** |
| chemical edges / synapses on the cell set of the author's matrix (D) | `cmp_d<k>_paper_matrix__vs__<v>_restricted_to_matrix_cells_b_*` | 2,202 / 7,463; 2,191 / 7,977 | 2,200 / 7,446; 2,191 / 7,977 | — (= wheel CSV) | 2,202 / 7,467; 2,186 / 7,970 | — |
| chemical self-edges | pre = post | 11 / 5 | 11 / 5 | 11 / 5 | 11 / 0 | 11 / 0 |
| chemical synapses (weight sum) | Σ `synapses` = Σ len(syn) | 7,465 / 7,981 | 7,448 / 7,981 | 7,465 / 7,981 | **7,467 / 7,970** | **7,467 / 7,970** |
| chemical, Σ syn values | JSON only | — | 7,448 / 7,981 | 7,469 / 7,985 | 7,467 / 7,970 | — |
| distinct presynaptic connector ids | JSON only | — | 3,556 / 3,680 | 3,562 / 3,681 | 3,562 / 3,674 | — |
| repeated connector-id records within an entry | weight minus per-entry distinct ids | — | 67 / 86 | 67 / 86 | 71 / 86 | — |
| chemical edges, both ends NemaNode neuron-coded | | 1,944 / 1,936 | 1,942 / 1,936 | 1,944 / 1,936 | 1,944 / 1,933 | 1,944 / 1,933 |
| … their synapse sum | | 6,587 / 7,108 | 6,570 / 7,108 | 6,587 / 7,108 | 6,587 / 7,099 | 6,587 / 7,099 |
| gap-junction rows | stored | 296 / 310 | 586 / 612 | 586 / 612 | 579 / 616 | 291 / 310 |
| gap unordered pairs | incl. self | 296 / 310 | 296 / 310 | 296 / 310 | 294 / 314 | 291 / 310 |
| gap self pairs | a = a | 6 / 8 | 6 / 8 | 6 / 8 | 6 / 8 | 6 / 8 |
| gap weight sum | Σ over unordered pairs | 406 / 430 | 406 / 430 | 406 / 430 | 403 / 434 | 400 / 430 |
| distinct gap connector ids | JSON only | — | 406 / 430 | 406 / 430 | 403 / 434 | — |

All web-search excerpts above are search-engine renderings of the listed
pages. Their exact wording and page location are unconfirmed because
nature.com, PMC, bioRxiv, escholarship and zenodo are blocked here.

## Discrepancies, flags and open questions

**Headline finding.** NemaNode's history holds three versions of datasets 7
and 8, all committed by the first author:

- `8a50236` (2020-05-14), the first upload, replaced four days later by a
  bug fix ("two synapses were counted only once");
- the **pre-revision** content (`b6dfd28`, 2020-05-18; renamed in `859641e`,
  2020-05-22), which is what the wheel CSVs hold;
- the **published** content (`baf8ec8`, 2021-03-15, "Updated witvliet
  datasets after paper revision"), which equals the first author's table
  export (D; Nature ESM identity unverified) and the WormWiring
  spreadsheets carried by the ConnectomeToolbox.

Randi et al.'s code works from the pre-revision content.
`wormneuroatlas` reads the wheel CSVs only when called with non-default
parameters; with its defaults (`chem_th=0, gap_th=0, exclude_white=False,
average=False`) `NeuroAtlas.get_aconnectome_from_file` returns
`aconnectome_default.h5`, which was compiled from those CSVs (P1-W2). Randi's
analysis repository `leiferlab/pumpprobe` @ `1dbc5e0a` carries byte-identical
copies of the CSVs, and its `Funatlas.get_aconnectome_from_file` reads them
directly (`_get_aconnectome_witvliet`). Which code path produced the paper's
figures is a randi2023 question; both paths use the pre-revision content.

All three published-version copies agree edge for edge on chemical synapses.
The wheel CSVs do not. Choosing the version is an owner decision (Q-W1). Until
then, the wheel CSVs' counts are a mismatch against the published version and
are logged as a blocker.

- **P1-W1. Randi used the superseded version** (BLOCKER until Q-W1 is
  decided).
  - The wheel CSVs equal NemaNode's pre-revision content (repository content
    from 2020-05-18 to 2021-03-15).
  - The author's table export (D), NemaNode since 2021-03-15, and the
    WormWiring xlsx all equal the revised data.
  - As stored, the wheel files are 2,204/7,465 (d7) and 2,194/7,981 (d8);
    the published files are 2,202/7,467 and 2,186/7,970. On the cell set of
    the author's matrix (D) the wheel files are 2,202/7,463 and 2,191/7,977.
  - Reproducing Randi's anatomy comparisons needs the wheel version; using
    "Witvliet 2021 as published" needs the revised version. They are not
    interchangeable for dataset 8 (22 edge-set changes and 50 weight
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
    `…/scratchpad/agent_witvliet2021/scripts/repro_default.py`. The Phase 1
    verifier reproduced it independently with its own reimplementation.
  - The h5's VD9 row holds 4,141 incoming chemical synapses, of which 974
    come from Witvliet 7 and 978 from Witvliet 8. **AWCON and AWCOFF have
    zero anatomical synapses** in that file. (Scratch numbers, not in
    `record_counts`: they need a randi2023 file.)
  - The same rule is in Randi's analysis code: `pumpprobe` @ `1dbc5e0a`
    `Funatlas.ids_to_i` starts every id at −1 and overwrites it only on a
    match, and `_get_aconnectome_witvliet` indexes `chem[ai_to, ai_from]`
    without a check. Its atlas is `np.unique` of `aconnectome_ids.txt`
    (300 ids), whose last sorted id is VD9 (scratch check of that file). So
    the VD9 folding is not specific to the h5.
  - This project must build its anatomy from the raw files, never from
    `aconnectome_default.h5`.
- **P1-W3. `41586_2021_3284_MOESM5_ESM.xlsx` is not a Witvliet file.**
  - 41586_2021_3284 is Brittin et al. 2021, Nature 591:105, doi
    10.1038/s41586-021-03284-x. The toolbox's
    `cect/validation/Brittin2021.md` calls it "Supplementary data file 3 …
    containing the M^δ, C^δ and G^δ reference graphs". Toolbox path
    `cect/data/41586_2021_3284_MOESM5_ESM.xlsx`, blob `10fa5f0e…`.
  - Sheets: `restricted_cells` (173 cells; columns `cell`,
    `bilateral_cell_class`, `single_cell_class`); `M` (2,955 contact rows),
    `C` (1,474 chemical rows) and `G` (389 gap rows), each with columns
    `cell_1, cell_2, weight, delta`.
  - Its `docProps/core.xml` says created 2024-11-11 and modified
    2024-11-11 by "Microsoft Office User" (Excel for Mac). It was re-saved
    after publication, so it is probably not byte-identical to the Nature
    ESM.
  - Not acquired here; a separate source if the owner wants a contactome
    (Q-W9). (Scratch reading, not in `record_counts`.)
- **P1-W4. Gap junctions and an `anat_gap` column.**
  - Witvliet states gap junctions were only partially annotated, were not
    consensus-scored, and were excluded from the paper's analyses (excerpts
    above). The author's tables (D) carry no gap junctions.
  - The files that do carry them are NemaNode, the CSV and the xlsx.
    Post-revision: 403 / 434 gap-junction ids (d7 / d8) against 3,562 /
    3,674 chemical ids. Pre-revision: 406 / 430 against 3,562 / 3,681.
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
       dataset 8, so NemaNode loses nothing for real cells. (Scratch check.)
    5. Orientation is meaningless, and storage differs by copy: both
       directions in JSON, one in CSV/xlsx.
- **P1-W5. Coverage of the head set.**
  - 34 of Randi's 188 head neurons (`randi2023/aconnectome_ids_ganglia.json`)
    never occur in either adult Witvliet dataset, in any version:
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
  omitted from the author's `_neurons.csv` (D). The author's count matrices
  (D) do carry CAN: `synapse_count_matrices.xlsx` lists `CANL` and `CANR`
  among its 12 "Other" post rows (with `CEPshDL/DR/VL/VR` and
  `GLRDL/DR/L/R/VL/VR`).
  Randi's atlas has no CAN.
- **P1-W9. Self-loops in chemical data.** d7 has 11 in every version
  (ADEL, AIMR, ASER, ASHL, RMDDL, RMDDR×2, RMED, RMEL, RMER, RMGL, SDQL).
  d8 has 5 pre-revision (and at `8a50236`) and 0 published.
- **P1-W10. The paraphrased paper figures match the pre-revision data.**
  - 3,113 classified connections and 1,292 per dataset are reproduced
    exactly by NemaNode's pre-revision classification and datasets (3,113;
    10,336 / 8 = 1,292.0). The authors' Feb-2021 tables give 3,122 and
    1,298.6. Reproduction tests: `tests/test_reproduction.py`
    (`test_witvliet_3113_…`, `test_witvliet_1292_…`).
  - Both figures are known only from the ConnectomeToolbox paraphrase, which
    cites the Nature paper. So either the paraphrased text is from a
    pre-revision version (e.g. the preprint), or the published text kept
    figures computed from the pre-revision data while its tables are
    post-revision. Which one holds is unverified until the paper text is
    read.
  - 1.7 → 6.9 synapses per connection: the closest definition found
    (dataset-1 connections still present in dataset 8) gives 6.85
    post-revision and 6.87 pre-revision; it does not discriminate between
    versions.
- **P1-W11. The toolbox's "NemaNode exports".** The toolbox calls the xlsx
  WormWiring spreadsheets. They are LibreOffice files, so the export tool is
  unknown. Their content equals the post-revision NemaNode data minus
  fragment gap junctions.
- **P1-W12. NemaNode's first upload (`8a50236`) is a third version.** It is
  superseded by a bug fix four days later and equals neither the wheel nor
  the published data (d7 2,202 edges / 7,448 synapses, which on the
  matrix's cell set is 2,200 / 7,446; d8 2,194 / 7,981 with 4 weights that
  differ from `859641e`). Acquired so that every version found is on
  record; not a candidate for `anat_chem_witvliet` unless the owner says so.
- **Available but not acquired** (no silent drops):
  - **Datasets 1–6 (L1–L3), other copies.**
    - Toolbox `cect/data/witvliet_2020_{1..4} L1.xlsx`,
      `witvliet_2020_5 L2.xlsx` and `witvliet_2020_6 L3.xlsx` (blobs
      `961275d9…`, `44bb6852…`, `2296913f…`, `92d5f930…`, `c6e4ee54…`,
      `ddd71487…`).
    - NemaNode `connections/witvliet_2020_{1..6}.json` at `baf8ec8`
      (published; blobs `717592bd…`, `7986d43b…`, `1dbe8fb6…`, `0b0842d7…`,
      `7153b50a…`, `e1df025a…`) and their first versions at `8a50236`
      (`SEM_L1_3`, `TEM_L1_5`, `SEM_L1_4`, `SEM_L1_2`, `SEM_L2_2`, `TEM_L3`
      `.head.json`; blobs `d6014d0c…`, `e68d764f…`, `9cddd71f…`,
      `4047ebe9…`, `902095aa…`, `e8d07746…`). The `859641e` versions are
      acquired.
    - `dwitvliet/nature2021` `data/nemanode/witvliet_2020_{1..6}.json` (same
      blobs as NemaNode `baf8ec8`).
    - The acquired `synapse_list.csv` and `synapse_count_matrices.xlsx`
      already contain datasets 1–6 but are only summarised here.
    - Owner decides if juvenile data matter (Q-W7).
  - **Upstream author data** in `dwitvliet/nature2021` @`0646af9`:
    - `data/synapses/Dataset{1..8}_{synapses,gapjunctions}.json` (raw
      CATMAID exports);
    - `data/skeletons/` (8 files), `data/physical_contact/` (14 files, no
      Dataset7);
    - `tables/synapse_size_matrices.xlsx` and `tables/contact_matrices.xlsx`.

    These are not needed for edge-level counts, and the gap-junction
    contents were checked equal to NemaNode in scratch.
  - **Other `dwitvliet/nature2021` files** @`0646af9`:
    - `tables/_cells_in_modules.pdf` and `.png`: a module-membership figure,
      changed after the first revision (`f9be786` "Updated modules after
      first revision", `95201cc` "Fixed module names", both 2021-02-17). Out
      of scope (no edges).
    - `data/legacy_data/{catmaid_JSH_nmjs.json, catmaid_N2U_nmjs.json,
      durbin.txt, wormwiring_N2U.txt}` (added in `76ce33b`, "Added legacy
      data"): White/N2U/JSH and Durbin legacy data, white1986 scope.
    - `figures/` (156 files of figure output) and `src/`,
      `generate_figures.ipynb` (code): not data releases.
  - **Other NemaNode files.**
    - `raw-data/datasets.json` (dataset ids, names and ages; changed again
      after `859641e` in `230afb6` and `4b700bc`, 2020-05-22): metadata only.
    - `annotations/complete.annotations.json`: a 383-byte "not-imaged" list
      of class pairs (blob `77b650d7…`), added in `8a50236` and moved
      unchanged by `a0ff6f3` (so present at `8a50236`, `b6dfd28` and
      `a0ff6f3`); emptied to `{}` by `04cbaeb` (2020-05-19, "Removed
      'not-imaged' annotations in preparation for better comparisons of
      data") and unchanged since (blob `bfd870e4…` at `859641e`, `baf8ec8`
      and `6b7ca03`). Not Witvliet connectivity.
    - `raw-data/adult-complete-neurons.json` (blob `3b2b7c31…`, 56,439 bytes
      per `git ls-tree -l`): added in `8a50236`, moved unchanged by
      `a0ff6f3` (so present at `8a50236`, `b6dfd28` and `a0ff6f3`), deleted
      by `859641e`. A NemaNode cell table in the `neurons.json` format
      (`name`, `classes`, `typ`, `nt`, `emb`, `inhead`, `intail`), not
      Witvliet connectivity; not needed.
    - `trajectories/`: not needed.
    - `white_1986_{jsh,n2u,whole,jse}.json`: these belong to the white1986
      source (Phase 0 flag F9). The Zhen-lab muscle annotations of JSH/N2U
      live there. Their pre-`859641e` names were `white_l4.head.json`,
      `white_ad.head.json`, `adult.complete.json` and `jse.tail.json`, and
      `b6dfd28` also changed `white_ad.head.json` and `white_l4.head.json`.
  - **ConnectomeToolbox @ `ffe5702`, other Witvliet files.**
    - `cect/cache/WitvlietDataReader{1..8}.json`: derived caches of the
      toolbox's readers.
    - `cect/validation/WitvlietDataReader{1..6}_expected_data.yaml`:
      juvenile datasets (Q-W7).
    - `cect/readers/WitvlietDataReader*.py`, `docs/api/…`: code and API
      documentation.
  - **`leiferlab/pumpprobe` @ `1dbc5e0a` `pumpprobe/aconnectome_witvliet_2020_{7,8}.csv`**
    (and the same blobs under `build/lib.linux-x86_64-3.8/`): byte-identical
    to the acquired wheel CSVs (same blob ids), so nothing new.
  - **Wheel `aconnectome_default.h5`.** A composite of four sources with the
    P1-W2 defect; it belongs to randi2023 if wanted at all.
  - **Nature ESM files for Witvliet** (e.g. `41586_2021_3778_MOESM4_ESM.xlsx`):
    host blocked.
  - **Zenodo record 5637219** (author data release, 2021-11-01, per a search
    result): host blocked; contents beyond the search result unknown.
  - **Paper text sources** (PMC8756380 author manuscript, bioRxiv preprint,
    the wormatlas PDF): hosts blocked; needed only to read the paper's
    figures.
  - **Brittin MOESM5:** see P1-W3.

### Owner questions

- **Q-W1. Which version is canonical for `anat_chem_witvliet`?**
  - The published version: NemaNode `baf8ec8`, equal to the author's
    tables (D) and the WormWiring xlsx.
  - Randi's pre-revision input: the wheel CSV, equal to NemaNode `859641e`.
  - Or both as separate columns: one to reproduce Randi, one to represent
    Witvliet 2021.
  - Note for the decision: the paper-text figures 3,113 and 1,292 (known
    only from a paraphrase) match the pre-revision data, so "the version the
    paper text describes" and "the version of the author's tables (D)" may
    not be the same (P1-W10). NemaNode `8a50236` is on record but superseded
    within four days by a bug fix (P1-W12).
- **Q-W2. Weight unit.** One-to-one (synapse, partner) records (NemaNode,
  CSV, the author's matrices (D)), or distinct presynaptic sites? For the
  pre-revision data, `len(syn)` or the sum of `syn`? How to treat connector
  ids repeated within one entry?
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
- **Q-W7. Juvenile datasets 1–6:** needed (beyond the per-dataset counts
  above)?
- **Q-W8. Edge-level attributes.** Use Witvliet's stable/variable/dynamic
  classification as an edge attribute? If so, which one: the post-revision
  `connection_classifications.csv` or the pre-revision NemaNode
  `head.annotations.json`? Use synapse size (dataset 8 only)?
- **Q-W9. Brittin 2021** (MOESM5 contactome and C/G graphs): a separate
  source?
