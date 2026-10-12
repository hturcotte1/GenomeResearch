# taylor2021: CeNGEN single-cell expression atlas, release 021821 (thresholds 1–4)

- Paper: Taylor SR, Santpere G, Weinreb A, Barrett A, Reilly MB, Xu C, Varol E,
  Oikonomou P, Glenwinkel L, McWhirter R, Poff A, Basavaraju M, Rafi I,
  Yemini E, Cook SJ, Abrams A, Vidal B, Cros C, Tavazoie S, Sestan N,
  Hammarlund M, Hobert O, Miller DM 3rd. *Molecular topography of an entire
  nervous system.* Cell 184(16), 4329–4347.e23 (2021).
  doi:10.1016/j.cell.2021.06.023. The author list is copied from
  `deployment/config_L4.R` in `cengenproject/CengenApp` @ `faafb4b`.
  Preprint: bioRxiv 10.1101/2020.12.15.422897.
- Module: `src/acquire/taylor2021.py`
- Status: **SECONDARY — primary comparison PENDING (blocks Phase 4 freeze)**
- Retrieval date (UTC): 2026-10-11 for all 14 files, from
  `data/raw/taylor2021/MANIFEST.json`

## Primary location (not reachable from this environment)

- **CeNGEN download page:** https://www.cengen.org/downloads/ (blocked).
  - A WebSearch excerpt of that page says: "csv files are available for
    thresholds 1 (most permissive), 2 (medium), 3 (more conservative), and 4
    (most stringent)".
  - The four `cengen_021821_*_threshold{1..4}.csv` files correspond to those
    downloads. **Whether the page still offers release "021821", and under
    what file names, is UNVERIFIED.** See flag TAY-6: the current CeNGEN L4
    web app is configured with a 2025-03-21 dataset.
- **Paper:** Cell, doi:10.1016/j.cell.2021.06.023 (blocked); also
  PMC8710130 (blocked).
- **Raw reads:** GEO GSE136049. This accession comes from a WebSearch summary,
  not from a page read verbatim. Blocked; not needed for Phase 1.
- **CeNGEN web-app exports (`GenesExpressing-*.csv`):** these were produced
  from the CeNGEN web app ("Gene expression by cell type", threshold 2). There
  is no primary copy of the export files themselves. Their primary check is
  the comparison against the threshold-2 matrix, which `record_counts`
  already does (exact match up to 3-decimal rounding; see below).
- **Ripoll-Sánchez input tables:** the authors' repository is
  https://github.com/LidiaRipollSanchez/Neuropeptide-Connectome. That is their
  own distribution, so it is the closest thing to a primary copy for these two
  derived tables. The underlying expression data is CeNGEN's.

Primary checks to perform once reachable:

1. Download the four threshold CSVs from cengen.org/downloads. Compare their
   SHA-256 with the pins below. If the bytes differ, compare the values
   numerically, joined on `Wormbase_ID`.
2. Record which release label the portal gives them.
3. Read the Taylor et al. STAR Methods for:
   - the exact threshold definitions;
   - the number of cell types or clusters;
   - the number of genes.

   Fill in the UNVERIFIED rows of the table below.

## Files acquired

