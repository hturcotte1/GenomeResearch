# canonical_neurons: candidate lists of hermaphrodite neuron names (WormAtlas / White 1986 naming)

- Paper: White JG, Southgate E, Thomson JN, Brenner S. *The structure of the
  nervous system of the nematode Caenorhabditis elegans.* Phil Trans R Soc
  Lond B 314, 1–340 (1986). doi:10.1098/rstb.1986.0056. Names as compiled by
  WormAtlas (Altun ZF, Herndon LA, Wolkow CA, Crocker C, Lints R, Hall DH
  (eds.), http://www.wormatlas.org). Some candidates come from other works:
  Cook et al. 2019 (Nature 571:63–71, doi:10.1038/s41586-019-1352-7) for
  `Cells.py`, NemaNode / Witvliet et al. 2021 for the NemaNode cell table, and
  Randi et al. 2023 for `neuron_ids.txt`.
- Module: `src/acquire/canonical_neurons.py`
- Status: **SECONDARY — primary comparison PENDING (blocks Phase 4 freeze)**
- Retrieval date (UTC): 2026-10-12 for all nine files, from
  `data/raw/canonical_neurons/MANIFEST.json`

This source exists only to supply candidates for the Phase 2 canonical
namespace (decision D-009). Nothing here picks a candidate, renames anything,
or derives classes by a naming rule. Those choices are listed as owner
questions at the end.

## Primary location (not reachable from this environment)

wormatlas.org is blocked. The WormAtlas pages these copies claim to come from
are:

| Acquired file | Primary it names or derives from | Primary check to perform once reachable |
|---|---|---|
| `IndividualNeurons.csv` | https://www.wormatlas.org/NeuronNames.htm. The file's first line names it. The toolbox reader's comment names https://wormatlas.org/neurons/Individual%20Neurons/Neuronframeset.html | Compare every name, expanded name, lineage and description row by row |
| `C. elegans Cell List - WormAtlas.tsv`, `cell_lineage.txt` | http://www.wormatlas.org/celllist.htm ("Complete Cell List"). It is named in owmeta `docs/data_sources.rst` and `owmeta/data_trans/wormatlas.py` | Diff both copies against the live list. They differ from each other (see below), so at most one can equal any given WormAtlas version |
| `C. elegans Cell List - WormBase.csv` | OpenWorm Google Sheet `1NDx9LRF_B2phR5w4HlEtxJzxx1ZIPT2gA0ZmNmozjos`, named in the file's first row as the "latest version". It is compiled from WormBase and WormAtlas | Compare against the sheet (docs.google.com reachability untested) and against WormBase WBbt ids |
| `neurons.csv` | Not documented. In owmeta `save_data.py` it is the `neurons` data source, "the principle such list for OpenWorm" | None possible; the origin is unknown |
| `Cells.py`, `all_cell_info.csv` | No primary. These are toolbox code and toolbox output. The header says "Much of this data taken from supplementary info of Cook et al 2019" | Compare the 302 names with Cook et al. 2019 SI (Nature supplement; blocked) |
| `cell_lineage.txt`, `neuron_ids.txt` | Randi et al. data release (funconn.princeton.edu / OSF; blocked). The package does not say where `cell_lineage.txt` came from | Compare with the portal's id list |
| `nemanode_da8ca7e__neurons.json` | https://nemanode.org/ cell table (blocked) | Same check as in `white1986` |

## Files acquired

Distributions (all SECONDARY):

- **(T)** GitHub `openworm/ConnectomeToolbox` @ `ffe570268b7cffb9329cd009a1bb37d60db2d465` (2026-09-29)
- **(O)** GitHub `openworm/owmeta` @ `945f7172f0dff1d022ce0574f3c630ee53297386` (2015-12-18, S. Larson, "clarify source of some data"). This is the commit that owmeta's own `docs/data_sources.rst` links to for the staged cell lists. The same three blobs are at `openworm/OpenWormData` master `69ecfd5e6645e37accea0347b0f1e41fa3a52475` (2020-12-14), under `data_source_data/*/4cbb96ef-710a-4731-b1cb-f104164678d1/`, so the content did not change between 2015 and 2020.
- **(W)** PyPI wheel `wormneuroatlas-0.0.7.3-py3-none-any.whl`, SHA-256 `166289031784c9565f6b9205e30dc718bafbc092db3b46f1aef73d93dc4d1325`
- **(N)** GitHub `zhenlab-ltri/NemaNode` @ `da8ca7e2fc0eece4b21c30625880b41f39961c76` (the same pin as `white1986`)

| File | Size (bytes) | SHA-256 | Distributor / URL | Integrity checks passed |
|---|---|---|---|---|
| `IndividualNeurons.csv` | 43,664 | `b69c0e994270493535994a69a47210dda04319592697eec2f4a65a9df8886195` | (T) https://raw.githubusercontent.com/openworm/ConnectomeToolbox/ffe570268b7cffb9329cd009a1bb37d60db2d465/cect/data/IndividualNeurons.csv | size + SHA-256 = pin; git blob `f37e334763659bc0d74cb9ec99c4b817800e1e7c` = blob at the commit |
| `Cells.py` | 76,075 | `9ad91db16d4825617a03070ff8fc81e680d24028cbc1e29ee63f0f71f47b90b5` | (T) …/cect/Cells.py | size + SHA-256 = pin; git blob `09a7384f5c1b8ae8c4ea4f2eacff18600b50ab0a` |
| `all_cell_info.csv` | 77,388 | `63c6fc5f55c90df092b24afe1cbfc96da63f577288e74621d6395fc195e6221d` | (T) …/cect/data/all_cell_info.csv | size + SHA-256 = pin; git blob `76994dc81d58a4c331a6f186d04dcabff3c955dc` |
| `C. elegans Cell List - WormAtlas.tsv` | 83,494 | `972665abe3ade4ead6bd0265282a09010b19772a7c7376c2e442ea9ca1c59fa1` | (O) https://raw.githubusercontent.com/openworm/owmeta/945f7172f0dff1d022ce0574f3c630ee53297386/OpenWormData/aux_data/C.%20elegans%20Cell%20List%20-%20WormAtlas.tsv | size + SHA-256 = pin; git blob `cff6d256cc97bfb9446d8e9ba8439016b8cf59d1` |
| `C. elegans Cell List - WormBase.csv` | 169,029 | `1fa858cc10d8a0d0eb87f8bbc0693d2821cfeed8e007d267c09507a8bde6c571` | (O) …/OpenWormData/aux_data/C.%20elegans%20Cell%20List%20-%20WormBase.csv | size + SHA-256 = pin; git blob `667305bf777e51c5d7be744cd11e638a7b227b23` |
| `neurons.csv` | 11,899 | `1bf39be45c40605320f92d4fe105760021fc2bf41c25dea24522d0309d63468b` | (O) …/OpenWormData/aux_data/neurons.csv | size + SHA-256 = pin; git blob `1405f5b3af7b55297163a359d84d361e22c85f40` |
| `cell_lineage.txt` | 83,696 | `d1f22fd7cdf125bf515e4c399f040319103139c34c4425a3c0e8411cddb3e840` | (W) member `wormneuroatlas/data/cell_lineage.txt` | wheel SHA-256 = PyPI's published digest (checked live); member = pin; member = wheel `RECORD` |
| `neuron_ids.txt` | 2,645 | `e2c7e54af611c1e85aa0705588fcf096ede5f0c28f7fd1d5f0cbec5480b786cc` | (W) member `wormneuroatlas/data/neuron_ids.txt` | same three checks |
| `nemanode_da8ca7e__neurons.json` | 58,575 | `c780e0b7cab28b311a7e0916a7b8e37b9cf72de152712bd4a5eb29fd9d595492` | (N) https://raw.githubusercontent.com/zhenlab-ltri/NemaNode/da8ca7e2fc0eece4b21c30625880b41f39961c76/src/server/populate-db/raw-data/neurons.json | size + SHA-256 = pin; git blob `81da4572b20674dcc852cfa9fd041e66a3c7a73c` |

A second acquisition run verified all nine files without re-downloading
them. File mtimes were unchanged and `MANIFEST.json` was byte-identical
(SHA-256 `c121206a…`). Two `--counts` runs gave byte-identical output.

### Byte-level relationships between copies

- `neuron_ids.txt` is byte-identical (same SHA-256) to `randi2023/neuron_ids.txt`.
- `nemanode_da8ca7e__neurons.json` is byte-identical to
  `white1986/nemanode_da8ca7e__neurons.json` and
  `witvliet2021/nemanode_baf8ec8__neurons.json`.
- The three (O) files are the same git blobs at owmeta `945f717` and at
  OpenWormData `69ecfd5`.
- `C. elegans Cell List - WormAtlas.tsv` vs `cell_lineage.txt`: **the
  content differs.** Both are LF-terminated with a final newline.
  - Header: `Cell / Lineage Name / Description` vs `#Cell  / Lineage Name  / Description` (the wheel adds trailing spaces).
  - Rows: 1,356 vs 1,359. 755 rows are identical as written.
  - Lineage separator: 1,308 rows match if the first space in the wheel's
    lineage is read as "." (the wheel writes `AB plapaaaapp`; OpenWorm writes
    `AB.plapaaaapp`).
  - The remaining differences:
    - the wheel repeats `ADFL`;
    - it writes `PHRB` where OpenWorm has `PHBR` (same lineage);
    - it adds `MCML`/`MCMR`;
    - the RIPR lineage is `AB arappaaaa` vs `AB.prappaaaa`;
    - the lineages of `M`, `pm1VR` and `pm4VR` differ;
    - `arc_ant`/`arcpost`/`cc_*` are spelled `arc ant DR`, `arc post DL`, `cc herm DL`, … (individually named);
    - `hyp7 ` and `mu_bod ` have trailing spaces on 3 and 14 rows;
    - two `int` descriptions differ;
    - "Mail tail seam" is corrected to "Male tail seam".
- `all_cell_info.csv` is generated from `Cells.py` + `IndividualNeurons.csv`
  by toolbox code, so it is a derived copy, not an independent list.

## What each file contains

**`IndividualNeurons.csv` (T): WormAtlas neuron-names table copy**

- First line: `# Data taken from https://wormatlas.org/NeuronNames.htm ;;;`.
- Then 397 `;`-separated rows of 4 fields: name; expanded name (e.g.
  "Anterior Process from Deirid Commissure A Left"); lineage (mostly space style,
  `AB plapaaaapp`, with a leading space after `;`; some rows carry extras such as
  `P1.aaaa/ W.aaa` or `TL.paa (PHsoL)`); description. LF line
  endings, no final newline.
- 393 distinct names. `DX1/2`, `DX3/4`, `EF1/2`, `EF3/4` each appear twice,
  once per lineage.
- Hermaphrodite and male neurons together. All 302 `Cells.py` names are
  present. The other 91 names (95 rows) are listed in full in `--counts`
  `diff.individual_minus_cellspy302`. Of those 95 rows, 93 have descriptions
  that say "Male specific …" or "Male sensory rays". The other two are
  PVS/PVU ("PVPR/PVPL interneuron of male …"). The file has no sex column,
  so this split rests only on the description text.
- AVFL/AVFR are separate rows, each with lineage `P1.aaaa/ W.aaa`. DB1's
  description says "(aka DB1/3)", and DB3's expanded name is "Dorsal B-type
  Motor Neuron 3/1".

**`Cells.py` (T): toolbox source, parsed with `ast` only, never imported**

- The literal `PREFERRED_HERM_NEURON_NAMES` holds 302 names, alphabetically
  sorted, with no duplicates.
- The toolbox also builds `PREFERRED_HERM_NEURON_NAMES_COOK` from Cook 2019
  category lists: sensory 83 + interneurons 89 + motor 123 + pharyngeal
  polymodal 5 + "unknown function" 2 (CANL, CANR). Resolving it statically
  (list literals and `+` only) gives the same 302-name set. The file asserts
  `len(PREFERRED_HERM_NEURON_NAMES_COOK) == 302`.
- Other lists: `PHARYNGEAL_NEURONS` (20), `VENTRAL_CORD_MOTORNEURONS` (71),
  `MALE_SPECIFIC_NEURONS` (90). It also has functions encoding naming rules
  (`get_SIM_class`, `remove_leading_index_zero`, …), which are recorded but
  not applied.

**`all_cell_info.csv` (T): derived**

- Header `Cell name,Type,Name details,Lineage,Classification`. 629 rows, CRLF.
- 386 rows have 5 fields; **243 rows have 6 fields under the 5-field
  header**. This is a toolbox generator defect: the non-neuron branch of
  `generate_cell_info_pages` writes 6 values.
- The `Type` column carries Cook 2019 category notes, e.g. "Layer 3
  interneuron" or "Sublateral motor neuron; interneuron in White et al.,
  1986".
- It contains all 302 names, but splits `DX1/2` etc. into `DX1`…`DX4`.

**`C. elegans Cell List - WormAtlas.tsv` (O): WormAtlas complete cell list copy**

- Tab-separated `Cell / Lineage Name / Description`, 1,356 rows covering
  every cell type (neurons, glia, muscles, hypodermis, gonad, …) with 685
  distinct names. There is **no neuron flag**, so a neuron count cannot be
  derived from this file alone.
- Lineages use "." (`AB.plapaaaapp`). 64 lineages contain a space: 63 are
  male ray cells with a second name, e.g. `V5L.pppppaaa, R1.aaa`, and one is
  `linker_killer` (`U.lp or U.rp`).
- Neuron-relevant name quirks:
  - `AVFL/R` appears twice (lineages `P1.aaaa`, `W.aaa`);
  - `DB1/3` (`AB.plpaaaapp`) and `DB3/1` (`AB.prpaaaapp`) appear;
  - `DX1/2`, `DX3/4`, `EF1/2`, `EF3/4` appear twice each.
- Consequently AVFL, AVFR, DB1 and DB3 do not occur as written. The owmeta
  translator resolved them by its own rule, with the comment "XXX: These
  renaming choices are arbitrary".

**`C. elegans Cell List - WormBase.csv` (O): OpenWorm cell spreadsheet**

- Layout: 3 heading rows (title, header, totals), then 1,356 data rows, all
  21 fields. CRLF, no final newline.
- The title row says it was "compiled and maintained by the OpenWorm
  project …, originally sourced from WormBase … and WormAtlas".
- 0/1 columns include "Neurons (no male-specific cells)" and "Neurons
  (male-specific)". Further columns: `WormBase ID` (WBbt), `Synonyms`, and
  VirtualWorm blender names.
- The totals row states 959 (identified adult-only hermaphrodite cells),
  1136 (adult-only male cells), 302, 68, 95, 37, 26, 499, 212, 125, 341,
  321, 606.
- For every 0/1 column, the number of rows marked 1 equals its stated
  total. The two "Total count" columns have no 1s.
- The hermaphrodite-neuron column marks 302 distinct names, each with a
  WBbt id.
- The male column marks 68 rows but only 64 distinct names (`DX1/2` etc.
  twice). It includes `HOsh`, `HOso`, `PChL`, `PChR`, which are absent from
  `IndividualNeurons.csv`.
- The synonyms of PHBR include `PHRB`.

**`neurons.csv` (O)**

- 302 rows of `name;type;lineage`, no header, LF.
- There are 46 distinct free-text type strings, e.g. "Sensory neuron
  (Chemosensory?)" or "Neuron with unknown function." (with and without a
  final period).
