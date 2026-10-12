# fenyves2020: Predicted synaptic polarity (NT+R) of the chemical connectome

- Paper: Fenyves BG, Szilágyi GS, Vassy Z, Sőti C, Csermely P. *Synaptic
  polarity and sign-balance prediction using gene expression data in the
  Caenorhabditis elegans chemical synapse neuronal connectome network.* PLoS
  Comput Biol 16(12): e1007974 (2020). doi:10.1371/journal.pcbi.1007974.
  Preprint: bioRxiv 10.1101/2020.05.22.110312. Also on arXiv as 2101.05177.
- Module: `src/acquire/fenyves2020.py`
- Status: **SECONDARY — primary comparison PENDING (blocks Phase 4 freeze)**
- Retrieval date (UTC): 2026-10-11 for all seven files, from
  `data/raw/fenyves2020/MANIFEST.json`

## Primary location (not reachable from this environment)

- Journal supporting information: https://doi.org/10.1371/journal.pcbi.1007974.s003,
  on the article page
  https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1007974.
  `journal.pcbi.1007974.s003.xlsx` corresponds to this item.
  - **Its caption is UNVERIFIED.** The best inference is that s003 is "S1
    Data", the NT+R prediction workbook. The evidence:
    - The workbook's USER GUIDE says "Method of prediction: NT+R".
    - The paper calls its NT+R database "S1 Data". WebSearch excerpt: "a
      simple, yet powerful algorithmic database (S1 Data) that takes as input
      connectome and gene expression data to predict synaptic polarity of
      ionotropic glutamatergic, cholinergic and GABA-ergic connections".
    - A WebSearch summary of the PLOS page
      (`journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1007974&rev=1`)
      lists s002 as a TIF, s004 as "S2 Data" (NT-only prediction) and s005 as
      "S3 Data" (receptor-only prediction). That would leave s003 between them.
      This was a summary, not verbatim.
  - **"s003" is not "S3 Data", and it is not "S3 Table"** (see flag FEN-1).
  - On the authors' side, both of Randi et al.'s codebases name this DOI for
    this workbook:
    - wormneuroatlas `SynapseSign.version` is
      `"https://doi.org/10.1371/journal.pcbi.1007974.s003|"`;
    - pumpprobe `Funatlas._get_aconn_sign_genetic_prediction` downloads that
      DOI and reads sheet `5. Sign prediction`.
- Other supporting-information items (NT-only, R-only, S1 Supporting
  Information with alternative-reconstruction tables, S1 Fig, S3/S4 Tables)
  are only on the journal page. None was found in any reachable distribution;
  see "Not acquired".
- Authors' web tool: EleganSign, http://elegansign.linkgroup.hu. Supplementary
  page: https://linkgroup.hu/elegansdata.php (S1–S5 per a WebSearch summary).
  Both are blocked.
- Input connectome: WormWiring (Emmons lab), https://wormwiring.org/series/
  ("Edge list (.csv)" for the adult hermaphrodite). The exact file URL and the
  WormWiring release date are UNVERIFIED.

Primary checks to perform once reachable:

1. Download doi .s003 and compare its SHA-256 with the pin below. If it
   differs, compare sheet 5 and Summary cell by cell.
2. Read the SI captions and confirm which label s003 carries.
3. Download WormWiring's hermaphrodite edge list and compare it with
   `herm_full_edgelist.csv`.

## Files acquired

