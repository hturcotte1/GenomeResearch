# bentley2016: The multilayer connectome: monoamine and neuropeptide edge lists

- Paper: Bentley B, Branicky R, Barnes CL, Chew YL, Yemini E, Bullmore ET,
  Vértes PE, Schafer WR. *The Multilayer Connectome of Caenorhabditis
  elegans.* PLoS Comput Biol 12(12): e1005283 (2016).
  doi:10.1371/journal.pcbi.1005283. PMC5215746. Preprint: arXiv:1608.08793.
- Module: `src/acquire/bentley2016.py`
- Status: **SECONDARY — primary comparison PENDING (blocks Phase 4 freeze)**
- Retrieval date (UTC): 2026-10-11 for the two toolbox files and the two
  wheel files; 2026-11-18 for the two pumpprobe files. From
  `data/raw/bentley2016/MANIFEST.json`.

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
  - A web-search excerpt of the paper (read on or before 2026-10-12) says
    "Edge lists for individual network layers along with a data model
    showing the relations and constraints used to construct the network are
    provided in the SI".
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
| `pumpprobe__esconnectome_monoamines_Bentley_2016.csv` | byte-identical to `esconnectome_monoamines_Bentley_2016.csv` | byte comparison (below) |
| `pumpprobe__esconnectome_neuropeptides_Bentley_2016.csv` | same content as `edgelist_NP.csv` plus a header line added by Randi; no 5th field | byte comparison (below) |

Primary checks to perform once reachable:

1. Download `.s004`, list every member, and compare the bytes of
   `edge_lists/edgelist_MA.csv` and `edge_lists/edgelist_NP.csv` with the two
   toolbox files (expected sha256 `5a206a67…` and `bec5f0c9…`). Confirm that
   neither member carries the `#source neuron, …` header line or the wheel's
   5th field.
2. Check whether the zip holds the expanded dopamine network (putative dop-5 /
   dop-6, Table 2 parentheses), per-monoamine lists, receptor-expression
   tables, or anything else not acquired here.
3. Read Table 2, the companion table of receptor nodes without synaptic input
   / non-synaptic edges, and the Results text of the PLOS version. Confirm the
   per-monoamine edge and node counts (the UNVERIFIED rows below) and resolve
   the receptor-expressing-neuron blocker (251 vs 235, flag B3).

## Files acquired

| File | Size (bytes) | SHA-256 | Distributor / URL | Integrity checks passed |
|---|---|---|---|---|
| `edgelist_MA.csv` | 66,718 | `5a206a6743479f4ae11eb82456378051c5d9aeb56ea5c1f82b121671c7fa2aa3` | GitHub openworm/ConnectomeToolbox @ `ffe570268b7cffb9329cd009a1bb37d60db2d465`, `cect/data/edgelist_MA.csv`; https://raw.githubusercontent.com/openworm/ConnectomeToolbox/ffe570268b7cffb9329cd009a1bb37d60db2d465/cect/data/edgelist_MA.csv | size + SHA-256 pin; git blob `a83c4b617244d2fd29b8890bfe87f59b6aad9aa7` matches the commit |
| `edgelist_NP.csv` | 202,657 | `bec5f0c9526db1523ed73fb6a8b386de95d48a2fd5eae75a9a4889758102389b` | same commit, `cect/data/edgelist_NP.csv`; https://raw.githubusercontent.com/openworm/ConnectomeToolbox/ffe570268b7cffb9329cd009a1bb37d60db2d465/cect/data/edgelist_NP.csv | size + SHA-256 pin; git blob `7c23acadf96bccaf77718210c7fc1bd372c59727` |
| `esconnectome_monoamines_Bentley_2016.csv` | 66,771 | `16a1527028c6d8eece4d8a2d792e5a19cc416650e45066612180c42adc83654e` | PyPI wheel `wormneuroatlas-0.0.7.3-py3-none-any.whl` (sha256 `166289031784c9565f6b9205e30dc718bafbc092db3b46f1aef73d93dc4d1325`), member `wormneuroatlas/data/esconnectome_monoamines_Bentley_2016.csv` | wheel SHA-256 equals PyPI's published digest (checked live); member matches pin; member matches wheel `RECORD` |
| `esconnectome_neuropeptides_Bentley_2016.csv` | 217,695 | `0abea9f09112e5d7af88823dd6e4ef91f181af7e919ce997fa12356c92c99e64` | same wheel, member `wormneuroatlas/data/esconnectome_neuropeptides_Bentley_2016.csv` | same three checks |
| `pumpprobe__esconnectome_monoamines_Bentley_2016.csv` | 66,771 | `16a1527028c6d8eece4d8a2d792e5a19cc416650e45066612180c42adc83654e` | GitHub leiferlab/pumpprobe @ `1dbc5e0a2b609d54bc9b1c90c73d4e3bf183d3c7`, `pumpprobe/esconnectome_monoamines_Bentley_2016.csv`; https://raw.githubusercontent.com/leiferlab/pumpprobe/1dbc5e0a2b609d54bc9b1c90c73d4e3bf183d3c7/pumpprobe/esconnectome_monoamines_Bentley_2016.csv | size + SHA-256 pin; git blob `eaa17360c76e311ad690f68395537d1f7628c4e5` matches the commit |
| `pumpprobe__esconnectome_neuropeptides_Bentley_2016.csv` | 202,710 | `b8544d2bc947d0dc2ddf510f141f06b90acae2e39fea49f4cf7ec13c3f59de6f` | same commit, `pumpprobe/esconnectome_neuropeptides_Bentley_2016.csv`; https://raw.githubusercontent.com/leiferlab/pumpprobe/1dbc5e0a2b609d54bc9b1c90c73d4e3bf183d3c7/pumpprobe/esconnectome_neuropeptides_Bentley_2016.csv | size + SHA-256 pin; git blob `190868bd841ccf4b2f671fb83396a9d9ca193a7e` |