- Lineages use "." style.

**`cell_lineage.txt` (W)**

- A second copy of the WormAtlas cell list: 1,359 rows, 696 distinct names;
  differences listed above.
- How the authors' `CellLineage` class reads it: it skips names containing
  "/" (so AVFL/R, DB1/3 and DB3/1 are dropped). It does not skip the header
  line, so `#Cell ` becomes a "cell".
- Its `version`/`description` attributes are copy-pasted from the
  synapse-sign class ("Currently using results from Fenyves et al. 2020").

**`neuron_ids.txt` (W)**

- 300 rows of `index<TAB>id`, with indices 0–299. The order is not
  alphabetical.
- The ids equal the 302 minus {AWCL, AWCR, CANL, CANR}, plus {AWCOFF, AWCON}.

**`nemanode_da8ca7e__neurons.json` (N)**

- 447 entries with keys `classes, emb, inhead, intail, name, nt, typ`.
- It covers neurons plus 145 non-neuron entries (BWM-DL01…, `pm1`, `mc1DL`,
  `GLRL`, `CEPshDL`, `hyp`, `LegacyBodyWallMuscles`, …).
- All 302 names are present.
- Its `classes` field is the only explicit class assignment among the
  candidates. Numbered motor-neuron groups are single classes (`ASn`, `DAn`,
  `DBn`, `DDn`, `VAn`, `VBn`, `VCn`, `VDn`). The single-letter `typ`/`nt`
  codes are not documented in the file and are not interpreted here.