| File | Size (bytes) | SHA-256 | Distributor / URL | Integrity checks passed |
|---|---|---|---|---|
| `journal.pcbi.1007974.s003.xlsx` | 983,199 | `85959066fd7cbdbc2024d0ebb323b71c4365f4083bc85e555ee973f470697c47` | PyPI wheel `wormneuroatlas-0.0.7.3-py3-none-any.whl` (sha256 `166289…1325`), member `wormneuroatlas/data/journal.pcbi.1007974.s003.xlsx` | wheel SHA-256 equals PyPI's published digest (live); member matches pin; member matches wheel `RECORD` |
| `Data (rev 12-09-2020).csv` | 321,820 | `8748f968d759157e9e955b325d59314cc0ad8f4bf4501521f380a73a674c66ff` | GitHub `bank-fenyves/CeConn-SignPrediction` @ `e657d5f3c3986e99ccd39601b245b9b32c22d949`, raw URL in MANIFEST | size + SHA-256 match pin; git blob `660e2100…` matches the commit |
| `data.csv` | 531,133 | `0d45dcf0970b94a90f23eef51695f9a47a69bbef9615920915c824877959c9f7` | same repository and commit | same; blob `2442ce8f…` |
| `SignPred Calc` | 2,509 | `0966414de2c990ecd70747127797d00e7f54e8eff808ad345a6a4edb895adb8b` | same | same; blob `98f566a3…` |
| `Search Tool` | 465 | `94641ae0887ea955477ae348f40ccf3e0fa759532d3e66aba4c8db6449b49d15` | same | same; blob `ebd78dfe…` |
| `README.md` | 968 | `beff99dfcb1b79f34b56b11c6e83c19291ccff20a61c30be3ebab693c52c0142` | same | same; blob `ce6c7c59…` |
| `herm_full_edgelist.csv` | 245,463 | `142693f17556148d7f962835b18ac6dd5af18b7467eef61815ebc1dd5474c0ca` | GitHub `openworm/ConnectomeToolbox` @ `ffe570268b7cffb9329cd009a1bb37d60db2d465`, `cect/data/herm_full_edgelist.csv` | size + SHA-256 match pin; git blob `89ffc2a2…` matches the commit |

About the authors' repository, `bank-fenyves/CeConn-SignPrediction`:

- It belongs to the first author. Its README names the paper.
- It is declared SECONDARY because this project's rules treat every GitHub
  repository that way.
- File history in that repository:
  - `data.csv`: added 2020-01-23 (commit `623f4fb`), never changed.
  - `Data (rev 12-09-2020).csv`: added 2020-09-14 (commit `b2ae4a9`).
  - The R scripts: January 2020.
  - Pinned HEAD `e657d5f` (2021-01-07) only edits the README.

### Byte-level relationships between copies

- **xlsx.** The wheel member is byte-identical to
  `francescorandi/wormneuroatlas@b2e13d88:wormneuroatlas/data/journal.pcbi.1007974.s003.xlsx`
  (blob `0457b2fa`, same SHA-256). That copy is not acquired separately.
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
- **`herm_full_edgelist.csv`.** The toolbox blob `89ffc2a2` is byte-identical
  to `openworm/c302` master `c302/data/herm_full_edgelist.csv`. GitHub's
  history page shows a single c302 commit for that path, `49acae1`, dated
  2018-07-06.
  - It is **not** the toolbox's `herm_full_edgelist_MODIFIED.csv` (not
    acquired). On the 302 sheet-1 neurons, that file has 15 extra chemical
    rows and one different weight (VB04→VB05: 5 vs 1).

## What each file contains

**`journal.pcbi.1007974.s003.xlsx`**

- Document properties: created 2019-07-01T09:46:44Z, modified
  2020-09-10T23:15:24Z, lastModifiedBy "Fenyves Bánk", Microsoft Macintosh
  Excel.
- All values used here are Excel's **cached** formula results. For all 3,638
  rows, B:C, G:L and Q are consistent with the workbook's own formulas
  re-evaluated against sheets 1 and 4.

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
  - Names are zero-padded (VA01, AS10; 64 names). AWC appears as AWCL/AWCR.
  - CANL/CANR are present.
- `2. Receptor gene table`: 62 ionotropic receptor genes in six classes,
  columns A..F. Glu Pos 10, Glu Neg 6, ACh Pos 30, ACh Neg 6, GABA Pos 2,
  GABA Neg 8. Columns J:K give the number of neurons expressing each gene.
- `3. Receptor Gene expression`: no header row. One row per neuron (302), with
  a ragged list of expressed receptor gene names. One token, `gar-2`
  (metabotropic), belongs to no sheet-2 class.
- `4. Receptor type expression ` (the trailing space is in the sheet name):
  rows 3–304, same neuron order as sheet 1.
  - Columns B..G are counts of expressed genes per class. **D and E (ACh
    Pos/Neg) are typed values in all 302 rows, not formulas**; B, C, F, G are
    formulas. Today D and E equal what sheets 2+3 imply.
  - Column I is "multi-receptor complexity" (TRUE for 85 neurons).
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
- `Summary`: formulas over whole columns of sheet 5 (cells quoted below).

Excel's defined names `herm_full_edgelist` (A2:F3477), `pred_polarity`,
`synapses`, `unconv` and `nopredsyn` (rows 4–3477) are **stale**:

