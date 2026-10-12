# bentley2016: The multilayer connectome: monoamine and neuropeptide edge lists

- Paper: Bentley B, Branicky R, Barnes CL, Chew YL, Yemini E, Bullmore ET,
  Vértes PE, Schafer WR. *The Multilayer Connectome of Caenorhabditis
  elegans.* PLoS Comput Biol 12(12): e1005283 (2016).
  doi:10.1371/journal.pcbi.1005283. PMC5215746. Preprint: arXiv:1608.08793.
- Module: `src/acquire/bentley2016.py`
- Status: **SECONDARY — primary comparison PENDING (blocks Phase 4 freeze)**
- Retrieval date (UTC): 2026-10-11, for all 4 files, from
  `data/raw/bentley2016/MANIFEST.json`

## Primary location (not reachable from this environment)

- **PLOS supporting information, S1 Dataset:**
  https://doi.org/10.1371/journal.pcbi.1005283.s004 (a zip; journals.plos.org
  and doi.org are blocked).
  - The ConnectomeToolbox validation note `cect/validation/BentleyEtAl2016.md`
    (at the pinned commit) quotes its caption: "Included are edge lists for
    monoamine and neuropeptide networks".
  - The same note says: "The contents of this zip file were extracted and the
    2 files edge_lists/edgelist_MA.csv and edge_lists/edgelist_NP.csv were
    added to our repository".
  - A web-search excerpt of the paper says "Edge lists for individual network
    layers along with a data model showing the relations and constraints used
    to construct the network are provided in the SI".
  - So the zip probably holds more than the two edge lists (at least a "data
    model"). What else it holds is **UNKNOWN**.
- The PLOS figshare collection for the article is
  https://plos.figshare.com/collections/The_Multilayer_Connectome_of_i_Caenorhabditis_elegans_i_/3647060
  (found by web search; blocked).

Mapping of acquired files to the primary:

| Acquired file | Corresponds to (claimed) | Basis |
|---|---|---|
| `edgelist_MA.csv` | `edge_lists/edgelist_MA.csv` inside S1 Dataset (.s004) | toolbox validation note |
| `edgelist_NP.csv` | `edge_lists/edgelist_NP.csv` inside S1 Dataset (.s004) | toolbox validation note |
| `esconnectome_monoamines_Bentley_2016.csv` | same content as `edgelist_MA.csv` plus a header line added by Randi | byte comparison (below) |
| `esconnectome_neuropeptides_Bentley_2016.csv` | same content as `edgelist_NP.csv` plus a header line and a 5th field added by Randi | byte comparison + git history (below) |

Primary checks to perform once reachable:

1. Download `.s004`, list every member, and compare the bytes of
   `edge_lists/edgelist_MA.csv` and `edge_lists/edgelist_NP.csv` with the two
   toolbox files (expected sha256 `5a206a67…` and `bec5f0c9…`).
2. Check whether the zip holds the expanded dopamine network (putative dop-5 /
   dop-6, Table 2 parentheses), per-monoamine lists, or anything else not
   acquired here.
3. Read Table 2 and the Results text of the PLOS version. Confirm the
   per-monoamine edge and node counts (see the UNVERIFIED rows below) and the
   number of receptor-expressing neurons (251 vs 235, flag B3).

## Files acquired

| File | Size (bytes) | SHA-256 | Distributor / URL | Integrity checks passed |
|---|---|---|---|---|
| `edgelist_MA.csv` | 66,718 | `5a206a6743479f4ae11eb82456378051c5d9aeb56ea5c1f82b121671c7fa2aa3` | GitHub openworm/ConnectomeToolbox @ `ffe570268b7cffb9329cd009a1bb37d60db2d465`, `cect/data/edgelist_MA.csv`; https://raw.githubusercontent.com/openworm/ConnectomeToolbox/ffe570268b7cffb9329cd009a1bb37d60db2d465/cect/data/edgelist_MA.csv | size + SHA-256 pin; git blob `a83c4b617244d2fd29b8890bfe87f59b6aad9aa7` matches the commit |
| `edgelist_NP.csv` | 202,657 | `bec5f0c9526db1523ed73fb6a8b386de95d48a2fd5eae75a9a4889758102389b` | same commit, `cect/data/edgelist_NP.csv` | size + SHA-256 pin; git blob `7c23acadf96bccaf77718210c7fc1bd372c59727` |
| `esconnectome_monoamines_Bentley_2016.csv` | 66,771 | `16a1527028c6d8eece4d8a2d792e5a19cc416650e45066612180c42adc83654e` | PyPI wheel `wormneuroatlas-0.0.7.3-py3-none-any.whl` (sha256 `166289031784c9565f6b9205e30dc718bafbc092db3b46f1aef73d93dc4d1325`), member `wormneuroatlas/data/esconnectome_monoamines_Bentley_2016.csv` | wheel SHA-256 equals PyPI's published digest (checked live); member matches pin; member matches wheel `RECORD` |
| `esconnectome_neuropeptides_Bentley_2016.csv` | 217,695 | `0abea9f09112e5d7af88823dd6e4ef91f181af7e919ce997fa12356c92c99e64` | same wheel, member `wormneuroatlas/data/esconnectome_neuropeptides_Bentley_2016.csv` | same three checks |

Acquisition was run three times. The second and third runs re-verified the
files without re-downloading them; raw file mtimes did not change. The third
run's `MANIFEST.json` is byte-identical to the second; the second differs
from the first only in one `note` string, which was reworded between runs.
`--counts` output is byte-identical across runs.

### Byte-level relationships between the copies

All checked directly on bytes. The checks are re-run by `record_counts`
under the `relationships` key.

- **Monoamine.** `esconnectome_monoamines_Bentley_2016.csv` (wheel) is a
  53-byte first line, then exactly the bytes of `edgelist_MA.csv` (toolbox).
  - The first line is `#source neuron, target neuron, transmitter, receptor\n`.
  - Removing it yields a SHA-256 equal to the toolbox file's `5a206a67…`.
- **Neuropeptide.** `esconnectome_neuropeptides_Bentley_2016.csv` (wheel) is
  a 54-byte first line, then 8,931 rows.
  - The first line is `#source neuron, target neuron, transmitter, receptor,\n`,
    with a trailing comma.
  - Each row is the toolbox row with `,<field5>` appended before the LF.
  - Removing the first line and the 5th field yields bytes identical to
    `edgelist_NP.csv` (`bec5f0c9…`). Removing only the first line does not.
- **The 5th field was added by the wormneuroatlas author.** It is not in the
  toolbox's S1 extraction. In GitHub `francescorandi/wormneuroatlas`
  (blobless clone in scratch; not acquired):
  - commit `5ebe7f4c3bdb59bb03592a21371989e25a0bdee3` (2022-12-13, "working
    cengen interface") first adds the file as blob
    `190868bd841ccf4b2f671fb83396a9d9ca193a7e` (202,710 bytes). That blob
    is the 53-byte header plus exactly the toolbox `edgelist_NP.csv` bytes,
    with 4 fields and no 5th field.
  - commit `7a7c653b6dfb4122921429e6a6636bbf3f43b852` (2022-12-23, "Added
    signal propagation (funatlas) and some utilities") replaces it with blob
    `fce8a0a1…` (217,695 bytes), the wheel's version, in the same commit
    that adds `cached_seq_ids.txt`.
  - The monoamine file has had the same blob (`eaa17360…`, equal to the
    wheel member) since 5ebe7f4. Repository HEAD `b2e13d88` (2025-08-24)
    still has both wheel versions.
- **History of the toolbox copy.** Both toolbox files were added in commit
  `f052c0d2e28ca78c037c3476bdfdf3f48bd6e2a2` (2026-06-24, P. Gleeson,
  "Reimplemetation of Bentley et al MA & Pep readers with using Bentley
  edgelist csv fiels directly") and have not changed since.
  - Before that commit, the toolbox read Bentley data through the
    wormneuroatlas package (the same commit's diff of `BentleyEtAl2016.md`).
  - The toolbox's lack of a header and of a 5th field is consistent with the
    stated zip extraction. Whether the bytes equal the zip member is PENDING
    (primary check 1).
- **Conclusion.** For the four columns source/target/ligand/receptor, the two
  distributions carry the same 2,626 + 8,931 rows, in the same order and
  with the same bytes. The network counts computed from each copy are
  identical (`*_network_counts_identical_across_copies = true`).

## What each file contains

**Row format (all four files).**

- ASCII; LF line endings (0 CR); a final newline.
- Comma-separated with no quoting and no spaces around fields (0 fields with
  surrounding whitespace or empty, in fields 1–4).
- Fields: `source, target, ligand, receptor`. The toolbox files have no
  header. The wheel files have the `#…` header described above, and the
  wheel neuropeptide file has a 5th field.
- Ligand (field 3) is a monoamine name (`dopamine`, `octopamine`,
  `serotonin`, `tyramine`) or a neuropeptide gene (`flp-1` … `pdf-2`).
  Receptor (field 4) is a gene name.
- No duplicate rows: 2,626 and 8,931 distinct (source, target, ligand,
  receptor) tuples.

**Orientation: field 1 = sender (expresses the ligand), field 2 = receiver
(expresses the receptor).** Evidence:

1. The wheel header: "source neuron, target neuron".
2. The toolbox readers take row[0] as pre and row[1] as post.
3. The monoamine list has exactly 18 distinct field-1 names. The paper
   reports 18 monoamine-releasing neurons (E5). By transmitter, the senders
   are:
   - tyramine: RIML/RIMR;
   - octopamine: RICL/RICR;
   - dopamine: ADEL/R, CEPDL/R, CEPVL/R, PDEL/R;
   - serotonin: ADFL/R, HSNL/R, NSML/R.

   The paper's Fig 2 caption names "RIM tyramine releasing neurons" and "RIC
   octopamine releasing neurons" (E10).
4. Randi's loader `NeuroAtlas._get_esconnectome_bentley` reads `sl[0]` as
   `id_from` and `sl[1]` as `id_to`. It sets `esc[ai_to, ai_from] = True`,
   i.e. [receiver, sender], matching the atlas's [responding, stimulated]
   layout.

**Structure.**

- Every (ligand, receptor) block is the complete bipartite product of its
  senders and receivers: every sender of the ligand × every neuron expressing
  that receptor (`complete_bipartite_sources_x_targets = true` for all 17
  monoamine and all 22 neuropeptide blocks).
- So the edges come purely from expression, with no spatial or anatomical
  constraint.
- A neuron that both makes a ligand and expresses its receptor gets a
  self-row (autocrine).
- A neuron pair linked through k receptors of the same ligand appears on k
  rows. The paper states the de-duplication rule for monoamines:
  "Neurons expressing multiple receptors for a single monoamine receive a
  single edge from each sending neuron. Reciprocal connections between nodes
  are considered as 2 separate unidirectional connections" (E9).

**Monoamine list.**

- 4 transmitters and 17 receptor genes:
  - dopamine: dop-1, dop-2, dop-3, dop-4, lgc-53;
  - octopamine: octr-1, ser-3, ser-6;
  - serotonin: mod-1, ser-1, ser-4, ser-5, ser-7;
  - tyramine: lgc-55, ser-2, tyra-2, tyra-3.
- There are **no dop-5 / dop-6 rows**. The paper's "expanded network
  including putative dop-5 and dop-6 connections" (E6) is therefore not in
  these files.
- No ordered pair occurs under two monoamines, because the senders are
  disjoint. So the aggregate count of distinct pairs equals the sum over
  monoamines.

**Neuropeptide list.**

- 15 peptide genes and 12 receptor genes, in 22 peptide→receptor
  combinations (listed in the counts table).
- 943 ordered pairs are linked by more than one peptide.

**Wheel neuropeptide 5th field.** It holds a receptor sequence name.

- It is non-empty on only 843 of 8,931 rows, inconsistently. Examples:
  - `flp-18 -> npr-1`: 110 rows `C39E6.6`, 550 rows empty;
  - `flp-21 -> npr-11`: 48 rows `C25G6.5`, 76 rows empty;
  - `flp-1 -> npr-4`: `C16D6.2`, while `flp-18 -> npr-4` and
    `flp-4 -> npr-4` are empty.
- Randi's loader ignores it: it reads fields 0–3. `PeptideGPCR.supplement`
  reads `usecols=(2,3)`.
- It is not part of Bentley's data (see above). Downstream code must not
  treat it as such.

**Names (raw, not normalised).**

- Ventral-cord names are unpadded: VA1…VA12, VB1…VB11, VD1…VD13, DA1…DA9,
  DB1…DB7, DD1…DD6, AS1…AS11, VC1…VC6.
- AWC appears as `AWCL`/`AWCR`.
- `CANL`/`CANR` appear (monoamine list only: dopamine dop-4 and lgc-53
  targets, and tyramine ser-2 and tyra-2 targets).
- Randi's package id list (`data/raw/randi2023/neuron_ids.txt`) has
  `AWCOFF`/`AWCON` and no `CANL`/`CANR`. The atlas h5 has `AWCOF`/`AWCON`.
  - Monoamine names absent from that list (scratch check): AWCL, AWCR,
    CANL, CANR. They occur on 44 rows: AWCL/AWCR as tyramine tyra-3
    targets, and the CAN rows above.
  - Neuropeptide names absent from that list: AWCL, AWCR, on 26 rows, as
    flp-4 and nlp-1 senders.
- No names are changed here (Phase 2, Q-005).

## Record counts

Counts come from `python -m src.acquire --counts bentley2016`.

- They are computed separately from each copy; the toolbox and wheel copies
  give identical network counts.
- "Pairs" = distinct ordered (source, target).
- "excl self" drops source == target.
- "Per-ligand" pairs are de-duplicated across a ligand's receptors.

Web-search excerpts used below. All are search-tool renderings of
journals.plos.org / PMC5215746 / arXiv:1608.08793 / ResearchGate copies;
the tool returned snippets and paraphrases, not page text. Version
attributions (PLOS vs arXiv) are the search tool's.

- **E1** (PLOS version, https://journals.plos.org/ploscompbiol/article?id=10.1371%2Fjournal.pcbi.1005283;
  also ResearchGate 307541125 / 321265925): "out of 1940 monoamine
  connections only 80 overlap with chemical or electrical synapses".
  Separately: "the monoamine network adds 1,940 directed edges" (a summary
  page).
- **E2** (arXiv, https://arxiv.org/pdf/1608.08793): "out of 2036 monoamine
  connections only 89 overlap with chemical or electrical synapses, meaning
  96% of the monoamine connections are unique to the monoamine layer."
- **E3** (PLOS version): "Even for this partial network, 239 neurons are seen
  to be involved in neuropeptide signalling (out of 302 possible) with 7035
  connections between them, providing greater connectivity than either the
  synaptic or monoamine layers".
- **E4** (arXiv): the same sentence with **7046** connections.
- **E5** (search summary of PLOS vs arXiv): "The PLOS text reports that 251
  neurons (83%) were found to express one or more monoamine receptors, while
  the arXiv preprint reports 248 neurons (82%). The monoamine-releasing count
  is the same in both: 18 of 302 neurons." (Paraphrase-level, not a
  verbatim quote.)
- **E6** (PLOS, Table 2 caption): "Table showing the number of nodes and
  edges in the individual and aggregate monoamine networks. Values for an
  expanded network including putative dop-5 and dop-6 connections are in
  parentheses."
- **E7** (search-tool reconstructions of Table 2, mutually inconsistent;
  "the extracted table's column headers are garbled"):
  - (a) "248 neurons … and 2,164 edges in the aggregate network. The
    per-system rows are serotonin (490 edges), dopamine (1,392), octopamine
    (54), and tyramine (228)". A later result attributes 2164 to "the arXiv
    table".
  - (b) "a dopamine row in Table 2 showing 137 nodes and 1339 edges".
  - (c) "dopamine 1,339 non-synaptic edges … octopamine 54 (100%)",
    attributed to a companion table.
- **E8** (arXiv / PMC): "They focused on 12 neuropeptide receptors with
  well-established ligands and precisely-characterized expression patterns
  for both receptor and peptide precursor genes".
- **E9** (Methods, as summarised in the toolbox's `docs/Bentley_2016.md` and
  in search results): "Neurons expressing multiple receptors for a single
  monoamine receive a single edge from each sending neuron. Reciprocal
  connections between nodes are considered as 2 separate unidirectional
  connections."
- **E10** (Fig 2 caption, ResearchGate figure page
  https://www.researchgate.net/figure/Monoamine-signalling-in-C-elegans-is-primarily-extrasynaptic-A-RIM-tyramine-releasing_fig2_307541125):
  "Monoamine signalling in C. elegans is primarily extrasynaptic (A) RIM
  tyramine releasing neurons … (B) RIC octopamine releasing neurons".
- **E11** (toolbox `docs/Bentley_2016.md`, pinned commit, a secondary
  summary): "15 neuropeptides and 12 receptors were matched and included."
- **T** (toolbox validation files, pinned commit, the toolbox's own expected
  counts, not the paper's):
  - `Bentley2016MAReader_expected_data.yaml` `total_nonzero_conns`:
    Dopamine 1176, Tyramine 228, Octopamine 56, Serotonin 492.
  - `Bentley2016PepReader_expected_data.yaml`: Peptidergic 7078.
  - `WormNeuroAtlasMAReader_expected_data.yaml` (via Randi's package):
    Dopamine **1160**, Tyramine **224**, Octopamine 56, Serotonin 492.

| Quantity | Definition | Count in acquired file | Paper reports | Where the paper reports it | Match |
|---|---|---|---|---|---|
| Monoamine connections (aggregate) | distinct ordered pairs, excl self, all 4 monoamines | **1,940** (incl self: 1,952; rows: 2,626) | 1940 (PLOS); 2036 (arXiv) | E1; E2 | **YES** vs PLOS text (snippet level). Not the arXiv figure |
| Monoamine-releasing neurons | distinct field-1 names, monoamine list | **18** | 18 of 302 | E5 | **YES** (paraphrase-level excerpt) |
| Monoamine edges, dopamine | per-ligand pairs excl self | **1,168** (incl self 1,176; rows 1,752; 8 senders × 147 targets) | E7(a) 1,392; E7(b) 1,339 | E7 (Table 2, garbled; version and parenthetical status unknown) | **UNVERIFIED.** No clean excerpt. Arithmetic: E1's 1,940 equals 1,168 + 490 + 54 + 228 (this file's per-monoamine values), so the PLOS text total is consistent with 1,168. If PLOS Table 2's main (non-parenthetical) dopamine value is 1,392, this is **NO — BLOCKER** (flag B2) |
| Monoamine edges, serotonin | same | **490** (incl self 492; rows 540) | 490 | E7(a) | **UNVERIFIED** (equal to the search-tool reconstruction, which is not a reliable excerpt) |
| Monoamine edges, octopamine | same | **54** (incl self 56; rows 72) | 54 | E7(a), E7(c) | **UNVERIFIED** (same caveat) |
| Monoamine edges, tyramine | same | **228** (incl self 228; rows 262) | 228 | E7(a) | **UNVERIFIED** (same caveat) |
| Monoamine network neurons (aggregate) | distinct names in field 1 ∪ field 2 | **237** (targets 235; sources 18; both 16; sources never targets ADFL/ADFR) | 248 (E7(a), arXiv table "nodes"); 251 / 248 neurons expressing ≥1 monoamine receptor (PLOS / arXiv) | E5, E7(a) | **NOT COMPARABLE as defined.** The paper's quantity is receptor *expression*. The file holds only receivers of receptors included in the network (no dop-5/dop-6, E6). Raw gap: 235 targets vs 251 (PLOS). Flag B3; resolve at the primary check |
| Monoamine self-pairs | distinct neurons with a self-row | **12** (dopamine 8 [all 8 DA neurons, via dop-2]; octopamine 2 [RICL/R, via ser-6]; serotonin 2 [NSML/R, via ser-4]) | not found | — | UNVERIFIED (the paper's totals E1/E3 match only with self excluded) |
| Neuropeptide connections (aggregate) | distinct ordered pairs excl self, all peptides | **7,035** (incl self 7,078; rows 8,931; sum of per-peptide pairs excl self 7,991) | 7035 (PLOS); 7046 (arXiv) | E3; E4 | **YES** vs PLOS text (snippet level). Not the arXiv figure |
| Neuropeptide neurons | distinct names in field 1 ∪ field 2 | **239** (sources 141; targets 187; both 89) | 239 | E3, E4 | **YES** |
| Neuropeptide receptors | distinct field-4 genes | **12** (ckr-2, egl-6, frpr-4, npr-1, npr-2, npr-3, npr-4, npr-5, npr-11, npr-17, ntr-1, pdfr-1) | 12 | E8; E11 | **YES** |
| Neuropeptides | distinct field-3 genes | **15** (flp-1, -4, -5, -10, -13, -15, -17, -18, -21; nlp-1, -12, -24; ntc-1; pdf-1, pdf-2) | 15 | E11 (toolbox summary of the paper; no direct paper excerpt found) | **YES** on E11 only; paper text UNVERIFIED |
| Neuropeptide self-pairs | distinct neurons with a self-row | **43** (62 self-rows) | not found | — | UNVERIFIED |
| Neuropeptide edges per peptide→receptor | rows (= pairs; no duplicates within a block) | flp-1→npr-11 60; flp-1→npr-4 135; flp-10→egl-6 75; flp-13→frpr-4 152; flp-15→npr-3 200; flp-17→egl-6 15; flp-18→npr-1 660; flp-18→npr-11 48; flp-18→npr-4 108; flp-18→npr-5 360; flp-21→npr-1 1,705; flp-21→npr-11 124; flp-21→npr-2 589; flp-21→npr-5 930; flp-4→npr-4 162; flp-5→npr-11 36; nlp-1→npr-11 40; nlp-12→ckr-2 52; nlp-24→npr-17 16; ntc-1→ntr-1 780; pdf-1→pdfr-1 1,804; pdf-2→pdfr-1 880 | not found | — | UNVERIFIED |
| Monoamine edges per transmitter→receptor | rows (= pairs) | DA: dop-1 576, dop-2 160, dop-3 664, dop-4 80, lgc-53 272; OA: octr-1 24, ser-3 24, ser-6 24; 5-HT: mod-1 216, ser-1 132, ser-4 78, ser-5 36, ser-7 78; TA: lgc-55 54, ser-2 118, tyra-2 36, tyra-3 54 | not found | — | UNVERIFIED |
| Toolbox's own expected counts | per-ligand pairs incl self | DA 1,176; TA 228; OA 56; 5-HT 492; NP 7,078 | (toolbox, not paper) | T | consistent with the file (incl-self definition) |

Density, for the Q-009 context only. This is arithmetic, not a paper
comparison; n = 302 is the paper's neuron total (E3):

- Bentley monoamine: 1,940 / (302·301) = 0.021342 (incl self: 0.021474).
- Ripoll-Sánchez et al. 2023 report a monoamine density of 0.0236
  (`docs/provenance/ripollsanchez2023.md`, E3 there). Neither Bentley value
  equals it, nor does the 08062023 monoamine file (0.0315).

## Discrepancies, flags and open questions

- **B1. The paper versions differ, and the files match the PLOS version.**
  - The PLOS text gives 1,940 monoamine and 7,035 neuropeptide connections,
    and 251 receptor-expressing neurons.
  - The arXiv preprint gives 2,036, 7,046 and 248.
  - The acquired edge lists reproduce both PLOS totals exactly, with
    self-pairs excluded, and neither arXiv total.
  - Any "reproduce the paper" test should cite the PLOS version.
- **B2. Table 2 per-monoamine counts are UNVERIFIED. This is a possible
  blocker.**
  - One search reconstruction of Table 2 gives dopamine 1,392 and aggregate
    2,164; the file gives 1,168 and 1,940.
  - 2,164 − 1,940 = 224 = 8 dopamine senders × 28. That is consistent with
    28 extra dopamine receivers, for example the dop-5/dop-6 "expanded
    network" in the Table 2 parentheses (E6), or an arXiv-version table.
    That reading is an inference, not verified.
  - The other three monoamines (490 / 54 / 228) equal the file's values.
  - Needs the PLOS Table 2 (primary check 3).
- **B3. Receptor-expressing neurons: 251 (PLOS) / 248 (arXiv) vs 235
  receivers in the file.**
  - The edge list cannot show receptor expression outside the network's
    receptor set, for example dop-5/dop-6. So the two quantities are not
    defined the same way.
  - The gap of 16 is unexplained and must be checked against the primary
    (expression tables / S1 Dataset).
- **B4. Randi's loader silently mis-assigns names missing from its id list.
  This matters for anyone reusing Randi's extrasynaptic matrices.**
  - In wormneuroatlas 0.0.7.3, `ids_to_ai` returns −1 for a name not in its
    list. `_get_esconnectome_bentley` then writes `esc[ai_to, ai_from]`
    without checking, so −1 indexes the last neuron in the sorted id list,
    **VD9**.
  - A scratch re-implementation (the package was not executed; default
    merge flags) gives these results:
    - monoamine: 1,928 nonzero entries instead of 1,952 distinct pairs. The
      24 pairs involving AWCL/AWCR/CANL/CANR collapse onto existing VD9
      entries.
    - per monoamine: dopamine **1,160**, which reproduces the toolbox's
      `WormNeuroAtlasMAReader` expected 1,160 (T).
    - neuropeptide: **10 spurious entries** that make VD9 a sender (flp-4 /
      nlp-1, via the AWCL/AWCR rows) to AIAL, AIAR, AIYL, AIYR, AVAL, AVAR,
      BAGL, BAGR, RIVL, RIVR.
  - The toolbox's WormNeuroAtlas route gives tyramine 224. My simulation
    gives 220, and the file gives 228. The toolbox reader adds its own name
    handling, which I did not investigate further.
  - A second loader bug: `if recept[-1] == "\n": recept = recept[-1]` sets
    the receptor to "\n" on every monoamine row (4-field lines end in the
    receptor). It only matters when filtering by receptor.
  - The edge table must be built from these raw files, not from the
    package's matrices.
- **B5. The wheel neuropeptide 5th field is not Bentley data.** It is sparse
  and inconsistent (843 / 8,931 rows filled) and was added by the package
  author. It should be ignored, or explicitly attributed if used.
- **B6. Self-pairs.**
  - There are 12 monoamine and 43 neuropeptide autocrine self-pairs. Their
    multiplicity is 12 and 62 rows.
  - The paper's totals exclude them (they match only on the excl-self
    definition).
  - The toolbox's expected counts (T) include them.
  - Whether `monoamine_edge` / `neuropeptide_edge` include self-pairs is for
    the owner (relates to Q-001).
- **B7. Edges carry ligand and receptor identity, which the aggregate count
  hides.**
  - 116 monoamine pairs are supported by 3 receptors and 442 by 2.
  - 943 neuropeptide pairs are supported by more than one peptide.
  - The data allow (a) a binary any-ligand edge, (b) per-monoamine or
    per-peptide edges, or (c) per ligand→receptor edges. Which to carry is
    an owner decision.
- **B8. Whole-animal lists, not head subsets.**
  - Names follow the WormAtlas/White style without zero-padding (VA1, not
    VA01).
  - AWCL/AWCR versus the atlas's AWCON/AWCOFF (Q-005).
  - CANL/CANR have no Randi counterpart.
  - Phase 2 must map these explicitly; nothing is normalised here.
- **B9. Toolbox documentation pages.**
  - `docs/Bentley_2016.md` links `Bentley2016_MA_data_graph.md` and
    `Bentley2016_PEP_data_graph.md`. These files do not exist in `docs/` at
    the pinned commit; they appear to be generated for the website (web
    search finds openworm.org/ConnectomeToolbox/Full1_Bentley2016_MA_data).
  - They are not data and were not acquired.
- **B10. The Bentley list includes ligand-gated channel genes as receptors.**
  The monoamine receptor set includes lgc-53, lgc-55 and mod-1. Per
  `docs/provenance/ripollsanchez2023.md`, the Ripoll-Sánchez 08062023
  monoamine network uses 14 GPCR pairs only. This is one structural
  difference between the two Q-009 candidates.

**Owner questions (not decided here):**

- **Q-009 / Q-B1. `monoamine_edge` source.** The candidates are:
  - Bentley 2016 (this source): 4 monoamines, 17 receptor genes, 1,940
    non-self pairs; matches the PLOS text.
  - Ripoll-Sánchez et al. 2023 `08062023_monoamine_connectome.csv` (source
    `ripollsanchez2023`): 14 GPCR pairs, CeNGEN threshold 4, 2,866 non-self
    edges.

  Per the ripollsanchez2023 doc, they share 1,256 ordered pairs. Neither
  reproduces the 0.0236 monoamine density in Ripoll-Sánchez et al. Or should
  both be carried as separate columns?
- **Q-B2. Which copy is the pipeline input?** The edges are identical. The
  toolbox copy is the claimed S1 extraction, with no added field. The wheel
  copy is what Randi's package loads, with a header and Randi's 5th field.
  Recommendation for the owner's consideration: read edges from the toolbox
  copy and keep the wheel copy as a cross-check. This is the owner's call.
- **Q-B3. Edge granularity.** Binary any-ligand, per-ligand, or per
  ligand→receptor (B7)? And include self-pairs (B6)?
- **Q-B4. Expanded dopamine network.** Is the dop-5/dop-6 expanded network
  (E6) wanted? It is not in these files. Where it lives in the primary SI is
  unknown.
- **Q-B5. `neuropeptide_edge` source.** Bentley's partial neuropeptide layer
  (15 peptides / 12 receptors) or the Ripoll-Sánchez neuropeptide connectome
  (Q-RS-1)? Or both as separate columns?

**Not acquired, with reasons:**

- PLOS S1 Dataset zip (`journal.pcbi.1005283.s004`) and the other PLOS SI
  items: the host is blocked. Their full contents are unknown (primary
  checks 1–2).
- The original 4-field wheel-repository version of the neuropeptide file
  (`francescorandi/wormneuroatlas` blob `190868bd…`, commit 5ebe7f4). It
  equals the 53-byte header plus `edgelist_NP.csv`, so its content is fully
  represented, and the relationship is documented above.
- Toolbox cache files (`cect/cache/Bentley2016MAReader.json`,
  `Bentley2016PepReader.json`, `WormNeuroAtlas*Reader.json`): derived
  outputs of the toolbox's readers, not source data.
- University of Kiel open-data "Multi-layer connection of C. elegans"
  (fdr_mods_00000079): a third-party compilation (WormAtlas + Bentley et al.)
  for a 2021 locomotory-circuit study. Derived, and its host is blocked.