### Name style, per candidate (from `--counts` `probe`)

| Candidate | Distinct names | CANL/CANR | AWC | 20 pharyngeal (I1L…I6, M1…M5, MCL/R, MI, NSML/R) | VNC numbering | Names with "/" |
|---|---|---|---|---|---|---|
| `Cells.py` 302 | 302 | yes | AWCL, AWCR | 20/20 | 75 numbered names, none zero-padded (VB1) | none |
| WormBase.csv herm column | 302 | yes | AWCL, AWCR | 20/20 | 75, unpadded | none |
| `neurons.csv` | 302 | yes | AWCL, AWCR | 20/20 | 75, unpadded | none |
| `IndividualNeurons.csv` | 393 | yes | AWCL, AWCR | 20/20 | 75, unpadded | DX1/2, DX3/4, EF1/2, EF3/4 |
| `neuron_ids.txt` | 300 | **no** | **AWCOFF, AWCON** | 20/20 | 75, unpadded | none |
| NemaNode table | 447 (all cells) | yes | AWCL, AWCR | 20/20 | 75, unpadded | none |
| WormAtlas.tsv (all cells) | 685 | yes | AWCL, AWCR | 20/20 | **73** (no DB1, DB3) | AVFL/R, DB1/3, DB3/1, DX…, EF…, P1/2L…, hyp8/9 |
| `cell_lineage.txt` (all cells) | 696 | yes | AWCL, AWCR | 20/20 | **73** (no DB1, DB3) | same as the .tsv |
| `all_cell_info.csv` | 629 | yes | AWCL, AWCR | 20/20 | 75, unpadded | none |