- they stop 163 data rows short;
- several workbook-level duplicates are `#REF!`;
- the Summary does not use them;
- the autofilter range A2:Q3640 covers all data.

**`Data (rev 12-09-2020).csv`**: sheet 5 A..Q as text (see above).

**`data.csv`**: the January 2020 version.

- 3,638 chemical rows plus 2,167 electrical rows (`Pred_pol` = "electrical",
  all receptor columns HAMIS) plus the legend row.
- Electrical rows:
  - 13 are self-rows;
  - 2,148 directed rows have their reverse listed, and 24 of those rows
    (12 pairs) have asymmetric weights (e.g. AVAL→VA05 4, VA05→AVAL 5);
  - 6 rows are listed in one direction only;
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

**`herm_full_edgelist.csv`**: header `Source,Target,Weight,Type`, 7,379 rows.

- **Every row has space-padded names** (e.g. `I1L , I2L           ,10,chemical`).
- Rows: 4,681 chemical (weight 27,019) and 2,698 electrical (weight 12,683).
- 448 distinct names: neurons plus muscles and other cells (`dBWML1`,
  `pm1`…, `mc*`, `um*`/`vm*`, intestine, sph).
- Names are zero-padded like the xlsx.
- The ConnectomeToolbox reader describes it as "legacy dataset (based on Cook
  et al. 2019) used in the past in OpenWorm. Only included here for
  reference! Do not use!".

## Record counts

Counts come from `python -m src.acquire --counts fenyves2020`.

- "Connections" = rows of sheet 5.
- "Synapses" = sum of column E.
- Categories are the file's own column Q values.
- Paper excerpts were read through WebSearch, which returns excerpts of the
  blocked pages. The URL given is the page the excerpt was attributed to.

Summary sheet, quoted exactly (cell: label / cached value / formula):

