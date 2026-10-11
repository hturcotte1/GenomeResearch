# Phase 0: prior work on per-edge channel attribution in the Randi et al. 2023 atlas

- Date: 2026-10-11
- Scope: the anatomy-vs-function comparison in Randi et al. 2023, what it left open,
  and whether any later work has closed it.
- No pipeline code has been written. The numbers marked **[verified]** came from
  one-off inspection of the authors' own data release. That inspection was done in
  a scratch directory and is described in section 1.2 so it can be repeated. It
  will be formalised as Phase 3 tests.

---

## 0. Read this first: how this was researched, and what that limits

**Network.** This session's container sits behind an egress policy that blocks
almost every academic host. Blocked (HTTP 403 at the proxy): arxiv.org,
www.nature.com, www.ncbi.nlm.nih.gov / PMC, europepmc.org, www.ebi.ac.uk,
api.openalex.org, api.semanticscholar.org, api.crossref.org, www.biorxiv.org,
doi.org, osf.io, zenodo.org, figshare.com, funconn.princeton.edu, nemanode.org,
openworm.org, wormatlas.org, cengen.org, journals.plos.org, www.cell.com. The
page-fetch tool fails on the same hosts. Two things worked: GitHub (clone and
read) and PyPI (download). A server-side web search tool also worked, but it
returns only excerpts and summaries, not full documents.

Consequences, stated plainly:

1. **I did not read Randi et al. 2023 or its Supplementary Information in full.**
   I could not reach the Nature, PMC or arXiv full text. In its place I used three
   sources:
   - (a) excerpts of the Nature, PMC and arXiv text returned by web search;
   - (b) the authors' own analysis code, `leiferlab/pumpprobe` at commit
     `1dbc5e0a2b609d54bc9b1c90c73d4e3bf183d3c7` (2023-09-20). Its
     `scripts/fconnectivity/figures/paper/` folder lists the exact command behind
     each main and supplementary figure;
   - (c) the authors' own data release, `wormneuroatlas` 0.0.7.3 on PyPI. That
     package was written by Randi and bundles the atlas as `funatlas.h5`. I checked
     that this file reproduces the paper's headline counts exactly (section 1.2).

   For *what the analyses were*, (b) and (c) are arguably stronger evidence than
   the prose. For *what the authors claim and how they hedge it*, I am relying on
   excerpts. If anything in the Supplementary Information contradicts this
   document, the Supplementary Information wins.
2. **The citation sweep was search-based, not exhaustive.** A proper sweep lists
   every work citing DOI 10.1038/s41586-023-06683-4 from a citation index (OpenAlex,
   Semantic Scholar, Crossref, Europe PMC) and screens each one. All of those
   indexes are blocked. Instead I ran about 30 targeted searches built around the
   concepts that per-edge attribution work would have to use: unc-31, extrasynaptic,
   wireless, neuropeptide connectome, polarity or sign, multi-hop, effectome,
   residual or unexplained, reanalysis. I also followed the Leifer lab's own
   follow-ups. A paper that does per-edge attribution under unusual vocabulary
   could have been missed.
3. Several papers below are characterised from abstracts or excerpts only. That
   is flagged per entry.

Section 5 lists the hosts that would need allowlisting to close these gaps.

---

## 1. What Randi et al. 2023 actually did on anatomy vs function

Randi F, Sharma AK, Dvali S, Leifer AM. *Neural signal propagation atlas of
Caenorhabditis elegans.* Nature 623:406–414 (2023). doi:10.1038/s41586-023-06683-4.
The preprint is arXiv:2208.04790; its v1 title was *A functional connectivity atlas
of C. elegans measured by neural activation*.

### 1.1 The measurement

- Single neurons were activated optogenetically while calcium was imaged across
  the whole brain. Neurons were identified with NeuroPAL; the figure-1 command
  paths in the authors' repository reference a NeuroPAL strain.
