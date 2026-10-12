# ripollsanchez2023: The neuropeptidergic connectome (short-, mid-, long-range models) and the same group's monoamine network

- Paper: Ripoll-Sánchez L, Watteyne J, Sun H, Fernandez R, Taylor SR,
  Weinreb A, Bentley BL, Hammarlund M, Miller DM 3rd, Hobert O, Beets I,
  Vértes PE, Schafer WR. *The neuropeptidergic connectome of C. elegans.*
  Neuron 111(22), 3570–3589.e5 (2023). doi:10.1016/j.neuron.2023.09.043.
  Preprint: bioRxiv doi:10.1101/2022.10.30.514396.
- Module: `src/acquire/ripollsanchez2023.py`
- Status: **SECONDARY — primary comparison PENDING (blocks Phase 4 freeze)**
- Retrieval date (UTC): 2026-10-11, for all 13 files, from
  `data/raw/ripollsanchez2023/MANIFEST.json`

## Primary location (not reachable from this environment)

- **Journal:** https://www.cell.com/neuron/fulltext/S0896-6273(23)00756-0.
  Supplementary Table S6, "Neuron information", is expected to be the
  journal file `1-s2.0-S0896627323007560-mmc7.xlsx` on the Elsevier
  supplementary host (ars.els-cdn.com, blocked). The mmc7 ↔ Table S6 mapping
  rests on content, not on the journal page: the toolbox's `mmc7.xlsx` and
  the author's `Table S6. Neuron information.xlsx` have identical cells.
- **Data deposit:** a Figshare collection,
  doi:10.6084/m9.figshare.c.6895870.v1. Web search reports it from the paper's
  key-resources / data-availability statement, and reports that "a more
  recent version of this collection is available". Its contents, and which
  of its files corresponds to which acquired file, are **UNVERIFIED**
  (figshare.com is blocked).
- **Code archive:** Zenodo doi:10.5281/zenodo.8387059, "Neuropeptide Networks
  Analysis", per the same web-search report. Blocked. GitHub-to-Zenodo
  archives are normally made from a release tag. The repository's only tag,
  `Paper`, points to `36ecbbf` (2023-06-02), whose tree holds the 07072022
  matrices. That this archive equals that tag is **UNVERIFIED**.
