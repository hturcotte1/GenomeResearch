# fenyves2020: Predicted synaptic polarity (NT+R) of the chemical connectome

- Paper: Fenyves BG, Szilágyi GS, Vassy Z, Sőti C, Csermely P. *Synaptic
  polarity and sign-balance prediction using gene expression data in the
  Caenorhabditis elegans chemical synapse neuronal connectome network.* PLoS
  Comput Biol 16(12): e1007974 (2020). doi:10.1371/journal.pcbi.1007974.
  Preprint: bioRxiv 10.1101/2020.05.22.110312 (at least versions v1 and v2
  exist; search results link `…110312v2` and a v1 PDF on linkgroup.hu). Also
  on arXiv as 2101.05177.
- Module: `src/acquire/fenyves2020.py`
- Status: **SECONDARY — primary comparison PENDING (blocks Phase 4 freeze)**
- Retrieval date (UTC), from `data/raw/fenyves2020/MANIFEST.json`:
  2026-10-11 for the seven files acquired first; 2026-10-13 for
  `herm_full_edgelist_CElegansNeuroML-3808b6b.csv` and
  `herm_full_edgelist_MODIFIED.csv`.

## Primary location (not reachable from this environment)

- Journal supporting information: https://doi.org/10.1371/journal.pcbi.1007974.s003,
  on the article page
  https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1007974.
  `journal.pcbi.1007974.s003.xlsx` corresponds to this item.
  - **Its caption is UNVERIFIED.** The best inference is that s003 is "S1
    Data", the NT+R prediction workbook. The evidence, none of it verbatim
    from the journal page:
    - The workbook's USER GUIDE says "Method of prediction: NT+R".
    - The paper calls its NT+R database "S1 Data". WebSearch excerpt: "a
      simple, yet powerful algorithmic database (S1 Data) that takes as input
      connectome and gene expression data to predict synaptic polarity of
      ionotropic glutamatergic, cholinergic and GABA-ergic connections".
    - A WebSearch summary of the PLOS page
      (`journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1007974&rev=1`)
      lists s002 as a TIF, s004 as "S2 Data" (NT-only prediction) and s005 as
      "S3 Data" (receptor-only prediction). That would leave s003 between them.
    - The independent verification pass reported a WebSearch summary of PMC
      listing s003 as "S1 Data … prediction of synaptic signs based on
      neurotransmitter and receptor expression data" at about 960 KB
      (983,199 B = 960.2 KiB). Later searches (2026-10-13) did not re-find it, and its
      wording is also the USER GUIDE's first line, so the summary may echo
      the file rather than the caption.
    - The journal Results sentence giving 9,070 / 2,580 / 3,413 is reported
      (WebSearch summaries only) to end "(Fig 3A and S1 Data)", and the
      workbook's Summary sheet reproduces those three numbers.
  - **"s003" is not "S3 Data", and it is not "S3 Table"** (see flag FEN-1).
  - On the consumer side, both of Randi et al.'s codebases name this DOI for
    this workbook:
    - wormneuroatlas `SynapseSign.version` is
      `"https://doi.org/10.1371/journal.pcbi.1007974.s003|"`. The same string
      is also `CellLineage.version`, whose file is `cell_lineage.txt` and
      whose description ("Container for predictions of synapse sign") is
      copied too, so the version string is weak evidence;
    - pumpprobe `Funatlas._get_aconn_sign_genetic_prediction` downloads that
      DOI and reads sheet `5. Sign prediction`.
- Other supporting-information items (NT-only, R-only, S1 Supporting
  Information with alternative-reconstruction tables, S1 Fig, S3/S4 Tables)
  are only on the journal page. None was found in any reachable distribution;
  see "Not acquired".
- Authors' web tool: EleganSign, http://elegansign.linkgroup.hu. Supplementary
  page: https://linkgroup.hu/elegansdata.php (S1–S5 per a WebSearch summary).
  Both are blocked.
- Input connectome: the hermaphrodite edge list.
  - Earliest copy found: `openworm/CElegansNeuroML` commit `3808b6b`
    (2016-12-06, lungd, "Add herm_full_edgelist.csv", blob `a1313b0e`),
    acquired here. The commit names no source.
  - Presumed origin: WormWiring (Emmons lab), https://wormwiring.org/series/
    ("Edge list (.csv)" for the adult hermaphrodite), because the USER GUIDE
    says "Source data: Wormwiring connectome reconstruction". No
    WormWiring-hosted copy was compared. The WormWiring origin, file URL and
    release date are UNVERIFIED.

Primary checks to perform once reachable:

1. Download doi .s003 and compare its SHA-256 with the pin below. If it
   differs, compare sheet 5 and Summary cell by cell.
2. Read the SI captions and confirm which label s003 carries.
3. Download WormWiring's hermaphrodite edge list and compare it with
   `herm_full_edgelist_CElegansNeuroML-3808b6b.csv` (the pre-edit copy).
4. Read the bioRxiv v1 and v2 texts and supplements: which version reports
   9,034 / 3,431, and whether its S1 Data equals `data.csv`.
5. Read Fig 3A and its caption: whether it prints an exact E:I value.

## Files acquired