- Each stimulated → responding pair gets:
  - a mean ΔF/F over a response window (`dFF`);
  - per-trial values (`dFF_all`);
  - a fitted response kernel (sum of exponential convolutions, giving rise and
    decay times);
  - an observation count (`occ1`);
  - a **q-value for "functionally connected"** (`q`);
  - a **q-value from an equivalence test (TOST) for "functionally not connected"**
    (`q_eq`).

  These fields are stored per strain (WT and unc-31) in `funatlas.h5`.
- The **head** set has 188 neurons. That includes 20 pharyngeal neurons (I1L/R,
  I2L/R, I3–I6, M1, M2L/R, M3L/R, M4, M5, MCL/R, MI, NSML/R) and the
  retrovesicular ganglion. **AWC is identified as AWCON / AWCOF, not
  AWCL / AWCR.**

### 1.2 Headline numbers, checked against the authors' data release

Source file: `wormneuroatlas-0.0.7.3-py3-none-any.whl`. Wheel SHA-256:
`166289031784c9565f6b9205e30dc718bafbc092db3b46f1aef73d93dc4d1325`. Inside it is
`wormneuroatlas/data/funatlas.h5`, SHA-256
`53a99055667b853e1d3d6be573ec2613d38c9f6989f302ec38ecd38dd50c7975`, with
internal attribute `time_compiled = 2023-06-28_19-52-14`.

The counting rule comes from the authors' `Numbers_script.py`: restrict to the
188 head neurons and count the finite q-values.

| Quantity | Paper (Nature) | `funatlas.h5` | Match |
|---|---|---|---|
| Measured head pairs, WT | 23,433 | 23,433 | **[verified] exact** |
| WT pairs at q < 0.05 | 1,310 ("6%") | 1,310 | **[verified] exact** |
| Inhibitory share of q < 0.05 | 11% | not checked | — |

Details the headline numbers hide. All of these are **[verified]** from the file:

- **The 23,433 includes 168 self-pairs** (i → i, the stimulated neuron's own
  response). **Off-diagonal ordered pairs: 23,265.** Likewise, 159 of the 1,310
  q < 0.05 entries are self-pairs, so **off-diagonal WT functional connections
  number 1,151.**
- **The brief's figure of 23,427 does not match the Nature paper.** Search
  excerpts attribute "23,427" to an arXiv abstract version. I could not open that
  page to confirm it. The Nature figure, 23,433, is the one the released data
  reproduces.
- **unc-31 coverage is much smaller.** There are 9,228 head pairs with finite q
  (109 of them self-pairs), and 430 at q < 0.05. **Only 8,150 off-diagonal head
  pairs were measured in both strains.**
- **Of the 1,151 off-diagonal WT connections, 617 (54%) have no unc-31
  measurement at all.**
- Among WT-measured off-diagonal pairs there are three evidence states:
  - 1,151 connected (q < 0.05);
  - 13,332 with a confident non-connection (q_eq < 0.05);
  - 9,109 inconclusive (q ≥ 0.05 and q_eq ≥ 0.05).

  The file also stores `q_eq_th = 1.2` for both strains. I have not confirmed from
  the Methods what that equivalence margin means.

### 1.3 The anatomy-vs-function analyses

Each item below is mapped to the script that produced it.

1. **Connection probability vs anatomical hop depth.** Fig. 2
   (`Anatomical_hop_depth.py`, plus a TOST variant). Directly wired pairs are more
   likely to be functionally connected, and the probability falls with hop count.
   Bilateral-pair statistics come from `LRStatistics.py`.
2. **Measured responses vs an anatomy-derived biophysical simulation.** Fig. 3
   (`funatlas_vs_anatomy.py`). Responses were simulated on the connectome with a
   Kunert-style model, with synapse signs from expression data
   (`activity_connectome_sign2`). The code references the Fenyves et al. 2020 S3
   table as a sign source; I have not confirmed which sign table this figure used.
   The comparison is reported as correlation and R² over all pairs. A second
   version **fits weights and signs while forbidding connections absent from the
   wiring diagram**. Per the excerpt, this "improved the agreement … although
   overall agreement remained poor."
