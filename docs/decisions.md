# Decisions log

A running record of every judgement call and its reasoning.

- An **engineering** decision may be made and noted here.
- A **biological or threshold** decision stays OPEN until the project owner
  rules on it.

Each entry: ID, date, phase, status (DECIDED / OPEN), decision or question, and
reasoning.

---

## Phase 0

### D-001 (2026-10-11, Phase 0, DECIDED, engineering)
**Use the authors' own code and data release as primary evidence for what Randi
et al. did, because the full text could not be reached.**

Reasoning: the container's egress policy blocks Nature, PMC, arXiv and the
citation indexes. `leiferlab/pumpprobe` holds the command behind every figure,
and `wormneuroatlas` 0.0.7.3 ships the atlas. That atlas reproduces the paper's
23,433 measured pairs and 1,310 at q < 0.05 exactly. This is stated as a
limitation in `docs/phase0-prior-work.md` §0.

### D-002 (2026-10-11, Phase 0, DECIDED, engineering)
**One-off inspection scripts stay in the session scratch directory, not in the
repository.**

Reasoning: Phase 0 is a no-code phase. The inspection was used only to check
facts about the published data, and the counting rule is described in prose
(phase0 §1.2). It will be re-implemented as a proper reproduction test in
Phase 3.

### OPEN questions raised in Phase 0 (owner decision required)

Full context for each is in `docs/phase0-prior-work.md` §5.

| ID | Question |
|---|---|
| Q-001 (F1) | Phase 3 pair-count target: 23,433 (Nature, reproduced) or 23,427 (brief / reportedly an arXiv version)? Are the 168 self-pairs in scope for the edge table? |
| Q-002 (F2) | Encode per-strain evidence as four states (connected q<0.05 / confidently absent q_eq<0.05 / inconclusive / untested) instead of a boolean `randi_tested`? |
| Q-003 (F3) | 617 of 1,151 WT connections have no unc-31 measurement. Confirm the data layer should carry an explicit "DCV-dependence undetermined" state. Its use in the rubric is deferred to the classification pass. |
| Q-004 (F5) | Category D (hop limit, sign composition, gap-junction handling, timing) must be frozen before E is inspected. Who owns that rubric, and when is it frozen? (Not for this repo, but it determines which anatomical path features the table must expose.) |
| Q-005 (F7) | AWC: keep AWCON/AWCOF, map to AWCL/AWCR, or collapse to AWC? |
| Q-006 (F8) | Bilateral policy given that the authors' averaged q-values are statistically invalid: split-only, or collapse with statistics recomputed from trial-level `dFF_all`? |
| Q-007 (F9) | Which "White 1986" version is `anat_chem_white`: White A/L4/whole as used by Randi, or NemaNode jsh/n2u as used by Creamer? |
| Q-008 (F10) | `predicted_sign` source: Fenyves 2020 primary, and whether to add the 2026 refinement, Wang 2024, or a CeNGEN threshold variant as separate columns. |
| Q-009 (F13) | `monoamine_edge` source: Bentley 2016 or the later monoamine connectome file? |
| Q-010 | Data access: approve secondary copies (the PyPI `wormneuroatlas` wheel, the ConnectomeToolbox GitHub repo) with SHA-256 recorded, or allowlist the primary hosts listed in phase0 §5 first? |