| File | Size (bytes) | SHA-256 | Distributor / URL | Integrity checks passed |
|---|---|---|---|---|
| `journal.pcbi.1007974.s003.xlsx` | 983,199 | `85959066fd7cbdbc2024d0ebb323b71c4365f4083bc85e555ee973f470697c47` | PyPI wheel `wormneuroatlas-0.0.7.3-py3-none-any.whl` (sha256 `166289031784c9565f6b9205e30dc718bafbc092db3b46f1aef73d93dc4d1325`), member `wormneuroatlas/data/journal.pcbi.1007974.s003.xlsx` | wheel SHA-256 equals PyPI's published digest (live); member matches pin; member matches wheel `RECORD` |
| `Data (rev 12-09-2020).csv` | 321,820 | `8748f968d759157e9e955b325d59314cc0ad8f4bf4501521f380a73a674c66ff` | GitHub `bank-fenyves/CeConn-SignPrediction` @ `e657d5f3c3986e99ccd39601b245b9b32c22d949`, raw URL in MANIFEST | size + SHA-256 match pin; git blob `660e2100158cc40bf37262075dba59c82ed4d1e1` matches the commit |
| `data.csv` | 531,133 | `0d45dcf0970b94a90f23eef51695f9a47a69bbef9615920915c824877959c9f7` | same repository and commit | same; blob `2442ce8f225cdc82c8d8f3363f38f83ea9c2f1fb` |
| `SignPred Calc` | 2,509 | `0966414de2c990ecd70747127797d00e7f54e8eff808ad345a6a4edb895adb8b` | same | same; blob `98f566a3632b81f82484cb945eec1bc57462c99a` |
| `Search Tool` | 465 | `94641ae0887ea955477ae348f40ccf3e0fa759532d3e66aba4c8db6449b49d15` | same | same; blob `ebd78dfe12369207cabbad276b09720a39ad3595` |
| `README.md` | 968 | `beff99dfcb1b79f34b56b11c6e83c19291ccff20a61c30be3ebab693c52c0142` | same | same; blob `ce6c7c596f601f2bdb937dd746b3bc0bf479d849` |
| `herm_full_edgelist.csv` | 245,463 | `142693f17556148d7f962835b18ac6dd5af18b7467eef61815ebc1dd5474c0ca` | GitHub `openworm/ConnectomeToolbox` @ `ffe570268b7cffb9329cd009a1bb37d60db2d465`, `cect/data/herm_full_edgelist.csv` | size + SHA-256 match pin; git blob `89ffc2a2d9e1934ddc462d51032acead5e4cfc91` matches the commit |
| `herm_full_edgelist_CElegansNeuroML-3808b6b.csv` | 245,430 | `7dfc27e4fa04844cd8b38554da5f4765c4a90ddce313d0f2612ee03e526829a6` | GitHub `openworm/CElegansNeuroML` @ `3808b6b235aa39ffac48bee319b06598bd23ff4d`, path `herm_full_edgelist.csv` (stored under a distinct local name) | size + SHA-256 match pin; git blob `a1313b0e53d258c361032d08657ce97566066ced` matches the commit |
| `herm_full_edgelist_MODIFIED.csv` | 245,926 | `8ba817eaed196e4aff3c6646af3d9493f5929ca6cea134439ee1e181087ac205` | GitHub `openworm/ConnectomeToolbox` @ `ffe570268b7cffb9329cd009a1bb37d60db2d465`, `cect/data/herm_full_edgelist_MODIFIED.csv` | size + SHA-256 match pin; git blob `5065baf77a58e990a28f460a1e4c1d6c5d2eecaf` matches the commit |

All nine are `secondary`. `herm_full_edgelist_MODIFIED.csv` is acquired only
as evidence that it is not the Fenyves input (its MANIFEST note says so).

About the authors' repository, `bank-fenyves/CeConn-SignPrediction`:

- It belongs to the first author. Its README names the paper.
- It is declared SECONDARY because this project's rules treat every GitHub
  repository that way.
- File history in that repository:
  - `data.csv`: added 2020-01-23 (commit `623f4fb`), never changed.
  - `Data (rev 12-09-2020).csv`: added 2020-09-14 (commit `b2ae4a9`).
  - The R scripts: January 2020.
  - Pinned HEAD `e657d5f` (2021-01-07) only edits the README.

About the edge lists' history (blobless clones of `openworm/CElegansNeuroML`
and `openworm/c302`, read 2026-10-13; author dates):

| Blob | First commit with that blob at `herm_full_edgelist.csv` | Relation |
|---|---|---|
| `a1313b0e` | CElegansNeuroML `3808b6b235aa39ffac48bee319b06598bd23ff4d`, 2016-12-06 10:51 UTC, "Add herm_full_edgelist.csv" | first version; acquired as `herm_full_edgelist_CElegansNeuroML-3808b6b.csv` |
| `89ffc2a2` | CElegansNeuroML `1ca08b14f4e795a973ce447565e0c97b897ee4dc`, 2016-12-06 10:53 UTC, "Add missing GJ PVCR-PVDR to herm_full_edgelist.csv" | `a1313b0e` plus one line, `PVCR , PVDR        ,2,electrical`; still the master version; copied to c302 in `49acae1` (2018-07-06, "Added herm_full_edgelist.csv & fixed UpdatedSpreadsheetDataReader.py") and present in ConnectomeToolbox; acquired as `herm_full_edgelist.csv` |
| `5065baf7` | CElegansNeuroML `1c24a6ce1cc27051f6e9765e1aff837a540ae260`, 2017-10-12, "intermediate commit" (branches `test_lungd`, `fw_update`, `ow-0.8_py3`); also `a40fccb764975bfc9dd13c19ea7e0dd190cc5186`, 2018-01-26, "DO NOT MERGE!! Manual changes to connectome!" (branches `ow-0.8`, `ow-0.8_py3`, `fw_update`) | an edit of `89ffc2a2` (the parent of both commits holds `89ffc2a2`); not on master; copied to c302 as `c302/data/herm_full_edgelist_MODIFIED.csv` in `3e723fb840f220268e7b5e3181a6ba5f945b5b93` (2018-07-10); equals ConnectomeToolbox `herm_full_edgelist_MODIFIED.csv`; acquired |

### Byte-level relationships between copies

- **xlsx.** The wheel member is byte-identical to
  `francescorandi/wormneuroatlas@b2e13d88:wormneuroatlas/data/journal.pcbi.1007974.s003.xlsx`
  (blob `0457b2faf3d051c1826b9865421c258f2dc37509`, same SHA-256). That copy
  is not acquired separately.