| File | Size (bytes) | SHA-256 | Distributor / URL | Integrity checks passed |
|---|---|---|---|---|
| `cengen_021821_liberal_threshold1.csv` | 14,921,760 | `74ac7e400f3f841d8784946db67bdbc211598c8682020ef57730b29e564e0cb6` | PyPI `wormneuroatlas` 0.0.7.3 wheel, member `wormneuroatlas/data/cengen_021821_liberal_threshold1.csv` | wheel SHA-256 = PyPI digest (checked live); member = pin; member = wheel `RECORD` |
| `cengen_021821_medium_threshold2.csv` | 13,555,783 | `de03fc03cacdf4c1aa7ffd7565df89135ed72eab68d0b3cf03f542932abc63c8` | same wheel, `…/cengen_021821_medium_threshold2.csv` | same three |
| `cengen_021821_conservative_threshold3.csv` | 11,612,055 | `2454624b7b0409b8ce62c5687c431e0c9b9dd5f38148e0bc9b0fb48c26887236` | same wheel, `…/cengen_021821_conservative_threshold3.csv` | same three |
| `cengen_021821_stringent_threshold4.csv` | 9,818,818 | `478791be7f43d46e11cb751cf12016ae517d59b34db3325f29703646853df875` | same wheel, `…/cengen_021821_stringent_threshold4.csv` | same three |
| `cengen.h5` | 32,852,608 | `d8e6f6f2a25e05211676cfd9c3dd18b8a8bb5c3db4d673fd87b61ed91637ed23` | same wheel, `…/cengen.h5` | same three |
| `GenesExpressing-daf-2-thrs2.csv` | 1,905 | `bf2d2e920ad018a1993948f115ba9d7d8b2f11f7f8274f8e858ee423f020683b` | same wheel | same three |
| `GenesExpressing-npr-11-thrs2.csv` | 652 | `37e5fadb7c00f4b382388172a28afca631132bced87c3c0f57a0619230000f73` | same wheel | same three |
| `GenesExpressing-npr-4-thrs2.csv` | 1,294 | `20df91002182487d6bb6e24dff82324ff4281a21b0f552dae7c3fe1634e93a8a` | same wheel | same three |
| `GenesExpressing-pdfr-1-thrs2.csv` | 1,999 | `1a0523ddf5633e21a9fc7dcbb0daad4047c3ed67d1e8bf910717d76676ff7515` | same wheel | same three |
| `GenesExpressing-neuropeptide-receptors.csv` | 80,763 | `1e88e1047a8a8ecd545907f7336212889e59d8dd1ff4ce9731d9c3bf935087c9` | same wheel | same three |
| `GenesExpressing-neuropeptides.csv` | 63,665 | `6f47ec2b853d4aa3433ea98b75253024f01c585c60be01fa45a27fb9ec99a07b` | same wheel | same three |
| `GenesExpressing-unc-7-unc-9-inx-_-eat-5-thrs2.csv` | 12,761 | `ac96905ac5d89068412966cd8e6ab0bca653fe3d94394b7aec44b22fb2bb7954` | same wheel | same three |
| `30072020_CENGEN_threshold4_expression_NPP_NPR_MR_LGC_allneurons.csv` | 354,171 | `b3055e3e954273a9f15e9ad288f3d7e0f14f6a5ad7c2580861cf7a7750f4f3e5` | https://raw.githubusercontent.com/LidiaRipollSanchez/Neuropeptide-Connectome/6689619236ba1b4681a9a77b3d918d513416336c/Scripts%20%26%20data/30072020_CENGEN_threshold4_expression_NPP_NPR_MR_LGC_allneurons.csv | size + SHA-256 = pin; git blob `4401afd4815514a75e9da7e0de936fe7a8aac0f0` = blob recorded at that commit |
| `13112020_CENGEN_threshold3_expression_NPP_NPR_MR_LGC_allneurons.csv` | 394,413 | `72fdc4f4c617d70c1606d7d6d8fd9e7c2d53514478669c770f00d43327df5b80` | https://raw.githubusercontent.com/LidiaRipollSanchez/Neuropeptide-Connectome/6689619236ba1b4681a9a77b3d918d513416336c/Sensitivity%20Analysis/Input%20data/13112020_CENGEN_threshold3_expression_NPP_NPR_MR_LGC_allneurons.csv | size + SHA-256 = pin; git blob `d26fca9c52c95ef47e5f90330b0b7865236fee53` = blob recorded at that commit |

The wheel is
`wormneuroatlas-0.0.7.3-py3-none-any.whl`, SHA-256
`166289031784c9565f6b9205e30dc718bafbc092db3b46f1aef73d93dc4d1325`, at
https://files.pythonhosted.org/packages/b3/dc/634b2a009739f692bad83325e5c0f8fd5b1323ac1a9ce11df7d4c8ac40db/wormneuroatlas-0.0.7.3-py3-none-any.whl
(declared once in `src/acquire/distributions.py`). Zip timestamps of the
members:

- the four threshold CSVs: 2022-12-16 20:31;
- `cengen.h5`: 2022-12-16 21:32.

The Ripoll-Sánchez commit `6689619` (2024-09-20) is the same HEAD that
`src/acquire/ripollsanchez2023.py` pins.

### Why these files and not others

- **The four threshold CSVs.** They are release 021821, the release the
  `wormneuroatlas` package declares (`Cengen.version = "021821"`,
  `description = "Taylor et al. 2021"`). Which threshold the project uses is
  an owner decision, so all four are kept.
- **`cengen.h5`.** This is the file the package's `Cengen` class actually
  reads. It is a lossy (float32) derivative, so it is kept beside the CSVs,
  not instead of them.
- **The seven `GenesExpressing-*.csv` exports.** These are the files the
  Randi et al. code reads:
  - for innexins, neuropeptides and neuropeptide receptors:
    `NeuroAtlas.fname_innexins` / `fname_neuropeptides` /
    `fname_neuropeptide_receptors`, and the same names in
    `pumpprobe/Funatlas.py`;
  - in the pumpprobe RID figure scripts:
    `scripts/fconnectivity/figures/RID/RID_exp_levels_vs_responses.py` reads
    the npr-4, npr-11 and pdfr-1 exports.
- **The two Ripoll-Sánchez tables.** They are the CeNGEN input of the
  neuropeptide connectome the project uses (threshold 4 for the main analyses,
  threshold 3 for the sensitivity analysis). The repository README @ `6689619`
  says: "All main figures analysis is done at CeNGEN threshold 4 and EC50
  deorphanisation data thresholded to 500nM".
  - They show what those authors did to cell-type names, notably AWC. The
    owner must decide whether to follow it.
  - They are in neither the repository's "Paper" tag (`36ecbbf`, 31 paths) nor
    the ConnectomeToolbox.

## What each file contains

### The four threshold CSVs (`cengen_021821_*_threshold{1..4}.csv`)

**Format**