3. **RID case study.** Fig. 4: a neuron with few wired outputs but broad
   functional effects, compared between WT and mutants.
4. **WT vs unc-31.** Fig. 5 and Extended Data
   (`wt_unc31_differences.py`).
   - unc-31 animals have a lower fraction of q < 0.05 among pairs measured in
     both strains.
   - The authors define **"candidate purely extrasynaptic" connections**: WT
     q < 0.05 AND unc-31 q_eq < 0.05 AND unc-31 q > 0.05. That gives **55
     entries, 53 off-diagonal plus 2 self-pairs [verified]**. The same 55 values
     appear in `anatomical_data/leifer_extrasynaptic_pairs.csv` in the Creamer et
     al. repository.
   - They then checked how many of these 55 sit on a 1-hop anatomical edge,
     compared their anatomy-derived simulated responses and rise times with all
     WT connections (one-sided KS tests), and measured enrichment for pharyngeal
     neurons.
   - They also define **"new in unc-31"** pairs: confidently absent in WT,
     present in unc-31. There are **136 off-diagonal [verified]**.
   - For candidate extrasynaptic pairs they listed **candidate neuropeptide–GPCR
     pairs**, using the Beets et al. deorphanization screen plus CeNGEN
     expression. Examples: M3L → URYVL; AVDR → AVDL, which they suggest runs
     through autocrine loops NLP-10 → NPR-35 and FLP-6 → FRPR-8.
5. **Spontaneous activity.** Fig. 6: the measured atlas predicts correlations in
   spontaneous activity better than the anatomy-derived model does.
6. **Monoamine layer.** The authors' toolkit loads the Bentley et al. 2016
   extrasynaptic connectome. I found no per-pair monoamine attribution in the
   figure scripts.

---

## 2. What they left unresolved

Every anatomy-vs-function result in the paper is one of two kinds:

- **distributional**: KS tests, R², connection probability by hop count;
- **a single strict list**: the 55 candidate purely extrasynaptic entries.

As far as I can establish from the code and excerpts, the following was **not**
done.

1. **No complete per-pair partition.** No published table assigns each measured
   pair to a mutually exclusive channel: wired-concordant, wired-discordant,
   DCV-dependent, polysynaptic, or unexplained.
2. **No per-edge sign concordance.** I found no table comparing each wired pair's
   measured sign with an expression-based predicted polarity (Fenyves-style).
   Signs enter only through the biophysical simulation, which is scored in
   aggregate.
3. **Multi-hop handled only in aggregate.** Hop-depth curves and the
   simulation's R² do not label a specific non-wired pair as "explained by a
   signed polysynaptic path."
4. **The extrasynaptic call covers only part of the atlas.** It needs *confident
   absence* in unc-31. 617 of the 1,151 WT connections were never measured in
   unc-31, so their DCV-dependence is undetermined, not negative. Among the 534
   that were measured in both, most fall between "lost" and "retained" as
   inconclusive.
5. **No residual set.** Nobody has published the set of WT connections that have
   no direct synapse, are not DCV-dependent, and are not reachable by a
   sign-consistent polysynaptic path.
6. **Peptides vs monoamines.** The authors describe unc-31 as disrupting DCV
   release of both peptides and monoamines. A loss in unc-31 therefore does not
   separate the two.

---

## 3. Has anyone closed it since? (citation sweep)