- **xlsx sheet 5 vs `Data (rev 12-09-2020).csv`.** Different formats, same
  content. Columns A..Q of sheet 5 equal the CSV's 17 columns cell for cell
  and in the same row order (3,638 rows). Booleans are spelled TRUE/FALSE in
  the CSV and are boolean cells in the xlsx. The CSV:
  - lacks columns R..U (R is empty; S/T/U are derived signed-synapse columns);
  - is `;`-separated UTF-8 with BOM, CRLF line ends and no final newline.
- **xlsx sheet 5 vs `data.csv` (January 2020).** The content differs. Same
  3,638 chemical (source, target, weight) rows in the same order, but:
  - 2,167 electrical rows are interleaved;
  - one legend row comes last:
    `;;;;;;+;-;+;-;+;-;;TRUE if there is a Complex;TRUE if double signaling;;`;
  - booleans are written in Hungarian, `IGAZ`/`HAMIS`;
  - `NT_complex` is spelled `complex` where the xlsx has TRUE (130 rows);
  - **13 rows have a different prediction**, all excitatory in the xlsx (list
    in Record counts). Format: no BOM, CRLF, no final newline.
- **Edge lists.** All three are comma-separated, LF line ends, no final
  newline, every name space-padded.
  - `herm_full_edgelist_CElegansNeuroML-3808b6b.csv` → `herm_full_edgelist.csv`:
    the second has exactly one extra row, PVCR→PVDR (2, electrical), and no
    other difference (`git diff` of the two blobs shows that single inserted
    line; `record_counts` confirms it on the parsed rows).
  - **The pre-edit copy equals `data.csv` on both layers.** Its rows whose
    two names are both in the xlsx's sheet-1 list are 3,638 chemical rows
    (weight 20,589) and 2,167 electrical rows (weight 8,640). As multisets
    of (source, target, weight), they equal `data.csv`'s chemical rows and
    its electrical rows respectively. The row order differs.
  - `herm_full_edgelist.csv` → `herm_full_edgelist_MODIFIED.csv`: the chemical
    row VB04→VB05 (1) is removed and 16 chemical rows of weight 5 are
    appended (DB01→DB02 … DB06→DB07, VB01→VB02 … VB10→VB11, including
    VB04→VB05). Electrical rows are unchanged.

## What each file contains

**`journal.pcbi.1007974.s003.xlsx`**

- Document properties: created 2019-07-01T09:46:44Z, modified
  2020-09-10T23:15:24Z, lastModifiedBy "Fenyves Bánk", Microsoft Macintosh
  Excel.
- All values used here are Excel's **cached** formula results. For all 3,638
  rows, B:C, G:L and Q are consistent with the workbook's own formulas
  re-evaluated against sheets 1 and 4. Sheet 4's B..G are consistent with
  their formulas re-evaluated against sheets 2 and 3.

Sheets:

- `USER GUIDE`:
  - "This file predicts synaptic signs based on neurotransmitter and receptor
    expression data";
  - "Source data: Wormwiring connectome reconstruction";
  - "Method of prediction: NT+R".
- `1. NT expr`: rows 2–303, 302 neurons. Columns: `Class member`,
  `Dominant NT`, `Alternative NT`, `Neurotransmitters` (=B&C).
  - Dominant NT: ACh 157, Glu 78, GABA 33, blank 34.
  - Alternative NT: GABA 8, ACh 4, blank 290.
  - 64 names carry a zero-padded single-digit index (e.g. VA01, AS01). The 11
    two-digit indices are not padded: AS10, AS11, VA10–VA12, VB10, VB11,
    VD10–VD13. AWC appears as AWCL/AWCR.
  - CANL/CANR are present.
- `2. Receptor gene table`: 62 ionotropic receptor genes in six classes,
  columns A..F. Glu Pos 10, Glu Neg 6, ACh Pos 30, ACh Neg 6, GABA Pos 2,
  GABA Neg 8. Columns J:K give the number of neurons expressing each gene.
- `3. Receptor Gene expression`: no header row (row 1 is empty). One row per
  neuron (302, rows 2–303), with a ragged list of expressed receptor gene
  names. One token, `gar-2` (metabotropic), belongs to no sheet-2 class.
- `4. Receptor type expression ` (the trailing space is in the sheet name):
  rows 3–304, same neuron order as sheet 1.
  - Columns B..G are counts of expressed genes per class, and **all 302 × 6
    cells are formulas**, `=SUMPRODUCT(COUNTIF(<class>,'3. Receptor Gene expression'!$B<k>:$EL<k>))`
    with `<class>` the defined names `glupos`, `gluneg`, `achpos`, `achneg`,
    `gabapos`, `gabaneg` and k the row above. D and E (ACh Pos/Neg) are
    array (CSE) formulas; B, C, F and G are ordinary formulas. All 302 × 6
    cached values equal the formulas re-evaluated on sheets 2 and 3, and each
    row's sheet-3 row names the same neuron.
  - Column I is "multi-receptor complexity" (TRUE for 85 neurons). Row 3
    holds `=IF(OR(AND(B3>0,C3>0),AND(D3>0,E3>0),AND(F3>0,G3>0)),TRUE,FALSE)`
    (`sheet4_colI_first_row_formula`), and every one of the 302 rows holds
    the same formula on its own row
    (`sheet4_colI_rows_not_matching_first_row_formula_pattern` = 0). In the
    file it is one shared formula with range I3:I304 (read from the raw
    `xl/worksheets` XML, not `--counts`).
  - A results block in U4:V20.