- Comma-separated, quoted, ASCII.
- **CRLF line endings** (13,670 CRLF, 0 bare LF), no BOM.
- Header: `""`, `"gene_name"`, `"Wormbase_ID"`, then **128 cell-type
  columns**.
- The first column is the row number, 1…13,669.

**Rows and columns**

- Rows are genes (13,669 per file) and columns are cell types: **[gene, cell
  type]**.
- The 13,669 `Wormbase_ID`s are unique and all match `WBGene\d{8}`.
- The `gene_name`s are unique; 6,171 contain a period (sequence-style names
  such as `F07G11.1`).
- **Row order differs between the four files**, although the gene sets and
  the (WormBase ID, name) pairs are identical. Join on `Wormbase_ID`, never on
  row position.

**Values**

- Non-negative reals; no NaN, no negatives.
- A zero means not called expressed at that threshold.
- The nonzero sets are **nested**: every cell nonzero at threshold k+1 is
  nonzero at threshold k (checked for 1⊇2⊇3⊇4).
- Where a cell is nonzero in two files, the value is the same number:
  - the maximum relative difference is 4.97×10⁻⁷;
  - this is purely printing precision. For example, `10.0146949709257` in
    one file is `10.01469` in another;
  - between 32,359 and 63,734 cells per file pair differ as strings.
- Per-cell-type column sums:

  | Threshold | Column sum range |
  |---|---|
  | th1 | 965,792–1,000,000.005 |
  | th2 | 926,765–1,000,000.0 |
  | th3 | 807,464–993,216 |
  | th4 | 681,137–982,596 |

  These sums are consistent with TPM, where an unthresholded column would sum
  to 10⁶, with sub-threshold genes zeroed.
- Every gene row has at least one nonzero cell type in **every** file,
  including threshold 4.

**The 128 cell-type columns, verbatim and in file order**

ADA ADE ADF ADL AFD AIA AIB AIM AIN AIY AIZ ALA ALM ALN AQR AS ASEL ASER ASG
ASH ASI ASJ ASK AUA AVA AVB AVD AVE AVF AVG AVH AVJ AVK AVL AVM AWA AWB AWC_OFF
AWC_ON BAG BDU CAN CEP DA DA9 DB DB01 DVA DVB DVC FLP HSN I1 I2 I3 I4 I5 I6
IL1 IL2_DV IL2_LR LUA M1 M2 M3 M4 M5 MC MI NSM OLL OLQ PDA PDB PDE PHA PHB PHC
PLM PLN PQR PVC PVD PVM PVN PVP PVQ PVR PVT PVW RIA RIB RIC RID RIF RIG RIH RIM
RIP RIR RIS RIV RMD_DV RMD_LR RME_DV RME_LR RMF RMG RMH SAA SAB SDQ SIA SIB SMB
SMD URA URB URX URY VA VA12 VB VB01 VB02 VC VC_4_5 VD_DD.

**Naming conventions to resolve in Phase 2.** These are recorded here; none is
decided.

- **Class-level names without L/R or D/V**, e.g. `AVA`, `CEP`, `OLQ`, `SMD`,
  `URY`, `SAA`, `SAB`, `IL1`.
  - One column stands for 2, 4 or 6 neurons.
  - The exception is **ASEL/ASER**, which are separate columns.
- **AWC:** `AWC_OFF` / `AWC_ON`, with underscores. This differs from:
  - `AWCON` / `AWCOF` in the Randi atlas;
  - `AWCOFF` / `AWCON` in the innexin export;
  - AWCL / AWCR in the anatomical connectomes.
  - Phase 0 Q-005 applies.
- **Six-fold classes split into two columns:** `IL2_DV` / `IL2_LR`,
  `RMD_DV` / `RMD_LR`, `RME_DV` / `RME_LR`.
  - In contrast, `IL1`, `CEP`, `OLQ`, `URA`, `URY`, `SAA`, `SIA`, `SIB`,
    `SMB` and `SMD` are single columns.
  - WebSearch excerpts, attributed by the search to the Taylor et al. Cell
    paper or its bioRxiv version, say: "distinct subclusters for two neuron
    classes that display six-fold symmetry at the nerve ring, the inner labial
    IL2 neurons and the RMD neurons". They also say "VC4 and VC5, which flank
    the vulva, clustered independently from the other four VC neurons".
- **Numbered motor-neuron subtypes beside their parent class:**
  - `DA` + `DA9` (not zero-padded);
  - `DB` + `DB01` (zero-padded);
  - `VA` + `VA12`;
  - `VB` + `VB01` + `VB02` (zero-padded);
  - `VC` + `VC_4_5`;
  - `AS` (one column).
  - The Randi atlas uses unpadded ids (`VB1`, `DB1`, `DA9`, `VC4`). The
    Ripoll-Sánchez tables use padded ids (`VB01`, `DB01`, `DA09`, `VC04`).
  - **This matters for the head set:** the retrovesicular ganglion is part of
    the authors' head definition (randi2023 flag F12).