| Work | What it does | Closes the gap? | How I read it |
|---|---|---|---|
| **Creamer, Leifer & Pillow**, *Bridging the gap between the connectome and whole-brain activity in C. elegans*. bioRxiv 10.1101/2024.09.22.614271 (v1 2024, PMC12485687, later versions 2025–26). Code: `Nondairy-Creamer/Creamer_LDS_2026` @ `bba43302` | Fits a latent linear dynamical system to Randi's WT stimulation data. Weights are allowed **only on anatomical edges** (9.4% of pairs). Reported to capture causal interactions at **92% (v1) / 82% (later PDF)** of the data's own reproducibility. Interactions between unconnected neurons are explained by **multi-hop propagation**, and multi-hop is common even for directly wired pairs. Adding non-anatomical weights did not help. A shuffled connectome does much worse. | **No.** This is an aggregate model-level claim. There is no per-edge categorical attribution and no residual list. The repo releases model weights, not per-pair labels. I found no unc-31 analysis; the unc-31 loader is commented out in `create_data_set.py`. | Abstract, excerpts, and the code repo. Full text not read. |
| **Dvali, Seguin, Betzel & Leifer**, *Diverging network architecture of the C. elegans connectome and signaling network*. PRX Life 3:033021 (2025); arXiv 2412.14498 | Network-level comparison: modules, rich club, clustering. Signalling modules do not align with anatomical modules, and rich-club membership differs. Uses the 188 head neurons. | **No.** Topology, not edge attribution. | Abstract and excerpts. |
| Leifer, APS March Meeting 2026, *How a neural network's signaling relates to its structure* | Talk on the same line of work. | No. | Abstract. |
| **Simeon, Kashyap, Kording & Boyden**, *Homogenized C. elegans Neural Activity and Connectivity Data*. arXiv 2411.12091 | A harmonised data layer covering 12 imaging datasets and connectome annotations, including one signal-propagation study. Built for GNN modelling. | **No.** Data plumbing with no attribution. It is relevant to Phases 1–2 as a cross-check on naming and harmonisation choices. | Abstract and excerpts. |
| **Sunil, Benali & Moutuou**, *Thermodynamic connectivity reveals functional specialization and multiplex organization of extrasynaptic signaling*. arXiv 2604.02057 (Apr 2026) | Infers functional connectivity *from synaptic wiring* with an equilibrium (KMS) model and compares it with the neuropeptide connectome, giving four "communication regimes." | **No**, as far as I can tell. The functional layer is model-derived, and I found no evidence it uses Randi's measurements. **Unverified**: full text not accessible. | Abstract and reference-list excerpts. |
| **Szilágyi, …, Csermely & Fenyves**, *Signed motif analysis of the C. elegans neuronal network*. BMC Biology 24:167 (2026); bioRxiv 2025.01.09.632090 | Motif analysis on predicted polarity. Relabels "complex" synapses as excitatory, inhibitory or unknown from the anion- vs cation-gated receptor ratio. | No. It is structural only. **But it is a newer polarity source than Fenyves 2020**; see flag F10. | Abstract and excerpts. |
| Ripoll-Sánchez et al., Neuron 111:3570 (2023); Venkatesh, Ripoll-Sánchez, Beets et al., J Biosci (2025) review; Genetics 228:iyae141 (2024) review; Beets & Watteyne, Curr Opin Neurobiol (2025) review | Structural neuropeptide connectome and reviews of the wired plus wireless connectome. | **No.** I found no per-edge reconciliation with Randi's measurements. Not checked in full text. | Abstracts and excerpts. |
| Dyballa et al., ICLR 2024; dLDS, Commun Biol (2025); Beiran & Litwin-Kumar, Nat Neurosci (2025) | Dynamic functional connectomes from spontaneous activity, or connectome-constrained theory (Drosophila examples). | No. | Abstracts. |
| Wang et al., eLife 2024 (*A neurotransmitter atlas of C. elegans males and hermaphrodites*) | Updated transmitter identities. | No. It is a candidate **input** for predicted sign; see flag F10. | Known only through the ConnectomeToolbox file list (`elife-95402-supp*.xlsx`). I matched eLife 95402 to Wang et al. from memory; not verified. |