- `5. Sign prediction`: rows 1–2 are a two-line header; data in rows
  3–3640.
  - **One row = one directed chemical connection, Source (A) → Target (D),
    weight E = synapse count, Edge type F (always "chemical").**
  - B/C: presynaptic NTs (VLOOKUP into sheet 1; 0 = none).
  - G..L: TRUE if the source releases that NT and the target expresses that
    receptor class (Glu+, Glu−, ACh+, ACh−, GABA+, GABA−).
  - M: number of matches.
  - N: double NT signalling.
  - O: "+ & − for two NT?".
  - P: "Both + and − for one NT?".
  - **Q: "Predicted polarity" ∈ {`+`, `-`, `complex`, `no pred`}**:
    `complex` if O or P; else `+` if any of G/I/K; else `-` if any of H/J/L;
    else `no pred`.
  - S: +E / −E / 0 / "complex". T: −E for complex. U: E for no pred.
  - Rows are sorted by (source, target). There are 34 self-pairs.
  - The stored used range is A1:U5808, although the last non-empty row is
    3640. 5,808 − 2 header rows = 5,806, which is the number of data rows of
    `data.csv` (3,638 chemical + 2,167 electrical + 1 legend). The S and T
    formulas also keep an "electrical" branch
    (`=IF(Q3="no pred",0,IF(Q3="complex","complex",IF(Q3="electrical","electrical",IF(Q3="+",E3,-E3))))`
    and `=IF(S3="electrical",E3,IF(S3="complex",-E3,"FALSE"))`), although no
    row of the sheet is electrical. Both suggest, but do not prove, that the
    sheet once held `data.csv`'s rows.
- `Summary`: formulas over whole columns of sheet 5 (cells quoted below).

Excel's defined names `herm_full_edgelist` (A2:F3477), `pred_polarity`,
`synapses`, `unconv` and `nopredsyn` (rows 4–3477) are **stale**:

- they stop 163 data rows short;
- several workbook-level duplicates are `#REF!`;
- the Summary does not use them;
- the autofilter range A2:Q3640 covers all data.

**`Data (rev 12-09-2020).csv`**: sheet 5 A..Q as text (see above).

**`data.csv`**: the January 2020 version.

- 3,638 chemical rows plus 2,167 electrical rows (`Pred_pol` = "electrical")
  plus the legend row.
- The receptor-match columns are filled on electrical rows too: 1,227 of the
  2,167 electrical rows have at least one `IGAZ` in G:L (1,692 `IGAZ`
  tokens). `rec_complex` is `IGAZ` in 329 electrical rows and `double_NT` in
  136.
- Electrical rows (no duplicated source→target row):
  - 13 are self-rows;
  - 2,148 directed rows have their reverse listed. 24 of those rows
    (12 unordered pairs) have a reverse of a different weight (e.g.
    AVAL→VA05 4, VA05→AVAL 5);
  - 6 rows are listed in one direction only: AVKL→PDER (1), PDEL→VD06 (2),
    PVDR→PVCR (2), PVM→DB03 (2), PVM→VD09 (1), VB04→DVA (1);
  - 1,093 unordered pairs;
  - weight sum 8,640.
- Names: 297 in the chemical layer, 296 in the electrical layer, 300 in the
  union (sheet 1 minus CANL/CANR). M5, PLML and PLMR occur only in electrical
  rows.

**`SignPred Calc`** (R, never executed here):

- reads `data.csv` with `;`;
- sums `Synapses` by `Pred_pol` over `Type == "chemical"`;
- also computes an NT-only ("old") prediction.

It documents that the authors' totals are synapse-weighted sums over chemical
rows.

**`Search Tool`** (R): interactive single-pair lookup.

**`README.md`**: links the repository to the paper. It describes `data.csv`
(not the September revision).

**`herm_full_edgelist.csv`** (toolbox, blob `89ffc2a2`): header
`Source,Target,Weight,Type`, 7,379 rows.

- **Every row has space-padded names** (e.g. `I1L , I2L           ,10,chemical`).
- Rows: 4,681 chemical (weight 27,019) and 2,698 electrical (weight 12,683).
- 448 distinct names: neurons plus muscles and other cells (`dBWML1`,
  `pm1d`…, `mc*`, `um*`/`vm*`, `intestine`, `sph`, `hyp`, `anal`). 148 of
  them are not in the xlsx's sheet-1 list, and none of those 148 starts with
  an upper-case letter.
- Names are zero-padded like the xlsx.
- The ConnectomeToolbox reader (`cect/readers/UpdatedSpreadsheetDataReader.py`
  @ `ffe5702`) describes it as "legacy dataset (based on Cook et al. 2019)
  used in the past in OpenWorm. Only included here for reference! Do not
  use!".

**`herm_full_edgelist_CElegansNeuroML-3808b6b.csv`** (blob `a1313b0e`): the
same header, 7,378 rows: 4,681 chemical (weight 27,019) and 2,697 electrical
(weight 12,681).

**`herm_full_edgelist_MODIFIED.csv`** (blob `5065baf7`): the same header,
7,394 rows: 4,696 chemical (weight 27,098) and 2,698 electrical (weight
12,683). On the xlsx's 302 neurons: 3,653 chemical rows (weight 20,668), 15
pairs sheet 5 lacks, none missing, and VB04→VB05 = 5 where sheet 5 has 1.

## Record counts

Counts come from `python -m src.acquire --counts fenyves2020`, except the
Cook et al. 2019 SI 5 comparison, which comes from the committed script named
in that section.

- "Connections" = rows of sheet 5.
- "Synapses" = sum of column E.
- Categories are the file's own column Q values.
- Paper excerpts were read through WebSearch, which returns excerpts or
  model-written summaries of the blocked pages. The URL given is the page the
  excerpt was attributed to. "Summary" marks wording that may be paraphrase.

Summary sheet, quoted exactly (cell: label / cached value / formula):