- **`VD_DD`: two classes (VD, DD) merged into one column.**
- **Pharynx:** columns `I1`–`I6`, `M1`–`M5`, `MC`, `MI` and `NSM` are
  present.
  - These are the same 14 name stems as the 20 neurons that
    `data/raw/randi2023/aconnectome_ids_ganglia.json` lists under "anterior
    pharyngeal bulb" and "posterior pharyngeal bulb".
  - Pharyngeal neurons therefore all have a column; M2, M3, I1, I2, MC and NSM
    are class-level (L/R pooled).
- **`CAN` is present.** The Randi atlas has no CAN.
- **No non-neuronal types** are present in this release's matrices. The later
  080421 table (not acquired) has them.

### `cengen.h5`

- 13 datasets, no attributes:
  - `neuron_ids` (128, object);
  - `gene_names_th{1..4}` and `gene_wbids_th{1..4}` (13,669 each, object);
  - `tpm_th{1..4}` (**128 × 13,669, float32**).
- Derivation: `scripts/build_datasets/cengen_make_h5_from_csv.py` in
  `francescorandi/wormneuroatlas` @ `b2e13d8` reads each CSV with
  `np.genfromtxt` and stores `data[1:,3:].astype(np.float32).T`.
- Checked by `record_counts`:
  - `neuron_ids` equals the CSV header;
  - each `gene_*_thN` equals that CSV's row order;
  - each `tpm_thN` equals float32(CSV values) transposed, **bit for bit**.
  - Orientation is therefore **[cell type, gene]**: transposed relative to
    the CSVs.
- The `Cengen` class defaults to `th=4`.

### `GenesExpressing-*.csv`: CeNGEN app exports, threshold 2

**Single-gene exports (four files)**

- Files: `daf-2`, `npr-11`, `npr-4`, `pdfr-1`.
- Columns: `""`, `"Cell type"`, `"Expression level"`. LF line endings.
- Rows are sorted by value, descending.
- For each gene, the listed cell types are **exactly** the gene's nonzero
  cell types in the threshold-2 CSV. They are not equal to the nonzero set at
  any other threshold.
- Values equal threshold 2 rounded to 3 decimals (max abs diff ≤ 4.95×10⁻⁴).

**Matrix exports (three files)**

- Header: `""`, `gene_name`, `X` (WormBase ID), `threshold` (always `2`),
  then 128 cell types. CRLF line endings.
- `neuropeptides`:
  - 137 genes;
  - all 137 rows equal the threshold-2 row of the same WormBase ID.
- `neuropeptide-receptors`:
  - 141 genes;
  - 140 rows equal threshold 2 by WormBase ID;
  - the remaining row has `gene_name` = `X` = `F59D12.1` (a sequence name,
    not a WormBase ID). Its values are identical to the 021821 row `pcdr-1`
    / `WBGene00010329`.
- `unc-7-unc-9-inx-_-eat-5`:
  - 21 genes; **UTF-8 BOM**;
  - **AWC columns named `AWCOFF` / `AWCON`**.
  - On the 126 columns whose names match exactly, the 17 genes present in
    021821 equal threshold 2.
  - `inx-3`, `inx-5`, `inx-6` and `inx-9` are all-zero rows in the export and
    are **absent from the 021821 matrices**. See flag TAY-5.

### Ripoll-Sánchez tables (threshold 4 "30072020", threshold 3 "13112020")

**Format**

- Separated by `;` with CRLF line endings.
- The threshold-3 file has a UTF-8 BOM and no final newline; the threshold-4
  file has neither.
- Rows: 362 WormBase gene ids (no names). The file name lists the gene groups
  "NPP_NPR_MR_LGC".
- Columns: **302 individual neurons**, zero-padded (`AS01`, `DA09`, `VB01`,
  `VC04`, …), including `AWCL` / `AWCR`, `CANL` / `CANR` and `SABD`.

**Value match.** Each neuron column was compared with every 021821 column
(same zero pattern, relative difference ≤ 10⁻⁵ on all 362 genes):

- Every one of the 302 neuron columns equals **exactly one** 021821 column, at
  the threshold the file name states and at no other.
- The "30072020" file is therefore the 021821 threshold-4 matrix, and the
  "13112020" file the threshold-3 matrix, restricted to 362 genes and expanded
  to neurons.

**How those authors expanded cell types to neurons** (found by value match,
not by any naming rule):

- **`AWCL` and `AWCR` both carry `AWC_OFF`.** `AWC_ON` is used by no neuron.
- `DA09` carries `DA9`; `DB01` carries `DB01`; `VB01` and `VB02` carry `VB01`
  and `VB02`; `VA12` carries `VA12`.
- `VC04` and `VC05` carry `VC_4_5`; `VC01`–`03` and `VC06` carry `VC`.
- All `DD0x` and `VD0x` carry `VD_DD`.
- `IL1` is used for all six IL1 neurons, `CEP` for all four, `SAB` for
  `SABD`, `SABVL` and `SABVR`, and so on.
- The full table is in the counts output (`neuron_to_matching_021821_column`).

## Byte-level relationships between copies