**Summary.** The closest prior work is the Leifer lab itself.

- Randi et al. 2023 published a strict DCV-dependent subset, which is essentially
  a high-confidence slice of category C.
- Creamer et al. showed in aggregate that the wired connectome plus multi-hop
  propagation accounts for most measured causal structure, which bears on
  category D.

I found nobody who has assigned every measured pair to a channel or published an
unexplained-residual edge set.

---

## 4. Verdict

**VERDICT: PROCEED.** This is provisional, with moderate confidence. It rests on
a search-based sweep and on code- and data-level reading of Randi et al., not a
full-text read.

Reasoning:

- The specific deliverable does not exist in anything I could find. That
  deliverable is an exhaustive, coverage-aware per-edge partition into A–E, with
  per-edge sign concordance and an evidence-graded residual set E.
- The authors' own outputs stop at distributional statistics, one strict list
  (C-like), and an aggregate model (D-like).

The novelty is narrower than the brief implies. Two pieces exist in part:

- **Category C (strict)** exists: Randi's 55 candidate purely extrasynaptic
  entries. Our C should either reproduce it exactly as a sanity anchor, or differ
  from it in a documented way.
- **Category D** has been addressed in aggregate by Creamer et al., whose result
  argues that multi-hop explains most of the atlas. That is a **risk to the
  deliverable, not a reason to stop**. Under a permissive definition of D, E
  shrinks towards zero by construction. If E is small under a strict, pre-frozen
  D, that is itself a publishable finding. If E is not small, it contradicts the
  aggregate model at specific edges, which is more interesting still.

What would flip this to ALREADY DONE:

- a paper or dataset assigning every Randi pair to a channel, or publishing an
  unexplained-residual edge set;
- the Randi Supplementary Information containing such a per-pair table, which I
  could not read;
- a later Creamer et al. version publishing per-pair residuals from the
  connectome-constrained model.

An index-based citation sweep (section 5) is the cheap way to rule these out.

---

## 5. Flags: things that look off, or need your decision before Phase 1

These are not answered here; they are yours to decide. The open questions are
also logged in `docs/decisions.md`.

- **F1. Target pair count.** The brief says 23,427. The Nature paper and the
  released data say **23,433**, and that figure includes **168 self-pairs**.
  Which number should the Phase 3 test assert, and are self-pairs in scope for
  the edge table? I suggest asserting 23,433 as the reproduction test, then
  excluding self-pairs from the edge table with an explicit exclusion-log entry.
  That is your call.
- **F2. Rule 2 needs three states, not two.** Randi's release separates:
  - "connected" (q < 0.05);
  - "confidently not connected" (q_eq < 0.05);
  - "inconclusive";
  - "never tested."

  A flag that only distinguishes tested from untested would hide the 9,109
  inconclusive WT pairs, whose measured null is not evidence of absence. The same
  applies per strain for unc-31. How should the edge table encode this? I
  recommend a per-strain categorical column rather than a boolean.
- **F3. unc-31 coverage caps categories C and E.** Only 8,150 off-diagonal pairs
  have both strains. 617 of 1,151 WT connections can never be called C or ruled
  out of C. Under the current A–E definitions, those 617 would fall into D or E
  by default, or need an "undetermined for DCV" status. This is a rubric decision
  for the later classification pass, but the data layer must preserve the
  distinction. It will.
- **F4. unc-31 is not a clean subtraction.**
  - 136 off-diagonal pairs are confidently absent in WT but present in unc-31,
    compared with 53 that go the other way under the authors' strict rule.
  - Part of that asymmetry is likely statistical power. WT has more trials, so
    confident absence is easier to establish in WT. I have not quantified this
    and am not drawing a biological conclusion.
  - Even so, "lost in unc-31" should not be read as pure peptidergic attribution.
  - unc-31 also affects monoamine DCV release (per the authors), so C means
    "DCV-dependent," not "peptidergic."