| Cell | Label (col A) | Value | Formula |
|---|---|---|---|
| B2 | Chemical synapses | 20589 | `=SUM('5. Sign prediction'!E:E)` |
| B3 | Total predicted chemical synapses | 15063 | `=B2-B4` |
| B4 | Total unpredicted chemical synapses | 5526 | `=SUMIFS('5. Sign prediction'!E:E,'5. Sign prediction'!F:F,"chemical",'5. Sign prediction'!Q:Q,"no pred")` |
| B5 | Strength of prediction | 0.7316042546991112 | `=B3/B2` |
| B7 / C7 | Predicted excitatory synapses | 9070 / 0.6021376883754896 | `=SUMIF('5. Sign prediction'!Q:Q,"+",'5. Sign prediction'!E:E)` / `=B7/SUM(B7:B9)` |
| B8 / C8 | Predicted inhibitory synapses | 2580 / 0.17128062139016131 | `=SUMIF('5. Sign prediction'!Q:Q,"-",'5. Sign prediction'!E:E)` / `=B8/SUM(B7:B9)` |
| B9 / C9 | Predicted complex synapses | 3413 / 0.22658169023434907 | `=SUMIF('5. Sign prediction'!Q:Q,"complex",'5. Sign prediction'!E:E)` / `=B9/SUM(B7:B9)` |
| B10 | Predicted E:I ratio | 3.5155038759689923 | `=B7/B8` |

Sheet 5 by predicted polarity (column Q):

| Q | Connections | Synapses | of which self-pairs (conn / syn) |
|---|---|---|---|
| `+` | 1,327 | 9,070 | 9 / 20 |
| `-` | 425 | 2,580 | 3 / 8 |
| `complex` | 471 | 3,413 | 4 / 16 |
| `no pred` | 1,415 | 5,526 | 18 / 61 |
| total | 3,638 | 20,589 | 34 / 105 |

Further sheet-5 counts:

- Weights range 1–71.
- 292 distinct sources, 297 distinct targets, 297 names in all.
- Every name is in sheet 1. The sheet-1 names absent from sheet 5 are CANL,
  CANR, M5, PLML and PLMR.
- 465 rows have a source with no dominant NT.
- Column O TRUE in 130 rows; column P TRUE in 431 rows.

| Quantity | Definition | Count in acquired file | Paper reports | Where the paper reports it | Match |
|---|---|---|---|---|---|
| Connections | rows of sheet 5 (all Edge type "chemical"); directed rows, self-pairs included | **3,638** | 3,638 | Abstract, via WebSearch excerpts attributed to the PLOS article (DOAJ record doaj.org/article/cedb463cd6164f4799ae406864e589b3; PMC7785220) and to the bioRxiv preprint: "(3,638 connections and 20,589 synapses total)". Re-found on 2026-10-13. The PLOS Results wording was seen only as a summary ("weighted edge list representing 20,589 chemical synapses in 3,638 connections"). The abstract does not say whether connections are directed; sheet 5's 3,638 are directed rows | **YES** |
| Chemical synapses | sum of E = Summary!B2 | **20,589** | 20,589 | same excerpts | **YES** |
| Excitatory synapses | Q = `+`, sum E = Summary!B7 | **9,070** | 9,070 | WebSearch excerpt attributed to journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1007974 and arxiv.org/pdf/2101.05177: "We predicted that 9,070 of the synapses are excitatory and 2,580 are inhibitory, while 3,413 synapses have complex function (Fig 3A and S1 Data)". It was returned in the verification pass (and reported by the earlier fix pass); two repeat searches on 2026-10-13 did not return it. The trailing "(Fig 3A and S1 Data)" was seen only in WebSearch summaries | **YES** |
| Inhibitory synapses | Q = `-`, sum E = Summary!B8 | **2,580** | 2,580 | same sentence. 2,580 is also the preprint's number, so it does not tell the versions apart | **YES** |
| Complex synapses | Q = `complex`, sum E = Summary!B9 | **3,413** | 3,413 | same sentence | **YES** |
| Share predicted | Summary!B5 = (B2−B4)/B2, `complex` counted as predicted | **0.7316 (73.2%)**; `data.csv` gives (20,589 − 5,544)/20,589 = 0.7307, also 73% | 73%; "more than two-thirds" | Fig 2 legend (pmc.ncbi.nlm.nih.gov/articles/PMC7785220/figure/pcbi.1007974.g002), WebSearch excerpt read 2026-10-13: "We were able to predict polarity for 73% of chemical synapses (green). The polarities of the rest of synapses were unpredicted due to unknown neurotransmitter expression of the presynaptic neurons (dark grey) or non-matching receptor gene expression of the postsynaptic neurons (light grey)". The unpredicted part is therefore the file's `no pred` (no presynaptic NT, or no matching receptor class), and `complex` counts as predicted, as in B5. Abstract: "made predictions for more than two-thirds of these chemical synapses". The thesis wording quoted in an earlier draft ("We predicted polarities for 73% of all ionotropic chemical synapses") was not found by exact-phrase search and is not used. 73% does not tell the versions apart | **YES** |
| E:I ratio, abstract wording | Summary!B10 = B7/B8 (synapses) | **3.5155**; connection-count alternative 1,327/425 = **3.1224** | "close to 4:1" | Abstract (arXiv 2101.05177 / PLOS): "observed an excitatory-inhibitory (E:I) ratio close to 4:1". "Close to 4:1" is not a count; no "4:1" appears anywhere in the workbook (0 text cells). Whether the paper derives it from 3.5155 or from another figure is not established | **NOT COMPARABLE** |
| E:I ratio, as printed in Fig 3A | Summary!B10 | **3.5155** | not seen | Fig 3A. The verification pass reported a WebSearch summary saying Fig 3A edges are weighted by E:I ratios "(see numbers)"; not re-found by searches on 2026-10-13. The figure itself was not seen | **UNVERIFIED** |
| Neurons with multi-receptor complexity | sheet 4 V17 = `COUNTIF(I:I,TRUE)` | **85** | 85 | WebSearch excerpt attributed to journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1007974: "Surprisingly, 85 neurons expressed both excitatory and inhibitory receptor genes for the same neurotransmitter". It was returned in the verification pass (and reported by the earlier fix pass, which also saw it in a summary of the bioRxiv preprint); two repeat searches on 2026-10-13 did not return it. Same definition as column I (row 3: `=IF(OR(AND(B3>0,C3>0),AND(D3>0,E3>0),AND(F3>0,G3>0)),TRUE,FALSE)`, `sheet4_colI_first_row_formula`; shared over I3:I304, read from the raw XML, not `--counts`) | **YES** |
| Neurons in the chemical layer | distinct names in sheet 5 | **297** (absent: CANL, CANR, M5, PLML, PLMR) | not found in Fenyves 2020 | No Fenyves 2020 statement of 297 was found. The verification pass reported a WebSearch excerpt from a later paper by the same group, Szilágyi et al. (bioRxiv 10.1101/2025.01.09.632090; BMC Biol 2026, PMC13374236): "comprises 3638 chemical connections (20,589 synapses) among 297 neurons", and an earlier pass an excerpt of the same paper: "CANL, CANR, PLML, PLMR, and M5 neurons are not connected by chemical connections hence were excluded". Neither was returned by searches on 2026-10-13. That paper is not Fenyves 2020 | **UNVERIFIED** |
| Neurons in the reconstruction | names in chemical ∪ electrical rows of `data.csv` | **300** | 300 (WebSearch summary only) | Summaries of the PLOS Methods said "3,638 chemical connections and 2,167 gap junctions, connecting 300 neurons", with CANL/CANR omitted. An exact-phrase search did not find this sentence | **UNVERIFIED** |
| Gap junctions | electrical rows of `data.csv` (directed rows); equally, neuron-neuron electrical rows of the pre-edit edge list | **2,167** rows (1,093 unordered pairs; weight 8,640). The acquired toolbox edge list has 2,168, because OpenWorm added PVCR→PVDR | 2,167 (summary only) | as above. If the paper's 2,167 counts these rows, it counts directed rows, not unordered pairs | **UNVERIFIED** |
| Excitatory / inhibitory / complex synapses, preprint | Jan 2020 `data.csv`, chemical rows by `Pred_pol` | **9,034 / 2,580 / 3,431** (no pred 5,544) | 9,034 / 2,580 / 3,431 | bioRxiv full text (biorxiv.org/content/10.1101/2020.05.22.110312.full.pdf, no version in the URL), via WebSearch: "We predicted that 9,034 of the synapses are excitatory and 2,580 are inhibitory, while 3,431 synapses have complex function". Compared with `data.csv`, not with the xlsx (which is the journal version). Which bioRxiv version (v1, v2) carries these numbers is UNVERIFIED | **YES** |