| Cell | Label (col A) | Value | Formula |
|---|---|---|---|
| B2 | Chemical synapses | 20589 | `=SUM('5. Sign prediction'!E:E)` |
| B3 | Total predicted chemical synapses | 15063 | `=B2-B4` |
| B4 | Total unpredicted chemical synapses | 5526 | `=SUMIFS('5. Sign prediction'!E:E,'5. Sign prediction'!F:F,"chemical",'5. Sign prediction'!Q:Q,"no pred")` |
| B5 | Strength of prediction | 0.7316042546991112 | `=B3/B2` |
| B7 / C7 | Predicted excitatory synapses | 9070 / 0.6021376883754896 | `=SUMIF('5. Sign prediction'!Q:Q,"+",'5. Sign prediction'!E:E)` / `=B7/SUM(B7:B9)` |
| B8 / C8 | Predicted inhibitory synapses | 2580 / 0.17128062139016131 | `=SUMIF(…Q:Q,"-",…E:E)` / `=B8/SUM(B7:B9)` |
| B9 / C9 | Predicted complex synapses | 3413 / 0.22658169023434907 | `=SUMIF(…Q:Q,"complex",…E:E)` / `=B9/SUM(B7:B9)` |
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
| Connections | rows of sheet 5 (all Edge type "chemical") | **3,638** | 3,638 | bioRxiv / PMC7785220 excerpt via WebSearch: "(3,638 connections and 20,589 synapses total)"; PLOS Results: "weighted edge list representing 20,589 chemical synapses in [3,638 connections]" | **YES** |
| Chemical synapses | sum of E = Summary!B2 | **20,589** | 20,589 | same excerpts | **YES** |
| Excitatory synapses | Q = `+`, sum E = Summary!B7 | **9,070** | 9,070 | journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1007974 and arxiv.org/pdf/2101.05177: "We predicted that 9,070 of the synapses are excitatory and 2,580 are inhibitory, while 3,413 synapses have com[plex function]" | **YES** |
| Inhibitory synapses | Q = `-`, sum E = Summary!B8 | **2,580** | 2,580 | same | **YES** |
| Complex synapses | Q = `complex`, sum E = Summary!B9 | **3,413** | 3,413 | same | **YES** |
| Share predicted | Summary!B5 = (B2−B4)/B2 | **0.7316 (73.2%)** | 73%; "more than two-thirds" | Fenyves PhD thesis, repo.lib.semmelweis.hu/…/fenyvesbank.d_DOIs.pdf: "We predicted polarities for 73% of all ionotropic chemical synapses"; abstract: "made predictions for more than two-thirds of these chemical synapses" | **YES** |
| E:I ratio | Summary!B10 = B7/B8 (synapses) | **3.5155**; connection-count alternative 1,327/425 = **3.1224** | "close to 4:1" | Abstract (arXiv 2101.05177 / PLOS): "observed an excitatory-inhibitory (E:I) ratio close to 4:1"; thesis: "the excitatory-inhibitory sign-balance is close to 4:1" | **NOT COMPARABLE**. The paper gives a rounded qualitative figure; no "4:1" appears anywhere in the workbook (0 text cells). The file's own E:I is 3.5155 (synapse-weighted); it rounds to 4 only at integer precision. The paper's exact counts (9,070 / 2,580) are reproduced, so the derived 3.5155 is what the paper's numbers imply |
| Neurons with multi-receptor complexity | sheet 4 V17 = COUNTIF(I:I,TRUE) | **85** | 85 | bioRxiv preprint (WebSearch summary of biorxiv.org/content/10.1101/2020.05.22.110312): "85 neurons expressed both excitatory and inhibitory receptor genes for the same neurotransmitter" | **YES** (preprint text; journal wording not seen) |
| Neurons in the chemical layer | distinct names in sheet 5 | **297** (excluded: CANL, CANR, M5, PLML, PLMR) | 297 | Szilágyi et al. 2025 bioRxiv 10.1101/2025.01.09.632090v1 (same group, same data): "CANL, CANR, PLML, PLMR, and M5 neurons are not connected by chemical connections hence were excluded" | **YES** (later paper by the same group) |
| Neurons in the reconstruction | names in chemical ∪ electrical rows of `data.csv` | **300** | 300 (WebSearch summary only) | Summaries of the PLOS Methods said "3,638 chemical connections and 2,167 gap junctions, connecting 300 neurons", with CANL/CANR omitted. An exact-phrase search did not find this sentence | **UNVERIFIED** |
| Gap junctions | electrical rows of `data.csv` | **2,167** rows (1,093 unordered pairs; weight 8,640) | 2,167 (summary only) | as above | **UNVERIFIED**. If the paper's 2,167 counts these rows, it counts directed rows, not unordered pairs |
| Excitatory / inhibitory / complex synapses, preprint | Jan 2020 `data.csv`, chemical rows by `Pred_pol` | **9,034 / 2,580 / 3,431** (no pred 5,544) | 9,034 / 2,580 / 3,431 | bioRxiv full text (biorxiv.org/content/10.1101/2020.05.22.110312.full.pdf), via WebSearch: "We predicted that 9,034 of the synapses are excitatory and 2,580 are inhibitory, while 3,431 synapses have complex function" | **YES for `data.csv`**; NOT COMPARABLE to the xlsx, which is the journal version |

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
  - *Derivable* from `herm_full_edgelist.csv` with one filter: Type ==
    "chemical" and both endpoints neurons.
  - Two endpoint rules both give exactly 3,638 rows / 20,589 synapses, equal
    to sheet 5 pair-for-pair and weight-for-weight:
    - "both names in the xlsx sheet-1 list";
    - "both names start upper-case".
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
  - "Close to 4:1" is the paper's rounded wording of 3.5155. A test asserting
    4.0 with a tight tolerance would fail on the paper's own data.

Other counts recorded:

- **Stale named ranges.** 163 sheet-5 data rows lie after the end (row 3477)
  of Excel's `herm_full_edgelist` named range.
- **The input edge list's electrical layer.** 2,168 neuron-neuron rows
  (weight 8,642). `data.csv` has every one of them except PVCR→PVDR
  (weight 2).

### Comparison with Cook et al. 2019 SI 5 (scratch analysis)

Not part of `record_counts`, because the files belong to `white1986`. The
"WormWiring connectome reconstruction" used here is **not** the Cook 2019 SI 5
hermaphrodite chemical matrix. On the 302 sheet-1 names, SI 5 has 3,709
non-zero pairs (20,965 synapses). Against sheet 5 there are:

- 122 pairs only in sheet 5;
- 193 pairs only in SI 5;
- 21 weight differences.