- **F5. The definition of category D decides the size of E.** The head network
  is small-world, and a few hops reach most neurons, so "explained by propagation
  through the signed network" needs:
  - a hop limit;
  - a sign-composition rule;
  - gap-junction handling;
  - possibly a timing constraint, since Randi's kernels give rise times.

  All of this should be frozen before anyone looks at E. Creamer et al. suggest
  multi-hop is common **even for directly wired pairs**. So a wired pair whose
  measured sign contradicts the direct synapse (category B) may in fact be
  polysynaptic, and A–E are not as cleanly mutually exclusive as stated. Flagged
  for the rubric, not for this repo.
- **F6. Measured sign is biased.** Responses are GCaMP calcium transients. Randi
  report 11% inhibitory, against roughly 20% from earlier estimates; Fenyves'
  predicted E:I is about 4:1. Inhibition may be under-detected in calcium
  imaging, which would push true inhibitory wired edges towards "no response" or
  "sign wrong." Worth knowing before trusting A vs B.
- **F7. AWC.** Randi uses AWCON/AWCOF, while the anatomical connectomes use
  AWCL/AWCR. The ON/OFF ↔ L/R mapping is stochastic per animal. This needs your
  call in Phase 2: map to AWCL/AWCR, keep ON/OFF, or collapse to AWC.
- **F8. Bilateral collapse is a statistics problem, not just a naming problem.**
  The authors' own loader prints a warning when merging bilateral neurons: "q
  values have been merged and AVERAGED. This is not mathematically accurate…
  Do not use q values like this." Any collapse policy must recompute statistics
  from trial-level data (`dFF_all`) or carry q-values only at split resolution.
  This constrains the Phase 2 options I will present.
- **F9. "White 1986" is not one dataset.** The distributed versions include
  `white_1986_whole`, `white_1986_A`, `white_1986_L4`, and the NemaNode-format
  `white_1986_jsh` / `white_1986_n2u`, the latter re-annotated in Cook et al.
  2019 and Witvliet et al. 2021. Randi combined White A, White L4, Witvliet 7 and
  Witvliet 8. Creamer used jsh, n2u, Witvliet 7 and Witvliet 8 from NemaNode.
  Which White should `anat_chem_white` mean?