The pumpprobe files carry a `pumpprobe__` prefix locally because the
monoamine file has the same name as the wheel member. Re-running
acquisition re-verifies files that are present without re-downloading them;
raw file mtimes do not change. On 2026-11-18 a second run after adding the
pumpprobe files left `MANIFEST.json` byte-identical, and `--counts` output
was byte-identical under `PYTHONHASHSEED` 0, 1 and 12345.

### Byte-level relationships between the copies

All checked directly on bytes. The checks are re-run by `record_counts`
under the `relationships` key (key names in brackets).

- **Monoamine, wheel.** `esconnectome_monoamines_Bentley_2016.csv` is a
  53-byte first line, then exactly the bytes of `edgelist_MA.csv` (toolbox)
  (`ma_wheel_first_line_bytes`, `ma_wheel_after_first_line_equals_toolbox_bytes`).
  - The first line is `#source neuron, target neuron, transmitter, receptor\n`.
- **Monoamine, pumpprobe.** `pumpprobe__esconnectome_monoamines_Bentley_2016.csv`
  is byte-identical to the wheel's monoamine file
  (`ma_pumpprobe_equals_wheel_bytes`; same SHA-256, and the same git blob
  `eaa17360…` that the file has in francescorandi/wormneuroatlas).
- **Neuropeptide, wheel.** `esconnectome_neuropeptides_Bentley_2016.csv` is
  a 54-byte first line, then 8,931 rows.
  - The first line is `#source neuron, target neuron, transmitter, receptor,\n`,
    with a trailing comma.
  - Each row is the toolbox row with `,<field5>` appended before the LF.
  - Removing the first line and the 5th field yields bytes identical to
    `edgelist_NP.csv` (`np_wheel_after_first_line_fields_1_to_4_equals_toolbox_bytes`).
    Removing only the first line does not
    (`np_wheel_after_first_line_equals_toolbox_bytes` = false).
- **Neuropeptide, pumpprobe.** `pumpprobe__esconnectome_neuropeptides_Bentley_2016.csv`
  is a 53-byte first line, then exactly the bytes of `edgelist_NP.csv`
  (`np_pumpprobe_first_line_bytes`, `np_pumpprobe_after_first_line_equals_toolbox_bytes`).
  - Its first line is the monoamine header, with no trailing comma
    (`np_pumpprobe_header_equals_ma_wheel_header`).
  - It has 4 fields per row and no 5th field, so it is not the wheel's
    version (`np_pumpprobe_equals_wheel_bytes` = false). Below the first
    line it equals the wheel's rows with the 5th field removed
    (`np_pumpprobe_after_first_line_equals_wheel_after_first_line_fields_1_to_4`).