This holds identically for all three SI 5 files (Nature MOESM9, WormWiring
original, WormWiring corrected July 2020). Those files are byte-identical to
`data/raw/white1986/{41586_2019_1352_MOESM9_ESM.xlsx, SI 5 Connectome
adjacency matrices.xlsx, SI 5 Connectome adjacency matrices, corrected July
2020.xlsx}`. The comparison script is in this session's scratch directory,
`agent_fenyves2020/scripts/cmp_si5.py`.

## How Randi et al.'s code consumed this file

- **wormneuroatlas 0.0.7.3, `SynapseSign.py`** reads **only sheets 1 and 2**.
  - It takes the NT per neuron and the six receptor-gene lists.
  - It rewrites names: `VA01`→`VA1`, `AWCL`→`AWCOFF`, `AWCR`→`AWCON`. The
    code comment says the AWC mapping "has no effect" because both are Glu.
  - `NeuroAtlas.get_chemical_synapse_sign` then **recomputes** signs. It uses
    CeNGEN expression (the package's own threshold) in place of Fenyves's
    sheet 3/4 expression. It uses dominant + alternative NTs and gives
    0 = conflicting.
  - `get_anatomical_connectome(signed=True)` flips only the −1 entries.
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
- **FEN-2. Two prediction versions exist** (owner question). They have
  identical connections and weights but 13 different calls (36 synapses):
  - the journal version (xlsx = `Data (rev 12-09-2020).csv`): 9,070 /
    2,580 / 3,413 / 5,526;
  - the preprint version (`data.csv`, Jan 2020): 9,034 / 2,580 / 3,431 /
    5,544.

  The authors' README still points to `data.csv`. Which defines
  `predicted_sign`?
- **FEN-3. E:I target.** The file's E:I is 3.5155 (synapses) or 3.1224
  (connections), not 4. Phase 0 flag F6's "about 4:1" is the paper's rounding.
  The owner should decide what Phase 3 asserts. One option is the exact
  9,070 / 2,580 (Summary B7/B8); another is a ratio with an explicit
  tolerance.
- **FEN-4. Whole-animal network, not head.** The 3,638 / 20,589 / E:I
  figures cover the whole WormWiring hermaphrodite neuron set: 297 neurons,
  ventral cord included. Any head restriction changes all of them; the head
  set is a Phase 2 decision.
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
  chemical subset of `herm_full_edgelist.csv` (WormWiring).
  - That file is not Cook 2019 SI 5.
  - The toolbox marks it "legacy … Do not use!".
  - Its WormWiring release date is UNVERIFIED. It existed in openworm/c302 by
    2018-07-06, and the workbook was created 2019-07-01.
  - Whether to treat it as an anatomical-connectome candidate is the owner's
    call (cf. Q-007 / F9).
- **FEN-9. Name conventions.**
  - Zero-padded VA01/AS10 (64 names).
  - AWCL/AWCR. Randi's package maps L→OFF and R→ON, and that mapping is a
    guess (F7).
  - The edge list has space-padded names everywhere.
  - No normalisation is applied here.
- **FEN-10. Workbook hygiene.** None of these changes values today; they
  matter if anyone edits or re-evaluates the workbook.
  - Stale named ranges (row 3477) and `#REF!` names.
  - Sheet 4's ACh count columns are typed values, not formulas (currently
    consistent).
  - Summary!B4 filters `Edge type == "chemical"` but B7–B9 do not. This is
    harmless because every row is chemical.
  - `gar-2` (metabotropic) is in sheet 3 but in no receptor class.
- **FEN-11. Gap junctions are not predictions.** `data.csv` carries 2,167
  electrical rows. Most pairs are listed in both directions, 12 pairs with
  asymmetric weights, and PVCR→PVDR is missing relative to the WormWiring
  list. They are acquired only as part of that file; they are not a gap
  junction source of record.
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
- EleganSign database and tool (elegansign.linkgroup.hu) and
  linkgroup.hu/elegansdata.php: blocked; no copy found. PyPI has no
  `elegansign` package (404).
- `herm_full_edgelist_MODIFIED.csv` (toolbox): an OpenWorm edit that does not
  match sheet 5; not a Fenyves input.
- `francescorandi/wormneuroatlas` GitHub copy of the xlsx and `openworm/c302`
  copy of the edge list: byte-identical to the acquired copies.
- Cook 2019 SI 5 files: already acquired by `white1986`, and not the Fenyves
  input.