Version comparison, `data.csv` (Jan 2020) → xlsx (journal):

- The 13 changed predictions, listed as source→target (synapses): Jan → journal.
  - complex → `+`: ADFR→AIYR (2), AIYR→AIYL (7), AWBL→AIYL (1), AWBR→AIYR
    (1), RIH→AIYL (3), RIH→AIYR (4). In total 6 connections, 18 synapses.
  - no pred → `+`: ALNR→ADER (1), IL2L→ADEL (6), IL2R→ADER (5), RMDL→ADEL
    (1), RMDL→ADER (3), SIAVL→ADEL (1), URBR→ADER (1). In total 7
    connections, 18 synapses.
- All 13 are ACh inputs to ADEL/ADER/AIYL/AIYR. Their ACh-receptor flags
  changed:
  - AIY went from ACh+ and ACh− to ACh+ only;
  - ADE went from neither to ACh+.
- This accounts exactly for the journal−preprint difference: 9,034 + 36 =
  9,070; 3,431 − 18 = 3,413; 5,544 − 18 = 5,526.

Owner's Phase 3 reproduction targets:

- **"3,638 connections"**:
  - *Directly present.* It is the number of data rows in sheet 5 (rows
    3–3640), and also the number in `Data (rev 12-09-2020).csv`. No filter is
    needed on the xlsx.
  - *Derivable* from `herm_full_edgelist.csv` or its pre-edit copy (not from
    the MODIFIED file) with one filter: Type == "chemical" and both endpoints
    neurons.
  - Two endpoint rules both give exactly 3,638 rows / 20,589 synapses from
    `herm_full_edgelist.csv`, equal to sheet 5 pair-for-pair and
    weight-for-weight:
    - "both names in the xlsx sheet-1 list";
    - "both names start upper-case".
    The first rule gives the same on the pre-edit copy (the two copies differ
    only by an electrical row).
  - The filter is justified by the paper's own scope: the
    "chemical synapse neuronal connectome", and the USER GUIDE's "Table of
    interneuronal connections". It **includes 34 self-pairs (105 synapses)**.
    Excluding them would give 3,604 / 20,484, which is not the paper's number.
- **"20,589 ionotropic synapses"**:
  - *Directly present* as Summary!B2. The file labels it "Chemical synapses",
    not "ionotropic".
  - It is the total synapse count of all 3,638 neuron-to-neuron chemical
    connections, whatever their receptors. 5,526 of them (26.8%) received no
    prediction.
  - Calling all 20,589 "ionotropic" is the paper's framing of the network,
    not a per-synapse fact in the file.
- **"approximately 4:1 excitatory:inhibitory"**:
  - *Not present* as such. The file's E:I is Summary!B10 = 9,070/2,580 =
    **3.5155** (synapse-weighted). Counting connections instead gives
    1,327/425 = 3.1224.
  - The abstract's "close to 4:1" is not a number in the file. Whether it
    rounds 3.5155 or refers to another figure (Fig 3A, not seen) is not
    established. A test asserting 4.0 with a tight tolerance would fail on
    the file's numbers.