- **The 5th field was added by the wormneuroatlas author.** It is not in the
  toolbox's S1 extraction and not in the pumpprobe copy. Git history
  (blobless clones in scratch, 2026-11-18; not acquired):
  - leiferlab/pumpprobe: both files were added in `8ceb2cb` (2022-07-15,
    "transferring files") as blobs `eaa17360…` (66,771 bytes) and
    `190868bd841ccf4b2f671fb83396a9d9ca193a7e` (202,710 bytes) and are
    unchanged at the pinned commit `1dbc5e0a` (2023-09-20). Commit
    `da18b9e` (2022-12-01) added the same two blobs under
    `build/lib.linux-x86_64-3.8/pumpprobe/`.
  - francescorandi/wormneuroatlas: commit
    `3eed4b823e3c122de04db3f1107e62db7114b86d` (2022-12-12, "Pushing some
    of the intial classes") first adds both files, at `wormneuroatlas/`, as
    the same blobs `eaa17360…` and `190868bd…`. Commit
    `5ebe7f4c3bdb59bb03592a21371989e25a0bdee3` (2022-12-13) moves them to
    `wormneuroatlas/data/` unchanged.
  - Commit `7a7c653b6dfb4122921429e6a6636bbf3f43b852` (2022-12-23, "Added
    signal propagation (funatlas) and some utilities") replaces the
    neuropeptide file with blob `fce8a0a138bf44fe2c4a02a33066122095f26a9a`
    (217,695 bytes), the wheel's version, in the same commit that adds
    `cached_seq_ids.txt`.
  - Repository HEAD `b2e13d88` (2025-08-24) still has the wheel's two
    versions (blobs `eaa17360…`, `fce8a0a1…`).
- **History of the toolbox copy.** Both toolbox files were added in commit
  `f052c0d2e28ca78c037c3476bdfdf3f48bd6e2a2` (2026-06-24, P. Gleeson,
  "Reimplemetation of Bentley et al MA & Pep readers with using Bentley
  edgelist csv fiels directly") and have not changed up to the pinned commit.
  - Before that commit, the toolbox read Bentley data through the
    wormneuroatlas package (the same commit's diff of `BentleyEtAl2016.md`).
  - The toolbox's lack of a header and of a 5th field is consistent with the
    stated zip extraction. Whether the bytes equal the zip member is PENDING
    (primary check 1).
- **Conclusion.** For the four columns source/target/ligand/receptor, the
  three distributions carry the same 2,626 + 8,931 rows, in the same order
  and with the same bytes. The network counts computed from each copy are
  identical (`monoamine_network_counts_identical_across_copies` and
  `neuropeptide_network_counts_identical_across_copies` = true, now over all
  three copies), and so are the neuron-name sets
  (`neuron_names.*.identical_in_wheel_copy`, `identical_in_pumpprobe_copy`).

## What each file contains

**Row format (all six files).**

- ASCII; LF line endings (0 CR); a final newline.
- Comma-separated with no quoting and no spaces around fields (0 fields with
  surrounding whitespace or empty, in fields 1–4).
- Fields: `source, target, ligand, receptor`. The toolbox files have no
  header. The wheel and pumpprobe files have the `#…` header line described
  above, and only the wheel neuropeptide file has a 5th field.
- Ligand (field 3) is a monoamine name (`dopamine`, `octopamine`,
  `serotonin`, `tyramine`) or a neuropeptide gene (`flp-1` … `pdf-2`).
  Receptor (field 4) is a gene name.
- No duplicate rows: 2,626 and 8,931 distinct (source, target, ligand,
  receptor) tuples.

**Orientation: field 1 = sender (expresses the ligand), field 2 = receiver
(expresses the receptor).** Evidence:

1. The wheel and pumpprobe header: "source neuron, target neuron".
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
4. Randi's loaders (wormneuroatlas `NeuroAtlas._get_esconnectome_bentley`
   and pumpprobe `Funatlas._get_esconnectome_bentley`, the same code) read
   `sl[0]` as `id_from` and `sl[1]` as `id_to`. They set
   `esc[ai_to, ai_from] = True`, i.e. [receiver, sender], matching the
   atlas's [responding, stimulated] layout.

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
- Receivers per transmitter (distinct field-2 names, `by_ligand.*.n_targets`):
  dopamine 147, octopamine 28, serotonin 82, tyramine 114; 235 in all.

**Neuropeptide list.**

- 15 peptide genes and 12 receptor genes, in 22 peptide→receptor
  combinations (listed in the counts table).
- 943 ordered pairs are linked by more than one peptide.

**Wheel neuropeptide 5th field.** It holds a receptor sequence name.

- It is non-empty on only 843 of 8,931 rows (empty on 8,088), inconsistently.
  Examples:
  - `flp-18 -> npr-1`: 110 rows `C39E6.6`, 550 rows empty;
  - `flp-21 -> npr-11`: 48 rows `C25G6.5`, 76 rows empty;
  - `flp-1 -> npr-4`: `C16D6.2`, while `flp-18 -> npr-4` and
    `flp-4 -> npr-4` are empty.
- Randi's wormneuroatlas loader ignores it: it reads fields 0–3.
  `PeptideGPCR.supplement` reads `usecols=(2,3)`. Randi et al.'s analysis
  code (pumpprobe) loads the 4-field file, which has no 5th field.
- It is not part of Bentley's data (see above). Downstream code must not
  treat it as such.

**Names (raw, not normalised).**

- Ventral-cord names are unpadded: VA1…VA12, VB1…VB11, VD1…VD13, DA1…DA9,
  DB1…DB7, DD1…DD6, AS1…AS11 in both lists; VC1…VC6 in the neuropeptide list
  only (no VC neuron appears in the monoamine list).
- AWC appears as `AWCL`/`AWCR`.
- `CANL`/`CANR` appear (monoamine list only: dopamine dop-4 and lgc-53
  targets, and tyramine ser-2 and tyra-2 targets).
- Randi's two id lists differ (scratch checks against the files acquired by
  the other sources):
  - wormneuroatlas `neuron_ids.txt` (`data/raw/randi2023/neuron_ids.txt`) has
    `AWCOFF`/`AWCON` and no `CANL`/`CANR`. The atlas h5 has `AWCOF`/`AWCON`.
    Monoamine names absent from it: AWCL, AWCR, CANL, CANR, on 44 rows
    (AWCL/AWCR as tyramine tyra-3 targets, and the CAN rows above).
    Neuropeptide names absent from it: AWCL, AWCR, on 26 rows, as flp-4 and
    nlp-1 senders.
  - pumpprobe `aconnectome_ids.txt` (`data/raw/white1986/aconnectome_ids.txt`,
    the id list `Funatlas` loads) has `AWCL`/`AWCR` and no `CANL`/`CANR`.
    Names absent from it: CANL, CANR (monoamine list, 40 rows); none in the
    neuropeptide list.
- No names are changed here (Phase 2, Q-005).

## Record counts

Counts come from `python -m src.acquire --counts bentley2016`.

- They are computed separately from each copy; the toolbox, wheel and
  pumpprobe copies give identical network counts.
- "Pairs" = distinct ordered (source, target).
- "excl self" drops source == target.
- "Per-ligand" pairs are de-duplicated across a ligand's receptors.
- "Receivers" = distinct field-2 names (`n_targets`); "senders" = distinct
  field-1 names (`n_sources`).

Web-search excerpts used below. All are search-tool renderings of
journals.plos.org / PMC5215746 / arXiv:1608.08793 / ResearchGate copies;
the tool returned snippets and paraphrases, not page text. Version
attributions (PLOS vs arXiv) are the search tool's. "Read on or before
2026-10-12" means the excerpt was recorded in this file by commit `fd1c7b6`
(2026-10-12) and its exact search date is not known; "re-found 2026-11-18"
means a search on that date returned it again.

- **E1** (PLOS version, https://journals.plos.org/ploscompbiol/article?id=10.1371%2Fjournal.pcbi.1005283;
  also ResearchGate 307541125 / 321265925; read on or before 2026-10-12,
  re-found 2026-11-18): "out of 1940 monoamine connections only 80 overlap
  with chemical or electrical synapses". Separately: "the monoamine network
  adds 1,940 directed edges" (a summary page; read on or before 2026-10-12).
- **E2** (arXiv, https://arxiv.org/pdf/1608.08793; read on or before
  2026-10-12, re-found 2026-11-18): "out of 2036 monoamine connections only
  89 overlap with chemical or electrical synapses, meaning 96% of the
  monoamine connections are unique to the monoamine layer."
- **E3** (PLOS version; read on or before 2026-10-12, re-found 2026-11-18):
  "Even for this partial network, 239 neurons are seen to be involved in
  neuropeptide signalling (out of 302 possible) with 7035 connections between
  them, providing greater connectivity than either the synaptic or monoamine
  layers".
- **E4** (arXiv; read on or before 2026-10-12, re-found 2026-11-18): the
  same sentence with **7046** connections.
- **E5** (search summaries, paraphrase level, not verbatim):
  - read on or before 2026-10-12: "The PLOS text reports that 251 neurons
    (83%) were found to express one or more monoamine receptors, while the
    arXiv preprint reports 248 neurons (82%). The monoamine-releasing count
    is the same in both: 18 of 302 neurons."
  - re-found 2026-11-18, attributed to the PLOS PDF on ResearchGate
    (https://www.researchgate.net/publication/321265925_The_Multilayer_Connectome_of_Caenorhabditis_elegans):
    of the 302 neurons, "18 release monoamines and 251 (83%) express at least
    one monoamine receptor"; arXiv:1608.08793 gives "248 neurons (82%)".
  - also 2026-11-18, attributed to arXiv:1608.08793: "18 of the 302 neurons
    in the hermaphrodite connectome are monoamine-releasing cells". One
    other rendering on the same day garbled the sentence (it gave 18 as the
    number of receptor-expressing neurons), which shows these are not
    verbatim. A secondary review (Georgia State University,
    https://neuroscience.gsu.edu/files/2025/09/Using-neurons-to-maintain-autonomy-Learning-from-C.-elegans.pdf,
    2026-11-18) gives "251 or 83% of the worm's neurons have receptors for
    these".
- **E6** (PLOS, Table 2 caption; read on or before 2026-10-12): "Table
  showing the number of nodes and edges in the individual and aggregate
  monoamine networks. Values for an expanded network including putative
  dop-5 and dop-6 connections are in parentheses."
- **E7** (arXiv-version tables as rendered by the search tool):
  - (a) read on or before 2026-10-12; the tool said "the extracted table's
    column headers are garbled": "248 neurons … and 2,164 edges in the
    aggregate network. The per-system rows are serotonin (490 edges),
    dopamine (1,392), octopamine (54), and tyramine (228)". A later result
    attributed 2164 to "the arXiv table". 2,164 also differs from the arXiv
    text's 2,036 (E2), so either the reconstruction is unreliable or the two
    arXiv figures use different definitions.
  - (b) a companion table of receptor nodes with no synaptic input and
    non-synaptic edges. Read on or before 2026-10-12 as "a dopamine row in
    Table 2 showing 137 nodes and 1339 edges" and "dopamine 1,339
    non-synaptic edges … octopamine 54 (100%)". Re-found 2026-11-18,
    attributed to https://arxiv.org/pdf/1608.08793: the dopamine network has
    "137 non-postsynaptic receptor nodes (78.3%) and 1,339 non-synaptic edges
    (96.2%)". **These are subsets, not totals.** Arithmetic (scratch): a
    dopamine total of 175 receptor nodes and 1,392 edges gives 137/175 =
    78.3% and 1,339/1,392 = 96.2%, so (b) is consistent with (a)'s 1,392
    being the arXiv dopamine total.
- **E8** (arXiv / PMC; read on or before 2026-10-12, a summary sentence; an
  exact-phrase search on 2026-11-18 for "neuropeptide receptors with
  well-established ligands" returned PMC5215746, arXiv:1608.08793 and
  ResearchGate 321265925): "They focused on 12 neuropeptide receptors with
  well-established ligands and precisely-characterized expression patterns
  for both receptor and peptide precursor genes".
- **E9** (Methods, as summarised in the toolbox's `docs/Bentley_2016.md` at
  the pinned commit, and in search results, 2026-11-18): "Neurons expressing
  multiple receptors for a single monoamine receive a single edge from each
  sending neuron. Reciprocal connections between nodes are considered as 2
  separate unidirectional connections."
- **E10** (Fig 2 caption, ResearchGate figure page
  https://www.researchgate.net/figure/Monoamine-signalling-in-C-elegans-is-primarily-extrasynaptic-A-RIM-tyramine-releasing_fig2_307541125;
  read on or before 2026-10-12, page title returned again 2026-11-18):
  "Monoamine signalling in C. elegans is primarily extrasynaptic (A) RIM
  tyramine releasing neurons … (B) RIC octopamine releasing neurons".
- **E11** (toolbox `docs/Bentley_2016.md`, pinned commit, blob `8c25f8d6`; a
  secondary summary, not paper text): "15 neuropeptides and 12 receptors
  were matched and included."
- **E12** (PLOS-version companion table, one search result only, 2026-11-18,
  attributed to https://journals.plos.org/ploscompbiol/article?id=10.1371%2Fjournal.pcbi.1005283;
  two further searches the same day did not return it): dopamine "121 (138)"
  cells with no synaptic input "(82.3%, or 73.8% in parentheses)", "1,133
  (1,422) non-synaptic edges, and 97% (95.6%) non-synaptic edges". **These
  are subsets, not totals.** Arithmetic (scratch) with this file's dopamine
  totals: 121/147 = 82.3% and 1,133/1,168 = 97.0%, both as printed. The
  parenthetical (expanded-network) values fit about 187 receptor nodes
  (138/187 = 73.8%).
- **E13** (2026-11-18; exact-phrase searches for "Of 114 neurons that express
  reporters for one or more of the four tyramine" and "only 7 are
  postsynaptic to a tyraminergic neuron" returned
  https://www.researchgate.net/publication/321265925_The_Multilayer_Connectome_of_Caenorhabditis_elegans
  and https://arxiv.org/pdf/1608.08793; a search restricted to PLOS/PMC
  domains returned the same content attributed to
  https://journals.plos.org/ploscompbiol/article?id=10.1371%2Fjournal.pcbi.1005283
  and https://pmc.ncbi.nlm.nih.gov/articles/PMC5215746): "Of 114 neurons that
  express reporters for one or more of the four tyramine (TA) receptors, only
  7 are postsynaptic to a tyraminergic neuron", the two tyraminergic neurons
  RIML and RIMR being "presynaptic to a total of 20 neurons", so that
  "approximately 94% of tyramine-responsive neurons must respond only to
  extrasynaptic TA". So the 114 is in both versions (snippet level).
- **T** (toolbox validation files at the pinned commit; the toolbox's own
  expected counts, not the paper's):
  - `Bentley2016MAReader_expected_data.yaml` (blob `1dff625f`)
    `total_nonzero_conns`: Dopamine 1176, Tyramine 228, Octopamine 56,
    Serotonin 492.
  - `Bentley2016PepReader_expected_data.yaml` (blob `159f7a7d`): Peptidergic
    7078.
  - `WormNeuroAtlasMAReader_expected_data.yaml` (blob `f75b1c67`; via the
    wormneuroatlas package): Dopamine **1160**, Tyramine **224**,
    Octopamine 56, Serotonin 492.

| Quantity | Definition | Count in acquired file | Paper reports | Where the paper reports it | Match |
|---|---|---|---|---|---|
| Monoamine connections (aggregate) | distinct ordered pairs, excl self, all 4 monoamines | **1,940** (incl self: 1,952; rows: 2,626) | 1940 (PLOS); 2036 (arXiv) | E1 (PLOS text, snippet level). The arXiv figure (E2) is the preprint version and is not matched | **YES** |
| Monoamine-releasing neurons | distinct field-1 names, monoamine list | **18** | 18 of 302 | E5 (search renderings of both versions, paraphrase level; one garbled rendering noted there) | **YES** |
| Monoamine receptor-expressing neurons (aggregate) | receivers: distinct field-2 names, all 4 monoamines | **235** (field 1 ∪ field 2: 237; senders 18; senders that are also receivers 16; senders never receivers ADFL/ADFR) | 251 (83%) PLOS; 248 (82%) arXiv | E5 (paraphrase level). The definitions coincide per transmitter: tyramine 114 = 114 (E13, row below). 235 − 251 = −16 (PLOS); 235 − 248 = −13 (arXiv). See flag B3 | **NO — BLOCKER** |
| Tyramine receptor-expressing neurons | receivers of tyramine rows (`by_ligand.tyramine.n_targets`) | **114** | 114 | E13 (snippet level; returned for the PLOS, PMC, ResearchGate and arXiv copies) | **YES** |
| Monoamine edges, dopamine | per-ligand pairs excl self | **1,168** (incl self 1,176; rows 1,752; 8 senders × 147 receivers) | no like-for-like total found. E7(a): 1,392 (garbled reconstruction attributed to the arXiv table). E7(b) 1,339 and E12 1,133 are subsets (non-synaptic edges), not totals | E7, E12. Arithmetic: E1's 1,940 equals 1,168 + 490 + 54 + 228 (this file's per-monoamine values), and E12's percentages fit 147 receivers and 1,168 edges (single excerpt). If PLOS Table 2's main (non-parenthetical) dopamine value is not 1,168, this becomes NO — BLOCKER (flag B2) | **UNVERIFIED** |
| Monoamine edges, serotonin | same | **490** (incl self 492; rows 540; 6 senders × 82 receivers) | 490 | E7(a) only, a garbled search-tool reconstruction attributed to the arXiv table | **UNVERIFIED** |
| Monoamine edges, octopamine | same | **54** (incl self 56; rows 72; 2 senders × 28 receivers) | 54 | E7(a), E7(b) (arXiv tables; same caveat) | **UNVERIFIED** |
| Monoamine edges, tyramine | same | **228** (incl self 228; rows 262; 2 senders × 114 receivers) | 228 | E7(a) (arXiv table; same caveat). Consistent with E13 by arithmetic: 2 senders × 114 receivers, no self-pairs | **UNVERIFIED** |
| Monoamine self-pairs | distinct neurons with a self-row | **12** (dopamine 8 [all 8 DA neurons, via dop-2]; octopamine 2 [RICL/R, via ser-6]; serotonin 2 [NSML/R, via ser-4]) | not found | — (closest: E1 and E3 match only with self-pairs excluded) | **UNVERIFIED** |
| Neuropeptide connections (aggregate) | distinct ordered pairs excl self, all peptides | **7,035** (incl self 7,078; rows 8,931; sum of per-peptide pairs excl self 7,991) | 7035 (PLOS); 7046 (arXiv) | E3 (PLOS text, snippet level). The arXiv figure (E4) is the preprint version and is not matched | **YES** |
| Neuropeptide neurons | distinct names in field 1 ∪ field 2 | **239** (senders 141; receivers 187; both 89) | 239 | E3, E4 | **YES** |
| Neuropeptide receptors | distinct field-4 genes | **12** (ckr-2, egl-6, frpr-4, npr-1, npr-2, npr-3, npr-4, npr-5, npr-11, npr-17, ntr-1, pdfr-1) | 12 | E8 | **YES** |
| Neuropeptides | distinct field-3 genes | **15** (flp-1, -4, -5, -10, -13, -15, -17, -18, -21; nlp-1, -12, -24; ntc-1; pdf-1, pdf-2) | not found in paper text | — (closest: E11, the toolbox's summary "15 neuropeptides and 12 receptors were matched and included"; a search on 2026-11-18 found no paper sentence with 15) | **UNVERIFIED** |
| Neuropeptide self-pairs | distinct neurons with a self-row | **43** (62 self-rows) | not found | — | **UNVERIFIED** |
| Neuropeptide edges per peptide→receptor | rows (= pairs; no duplicates within a block) | flp-1→npr-11 60; flp-1→npr-4 135; flp-10→egl-6 75; flp-13→frpr-4 152; flp-15→npr-3 200; flp-17→egl-6 15; flp-18→npr-1 660; flp-18→npr-11 48; flp-18→npr-4 108; flp-18→npr-5 360; flp-21→npr-1 1,705; flp-21→npr-11 124; flp-21→npr-2 589; flp-21→npr-5 930; flp-4→npr-4 162; flp-5→npr-11 36; nlp-1→npr-11 40; nlp-12→ckr-2 52; nlp-24→npr-17 16; ntc-1→ntr-1 780; pdf-1→pdfr-1 1,804; pdf-2→pdfr-1 880 | not found | — | **UNVERIFIED** |
| Monoamine edges per transmitter→receptor | rows (= pairs) | DA: dop-1 576, dop-2 160, dop-3 664, dop-4 80, lgc-53 272; OA: octr-1 24, ser-3 24, ser-6 24; 5-HT: mod-1 216, ser-1 132, ser-4 78, ser-5 36, ser-7 78; TA: lgc-55 54, ser-2 118, tyra-2 36, tyra-3 54 | not found | — | **UNVERIFIED** |

Cross-check against the toolbox's own expected counts (T; not paper
figures, so not in the table): the toolbox's `Bentley2016*Reader` totals
equal this file's per-ligand pairs **including** self-pairs (DA 1,176; TA
228; OA 56; 5-HT 492; NP 7,078). Its `WormNeuroAtlasMAReader` totals (DA
1,160; TA 224) are explained by Randi's loader bug (flag B4).

E13's "only 7 are postsynaptic to a tyraminergic neuron" and "presynaptic to
a total of 20 neurons" need the synaptic layer, which this source does not
hold; they are not compared here.

Density, for the Q-009 context only. This is arithmetic, not a paper
comparison; n = 302 is the paper's neuron total (E3), so the denominator is
302·301 = 90,902:

- Bentley monoamine: 1,940 / 90,902 = 0.021342 (incl self: 1,952 / 90,902
  = 0.021474).
- Ripoll-Sánchez et al. 2023 report a monoamine density of 0.0236
  (`docs/provenance/ripollsanchez2023.md`, E3 there). Neither Bentley value
  equals it, nor does the 08062023 monoamine file (0.0315, per that doc).

## Discrepancies, flags and open questions

- **B1. The paper versions differ, and the files match the PLOS version.**
  - The PLOS text gives 1,940 monoamine and 7,035 neuropeptide connections,
    and 251 receptor-expressing neurons.
  - The arXiv preprint gives 2,036, 7,046 and 248.
  - The acquired edge lists reproduce both PLOS connection totals exactly,
    with self-pairs excluded, and neither arXiv total. Neither version's
    receptor-expressing count is reproduced (B3).
  - Any "reproduce the paper" test should cite the PLOS version.
- **B2. Table 2 per-monoamine counts are UNVERIFIED.**
  - The only total-level dopamine figure found, 1,392, is a garbled
    reconstruction attributed to the arXiv table (E7(a)), with aggregate
    2,164. The file gives 1,168 and 1,940.
  - 2,164 − 1,940 = 224 = 8 dopamine senders × 28. The arXiv companion
    table (E7(b)) fits a dopamine total of 175 receptor nodes = 147 + 28
    and 1,392 edges = 1,168 + 224. So the arXiv tables appear to carry 28
    more dopamine receivers than this file. That is an inference from
    percentages, not verified.
  - 1,339 (E7(b)) is not a candidate total: it counts only the non-synaptic
    dopamine edges.
  - The PLOS companion table (E12, one excerpt) fits 147 dopamine receivers
    and 1,168 dopamine edges, i.e. this file. Its parenthetical values fit
    about 187 receivers in the expanded dop-5/dop-6 network (E6).
  - The other three monoamines (490 / 54 / 228) equal the file's values in
    E7(a).
  - Needs the PLOS Table 2 (primary check 3). If its main dopamine value is
    not 1,168, the dopamine row becomes NO — BLOCKER.
- **B3. BLOCKER. Receptor-expressing neurons: 251 (PLOS) / 248 (arXiv) vs
  235 receivers in the file.**
  - Like for like: the file's receivers are exactly the neurons that
    express a receptor in the network's receptor set, and for tyramine the
    paper's "neurons that express reporters for one or more of the four
    tyramine (TA) receptors" (114, E13) equals the file's tyramine receivers
    (114). The PLOS dopamine percentage (E12, one excerpt) also fits the
    file's 147 receivers. So, where it can be checked, the paper's "neurons
    expressing X receptors" are the network's receivers, and the aggregate
    235 is the comparable count.
  - 235 ≠ 251. The gap is 16 neurons (13 against the arXiv 248).
  - Unverified hypothesis, not a resolution: 251 may count expression of
    receptors outside the main network, such as dop-5/dop-6 (the expanded
    network has about 40 more dopamine receivers, 187 − 147, by E12
    arithmetic). Only the primary (expression tables / S1 Dataset / Table
    2) can settle it.
  - The paper figure itself is known only at paraphrase level (E5).
  - Phase 3 should carry this as an `xfail(strict=True)` "BLOCKER" test.
- **B4. Randi's loaders silently mis-assign names missing from their id
  lists. This matters for anyone reusing Randi's extrasynaptic matrices.**
  - Both loaders (wormneuroatlas 0.0.7.3 `NeuroAtlas._get_esconnectome_bentley`
    with `ids_to_ai`, and pumpprobe @ `1dbc5e0a`
    `Funatlas._get_esconnectome_bentley` with `ids_to_i`; the same code)
    skip the first line, look up each name, and write `esc[ai_to, ai_from]`.
    The lookup returns −1 for a name not in the atlas's id list, and the
    loader indexes with −1 without checking. So the row lands on the last
    neuron of the sorted id list (`np.unique`), which is **VD9** for both id
    lists under default settings (all merge flags False).
  - A scratch re-implementation (2026-11-18; the packages were not executed)
    gives:
    - wormneuroatlas (wheel files, `neuron_ids.txt`; the AWCOFF→AWCL mapping
      in `approximate_ids` is commented out in 0.0.7.3, so AWCL/AWCR and
      CANL/CANR are unresolved): monoamine 1,928 nonzero entries instead of
      1,952 distinct pairs incl self; the 24 pairs involving
      AWCL/AWCR/CANL/CANR collapse onto existing VD9 entries. With the
      transmitter filter: dopamine **1,160**, octopamine 56, serotonin 492,
      tyramine **220**. Neuropeptide: 7,062 nonzero = 7,052 resolvable
      pairs + **10 spurious entries** that make VD9 a sender (flp-4 / nlp-1,
      via the AWCL/AWCR rows) to AIAL, AIAR, AIYL, AIYR, AVAL, AVAR, BAGL,
      BAGR, RIVL, RIVR.
    - pumpprobe (pumpprobe files, `aconnectome_ids.txt`, which has AWCL/AWCR,
      so only CANL/CANR are unresolved): monoamine 1,932 nonzero (the 20
      pairs involving CANL/CANR collapse onto existing VD9 entries); dopamine
      1,160, octopamine 56, serotonin 492, tyramine 224. Neuropeptide: 7,078
      nonzero, all pairs incl self, none spurious.
    - The toolbox's `WormNeuroAtlasMAReader` (T: dopamine 1,160, tyramine
      224): its `get_all_cells` renames AWCOFF→AWCL and AWCON→AWCR in place
      in the atlas's `neuron_ids` before reading, so AWC resolves and only
      CANL/CANR fall on VD9. Re-implementing that gives dopamine 1,160 and
      tyramine 224, matching T.
  - A second loader bug: `if recept[-1] == "\n": recept = recept[-1]` sets
    the receptor to "\n" on every row whose 4th field ends the line: all
    2,626 monoamine rows (both distributions) and all 8,931 rows of
    pumpprobe's 4-field neuropeptide file; none of the wheel's 5-field
    neuropeptide rows. It only matters when filtering by receptor.
  - The edge table must be built from these raw files, not from the
    packages' matrices.
- **B5. The wheel neuropeptide 5th field is not Bentley data.** It is sparse
  and inconsistent (843 / 8,931 rows filled) and was added by the package
  author; the pumpprobe copy that Randi et al.'s analysis code loads does
  not have it. It should be ignored, or explicitly attributed if used.
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
  - 116 monoamine pairs are supported by 3 receptors and 442 by 2
    (`rows_per_ordered_pair_histogram`).
  - 943 neuropeptide pairs are supported by more than one peptide.
  - The data allow (a) a binary any-ligand edge, (b) per-monoamine or
    per-peptide edges, or (c) per ligand→receptor edges. Which to carry is
    an owner decision.
- **B8. Whole-animal lists, not head subsets.**
  - Names follow the WormAtlas/White style without zero-padding (VA1, not
    VA01).
  - AWCL/AWCR versus the atlas's AWCON/AWCOFF (Q-005).
  - CANL/CANR have no counterpart in either of Randi's id lists.
  - Phase 2 must map these explicitly; nothing is normalised here.
- **B9. Toolbox documentation pages.**
  - `docs/Bentley_2016.md` links `Bentley2016_MA_data_graph.md` and
    `Bentley2016_PEP_data_graph.md`. These files do not exist in `docs/` at
    the pinned commit; they appear to be generated for the website (web
    search finds openworm.org/ConnectomeToolbox/Bentley2016_MA_data_graph/
    and openworm.org/ConnectomeToolbox/Full1_Bentley2016_MA_data).
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
    edges (per that doc).

  How many ordered pairs they share depends on name normalisation. This is
  a cross-source scratch figure, not a record count of either source
  (`record_counts` reads only its own source's directory). It was computed
  on 2026-11-18 from `data/raw/bentley2016/edgelist_MA.csv` (non-self pairs)
  and the nonzero off-diagonal cells of
  `data/raw/ripollsanchez2023/08062023_monoamine_connectome.csv` (rows =
  senders, per P1-RS3 there):
  - names as raw strings: **792** shared ordered pairs in the same
    orientation, 108 transposed;
  - after un-padding Ripoll-Sánchez's ventral-cord names (one leading zero
    of a two-digit suffix removed: VA01→VA1, DB02→DB2, …; 60 of the names
    in that file's nonzero cells change): **1,256** in the same orientation,
    still 108 transposed. The 1,256 in the ripollsanchez2023 doc is this
    un-padded figure.

  No name mapping is applied to either source's data; which mapping Phase 2
  uses is Q-005. Neither file reproduces the 0.0236 monoamine density in
  Ripoll-Sánchez et al. Or should both be carried as separate columns?
- **Q-B2. Which copy is the pipeline input?** The edges are identical in
  all three. The toolbox copy is the claimed S1 extraction, with no added
  line or field. The wheel copy is what Randi's package loads, with a header
  and Randi's 5th field. The pumpprobe copy is what Randi et al.'s analysis
  code loads, with a header and no 5th field. Recommendation for the
  owner's consideration: read edges from the toolbox copy and keep the other
  two as cross-checks. This is the owner's call.
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
- leiferlab/pumpprobe @ `1dbc5e0a`
  `build/lib.linux-x86_64-3.8/pumpprobe/esconnectome_monoamines_Bentley_2016.csv`
  (blob `eaa17360…`) and
  `build/lib.linux-x86_64-3.8/pumpprobe/esconnectome_neuropeptides_Bentley_2016.csv`
  (blob `190868bd…`): build-directory duplicates, byte-identical (same git
  blobs) to the two acquired `pumpprobe__` files.
- francescorandi/wormneuroatlas copies: the 4-field neuropeptide file (blob
  `190868bd…`, commits `3eed4b8` and `5ebe7f4`) is byte-identical to the
  acquired `pumpprobe__esconnectome_neuropeptides_Bentley_2016.csv`; the
  monoamine file (blob `eaa17360…`, every commit) and the later neuropeptide
  file (blob `fce8a0a1…`, `7a7c653` to HEAD `b2e13d88`) are byte-identical
  to the two wheel members. Their history is documented above.
- Toolbox reader caches `cect/cache/Bentley2016MAReader.json` (blob
  `9fad3d03`) and `cect/cache/Bentley2016PepReader.json` (blob `9ed37af3`):
  derived outputs of the toolbox's readers, not source data. The pinned
  commit has no cache file for `WormNeuroAtlasMAReader` or
  `WormNeuroAtlasPepReader`.
- Toolbox evidence files, read at the pinned commit and quoted above but not
  data: `cect/validation/BentleyEtAl2016.md` (blob `73187343`),
  `cect/validation/Bentley2016MAReader_expected_data.yaml` (blob
  `1dff625f`), `cect/validation/Bentley2016PepReader_expected_data.yaml`
  (blob `159f7a7d`), `cect/validation/WormNeuroAtlasMAReader_expected_data.yaml`
  (blob `f75b1c67`), `docs/Bentley_2016.md` (blob `8c25f8d6`).
- University of Kiel open-data "Multi-layer connection of C. elegans"
  (fdr_mods_00000079): a third-party compilation (WormAtlas + Bentley et al.)
  for a 2021 locomotory-circuit study. Derived, and its host is blocked.