- **NemaMod** (https://www.nemamod.org, the authors' interactive app):
  blocked. Its GitHub repository `LidiaRipollSanchez/NemaMod` holds only an R
  workspace `Data.RData` (replaced 2024-02-02). Its README says: "For
  downloading the data from the paper in csv format go to this
  [repository](https://github.com/LidiaRipollSanchez/Neuropeptide-Connectome.git)".
  That repository is the one acquired from.

Primary checks to perform once reachable:

1. Download the Figshare collection, both v1 and the latest version. Compare
   every matrix with the three acquired versions (07072022 / 08062023 /
   01022024) and record which version each Figshare file equals.
2. Download mmc7 from the journal. Compare its bytes with both acquired xlsx
   copies; neither copy is expected to match, see below. Then compare cells.
3. Open the Zenodo archive and record which commit and matrices it holds.
4. Read the Neuron full text. Confirm the density figures (0.3437, 0.4429,
   0.5929, monoamine 0.0236, synaptic 0.0251), and whether 0.5929 appears in
   the published version or only in the preprint.

## Files acquired

All files are from GitHub, fetched at a pinned commit from
`https://raw.githubusercontent.com/<repo>/<commit>/<path>`. Each is checked
against its pinned size and SHA-256, and against the git blob id the commit
records for its path.

Distributors:

- **(A)** `LidiaRipollSanchez/Neuropeptide-Connectome`, the first author's
  repository (declared in the module, not in `distributions.py`), at three
  commits:
  - **A-HEAD** `6689619236ba1b4681a9a77b3d918d513416336c` (2024-09-20,
    master head);
  - **A-2023** `fb0ba8452aaee88793d731609dcff563d6265ec4` (2023-11-21, the
    last commit before the 2024-02-02 replacement of the matrices);
  - **A-TAG** `36ecbbffc3582a99f49e4a4f81e6a50fa0b9e32f` (2023-06-02, the
    only tag, `Paper`, a lightweight tag).
- **(B)** `openworm/ConnectomeToolbox` @ `ffe570268b7cffb9329cd009a1bb37d60db2d465`
  (owner-approved, D-003).

| File | Size (bytes) | SHA-256 | Distributor / path | Integrity checks passed |
|---|---|---|---|---|
| `01022024_neuropeptide_connectome_short_range_model.csv` | 185,765 | `ee630f66dbb78a49d1818bd5209f1f9a0ee46400c061126e30d0d0a4b9d2e44d` | A-HEAD, `Adjacency matrices for networks/` | size+SHA-256 pin; git blob `10c57394…` |
| `01022024_neuropeptide_connectome_mid_range_model.csv` | 185,866 | `97569885d58d947c2526e6ecc26c8b191b074d1b065f4da224102298203ad141` | A-HEAD, same folder | pin; blob `17672bb5…` |
| `01022024_neuropeptide_connectome_long_range_model.csv` | 186,132 | `57ebc0919860bafcb866e63f5ae06b8b5d59427897d8bd230b4461bfa833f6fe` | A-HEAD, same folder | pin; blob `d1b7e653…` |
| `08062023_neuropeptide_connectome_short_range_model.csv` | 185,773 | `7a9fd18305c4f145c51881ed145e09b442acd8cfda2836c0e87c1bce48c0c1a1` | A-2023, same folder | pin; blob `6acbee7e…` |
| `08062023_neuropeptide_connectome_mid_range_model.csv` | 185,874 | `e2b5f3ae7a760933e47e5c5bc449c915df11e537c2fa33e30728745a49b78cd4` | A-2023, same folder | pin; blob `7c24a9df…` |
| `08062023_neuropeptide_connectome_long_range_model.csv` | 186,152 | `cd3769c27427e972216e6faf7f3cb924fcc4e3e052586bf8f695f694bbcc0b3d` | A-2023, same folder | pin; blob `e229d102…` |
| `07072022_neuropeptide_connectome_short_range_model` | 182,735 | `598cc7d2bba39862e20882fee2365eba9e42c5856d083e57882695f9e8a8f719` | A-TAG, same folder | pin; blob `ce6aca49…` |
| `07072022_neuropeptide_connectome_mid_range_model` | 182,832 | `7a8434d6cca231bdb78cb6ce43f37f5befd953f7d8599dd3b900395323872c18` | A-TAG, same folder | pin; blob `9b517639…` |
| `07072022_neuropeptide_connectome_long_range_model` | 183,108 | `4da3a7b558b9ae02aedd39eb154cfee09a2ce2b35da5674856703bf39148af2f` | A-TAG, same folder | pin; blob `73cb72b5…` |
| `26012022_num_neuronID.txt` | 2,933 | `0f3a73e4f3cda8c9693c75f3c8df18c5b51dd64da6b05a840df7fb18827f954b` | A-TAG, repository root (same blob at HEAD under `Scripts & data/`) | pin; blob `698102a1…` |
| `08062023_monoamine_connectome.csv` | 185,444 | `629c99a54190940be954b5281fb414553dcb2e4913ced34f355aab27b3c9650f` | A-HEAD, `Adjacency matrices for networks/` | pin; blob `7a9db13b…` |
| `Table S6. Neuron information.xlsx` | 36,794 | `8cc3817a0efa76347688331c1a34f940bacab5941b4b205f9ce517382ed90f04` | A-HEAD, `Supplementary Tables/` | pin; blob `913c96f6…` |
| `1-s2.0-S0896627323007560-mmc7.xlsx` | 36,734 | `df379d1eff235b8c7289162048de593b79c94e9bd7cd0e724014e7f92a340654` | B, `cect/data/` | pin; blob `5dd66158…` |

**Duplicate copies across distributions (byte-level):**

- The ConnectomeToolbox at `ffe5702` carries
  `cect/data/01022024_neuropeptide_connectome_{short,mid,long}_range_model.csv`
  and `cect/data/08062023_monoamine_connectome.csv` with the **same git blob
  ids** as A-HEAD (`10c57394…`, `17672bb5…`, `d1b7e653…`, `7a9db13b…`). They
  are therefore byte-identical, and were acquired once, from A.
  - The toolbox validation note (`cect/validation/RipollSanchezEtAl2023.md`)
    names the author repository as its source.
  - The toolbox has **no** copy of the 08062023 or 07072022 neuropeptide
    matrices.
- `Table S6. Neuron information.xlsx` (A) and `1-s2.0-…-mmc7.xlsx` (B) have
  **identical content but different bytes**:
  - Every cell is the same, read both as formulas and as cached values
    (counts: `tableS6_author_vs_toolbox_cells_differ_* = 0`).
  - These zip members are byte-identical: `sharedStrings.xml`, `theme1.xml`,
    `calcChain.xml`, `app.xml`, `[Content_Types].xml`, `_rels`.
  - These differ: `sheet1.xml` (the toolbox copy lacks the `x14ac:dyDescent`
    row attributes and has a different `topLeftCell` view), `styles.xml`
    (one attribute), `workbook.xml` and `core.xml`.
  - `workbook.xml` records `absPath` `/Users/padraig/git/ConnectomeToolbox/cect/data/`
    (B) vs the author's own Supplementary folder (A). Excel build 10909 vs
    11028.
  - `core.xml`: B is modified 2024-11-20 by "Microsoft Office User"; A is
    modified 2023-11-14 by "Lidia Ripoll Sanchez". Both were created
    2023-07-31 by "Lidia Ripoll Sanchez".
  - So the toolbox copy was opened and re-saved in Excel by the toolbox
    maintainer after download. **Neither copy is shown to be byte-identical
    to the journal's mmc7.**

## What each file contains

**Neuropeptide connectome matrices (3 versions × 3 models, kept separate).**

- **Models.** Short-range: ligand and receptor neurons have processes in the
  same bundle. Mid-range: same body region. Long-range: no spatial
  constraint. These are the authors' three models.
- **Size.** 302 × 302 integer matrices covering all 302 hermaphrodite neurons,
  not a head subset.
- **Format.** The 08062023 and 01022024 files are CSV with a header row and a
  first column (corner cell `Row`); header = row labels = the order of
  `26012022_num_neuronID.txt`. The 07072022 files have **no header and no
  file extension**. Their order comes from `26012022_num_neuronID.txt`: the
  README at tag `Paper` says "26012022_num_neuronID.txt : neurons that
  correspond to each row and column in the adjancency matrices". Labelling
  them that way makes their diagonal match Table S6's Self-loops column for
  296 of 302 neurons, and their per-neuron degrees match Table S6 for 263–294
  of 302. A different order would not.
- **Line endings.** LF, final newline present, no BOM.
- **Orientation: `M[i, j]` — row i = sender (expresses the neuropeptide),
  column j = receiver (expresses the receptor).** Evidence:
  1. The authors' `buildnetwork` (`Scripts & data/Run_all_analysis_from_paper.m`)
     computes `B = reExp .* neExp`. NPP expression is a column vector ("so NPP
     expression is in the matrix rows") and receptor expression a row vector
     ("so that receptor expression is in the matrix columns").
     `writetable(array2table(...))` writes the matrix unchanged.
  2. Table S6's In-degree equals the column sums of the binarised,
     diagonal-free 08062023 matrices for 302/302 neurons. Under row sums
     (rows = receivers), 0/302 match for mid and 2/302 for short.
  3. The ConnectomeToolbox reader also reads rows as presynaptic.
  - **Caveat:** a comment at line 479 of the same script says "in my matrix
    the columns are the outdegree (NPP) and the rows the indegree (NPGCPR)".
    That contradicts the code and the data. The code and data agree with
    each other; the comment does not.
- **Weights.** Weight = the number of NPP–GPCR gene pairs, from the authors'
  500 nM EC50 interaction list, for which the row neuron expresses the ligand
  and the column neuron the receptor. CeNGEN threshold 4, binarised. The
  per-pair 0/1 networks are summed (`Group_networks`). The ConnectomeToolbox
  states the same: "Weights indicate the number of different NPP-GPCR
  pathways connecting a neuron pair in a given direction." Maximum weight:
  2022 is 18 (short, mid) and 19 (long); 2023 and 2024 are 19 (short, mid)
  and 20 (long). The networks are not binary.
- **Diagonal.** The diagonal holds autocrine pair counts. It equals Table S6's
  "Self-loops (Fig. 8)" column for 302/302 neurons in every 2023 and 2024
  matrix, and is identical across all three models of a version. The 2022
  diagonal differs in 6 cells.
- **Names.** 302 distinct names in the authors' order, which is not
  alphabetical. It includes AWCL/AWCR and CANL/CANR. 64 ventral-cord names
  are **zero-padded** (AS01…AS09, DA01…DA09, DB01…DB07, DD01…DD06,
  VA01…VA09, VB01…VB09, VC01…VC06, VD01…VD09; AS10, VA10… are naturally two
  digits). The ConnectomeToolbox reader strips this padding
  (`standardise_cell_name`). That is the toolbox's naming decision; none is
  applied here.

**Version history (from `git log` of repository A).**

- **07072022 (preprint era).**
  - Uploaded 2022-11-09.
  - Present at tag `Paper`.
  - Deleted 2023-11-17.
  - Built from 91 NPP–GPCR pairs ("Adjacency matrices of all 91 NPP-GPCR
    networks", README at the tag).
- **08062023.**
  - Uploaded 2023-11-17.
  - The script sets `date = '08062023_'`.
  - Built from 92 pairs: 92 individual networks per model at A-2023.
  - The README names `08062023_neuropeptide_connectome_short_range_model.csv`
    as the "Dataset used to build Cytoscape figure" (Fig. 1). For Fig. 5 it
    names the short- and mid-range files as the datasets "used to build
    matrix depiction".
  - Deleted 2024-02-02.
- **01022024 (post-publication).**
  - Uploaded 2024-02-02.
  - The README gained the line "The adjancency matrices in the Adjacency
    matrices for networks folder were updated on 02/02/2024 with updated
    scRNAseq data for dmsr-5 and npr-34." The README still names the
    08062023 files for the figures.
  - NemaMod's README says the same: "Expression data for dmsr-5 and npr-34
    was updated on 02/02/2024."
  - **This answers owner flag F11.** The ConnectomeToolbox files are this
    post-publication update. The Neuron paper was published 15 Nov 2023.

Differences between versions (counts `diff_*`; rows = senders):

| Model | 07072022 → 08062023 | 08062023 → 01022024 |
|---|---|---|
| short | 1,065 cells differ; +63 edges, −0; 23 sender rows changed (AVH, AVL, DVB, HSN, M1, M4, M5, PQR, RIM, RIR, RIV, URB, VC01–06) over 84 columns; 6 diagonal cells | 1,151 cells differ; +175, −236 edges; 26 sender rows changed (ADA, ADL, AIB, AIM, ASK, AVK, PVQ, PVT, RIB, RIM, RIS, RMH, URYD, URYV) over 225 columns; diagonal unchanged |
| mid | 1,456 cells; +100, −0; same 23 rows; 86 columns | 1,490 cells; +175, −276; same 26 rows; 246 columns |
| long | 1,978 cells; +142, −0; same 23 rows; 86 columns | 2,456 cells; +175, −652; same 26 rows; 246 columns |

**`26012022_num_neuronID.txt`.** Tab-separated `nodeID` / `nodeLabel`, 302
rows. The header line ends in LF, the data lines in CRLF, and there is no
final newline.

**`08062023_monoamine_connectome.csv`.**

- Same layout and labels as the 2023 neuropeptide CSVs.
- Written by the same script, from the same `buildnetwork` function. Ligands
  are serotonin, dopamine, octopamine and tyramine. Ligand expression comes
  from "20230605_Neurotransmitters_Expression_(L.Pereira et al. 2015 Hobert
  lab).csv"; receptors are from CeNGEN threshold 4.
- It uses the 14 monoamine–GPCR pairs in
  `05062023_Ligand-receptor-interactions_Mon_from_Barry_Bentley.csv`: SER-1/4/5/7,
  DOP-1/2/3/4, OCTR-1, SER-3/6, SER-2, TYRA-2/3. No ionotropic receptors.
- No spatial constraint.
- Weights 1–3, being the number of monoamine–receptor pairs. 2,866
  off-diagonal edges and 15 diagonal entries.
- Only 19 rows have outgoing edges: ADEL/R, ADFL/R, CEPDL/R, CEPVL/R,
  HSNL/R, I5, NSML/R, PDEL/R, RICL/R, RIML/R. These are the monoamine-producing
  neurons, consistent with row = sender.
- **It is not the Bentley et al. 2016 monoamine connectome** (see flag P1-RS4).
- Unchanged in repository A since 2023-11-17.

**`Table S6. Neuron information.xlsx` / `1-s2.0-S0896627323007560-mmc7.xlsx`.**

- One sheet, "Neuron information". Two header rows; 302 neuron rows in the
  matrices' order; column B "ID (Adjacency Matrix)" = 1…302.
- Columns:
  - Type; Segment (Fig. 2, 3);
  - Degree, In-degree and Out-degree (EC50 500nM), each for Mid-Range and
    Short-Range (Degree = In + Out for all 302);
  - Rich club: Excel formulas `=IF(E>=251,…)` for mid and `=IF(F>=203,…)`
    for short;
  - Cluster (Fig. 7): Periphery 147, Sensory core 55, Hubs 52, Motor core 48;
  - Self-loops (Fig. 8).
- Free-text notes in columns P onward cite sources ("Anatomical cell class -
  Worm Wiring project S.Cook, Nature 2019 paper", …).
- There are **no long-range columns**.

## Record counts

Counts come from `python -m src.acquire --counts ripollsanchez2023`.

- "Edges" = nonzero off-diagonal cells, i.e. ordered pairs i→j with i≠j.
- Diagonal (autocrine) entries are counted separately.
- Densities use n = 302. The authors' definition, from their code and from
  the paper's Methods ("Density d is the fraction of present connections K to
  possible connections", web-search excerpt), is K / (n(n−1)) on the
  binarised matrix:
  - short and mid are computed with self-loops removed;
  - **long is computed by `density_dir` on the matrix with its diagonal
    kept**, so K includes the 170–171 autocrine entries.

Web-search excerpts used below. All come from searches restricted to
cell.com / pmc.ncbi.nlm.nih.gov (Neuron article, PMC7615469) and
biorxiv.org; the search tool returned snippets, not the page text.

- **E1** (Neuron / PMC): "Even the conservative short-range network
  exhibited high connection density, with more than a third of all possible
  connections or edges (0.3437) present in the network."
- **E2**: "Allowing mid-range connections (0.4429) or long-range connections
  (0.5929) increased this density further". One snippet attributed the full
  sentence to the bioRxiv preprint. Another attributed "Allowing mid-range
  connections (0.4429) increased this density further" to the Neuron
  article. Whether "0.5929" is in the Neuron version is not established.
- **E3**: "the C. elegans synaptic (0.0251) and monoamine (0.0236) networks
  were far less dense". Version not established.
- **E4**: "Its rich club consists of 156 neurons (166 in a mid-range
  network), more than half of the nervous system." Version not established.
- **E5**: "Network graphs were constructed … for each of the 92 individual
  neuropeptide/receptor couples". Search paraphrase-level; version not
  established.

| Quantity | Definition | Count in acquired file | Paper reports | Where the paper reports it | Match |
|---|---|---|---|---|---|
| Neurons | matrix dimension / distinct labels | 302 in every matrix and in Table S6 | — | — | — |
| Edges, short-range | nonzero off-diagonal | 2022: 31,245 · **2023: 31,307** · 2024: 31,246 (diagonal: 170 / 171 / 171) | not found as a count | — | UNVERIFIED |
| Edges, mid-range | same | 2022: 40,256 · **2023: 40,355** · 2024: 40,254 (diag 170 / 171 / 171) | not found | — | UNVERIFIED |
| Edges, long-range | same | 2022: 53,723 · **2023: 53,864** · 2024: 53,387 (diag 170 / 171 / 171) | not found | — | UNVERIFIED |
| Density, short-range | off-diagonal K / (302·301) | 2022: 0.343722 · 2023: 0.344404 · 2024: 0.343733 | 0.3437 | E1 | **2022: YES · 2023: NO — BLOCKER · 2024: YES** at 4 d.p. The 2024 match is coincidental: net −61 edges vs 2023, and its mid and long values do not match |
| Density, mid-range | off-diagonal K / (302·301) | 2022: 0.442851 · 2023: 0.443940 · 2024: 0.442829 | 0.4429 | E2 | **2022: YES · 2023: NO — BLOCKER · 2024: NO — BLOCKER** (0.4428) |
| Density, long-range | all nonzero incl. diagonal / (302·301), as the authors' code computes it; off-diagonal-only in brackets | 2022: 0.592869 (0.590999) · 2023: 0.594431 (0.592550) · 2024: 0.589184 (0.587303) | 0.5929 | E2 (possibly preprint only) | **UNVERIFIED** for the Neuron text. Only the 2022 file reproduces 0.5929, and only with the diagonal counted |
| Per-neuron degree (F11 check) | binarised, diagonal removed; in = column sum, out = row sum, degree = in+out; compared with Table S6 Mid-Range / Short-Range columns | **2023: mid in/out/degree 302/302/302 exact; short 302/302/302 exact.** 2024: mid 208/276/182 exact (max abs diff 22/49/49); short 213/276/187 (max 20/46/46). 2022: mid 270/294/263 (max 6/19/19); short 279/294/271 (max 5/12/12) | Table S6 per-neuron values | `1-s2.0-S0896627323007560-mmc7.xlsx` and `Table S6. Neuron information.xlsx`, sheet "Neuron information", columns E–J, rows 3–304 | **2023: YES · 2024: NO — BLOCKER · 2022: NO — BLOCKER** |
| Self-loops per neuron | diagonal value vs Table S6 col N | 2023 and 2024: 302/302 for all three models; 2022: 296/302 | Table S6 col N | same files, column N | 2023/2024: YES · 2022: NO |
| Rich club, short-range | neurons with Table S6 degree ≥ 203 (the table's own formula threshold) | Table S6: 156 (cached "Yes" 156); computed: 2022 156 · 2023 156 · 2024 **157** | 156 | E4; Table S6 formulas | Table S6, 2022, 2023: YES · 2024: NO — BLOCKER |
| Rich club, mid-range | degree ≥ 251 | Table S6: 166; computed: 166 for all three versions | 166 | E4 | YES |
| Monoamine network density | off-diagonal K / (302·301), self-loops removed as in the authors' code | 0.031528 (2,866 edges; 15 diagonal) | 0.0236 | E3 | **NO — BLOCKER.** This file is not the monoamine network behind the paper's 0.0236. For reference (scratch check, not a count of this source): the wheel's `esconnectome_monoamines_Bentley_2016.csv` gives 1,940 distinct off-diagonal ordered pairs = 0.021342, which does not match either |
| Synaptic network density | — | no synaptic data in this source | 0.0251 | E3 | NOT COMPARABLE (another source's data) |
| NPP–GPCR pairs in the model | — | not encoded in the aggregated matrices | 92 | E5 | NOT COMPARABLE. Repository A has 92 per-pair networks per model at A-2023 and A-HEAD, and 91 at A-TAG (from the repository listing; those files were not acquired) |

## Discrepancies, flags and open questions

- **P1-RS1. The paper's numbers do not come from one version of the
  matrices. BLOCKER for any "reproduce the paper" test.**
  - Table S6 (per-neuron degrees, self-loops, rich-club sizes) is reproduced
    exactly by the **08062023** matrices.
  - The quoted densities 0.3437 / 0.4429 / 0.5929 are reproduced exactly only
    by the **07072022** (preprint-era, 91-pair) matrices, under the authors'
    own code definitions.
  - The 08062023 matrices give 0.3444 / 0.4439 / 0.5944.
  - The likely reading is that the text densities were carried over from the
    preprint computation. That is an inference, not verified. Which version
    is canonical is the owner's decision.
- **P1-RS2 (F11 resolved).** The `01022024_*` files, the ones in the
  ConnectomeToolbox, are a **post-publication update**: dmsr-5 and npr-34
  expression, per the author's README. Compared with Table S6 they differ in
  total degree for 120 (mid) and 115 (short) of 302 neurons, by up to 49.
  Relative to 08062023: −652 / +175 long-range edges, −276 / +175 mid,
  −236 / +175 short.
- **P1-RS3. Orientation.** Rows = senders (ligand), columns = receivers
  (receptor), established by code and data. The authors' own comment at line
  479 says the opposite. Do not rely on that comment.
- **P1-RS4. Monoamine file (Q-009).** `08062023_monoamine_connectome.csv` is
  the Ripoll-Sánchez pipeline's monoamine → GPCR network:
  - 14 GPCR pairs; ligand expression from Pereira et al. 2015; receptor
    expression from CeNGEN threshold 4; no spatial constraint.
  - It is **not** Bentley et al. 2016. It shares 1,256 ordered pairs with the
    wheel's Bentley 2016 monoamine edge list in the same orientation, and
    only 108 transposed. Bentley's list includes ionotropic receptors such
    as lgc-55, which this file does not. That comparison was done in
    scratch, not as a count of this source.
  - Its density (0.0315) does not match the paper's monoamine density
    (0.0236, E3), so it is not the network the paper used for that
    comparison.
  - It is acquired only as a candidate.
- **P1-RS5. Long-range density counts self-loops in the authors' code.**
  Short and mid do not. Any re-computation must say which definition it uses.
- **P1-RS6. Neither xlsx copy is the journal's file.** Both carry Table S6's
  content. The toolbox copy was re-saved by the toolbox maintainer
  (2024-11-20). The author's copy was last saved 2023-11-14. The journal
  supplement may be a third, earlier save. PENDING the primary check.
- **P1-RS7. Whole-animal matrices.**
  - These are 302-neuron matrices, not a head subset.
  - Names follow the authors' scheme: zero-padded ventral-cord names,
    AWCL/AWCR rather than Randi's AWCON/AWCOF, and CANL/CANR, which are
    absent from the Randi atlas.
  - No normalisation is applied here (Phase 2, Q-005).
- **P1-RS8. Weights are pathway counts, not strengths.** A weight of k means
  k ligand–receptor gene pairs could connect i→j. Whether
  `neuropeptide_edge` uses weight > 0, a weight threshold, or per-pair
  identity is an owner decision.

- **P1-RS9. The authors' pipeline cannot be fully re-run from the
  repository.** `Run_all_analysis_from_paper.m` reads four files that never
  appear anywhere in the repository's history (`git log --all`):
  - `20230605_Neurotransmitters_Expression_(L.Pereira et al. 2015 Hobert lab).csv`,
    the monoamine ligand expression;
  - `Syn_network.csv` and `GJ_network.csv`, the synaptic and gap-junction
    networks behind the 0.0251 comparison;
  - `20230601_Gene_ID_GPCR_common_name.xlsx`.

  So the monoamine network, and the synaptic and gap-junction comparisons,
  cannot be reproduced from this distribution alone.

**Owner questions:**

- **Q-RS-1. Version.** Which version defines `neuropeptide_edge`? The
  candidates are 07072022 (matches the paper's text densities), 08062023
  (matches Table S6 and the README's figure list), and 01022024 (the
  authors' current, post-publication correction, used by the
  ConnectomeToolbox). Or should several be carried side by side?
- **Q-RS-2. Models.** Carry all three range models as separate columns, as
  the brief says to keep them separate, or designate one as primary?
- **Q-RS-3 (part of Q-009).** Candidates for `monoamine_edge`: Bentley 2016,
  or this Ripoll-Sánchez 08062023 monoamine network. Neither reproduces the
  paper's 0.0236.
- **Q-RS-4. Per-pair attribution.** Should the per-NPP–GPCR networks (92 per
  model, 2023 and 2024 versions) be acquired? They would let the edge table
  carry which peptide–receptor pairs support each edge, not just a count.
- **Q-RS-5. Autocrine entries.** How should the diagonal be handled for
  Randi self-pairs (Q-001)?

**Not acquired, with reasons:**

- Per-pair networks: `Individual NPP-GPCR networks {SR,MR,LR}/01022024_neuropeptide_network001…092_*.csv`
  (HEAD), `Individual_net_{short,mid,long}_r/08062023_*` (A-2023) and
  `07072022_NPP_GPCR_networks_{short,mid,long}_range_model` (A-TAG; 91
  matrices stacked, 16.6 MB each), plus the 49 neuropeptide-grouped networks
  per model. They are 276–423 more files. Whether they are needed is
  Q-RS-4.
- `Sensitivity Analysis/CSV_networks_T{3,4}_{10nM,50nM,100nM,500nM,1µM}/…`:
  alternative CeNGEN / EC50 thresholds. The paper's main analyses use
  threshold 4 and 500 nM (README).
- Input data for rebuilding the networks: the CeNGEN threshold-4 expression
  table, the 500 nM ligand–receptor list, `072022_anatomical_class.csv`, and
  the monoamine pair list. Rebuilding is a derivation, not acquisition. The
  CeNGEN and deorphanisation data are other sources' domains.
- Derived analysis tables: `Degree_table_networks_comparison.xlsx` (its sheet
  labels look inconsistent: the "All grouped" sheet gives I1L degree 15
  against Table S6's 329), `08062023_Groups_mid_range_network_table.csv`,
  and the rich-club CSVs.
- The other supplementary tables (S1–S5, Fig. S2/S11 data) in
  `Supplementary Tables/`. Not needed for edges. Table S5 (NPP–GPCR pairs) is
  relevant only if Q-RS-4 is approved.
- NemaMod `Data.RData`: an R serialised workspace of the app. The author
  points CSV users to repository A. Not inspected.
- The Figshare collection, the Zenodo archive, the journal mmc7, and the
  bioRxiv supplements: the hosts are blocked.