Other counts recorded:

- **Stale named ranges.** 163 sheet-5 data rows lie after the end (row 3477)
  of Excel's `herm_full_edgelist` named range.
- **Electrical layer of the acquired (OpenWorm-amended) edge list.** 2,168
  neuron-neuron rows (weight 8,642). `data.csv` has every one of them except
  PVCR→PVDR (weight 2), the row OpenWorm added in `1ca08b1`. The pre-edit
  copy has 2,167 rows (weight 8,640), equal to `data.csv`'s electrical rows.

### Comparison with Cook et al. 2019 SI 5

The files belong to `white1986`, so the comparison is a committed cross-source
script rather than part of `record_counts`:
`scripts/provenance_checks/fenyves2020_vs_cook2019_si5.py`. It reads only
`data/raw/fenyves2020/journal.pcbi.1007974.s003.xlsx` and the three SI 5
workbooks in `data/raw/white1986/` (`41586_2019_1352_MOESM9_ESM.xlsx`,
`SI 5 Connectome adjacency matrices.xlsx`, `SI 5 Connectome adjacency
matrices, corrected July 2020.xlsx`), and prints sorted JSON. Its output:

- The SI 5 legend says "rows give the pre-synaptic cell, columns give the
  post-synaptic cell", and that weights are "the total number of EM serial
  sections", not synapse counts.
- On the 302 sheet-1 names, the "hermaphrodite chemical" sheet has 3,709
  non-zero pairs, weight sum 20,965 (serial-section units). This is
  identical in all three SI 5 files.
- Against sheet 5 (3,638 pairs):
  - 122 pairs only in sheet 5;
  - 193 pairs only in SI 5;
  - 3,516 pairs in both, of which 21 have a different weight.
- Reading SI 5 transposed would share only 1,359 pairs with sheet 5.

So the "WormWiring connectome reconstruction" used by Fenyves is **not** the
Cook 2019 SI 5 hermaphrodite chemical matrix. In 3,495 of the 3,516 shared
pairs (3,516 − 21) the sheet-5 synapse count equals the SI 5 serial-section
weight. What unit the edge list's `Weight` is in is not stated in any acquired
file.

## How Randi et al.'s code consumed this file