No candidate zero-pads ventral-cord names. Zero-padded forms such as VA01
occur only in the Varshney/Cook connectome files (see `white1986`).

### Exact set differences (names as written)

- `Cells.py` 302 = WormBase.csv herm column = `neurons.csv` (identical sets).
- 302 − `neuron_ids.txt` = {AWCL, AWCR, CANL, CANR};
  `neuron_ids.txt` − 302 = {AWCOFF, AWCON}.
- 302 − `IndividualNeurons.csv` = ∅. `IndividualNeurons.csv` − 302 = the 91
  male names listed in `diff.individual_minus_cellspy302`.
- 302 − NemaNode = ∅.
- 302 − WormAtlas.tsv = {AVFL, AVFR, DB1, DB3}.
- 302 − `cell_lineage.txt` = {AVFL, AVFR, DB1, DB3, PHBR}.
- `IndividualNeurons.csv` − WormAtlas.tsv = {AVFL, AVFR, CP0, DB1, DB3,
  MCML, MCMR, PHDL, PHDR, PVS, PVU}.
- `IndividualNeurons.csv` − `cell_lineage.txt` = {AVFL, AVFR, CP0, DB1, DB3,
  PHBR, PHDL, PHDR, PVS, PVU}.
- WormBase male column − `IndividualNeurons.csv` = {HOsh, HOso, PChL, PChR}.
- `IndividualNeurons.csv` − 302 − WormBase male column = 31 names: CA1–9,
  CEMDL/DR/VL/VR, CP0–3, CP9, MCML/R, PHDL/R, PVS, PVU, PVV, SPCL/R, SPDL/R,
  SPVL/R.