**Wheel vs. other GitHub copies**

- Every wheel member acquired here is **byte-identical** (same git blob id,
  hence same SHA-256) to the file of the same name in
  `francescorandi/wormneuroatlas` @ `b2e13d88b670efcb3438aeacba2ad4bd6c383933`
  under `wormneuroatlas/data/`:

  | File | Git blob |
  |---|---|
  | threshold 1 | `c2a1e191…` |
  | threshold 2 | `8f607c34…` |
  | threshold 3 | `e7ae755f…` |
  | threshold 4 | `cd18e969…` |
  | `cengen.h5` | `cef51ed6…` |

- The seven `GenesExpressing-*.csv` are also byte-identical to
  `leiferlab/pumpprobe` @ `1dbc5e0a` under `pumpprobe/`, and under
  `build/lib.linux-x86_64-3.8/pumpprobe/`.
  - Four of them also appear under
    `scripts/fconnectivity/preliminary_scripts/external_data/`.
  - pumpprobe additionally has an `.xlsx` innexin export
    (`GenesExpressing-unc-7-unc-9-inx-*-eat-5-thrs2.xlsx`, blob `66af34ce…`,
    19,221 B). It was not acquired and not compared.

**`cengen.h5` vs. the CSVs**

- Not byte-related: it is a different format.
- Its content equals the float32 cast of the CSVs, transposed, exactly.
- Float32 loses precision: the maximum absolute difference from the CSV
  float64 values is 0.0125, at large values; relative ≤ 6×10⁻⁸.

**Threshold CSVs among themselves**

- Same gene set and same 128 columns.
- Different row order.
- Nested nonzero sets.
- Shared nonzero values equal up to print precision.

**App exports vs. CSVs**

- Content equal to threshold 2:
  - single-gene files: rounded to 3 decimals;
  - matrix files: exact up to print precision.
- Exceptions: the `F59D12.1` / `pcdr-1` naming, the AWC header spelling in the
  innexin file, and the four all-zero innexins absent from the CSVs.

**Ripoll-Sánchez tables vs. CSVs**

- Content equal (≤ 10⁻⁵ relative) to the 021821 threshold-4 and threshold-3
  matrices, on 362 genes, expanded to 302 neurons as described above.
- The date prefixes 30-07-2020 and 13-11-2020 predate the "021821" label. See
  flag TAY-2.

## Record counts

Counts come from `python -m src.acquire --counts taylor2021` and are
deterministic (identical output on two runs).