- **wormneuroatlas 0.0.7.3, `SynapseSign.py`** reads **only sheets 1 and 2**.
  - It takes the NT per neuron and the six receptor-gene lists.
  - It rewrites names: `VA01`→`VA1`, `AWCL`→`AWCOFF`, `AWCR`→`AWCON`. The
    code comment says the AWC mapping "has no effect" because both are Glu.
  - `NeuroAtlas.get_chemical_synapse_sign` then **recomputes** signs. It uses
    CeNGEN expression (the package's own threshold) in place of Fenyves's
    sheet 3/4 expression. It uses dominant + alternative NTs and gives
    0 = conflicting.
  - `get_anatomical_connectome(signed=True)` sums the per-NT signs
    (`np.nansum`), sets pairs with both −1 and +1 to 0, and flips only
    entries equal to −1. A pair inhibitory through two NTs (sum −2) is
    therefore not flipped.
  - **Fenyves's own sheet-5 calls are therefore not what the package uses.**
- **leiferlab/pumpprobe @ 1dbc5e0a, `Funatlas._get_aconn_sign_genetic_prediction`**
  downloads doi .s003 and reads sheet 5. Emulated locally, it has two quirks:
  - `WS_np[2:3639]` skips the first data row (ADAL→ADAL, 6 synapses,
    `no pred`).
  - `.str.replace('0','')` deletes **every** zero, not only padding. AS10,
    VA10, VB10 and VD10 become AS1, VA1, VB1 and VD1, colliding with
    AS01/VA01/VB01/VD01.
  - No caller of `get_aconn_sign_genetic_prediction` exists in pumpprobe at
    that commit.

## Discrepancies, flags and open questions

- **FEN-1. "S3" naming.** The brief's "Fenyves S3" is the DOI suffix `.s003`.
  - Per the PLOS SI listing (WebSearch summary), "S3 Data" is a different
    item, s005, the receptor-only prediction.
  - "S3 Table" is reportedly the comparison with Rakowski & Karbowski 2017.
  - s003 is most likely "S1 Data" (NT+R), but this is UNVERIFIED.
  - Refer to this file by its DOI suffix, never as "S3".
- **FEN-2. At least two prediction versions exist** (owner question). They
  have identical connections and weights but 13 different calls (36
  synapses):
  - the journal version (xlsx = `Data (rev 12-09-2020).csv`): 9,070 /
    2,580 / 3,413 / 5,526;
  - the preprint version (`data.csv`, Jan 2020): 9,034 / 2,580 / 3,431 /
    5,544. Which bioRxiv version (v1, v2) reports these numbers, and whether
    any version's S1 Data equals `data.csv`, is UNVERIFIED.

  The authors' README still points to `data.csv`. The provisional choice is
  recorded in `docs/decisions.md` (Q-008: the journal version).
- **FEN-3. E:I target.** The file's E:I is 3.5155 (synapses) or 3.1224
  (connections), not 4. Phase 0 flag F6's "about 4:1" is the abstract's
  "close to 4:1"; whether that is a rounding of 3.5155 or a figure printed
  elsewhere (Fig 3A, not seen) is not established. The owner should decide
  what Phase 3 asserts. One option is the exact 9,070 / 2,580 (Summary
  B7/B8); another is a ratio with an explicit tolerance.
- **FEN-4. Whole-animal network, not head.** The 3,638 / 20,589 / E:I
  figures cover the whole hermaphrodite neuron set of the edge list: 297
  neurons, ventral cord included. Any head restriction changes all of them;
  the head set is a Phase 2 decision.
- **FEN-5. Self-pairs** (34 connections, 105 synapses, 9 of them `+` and 3
  `-`) are inside the 3,638. Should they stay in the edge table? (Cf. Randi
  F1.)
- **FEN-6. `complex` and `no pred`** cover 471 + 1,415 connections (3,413 +
  5,526 synapses). How should they be encoded in `predicted_sign`? Szilágyi
  et al. 2026 re-label "complex" synapses (Phase 0 F10); that is a different
  source.
- **FEN-7. Which "Fenyves sign" did Randi use?**
  - The package recomputes signs from CeNGEN and does not use sheet 5.
  - pumpprobe's sheet-5 reader has the two bugs above and no caller.
  - If the owner wants "Randi's predicted sign", it must be recomputed with
    the package's CeNGEN threshold. That is not the same as Fenyves's sheet 5.
- **FEN-8. Input connectome identity.** Sheet 5 equals the neuron-neuron
  chemical subset of the OpenWorm hermaphrodite edge list (blob `89ffc2a2`
  and its pre-edit version `a1313b0e`; not the MODIFIED blob `5065baf7`).
  - That list is not Cook 2019 SI 5.
  - The toolbox marks it "legacy … Do not use!".
  - It first appears in `openworm/CElegansNeuroML` `3808b6b` (2016-12-06,
    blob `a1313b0e`); blob `89ffc2a2` comes from `1ca08b1` the same day;
    c302 copied `89ffc2a2` in `49acae1` (2018-07-06). The workbook was
    created 2019-07-01.
  - Its WormWiring origin and release date are UNVERIFIED.
  - Whether to treat it as an anatomical-connectome candidate is the owner's
    call (cf. Q-007 / F9).
- **FEN-9. Name conventions.**
  - Single-digit indices are zero-padded (VA01, AS01; 64 names); the 11
    two-digit indices (AS10, AS11, VA10–VA12, VB10, VB11, VD10–VD13) are not.
  - AWCL/AWCR. Randi's package maps L→OFF and R→ON, and that mapping is a
    guess (F7).
  - The edge lists have space-padded names everywhere.
  - No normalisation is applied here.
- **FEN-10. Workbook hygiene.** None of these changes values today; they
  matter if anyone edits or re-evaluates the workbook.
  - Stale named ranges (row 3477) and `#REF!` names.
  - Summary!B4 filters `Edge type == "chemical"` but B7–B9 do not. This is
    harmless because every row is chemical.
  - `gar-2` (metabotropic) is in sheet 3 but in no receptor class.
- **FEN-11. Gap junctions are not predictions.** `data.csv` carries 2,167
  electrical rows. Most pairs are listed in both directions, 12 pairs with
  different weights per direction. They equal the pre-edit OpenWorm copy's
  neuron-neuron electrical rows exactly; the acquired toolbox copy adds
  PVCR→PVDR (2), an OpenWorm edit (CElegansNeuroML `1ca08b1`, 2016-12-06).
  They are acquired only as part of those files; they are not a gap junction
  source of record.
- **FEN-12. Primary identity unproven.** Matching headline numbers (9,070 /
  2,580 / 3,413 / 20,589 / 3,638) are strong evidence that this is the
  journal's s003 content, not proof. The byte-level comparison remains
  PENDING.

### Not acquired

- Journal copies of s001–s005 and any other SI items: journals.plos.org and
  doi.org are blocked, and no reachable redistribution was found.
  - This covers the NT-only (S2 Data, reportedly s004) and receptor-only
    (S3 Data, reportedly s005) predictions.
  - It also covers S1 Supporting Information, whose alternative-reconstruction
    tables reportedly give E:I 3.1–4.1 (unverified), and the S1 Fig TIF.
  - Searches covered GitHub, PyPI, the toolbox and the authors' repository.
- bioRxiv 10.1101/2020.05.22.110312 v1 and v2 supplementary files, if any:
  biorxiv.org is blocked, and the v1 PDF copy on linkgroup.hu is blocked too;
  no redistribution found. `data.csv`'s totals match the preprint text, but
  its identity with any preprint S1 Data is UNVERIFIED.
- EleganSign database and tool (elegansign.linkgroup.hu) and
  linkgroup.hu/elegansdata.php: blocked; no copy found. PyPI has no
  `elegansign` package (404).
- Other copies of acquired bytes:
  - `francescorandi/wormneuroatlas` GitHub copy of the xlsx (blob
    `0457b2fa`): byte-identical to the acquired copy; the only blob at that
    path in the repository's history (added 2023-01-26).
  - The other wormneuroatlas PyPI wheels. A scratch check on 2026-10-13
    (not part of `--counts`; it downloaded every wheel, confirmed each
    wheel's SHA-256 against PyPI's published digest, and hashed the member):
    - 0.0.2, 0.0.3, 0.0.4 and 0.0.5 do not contain the xlsx;
    - 0.0.6, 0.0.7.1 and 0.0.7.2 contain
      `wormneuroatlas/data/journal.pcbi.1007974.s003.xlsx`, byte-identical
      to the acquired member (983,199 bytes, SHA-256 `85959066…697c47`,
      matching their `RECORD`).
    - The sdists were not inspected.
  - `openworm/c302` master `c302/data/herm_full_edgelist.csv` and
    `openworm/CElegansNeuroML` master `herm_full_edgelist.csv`: blob
    `89ffc2a2`, byte-identical to the acquired `herm_full_edgelist.csv`.
  - `openworm/CElegansNeuroML` `1c24a6c` / `a40fccb` `herm_full_edgelist.csv`
    and `openworm/c302` master `c302/data/herm_full_edgelist_MODIFIED.csv`
    (added in `3e723fb`, 2018-07-10): blob `5065baf7`, byte-identical to the
    acquired `herm_full_edgelist_MODIFIED.csv`.
- Cook 2019 SI 5 files: already acquired by `white1986`, and not the Fenyves
  input.