- **F10. Newer polarity and transmitter sources exist.**
  - Fenyves 2020 (the brief's source);
  - its 2026 refinement (Szilágyi et al., BMC Biol), which resolves "complex"
    synapses;
  - Wang et al. 2024 eLife transmitter atlas;
  - and CeNGEN thresholds 1–4 change any expression-based call.

  Which defines `predicted_sign`? I recommend Fenyves 2020 as primary (it is the
  reproduction target), with the others as separate columns.
- **F11. The Ripoll-Sánchez files circulating may be post-publication versions.**
  The ConnectomeToolbox repository carries
  `01022024_neuropeptide_connectome_{short,mid,long}_range_model.csv`. The date
  prefix suggests February 2024 (or January 2, 2024), after the Neuron
  publication. I would verify against the Neuron supplementary before trusting
  record counts.
- **F12. "Head" includes the retrovesicular ganglion and the pharynx.** That
  brings in some ventral-cord-type names (DA/DB/VA/VB/DD/VD with numbers) and 20
  pharyngeal neurons. The zero-padding and pharynx-inclusion issues in the Phase 2
  brief apply to the head set, not only to whole-animal data.
- **F13. Monoamine source.** The brief names Bentley 2016. The ConnectomeToolbox
  also carries `08062023_monoamine_connectome.csv`, apparently an updated monoamine
  layer from the Ripoll-Sánchez/Schafer group; not verified. Which one is
  `monoamine_edge`?

### Data access for Phase 1

**Reachable now (secondary, author- or community-distributed):**

- the `wormneuroatlas` wheel on PyPI, which bundles:
  - `funatlas.h5` (WT and unc-31);
  - White and Witvliet CSVs;
  - Bentley 2016 monoamine and neuropeptide CSVs;
  - the Fenyves 2020 S3 xlsx;
  - CeNGEN 021821 at four thresholds;
  - the Beets deorphanization table;
- the `openworm/ConnectomeToolbox` GitHub repository, which carries:
  - the three Ripoll-Sánchez range models;
  - Cook 2019 SI5;
  - Witvliet 2021 per-dataset xlsx;
  - Wang 2024 eLife supplements;
  - and more.

Rule 5 asks for the primary URL and a matching record count. Using these
secondary copies therefore needs your explicit approval, and ideally a one-time
hash comparison against the primary.

**Blocked: needed for primary-source provenance.** Add these under the
environment's network settings (Allowed domains), or download them manually:

- funconn.princeton.edu
- osf.io and files.osf.io (Randi raw data at osf.io/qxhjd, per the Creamer README)
- www.nature.com and static-content.springer.com (Nature supplementary files)
- nemanode.org
- journals.plos.org (Fenyves 2020 and Bentley 2016 supplementary)
- elegansign.linkgroup.hu
- www.cell.com and ars.els-cdn.com (Ripoll-Sánchez supplementary)
- www.cengen.org / cengen.org
- openworm.org
- www.wormatlas.org (canonical neuron list)
- doi.org

**Blocked: needed to finish Phase 0 properly.**

- api.openalex.org
- api.semanticscholar.org
- api.crossref.org
- www.ebi.ac.uk (Europe PMC REST)
- arxiv.org
- www.ncbi.nlm.nih.gov / pmc.ncbi.nlm.nih.gov
- www.biorxiv.org / api.biorxiv.org

With these I can run a mechanical "cited-by" sweep and read the Randi and
Creamer full texts and Supplementary Information.

---

## Sources consulted

- Randi et al. 2023, Nature: https://www.nature.com/articles/s41586-023-06683-4 (excerpts only); PMC10632145; arXiv:2208.04790
- Authors' code: https://github.com/leiferlab/pumpprobe (commit `1dbc5e0a`); https://github.com/francescorandi/wormneuroatlas (commit `b2e13d88`)
- Authors' data release: https://pypi.org/project/wormneuroatlas/ 0.0.7.3
- Creamer, Leifer & Pillow: https://www.biorxiv.org/content/10.1101/2024.09.22.614271v1; https://pmc.ncbi.nlm.nih.gov/articles/PMC12485687/; https://github.com/Nondairy-Creamer/Creamer_LDS_2026 (commit `bba43302`)
- Dvali et al. 2025: https://journals.aps.org/prxlife/abstract/10.1103/6wgv-b9m6; https://arxiv.org/abs/2412.14498
- Leifer APS 2026: https://meetings-archive.aps.org/smt/2026/mar-l54/5/
- Simeon et al.: https://arxiv.org/abs/2411.12091
- Sunil, Benali & Moutuou 2026: https://arxiv.org/abs/2604.02057
- Szilágyi et al. 2026: https://link.springer.com/article/10.1186/s12915-026-02641-4
- Ripoll-Sánchez et al. 2023: https://www.cell.com/neuron/fulltext/S0896-6273(23)00756-0
- Venkatesh et al. 2025 review: https://link.springer.com/article/10.1007/s12038-025-00513-7
- Genetics 2024 review: https://academic.oup.com/genetics/article/228/3/iyae141/7795512
- Dyballa et al. ICLR 2024: https://arxiv.org/abs/2402.14102
- dLDS 2025: https://www.nature.com/articles/s42003-025-08599-3
- The Transmitter coverage: https://www.thetransmitter.org/connectome/worms-help-untangle-longstanding-brain-structure-function-mystery/
- Fenyves et al. 2020: https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1007974
- Bentley et al. 2016: https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1005283
- OpenWorm ConnectomeToolbox: https://github.com/openworm/ConnectomeToolbox