### Lineage disagreements among the 302 (comparison only; nothing rewritten)

Lineages were compared with the first space read as ".".

| Name | `IndividualNeurons.csv` | `neurons.csv` | WormBase.csv | WormAtlas.tsv | `cell_lineage.txt` |
|---|---|---|---|---|---|
| AVFL | `P1.aaaa/ W.aaa` | `W.aaa` | `P1.aaaa` | (`AVFL/R` ×2) | (`AVFL/R` ×2) |
| AVFR | `P1.aaaa/ W.aaa` | `P1.aaaa` | `W.aaa` | (`AVFL/R` ×2) | (`AVFL/R` ×2) |
| PVR | `C aappa` | `C.aappv` | `C.aappa` | `C.aappv` | `C aappv` |
| RIPR | `AB arappaaaa` | `AB.prappaaaa` | `AB.prappaaaa` (synonym `ABarappaaaa`) | `AB.prappaaaa` | `AB arappaaaa` |

All other names agree across every pair of files that contains them.

## Record counts

Counts are produced by `python -m src.acquire --counts canonical_neurons`.

The paper-reported numbers come from the WebSearch tool's excerpts of blocked
pages, retrieved on 2026-10-12:

- **White 1986 abstract.** A search for "total complement of 302 neurons"
  "essentially invariant structure" returned excerpts of the White et al.
  1986 abstract, with result URLs including
  https://pubmed.ncbi.nlm.nih.gov/22462104 and
  https://historyofinformation.com/detail.php?id=2761 (the journal page is
  https://royalsocietypublishing.org/doi/10.1098/rstb.1986.0056):
  - *"The hermaphrodite nervous system has a total complement of 302 neurons, which are arranged in an essentially invariant structure."*
  - *"Neurons with similar morphologies and connectivities have been grouped together into classes; there are 118 such classes."*