| Quantity | Definition | Count in acquired file | Paper reports | Where the paper reports it | Match |
|---|---|---|---|---|---|
| Genes per matrix | data rows of each threshold CSV (= `gene_wbids_thN` in h5) | **13,669** in each of the four (identical sets) | not found | Neither the Taylor et al. text nor cengen.org was reachable, and no gene count for the 021821 matrices was found by search | **UNVERIFIED** |
| Cell-type columns | header fields after `gene_name`, `Wormbase_ID` | **128** | 118 neuron classes | WebSearch excerpt (result list incl. https://pmc.ncbi.nlm.nih.gov/articles/PMC8710130 and https://www.hobertlab.org/wp-content/uploads/2021/07/Molecular-topography-of-an-entire-nervous-system.pdf): "Our approach generated profiles of 70,296 neurons, including all 118 canonical neuron classes and thus offers a comprehensive catalog of gene expression for an entire nervous system." Also ConnectomeToolbox `docs/Taylor_2021.md` @ `ffe5702` (read directly): "Gene expression profiles of all 118 neuron classes in the _C.elegans_ hermaphrodite" | **NOT COMPARABLE**. Columns are CeNGEN cell types, not classes: AWC, ASE, IL2, RMD and RME are split; DA9, DB01, VA12, VB01, VB02 and VC_4_5 are subtypes; VD and DD are merged. Reducing 128 to classes is a Phase 2 naming decision. A paper-stated number of cell types or clusters was **not found** (UNVERIFIED) |
| Neurons / cells profiled | — | not in these files (per-type aggregates only) | 70,296 neurons; 100,955 single-cell transcriptomes | First: excerpt above. Second: WebSearch excerpt (result list incl. PMC8710130): "100,955 single cell transcriptomes with a median of 928 UMIs and 328 genes/cell". The 2019 preprint (bioRxiv 737577) reports a different version: "This approach generated profiles of 52,412 neurons, representing 109 of the 118 canonical neuron classes" | **NOT COMPARABLE** (no per-cell data acquired) |
| Threshold labels and order | file names, and nesting of nonzero sets | `liberal_threshold1` ⊇ `medium_threshold2` ⊇ `conservative_threshold3` ⊇ `stringent_threshold4` (nonzero cells 790,889 ⊇ 709,735 ⊇ 551,375 ⊇ 406,717; nesting holds cell by cell) | 1 most permissive … 4 most stringent | cengen.org/downloads, WebSearch excerpt: "csv files are available for thresholds 1 (most permissive), 2 (medium), 3 (more conservative), and 4 (most stringent)". `cengenproject/Thresholding_sc` README @ `291a092` (read directly): 'from threshold "1", the most permissive (capturing more True Positives at the expense of more False Positives), to "4", the most restrictive' | **YES** |
| Value semantics | value range, zeros, column sums | non-negative, no NaN; 0 = absent; per-type column sums ≤ 1,000,000.005 | 0 = not expressed; >0 = average TPM per gene per neuron type (monocle3) | cengen.org/downloads, WebSearch excerpt: "a gene determined not expressed in a cell has a value of 0, a gene above the threshold has a value >0 (the average TPM per gene per neuron type, as calculated by the monocle3 package)". CengenApp README @ `faafb4b` (read directly): "Gene expression values under the threshold have been converted to 0." | **YES** (consistent; that the values are monocle3 TPM cannot be proven from the file) |
| Ripoll-Sánchez input threshold | value match of the 302 neuron columns | "30072020" file: 302/302 match 021821 **th4**, 0 at th1–3. "13112020" file: 302/302 match **th3**, 0 at others | threshold 4 (main); threshold 3 in sensitivity analysis | Neuropeptide-Connectome README @ `6689619` (read directly): "All main figures analysis is done at CeNGEN threshold 4 and EC50 deorphanisation data thresholded to 500nM"; "T4 = CeNGEN scRNAseq expression threshold 4, T3 = CeNGEN scRNAseq expression threshold 3" | **YES** |
| Neuropeptide / receptor genes per class | — | not computed | "∼23 neuropeptide-encoding genes and ∼36 neuropeptide receptors" per class (WebSearch summary of the abstract, not verbatim) | as stated | **NOT COMPARABLE**: depends on the gene lists and threshold the paper used, which were not reachable |

Per-file counts recorded for later phases:

| File | Nonzero cells | Nonzero < 1 | Min nonzero | Max | Cell type with fewest / most nonzero genes |
|---|---|---|---|---|---|
| threshold 1 | 790,889 / 1,749,632 | 22,770 | 0.0269 | 454,946 | ALN 1,390 / ASJ 8,503 |
| threshold 2 | 709,735 | 10,269 | 0.0662 | 454,946 | ALN 1,371 / ASJ 7,542 |
| threshold 3 | 551,375 | 1,651 | 0.178 | 454,946 | ALN 1,162 / IL2_LR 6,254 |
| threshold 4 | 406,717 | 245 | 0.363 | 454,946 | ALN 904 / CAN 5,659 |

`cengen.h5` `tpm_thN` nonzero counts equal the CSVs (790,889 / 709,735 /
551,375 / 406,717).

## Candidates examined and NOT acquired

| Candidate | Where (pinned) | What it is | Why not acquired |
|---|---|---|---|
| `L1_herm.rds`, `L4_herm.rds` (39,281,808 B, blob `9175d6cd…`), `adult_herm.rds`, `adult_male.rds` | `cengenproject/cengen-reference-data` @ `370a5725c5ca9d2095351bd06de16f36bb48e34f` (2026-08-26) | `pins` boards of **unthresholded** long tables (`gene`, `cell_type`, `avg_expr` = raw TPM, `pct_expr`). Per `data.txt`: L4_herm is "pipeline run 2025-03-21", 172 cell types ("CeNGEN's 132 neuron classes plus 40 non-neuronal types"), 22,469 genes | A **different, newer release** (2025 pipeline runs). It has a different cell-type partition (132 neuron classes vs 128 types here) and no thresholds, in R serialization (no reader in this venv). The owner may want it as an alternative (OQ-T2) |
| `percell-data-v1` release assets (`*_cells.rds`) | same repo, GitHub Releases | per-cell counts + metadata | Not inspected: needs the GitHub API to list assets (blocked). Newer release; R format |
| `data/072820_{homeobox_truth, innexin_truth, metabotropic_receptors, pan-neuronal_non-neuronal}.rds` (2,735 / 1,074 / 899 / 1,375 B) | `cengenproject/Thresholding_sc` @ `291a09238a7e53567d68d475107a52782e298479` | Ground-truth expression sets used to choose the thresholds. README: "for a set of genes (see Table S5 of the paper and the `data` directory here)". The R objects carry the same 128 cell-type names (e.g. `VA12`, `VB01`, `VC_4_5`, `VD_DD`) | Not an expression release and not a choice between releases. R serialization. Offered to the owner (OQ-T6) |
| `Data/CeNGEN_TPM_080421.tsv` (22,189,458 B, SHA-256 `e501ae496525742cebc86bbf19afe3ebc02d1cf174ded938d6292ebd34cf531d`, blob `9d8b1fdc…`) | `cengenproject/CeNGEN_integrated_analysis_biorxiv_code` @ `5809e19f643ad2dc52a6776b21e1ad9c9c691be0`; also gzipped in `CeNGEN_integrated_analysis_2024` @ `e97603a` | **Unthresholded** single-cell TPM, release "080421" (Barrett et al. 2022 bioRxiv). It has 22,469 genes × 131 columns, a different partition and non-neuronal types (details below) | **Different release**, inspected in scratch only. All 13,669 genes of 021821 are among its 22,469. On 707,918 cells nonzero in 021821 th1 and present in both, values are close but not equal: median relative difference 1.1×10⁻⁴, only 2,091 within 10⁻⁵. Offered to the owner (OQ-T2) |
| `Data/Integrated_thresholded/240721_Integrated_bsn12_cpm_threshold_{1..4}.csv` and the unthresholded version | `cengenproject/CeNGEN_integrated_analysis_2024` @ `e97603a5202d3dcafab6662f2251164ba04c55e0` | Bulk + single-cell **integrated** expression (2024 analysis), CPM | A different dataset and method from Taylor et al. 2021. Documented only |
| `120920_all_cells_Emptydrops_current_annotation_LUT.rds` (1,566,483 B) | `cengenproject/Initial_single_cell_analysis` @ `fb37a154f0d299846a3d8b7a54765c3023177a78` | Per-cell annotation lookup table | R format. It could support a cell count check against the paper's 100,955, but that needs an RDS reader. Offered to the owner (OQ-T6) |
| CengenApp data | `cengenproject/CengenApp` @ `faafb4bf12bb55bb1696195972d6eda8e458e268` | App code only. The L4 config points to `data/2025-03-21_L4`, which is not in the repository | No data in the repository |
| Duplicates in `francescorandi/wormneuroatlas` @ `b2e13d8` and `leiferlab/pumpprobe` @ `1dbc5e0a` | — | Byte-identical copies (see above) | Same bytes as the wheel members acquired |
| `GenesExpressing-unc-7-unc-9-inx-*-eat-5-thrs2.xlsx` | `leiferlab/pumpprobe` @ `1dbc5e0a`, `scripts/fconnectivity/preliminary_scripts/external_data/` | xlsx version of the innexin export | Not read by the package code. Not compared with the CSV |
| `Supplementary Tables/Table S3. reporter vs CeNGEN expression comparison.xlsx` | `LidiaRipollSanchez/Neuropeptide-Connectome` @ `6689619` | Ripoll-Sánchez supplementary table | Belongs to the ripollsanchez2023 source; not acquired here |
| cengen.org downloads, Monocle objects, GEO GSE136049, Cell supplementary tables | primary hosts | — | Blocked by the egress policy |

Details of the 080421 table:

- Columns that 021821 does not have: `AWC`, `IL2`, `RMD`, `RME`, `VD`, `DD`,
  `RIV_stressed` and `SMD_stressed`, plus the non-neuronal `Excretory`,
  `Glia`, `Hypodermis`, `Intestine`, `Muscle_mesoderm`, `Pharynx`,
  `Rectal_cells` and `Reproductive`.
- 021821 columns it does not have: `AWC_OFF`, `AWC_ON`, `IL2_DV`, `IL2_LR`,
  `RMD_DV`, `RMD_LR`, `RME_DV`, `RME_LR`, `VA12`, `VB01`, `VB02`, `VC_4_5`
  and `VD_DD`.
- Its 22,469 genes are the same number as the 2025 L4_herm pin's `n_genes`.
  This is an observation only; the two files were not compared.

## Discrepancies, flags and open questions

**TAY-1. The authors' own CeNGEN→atlas lookup mis-assigns two head neurons.**

How this was found:

- The logic of `wormneuroatlas` 0.0.7.3
  (`NeuroAtlas.__init__` + `cengen_ids_to_atlas`) was re-implemented in
  scratch, from reading the code. Downloaded code was never executed.
- The class defaults were used (`merge_bilateral` = `merge_dorsoventral` =
  `merge_numbered` = `merge_AWC` = False), together with the 300 ids of
  `data/raw/randi2023/neuron_ids.txt`.

What it shows:

- **`URYVL` and `SABD` match no CeNGEN column.**
  - The `URY` list is `["URYDR","URYDL","URYVR","URYDL"]`: URYDL appears
    twice and URYVL is missing.
  - The `SAB` list is `["SABDR","SABDL","SABVR","SABVL"]`, but the atlas has
    `SABD`.
- The code initialises `cengen_is = -1*np.zeros(...)`, which is all zeros. So
  both neurons silently receive **column 0 = `ADA`** expression.
- Prefix matching also maps `VB1` and `VB2` → `VB` (not `VB01` / `VB02`),
  `DB1` → `DB` (not `DB01`), and `VC4` / `VC5` → `VC` (not `VC_4_5`).

Why it matters:

- Randi et al. name **M3L → URYVL** as a candidate extrasynaptic pair with
  candidate peptide–GPCR pairs (phase0 §1).
- Whether the published analysis used this lookup, and with which merge
  flags, is **UNVERIFIED**.
- This is evidence for the Phase 3 reproduction, not a decision.

**TAY-2. Date codes do not identify releases.**

- The Ripoll-Sánchez files are named 30-07-2020 and 13-11-2020, yet their
  values equal the "021821" matrices exactly.
- Reading "021821" as 2021-02-18 is itself an inference (MMDDYY); it is
  unverified.
- The Thresholding_sc ground truth is dated "072820" and already uses the same
  128 cell-type names.
- Either the 021821 values did not change from mid-2020, or the labels mean
  something else. Identify the release by content, as done here, not by name.

**TAY-3. Row order differs between the four threshold files.**

- Any positional join across thresholds is wrong.
- `cengen.h5` stores a separate gene list per threshold for this reason.

**TAY-4. Print precision differs between files.**

- 32k–64k shared values per file pair differ as strings by ≤ 5×10⁻⁷
  relative.
- Compare numerically. Never hash or string-compare values across thresholds.

**TAY-5. The gene universe is truncated.**

- The 021821 matrices hold 13,669 genes, each nonzero somewhere even at
  threshold 4.
- The 080421 table holds 22,469.
- Genes such as `inx-3`, `inx-5`, `inx-6` and `inx-9` are absent from the 021821
  matrices. They are all-zero rows in the threshold-2 innexin export.
- Owner question: should a gene missing from the matrix be read as "not
  expressed at any threshold", or as "not reported"? This matters for innexin
  (gap-junction) and receptor coverage.

**TAY-6. "CeNGEN" today may not be release 021821.**

- `CengenApp` `deployment/config_L4.R` @ `faafb4b` sets
  `data_dir <- "data/2025-03-21_L4"`.
- `cengen-reference-data` holds 2025 pipeline runs, with a 132-neuron-class
  partition.
- The primary check must target the 021821 files specifically. Values looked
  up in the live app will not necessarily match.

**TAY-7. Transgene-overexpressed genes are flagged unreliable by CeNGEN.**

- `CengenApp` `deployment/config_L4.R` @ `faafb4b` (2025 L4 dataset) warns:
  "Expression values for … are unreliable as they have been overexpressed to
  generate transgenic strains".
- The list is:
  - lin-15A, lin-15B, rol-6, unc-119, pha-1, unc-54;
  - **eat-4**, dpy-20, **unc-47**, **cho-1**, unc-53, gcy-35;
  - C30A5.16, saeg-2, F38B6.2, C30F8.3, cex-1.
- A WebSearch summary also attributes to the CeNGEN literature that "eat-4
  and unc-47 can be unreliable because they were overexpressed". This was not
  verbatim and its source is uncertain.
- Whether the same list applies to release 021821 is **UNVERIFIED**.
- eat-4, unc-47 and cho-1 are the glutamate, GABA and acetylcholine identity
  genes. Any CeNGEN-based transmitter or sign call (Q-008) must not rely on
  them without the owner's ruling.

**TAY-8. Naming quirks inside the app exports.**

- The receptor export uses `F59D12.1` (= `pcdr-1`, `WBGene00010329`) in its
  WormBase-ID column.
- The innexin export spells AWC as `AWCOFF` / `AWCON` and starts with a BOM.

**TAY-9. AWC handling diverges between downstream sources.**

- Ripoll-Sánchez assigned the AWC_OFF profile to **both** AWCL and AWCR and
  dropped AWC_ON.
- The Randi package keeps AWCON / AWCOFF.
- Phase 2 must not silently inherit either; Q-005 applies.

**TAY-10. Coverage of the head set is complete at type level, but pooled.**

- Every pharyngeal and retrovesicular head class has a column.
- But many head neurons share a column with their bilateral, dorsoventral or
  numbered partners, so expression cannot distinguish them.
- How expression is attributed per neuron in the edge table is a Phase 2
  owner decision.

**Owner questions** (none decided here):

- **OQ-T1.** Which threshold (1–4) defines expression in Phase 4 columns?
  - cengen.org WebApp documentation, WebSearch excerpt: "We recommend the
    default threshold 2 as a good balance between false positives and false
    negatives. Users most interested in capturing expression as much as
    possible should use threshold 1. Users most concerned with eliminating
    false positive expression should use threshold 4."
  - The Randi package defaults to `th=4`.
  - Ripoll-Sánchez used 4, with 3 in its sensitivity analysis.
- **OQ-T2.** Which CeNGEN release?
  - 021821 is what Randi and Ripoll-Sánchez used.
  - The alternatives are 080421 (unthresholded TPM) and the 2025 pipeline
    runs (`cengen-reference-data`, current app). Should any of them also be
    acquired?
- **OQ-T3.** How to map CeNGEN types to neurons: AWC_ON / AWC_OFF ↔ AWCL /
  AWCR; VD_DD; the subtypes VB01, VB02, DB01, DA9, VA12 and VC_4_5; the
  six-fold DV/LR splits. See also Q-005.
- **OQ-T4.** Should the TAY-1 lookup bug be reproduced, so as to replicate the
  paper, or corrected, in any Phase 3 reproduction of Randi's peptide–GPCR
  candidates?
- **OQ-T5.** How should a gene missing from the matrix be treated (TAY-5)?
- **OQ-T6.** Acquire the Thresholding_sc ground truth and the per-cell
  annotation LUT? Both need an RDS reader, which would be a new dependency.
- **OQ-T7.** How to treat the overexpressed-transgene genes (TAY-7)?