- **Cook et al. 2020** (J Comp Neurol 528:2767–2784; PMC7601127,
  https://pmc.ncbi.nlm.nih.gov/articles/PMC7601127), on the pharynx:
  *"composed of 20 neurons that fall into 14 anatomically distinct types"*.

| Quantity | Definition | Count in acquired file | Paper reports | Where the paper reports it | Match |
|---|---|---|---|---|---|
| Hermaphrodite neurons | `Cells.py` `PREFERRED_HERM_NEURON_NAMES` length (distinct) | 302 (302) | 302 | White 1986 abstract (excerpt above) | YES |
| Hermaphrodite neurons | WormBase.csv rows marked 1 in "Neurons (no male-specific cells)" (distinct) | 302 (302) | 302 | White 1986 abstract | YES |
| Hermaphrodite neurons | `neurons.csv` rows (distinct) | 302 (302) | 302 | White 1986 abstract | YES |
| Hermaphrodite neurons, as stated in the file | WormBase.csv totals row for that column, vs rows marked 1 | stated 302; rows marked 302 | 302 | the file itself; White 1986 abstract | YES |
| Hermaphrodite neurons | `IndividualNeurons.csv` distinct names | 393 (397 rows) | 302 | White 1986 abstract | NOT COMPARABLE: the table also lists male-specific neurons. It contains all 302 exactly (302 − file = ∅), and the 91 extra names are male |
| Hermaphrodite neurons | `neuron_ids.txt` ids | 300 | 302 | White 1986 abstract | NOT COMPARABLE: this is the atlas package's id list, not a census. It omits CANL/CANR and writes AWC as AWCON/AWCOFF; otherwise it equals the 302 |
| Hermaphrodite neurons | NemaNode table / WormAtlas cell lists | 447 / 685 / 696 distinct names (all cell types) | 302 | White 1986 abstract | NOT COMPARABLE: no usable neuron flag (NemaNode's `typ` codes are undocumented; the cell lists have none). All 302 occur in NemaNode; 4 resp. 5 are spelled differently in the cell lists |
| Neuron classes | distinct NemaNode `classes` values over the 302 `Cells.py` names (exact lookup) | 118 | 118 | White 1986 abstract | YES for the count. NemaNode's class assignment was not checked member by member against White's class table (unreachable) |
| Neuron classes | any other candidate | not derivable without a naming rule | 118 | White 1986 abstract | NOT COMPARABLE: no class field; deriving one is a Phase 2 decision |
| Pharyngeal neurons | `Cells.py` PHARYNGEAL_INTERNEURONS + _MOTORNEURONS + _POLYMODAL_NEURONS; presence in each candidate | 20; all 20 present in every candidate | 20 | Cook et al. 2020 (excerpt above) | YES |
| Pharyngeal neuron classes | distinct NemaNode `classes` over those 20 names | 14 | 14 ("types") | Cook et al. 2020 | YES |

Not compared:

- Male neuron numbers. These are outside this project's head-connectome
  scope, and no paper figure was verified.
- The WormBase.csv totals 959 and 1136, which no paper excerpt was found
  for: UNVERIFIED.

## Discrepancies, flags and open questions

Flags (facts, no decision taken):

1. **Three 302-name lists are identical, but they are not independent of
   WormAtlas or of each other.**
   - `Cells.py` is curated from Cook et al. 2019.
   - The WormBase.csv column and `neurons.csv` are OpenWorm compilations.
   - All three are contained in the WormAtlas neuron-names copy, whose other
     91 names it describes as male neurons. All use AWCL/AWCR, CANL/CANR and
     unpadded VNC numbers.
   - No acquired file is a byte-level copy of a WormAtlas page that a
     primary check could confirm today.
2. **The WormAtlas complete cell list does not name AVFL, AVFR, DB1 or DB3
   individually.**
   - It writes `AVFL/R` twice (lineages P1.aaaa and W.aaa), `DB1/3` and
     `DB3/1`.
   - OpenWorm's two files assign AVFL/AVFR to these lineages in **opposite**
     ways: WormBase.csv has AVFL = P1.aaaa, while `neurons.csv` has AVFL =
     W.aaa.
   - The WormAtlas neuron-names copy gives both lineages to both.
   - This matters only if Phase 2 uses lineage.
3. **Wheel `cell_lineage.txt` defects:**
   - it writes `PHRB` instead of PHBR (WormBase.csv lists `PHRB` as a
     synonym of PHBR);
   - it duplicates the ADFL row;
   - it has trailing-space names `hyp7 ` / `mu_bod `;
   - the authors' reader drops every name containing "/" and keeps the
     header line as a cell.
4. **Lineage strings disagree for RIPR** (ABprappaaaa vs ABarappaaaa) **and
   PVR** (C.aappa vs C.aappv) between copies, and WormBase.csv's own RIPR
   synonym contradicts its lineage column. This is not a naming issue, but
   it shows the copies come from different WormAtlas revisions.
5. **`neuron_ids.txt` has no CANL/CANR and no AWCL/AWCR.** Randi's atlas
   therefore cannot be keyed to the 302 without an AWC decision (F7) and a
   decision on CAN. (CAN is also absent from the toolbox's
   `CElegansNeuronTables.xls` connectome, together with VC6; see not
   acquired.)
6. **`all_cell_info.csv` has 243 rows with 6 fields under a 5-field
   header** (toolbox generator defect). Parse by position with care, or
   don't use it; it is derived anyway.
7. **WormBase.csv's male-neuron column** (68 rows, 64 distinct) includes
   `HOsh`, `HOso`, `PChL`, `PChR`, which are not in the WormAtlas
   neuron-names copy. It omits 31 male names that the neuron-names copy has.
   Only relevant if male cells enter scope.
8. **The 118-class match rests on NemaNode's `classes` field.** Groupings
   such as `VBn` (VB1–VB11 as one class) and `DBn` are NemaNode's. Randi's
   own `approximate_ids` keeps VB1, VA1 and VA11 separate when merging
   numbered neurons, which is a different grouping. Which grouping defines
   "class" is a Phase 2 decision.
9. **wormatlas.org is blocked.** Every WormAtlas-derived file here is
   SECONDARY and its fidelity to the live pages is unverified.

**Not acquired** (and why):

- **Toolbox `cect/data/CElegansNeuronTables.xls`** (blob `ba565ffa…`; the
  same blob is in `openworm/c302` at `c302/` and `c302/data/`, and in
  `openworm/CElegansNeuroML`).
  - It is a legacy OpenWorm connectome workbook (sheets Connectome,
    NeuronsToMuscle, Sensory), not a neuron list.
  - The toolbox reader says "legacy dataset (based on White_whole) … Only
    included here for reference! Do not use!".
  - Its Connectome sheet names 299 distinct cells: the 302 minus CANL, CANR
    and VC6 (scratch inspection of the pinned blob).
  - Already discussed in `white1986.md`.
- **`Modified celegans db dump.csv`.** It is a per-neuron
  neurotransmitter/neuropeptide/receptor/innexin/type annotation table, not
  a name list. Three copies exist:
  - toolbox and owmeta `945f717` are byte-identical (blob `1f118a94…`);
  - the OpenWormData `69ecfd5` copy (blob `97ea0db9…`) differs only in
    replacing the evidence label "Altun et al., 2009" with "Altun2009" on
    652 lines and adding a final CRLF.
  - It belongs to a transmitter-identity source if wanted.
- **Wheel `anatlas_neuron_positions.txt`.**
  - It holds 3-D positions, not a name list, and no code in the wheel reads
    it.
  - Its header line names 303 tokens / 302 distinct (PVCL twice, the first
    as `#PVCL`), exactly the `Cells.py` 302 including CANL/CANR and
    AWCL/AWCR.
  - This is corroborating only. It can be added if the owner wants it.
- **Wheel `aconnectome_ids_ganglia.json`.** Already acquired by `randi2023`.
- **OpenWormData `69ecfd5` copies of the three (O) files.** They are the
  same git blobs as the acquired ones.
- **owmeta `tests/neurons.csv`.** A 1,452-byte test fixture.
- **`ShroffLab/celegans-cell-types`** (GitHub). An embryonic
  lineage-to-name mapping parsed from AceTree; its README does not cite
  WormAtlas. Not a WormAtlas copy.
- **`obophenotype/c-elegans-gross-anatomy-ontology`** (WBbt, GitHub).
  WormBase's anatomy ontology, an independent naming authority with explicit
  cell and class terms, but not a copy of WormAtlas. Not acquired pending an
  owner decision (see Q4).
- **`openworm/c302`, `openworm/CElegansNeuroML`.** No WormAtlas neuron-list
  table found in their trees: only connectome workbooks and NeuroML cell
  files.
- **The primaries** (wormatlas.org `NeuronNames.htm`, `celllist.htm`;
  nemanode.org; the OpenWorm Google Sheet). Hosts blocked or untested.

Owner questions:

- **Q1.** Which candidate is the Phase 2 source of truth for names?
  - the 302-name set shared by `Cells.py` / WormBase.csv / `neurons.csv`;
  - the WormAtlas neuron-names copy `IndividualNeurons.csv` (same 302 plus
    91 male names);
  - or wait for the primary WormAtlas page (allowlist wormatlas.org)?
- **Q2.** How should "class" be defined? Options: NemaNode's `classes` field
  (gives 118 over the 302, and 14 over the pharynx), White 1986's class
  table (not reachable), or a rule. Note that Randi's merging rule differs
  (VB1/VA1/VA11 kept apart).
- **Q3.** Should CANL/CANR stay in the namespace even though the Randi
  atlas has no CAN? And how should the cell-list spellings `AVFL/R`,
  `DB1/3`, `DB3/1` and `PHRB` be mapped, if the cell lists are used at all?
- **Q4.** Should the WBbt ontology be acquired as an independent check on
  names and classes?
- **Q5.** Male-specific neurons are present in `IndividualNeurons.csv` and
  WormBase.csv. Are they out of scope for the namespace?
