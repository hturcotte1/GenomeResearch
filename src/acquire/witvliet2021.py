"""Witvliet et al. 2021, Nature 596:257-261: brain connectomes of 8 isogenic animals, L1 to adult.

Only the two adult datasets (7 and 8) are acquired, the ones Randi et al. 2023
used. Datasets 1-6 (L1-L3) are listed in docs/provenance/witvliet2021.md as
available but not acquired. The primary hosts (nature.com, nemanode.org,
wormwiring.org) are blocked in this environment; see that document.

Four secondary distributions are acquired, because they hold two different
versions of the same two datasets plus the paper's own tables:

- ``aconnectome_witvliet_2020_{7,8}.csv``: members of the ``wormneuroatlas``
  0.0.7.3 wheel. These are the files Randi et al.'s code loads
  (``NeuroAtlas.aconn_sources``). Tab-separated despite the ``.csv`` suffix,
  no trailing newline, header ``pre post type synapses``.
- ``witvliet_2020_{7,8} adult.xlsx``: from the OpenWorm ConnectomeToolbox at
  the pinned commit. The toolbox says they are the WormWiring spreadsheets
  (``cect/validation/WitvlietEtAl2021.md``). One sheet, same four columns.
- ``nemanode_<commit>__*.json``: the source data of nemanode.org, from the Zhen
  lab's GitHub repository ``zhenlab-ltri/NemaNode``, at two commits:
  ``859641e`` (2020-05-22, "Renamed datasets to be consistent with
  manuscript", the pre-revision data) and ``baf8ec8`` (2021-03-15, committed
  by D. Witvliet, "Updated witvliet datasets after paper revision"). The blobs
  at ``baf8ec8`` are unchanged at the repository's master head ``6b7ca03``
  (2022-03-16). ``neurons.json`` is NemaNode's cell table (name, class,
  type code, transmitter code); its blob is identical at all three commits.
- ``synapse_count_matrices.xlsx``, ``synapse_list.csv``,
  ``connection_classifications.csv``, ``_neurons.csv``: the ``tables/``
  folder of the first author's figure-generation repository
  ``dwitvliet/nature2021`` at its master head ``0646af9`` (2021-06-01, "Fixed
  stats for publication"). The commits that added them are titled "Added
  export functions for supplementary tables", "Added supplementary tables" and
  "Added missing supplementary info" (2021-02-10/11/12). Whether they are
  byte-identical to the Nature supplementary files is unverified. They cover
  all 8 datasets (one file each); only datasets 7 and 8 are counted in detail.
  The same repository's ``data/nemanode/witvliet_2020_{7,8}.json`` have the
  same git blob ids as NemaNode ``baf8ec8``, i.e. the same bytes.

Facts checked by ``record_counts`` that later phases must respect:

- The wheel CSVs equal the PRE-revision NemaNode data (859641e), edge for edge
  and weight for weight. The toolbox xlsx equal the POST-revision data
  (baf8ec8), apart from gap-junction entries to unidentified fragments, which
  the xlsx omit. Randi et al. therefore used the pre-revision version.
- The paper's own ``synapse_count_matrices.xlsx`` (datasets 7, 8) and
  ``synapse_list.csv`` agree with the post-revision data, not with the wheel
  CSVs. Matrices are laid out [post row, pre column].
- Chemical rows are oriented pre -> post (presynaptic -> postsynaptic).
  Electrical rows have no direction. NemaNode JSON lists each gap junction in
  both directions; the CSV and xlsx list each unordered pair once (the xlsx
  always with pre <= post as strings, the CSV in no fixed order).
- A connection's weight is the number of entries in its ``syn`` list
  (NemaNode's own rule, ``populate-connections.js``: ``synapseCount =
  syn.length``). That equals the CSV/xlsx ``synapses`` column. A polyadic
  synapse is counted once per postsynaptic partner, and a connector id can be
  listed twice within one connection, so the weight sum is not a count of
  distinct synapses. Both are reported.
- Names are Witvliet/NemaNode names: AWCL/AWCR (not AWCON/AWCOFF), muscles as
  ``BWM-DL01``... (zero-padded), glia and other cells (CEPsh*, GLR*, excgl),
  and in the post-revision JSON the non-cell names ``NR_fragment``,
  ``vncfrag``, ``Fragment``, ``VAn``.
"""

from __future__ import annotations

import json
from collections import Counter

from .common import RAW_ROOT, ArchiveMember, RemoteFile, acquire_source, verify_pypi_digest
from .distributions import (
    WORMNEUROATLAS_PACKAGE,
    WORMNEUROATLAS_VERSION,
    WORMNEUROATLAS_WHEEL,
    connectome_toolbox_file,
)

SOURCE_ID = "witvliet2021"
CITATION = (
    "Witvliet D, Mulcahy B, Mitchell JK, et al. Connectomes across development "
    "reveal principles of brain maturation. Nature 596, 257-261 (2021). "
    "doi:10.1038/s41586-021-03778-8"
)
PRIMARY_PAPER = "https://www.nature.com/articles/s41586-021-03778-8"
PRIMARY_PORTAL = "https://nemanode.org/ (dataset ids witvliet_2020_7, witvliet_2020_8)"
PRIMARY_WORMWIRING = "https://wormwiring.org/pages/witvliet.html"

# The Zhen lab's NemaNode repository: the source data loaded into nemanode.org.
# Declared here, not in distributions.py, because only this source uses it.
NEMANODE_REPO = "zhenlab-ltri/NemaNode"
NEMANODE_PREREVISION = "859641e20748f5313a99eaa862227ae9f6d369ca"  # 2020-05-22
NEMANODE_REVISED = "baf8ec877455890d089d965d1a0b3ea0db110e9f"  # 2021-03-15, D. Witvliet
NEMANODE_MASTER_HEAD = "6b7ca03f6d68c4ea1af3c120d1a47681edc74a90"  # 2022-03-16; same blobs as REVISED
_NN_DIR = "src/server/populate-db/raw-data"

# The first author's figure-generation repository for the Nature paper.
NATURE2021_REPO = "dwitvliet/nature2021"
NATURE2021_COMMIT = "0646af9d25896ae660f97d462eab2d67282f5625"  # 2021-06-01, master head


def _nature2021_file(path: str, *, sha256: str, size: int, git_blob_sha1: str, note: str) -> RemoteFile:
    return RemoteFile(
        url=f"https://raw.githubusercontent.com/{NATURE2021_REPO}/{NATURE2021_COMMIT}/{path}",
        filename=path.rsplit("/", 1)[-1],
        sha256=sha256,
        size=size,
        distributor=f"GitHub {NATURE2021_REPO} @ {NATURE2021_COMMIT} (D. Witvliet, first author; figure code for the paper)",
        origin="secondary",
        primary_reference=f"{PRIMARY_PAPER} (Supplementary Information; correspondence to a specific supplementary file unverified)",
        git_blob_sha1=git_blob_sha1,
        note=note,
    )


def _nemanode_file(commit: str, path: str, *, filename: str, sha256: str, size: int,
                   git_blob_sha1: str, note: str) -> RemoteFile:
    return RemoteFile(
        url=f"https://raw.githubusercontent.com/{NEMANODE_REPO}/{commit}/{path}",
        filename=filename,
        sha256=sha256,
        size=size,
        distributor=f"GitHub {NEMANODE_REPO} @ {commit} (Zhen lab; source data of nemanode.org)",
        origin="secondary",
        primary_reference=f"{PRIMARY_PORTAL}; paper {PRIMARY_PAPER}",
        git_blob_sha1=git_blob_sha1,
        note=note,
    )


FILES = (
    # --- What Randi et al. used: wormneuroatlas 0.0.7.3 wheel members -------
    ArchiveMember(
        archive=WORMNEUROATLAS_WHEEL,
        member="wormneuroatlas/data/aconnectome_witvliet_2020_7.csv",
        filename="aconnectome_witvliet_2020_7.csv",
        sha256="1370d2a7e26a17e0765edfa834c95ca59ab44d8587efb5fda330432233074165",
        size=55102,
        primary_reference=f"{PRIMARY_PORTAL}; paper {PRIMARY_PAPER}",
        note=(
            "Dataset 7 (adult) as loaded by Randi et al.'s NeuroAtlas. Tab-separated. "
            "Content equals NemaNode pre-revision commit 859641e, not the post-revision data."
        ),
    ),
    ArchiveMember(
        archive=WORMNEUROATLAS_WHEEL,
        member="wormneuroatlas/data/aconnectome_witvliet_2020_8.csv",
        filename="aconnectome_witvliet_2020_8.csv",
        sha256="530a6d6b1c0c621d70a019e478ac79c8107cde475b55e79f225582f77b342ce4",
        size=55153,
        primary_reference=f"{PRIMARY_PORTAL}; paper {PRIMARY_PAPER}",
        note=(
            "Dataset 8 (adult) as loaded by Randi et al.'s NeuroAtlas. Tab-separated. "
            "Content equals NemaNode pre-revision commit 859641e, not the post-revision data."
        ),
    ),
    # --- WormWiring spreadsheets, via the OpenWorm ConnectomeToolbox ---------
    connectome_toolbox_file(
        "cect/data/witvliet_2020_7%20adult.xlsx",
        filename="witvliet_2020_7 adult.xlsx",
        sha256="d0fd2dd32adbe5f04ce90a2e5b74c01c9a831876527b0a2b8bd5b94edc86b037",
        size=53165,
        git_blob_sha1="9cec72011ebfb1052631fbb7f86d6bf3190ed421",
        primary_reference=f"{PRIMARY_WORMWIRING} (per the toolbox's cect/validation/WitvlietEtAl2021.md); portal {PRIMARY_PORTAL}",
        note=(
            "Dataset 7 (adult). LibreOffice 6.0.7.3 xlsx, zip entries dated 2022-09-20. "
            "Content equals NemaNode post-revision commit baf8ec8 minus gap junctions to unidentified fragments."
        ),
    ),
    connectome_toolbox_file(
        "cect/data/witvliet_2020_8%20adult.xlsx",
        filename="witvliet_2020_8 adult.xlsx",
        sha256="fdead89606257c1b26e57069fbe1de14c7696633b75b59b79e74c0bcc3497e62",
        size=53143,
        git_blob_sha1="b03bdbeddab70a0d70f6e430e8cdc584c46725c1",
        primary_reference=f"{PRIMARY_WORMWIRING} (per the toolbox's cect/validation/WitvlietEtAl2021.md); portal {PRIMARY_PORTAL}",
        note=(
            "Dataset 8 (adult). LibreOffice 6.0.7.3 xlsx, zip entries dated 2022-09-20. "
            "Content equals NemaNode post-revision commit baf8ec8 minus gap junctions to unidentified fragments."
        ),
    ),
    # --- NemaNode source data, post-revision (2021-03-15) --------------------
    _nemanode_file(
        NEMANODE_REVISED,
        f"{_NN_DIR}/connections/witvliet_2020_7.json",
        filename="nemanode_baf8ec8__witvliet_2020_7.json",
        sha256="350b247214763fe6b5a89b76a95cc018f7551c0446ad6501bd9c4774fb05fbae",
        size=854336,
        git_blob_sha1="201d50cd208f265d7b2819a87145cb2bcf718230",
        note=(
            "Dataset 7, post-revision ('Updated witvliet datasets after paper revision', D. Witvliet, "
            "2021-03-15). Same blob at master head 6b7ca03. Per-synapse connector ids included."
        ),
    ),
    _nemanode_file(
        NEMANODE_REVISED,
        f"{_NN_DIR}/connections/witvliet_2020_8.json",
        filename="nemanode_baf8ec8__witvliet_2020_8.json",
        sha256="465aeb3c1f42d84273023cef8e5f5d8ebbcf63248550b2219db68fccb9787033",
        size=887526,
        git_blob_sha1="135b1806872eea14a5f7bb667901285d269df720",
        note=(
            "Dataset 8, post-revision ('Updated witvliet datasets after paper revision', D. Witvliet, "
            "2021-03-15). Same blob at master head 6b7ca03. Per-synapse connector ids included."
        ),
    ),
    _nemanode_file(
        NEMANODE_REVISED,
        f"{_NN_DIR}/neurons.json",
        filename="nemanode_baf8ec8__neurons.json",
        sha256="c780e0b7cab28b311a7e0916a7b8e37b9cf72de152712bd4a5eb29fd9d595492",
        size=58575,
        git_blob_sha1="81da4572b20674dcc852cfa9fd041e66a3c7a73c",
        note=(
            "NemaNode cell table (447 cells: name, classes, typ, nt, emb, inhead, intail). Identical blob at "
            "859641e, baf8ec8 and 6b7ca03. Its typ/nt codes are NemaNode annotations, not Witvliet data."
        ),
    ),
    # --- NemaNode source data, pre-revision (2020-05-22) ---------------------
    _nemanode_file(
        NEMANODE_PREREVISION,
        f"{_NN_DIR}/connections/witvliet_2020_7.json",
        filename="nemanode_859641e__witvliet_2020_7.json",
        sha256="caff48ff6cde87983d616a67d1d5d1967871548a965f86722ab2b666fe0315c3",
        size=897485,
        git_blob_sha1="8ec3eab48416e4ea390fbcdf6be2085c14333f8d",
        note=(
            "Dataset 7, pre-revision ('Renamed datasets to be consistent with manuscript', 2020-05-22). "
            "Superseded in the repository on 2021-03-15. Source of the wheel CSV's content."
        ),
    ),
    _nemanode_file(
        NEMANODE_PREREVISION,
        f"{_NN_DIR}/connections/witvliet_2020_8.json",
        filename="nemanode_859641e__witvliet_2020_8.json",
        sha256="c13c42b5ba662e0bddcb1060693e0f75d579d85ee5c81ca539c620271819b07a",
        size=932228,
        git_blob_sha1="c156b36c7d9efb28d7cc048cbe173f6bc651ee39",
        note=(
            "Dataset 8, pre-revision ('Renamed datasets to be consistent with manuscript', 2020-05-22). "
            "Superseded in the repository on 2021-03-15. Source of the wheel CSV's content."
        ),
    ),
    # --- The paper's own tables (first author's repository) -----------------
    _nature2021_file(
        "tables/synapse_count_matrices.xlsx",
        sha256="bd725d1f6121abeb8ec08d0b80edad94d9e0fea954a8704ee07c7f4be7cebfe6",
        size=764283,
        git_blob_sha1="e2c29655de6932b1d9e9d968b16f7ed318d3e7e3",
        note=(
            "Chemical synapse count matrices, one sheet per dataset 1-8, rows = post, columns = pre, "
            "brain cells only; no gap junctions. Written by export_matrices.py (commit 0fa137d, 2021-02-10)."
        ),
    ),
    _nature2021_file(
        "tables/synapse_list.csv",
        sha256="36c431f25e72cd82946239a2eb555c1ed4494a2036092105bd37eb161ecf9340",
        size=1287223,
        git_blob_sha1="80fc81032f996e75349397c2dec505cd462ca48c",
        note=(
            "One row per (synapse, postsynaptic partner), datasets 1-8: dataset, pre, post, syn_id, sections, "
            "size (-1 = missing), post_is_branch. Commit d526424, 2021-02-11."
        ),
    ),
    _nature2021_file(
        "tables/connection_classifications.csv",
        sha256="da94863507a64da8d85d75a280ceff538d30f98a746390a7d0090607b0870f08",
        size=92737,
        git_blob_sha1="960ce494eee0352320bde8a3bc82a59fede4d713",
        note="The paper's per-connection classification (stable / variable / developmentally dynamic / post-embryonic). Commit 8b2ce2e, 2021-02-12.",
    ),
    _nature2021_file(
        "tables/_neurons.csv",
        sha256="2189e2ee262a1d1a81f1139fcc95c4b886681cfdd706dc5f77bd8cda2a49491d",
        size=2223,
        git_blob_sha1="bef93bfd871caa8c3fbea910741d01bc9c960ac8",
        note="The paper's brain cell classes (class, members, type, integration); tables.py omits CAN. Commit 65282f6, 2021-02-11.",
    ),
)

DATASETS = (7, 8)
VERSIONS = ("wna_csv", "cect_xlsx", "nemanode_859641e", "nemanode_baf8ec8")
_NEMANODE_TYP = {0: "chemical", 2: "electrical"}


def acquire() -> list[dict]:
    pypi_check = verify_pypi_digest(
        WORMNEUROATLAS_PACKAGE,
        WORMNEUROATLAS_VERSION,
        WORMNEUROATLAS_WHEEL.filename,
        WORMNEUROATLAS_WHEEL.sha256,
    )
    extra = {
        f.filename: [f"archive {WORMNEUROATLAS_WHEEL.filename}: {pypi_check}"]
        for f in FILES
        if isinstance(f, ArchiveMember)
    }
    return acquire_source(SOURCE_ID, FILES, extra)


# ---------------------------------------------------------------------------
# Readers. Each returns rows (pre, post, type, weight) exactly as stored, plus,
# for NemaNode JSON, the connector-id lists. No renaming, no filtering.
# ---------------------------------------------------------------------------

def _read_tsv(path) -> tuple[list[str], list[tuple[str, str, str, int]], dict]:
    raw = path.read_bytes()
    text = raw.decode("ascii")
    lines = text.split("\n")
    header = lines[0].split("\t")
    rows = []
    for line in lines[1:]:
        if line == "":
            continue
        pre, post, typ, n = line.split("\t")
        rows.append((pre, post, typ, int(n)))
    facts = {
        "bytes_contain_CR": b"\r" in raw,
        "ends_with_newline": raw.endswith(b"\n"),
        "delimiter_is_tab": all(len(line.split("\t")) == 4 for line in lines if line),
    }
    return header, rows, facts


def _read_xlsx(path) -> tuple[list[str], list[tuple[str, str, str, int]], dict]:
    import openpyxl

    wb = openpyxl.load_workbook(path, read_only=True)
    try:
        sheetnames = list(wb.sheetnames)
        values = [tuple(r) for r in wb.worksheets[0].iter_rows(values_only=True)]
    finally:
        wb.close()
    header = [str(v) for v in values[0]]
    cell_types = Counter(tuple(type(v).__name__ for v in r) for r in values[1:])
    rows = [(str(a), str(b), str(c), int(d)) for a, b, c, d in values[1:]]
    facts = {
        "sheetnames": sheetnames,
        "data_row_cell_types": {"|".join(k): v for k, v in sorted(cell_types.items())},
    }
    return header, rows, facts


def _read_nemanode(path) -> tuple[list[tuple[str, str, str, int]], list[dict], dict]:
    entries = json.loads(path.read_text(encoding="utf-8"))
    typ_values = Counter(e["typ"] for e in entries)
    rows = [(e["pre"], e["post"], _NEMANODE_TYP.get(e["typ"], f"typ={e['typ']}"), len(e["syn"])) for e in entries]
    facts = {
        "entry_key_sets": sorted({",".join(sorted(e.keys())) for e in entries}),
        "typ_values": {str(k): v for k, v in sorted(typ_values.items())},
        "syn_values": {str(k): v for k, v in sorted(Counter(s for e in entries for s in e["syn"]).items())},
        "all_list_lengths_equal": all(
            len(e["syn"]) == len(e["ids"]) == len(e["pre_tid"]) == len(e["post_tid"]) for e in entries
        ),
    }
    return rows, entries, facts


def _load_all(raw):
    out = {}
    for k in DATASETS:
        h, rows, facts = _read_tsv(raw / f"aconnectome_witvliet_2020_{k}.csv")
        out[("wna_csv", k)] = {"header": h, "rows": rows, "facts": facts, "entries": None}
        h, rows, facts = _read_xlsx(raw / f"witvliet_2020_{k} adult.xlsx")
        out[("cect_xlsx", k)] = {"header": h, "rows": rows, "facts": facts, "entries": None}
        for commit in ("859641e", "baf8ec8"):
            rows, entries, facts = _read_nemanode(raw / f"nemanode_{commit}__witvliet_2020_{k}.json")
            out[(f"nemanode_{commit}", k)] = {"header": None, "rows": rows, "facts": facts, "entries": entries}
    return out


def _cell_groups(names, cells: dict) -> dict:
    """Partition names by NemaNode neurons.json ``typ``. No biological judgement is added."""
    groups = {"typ_b_muscle": [], "typ_u_unknown": [], "typ_neuron_codes": [], "absent_from_neurons_json": []}
    for n in sorted(names):
        if n not in cells:
            groups["absent_from_neurons_json"].append(n)
        elif cells[n]["typ"] == "b":
            groups["typ_b_muscle"].append(n)
        elif cells[n]["typ"] == "u":
            groups["typ_u_unknown"].append(n)
        else:
            groups["typ_neuron_codes"].append(n)
    return groups


def _edge_dicts(rows):
    chem = {}
    gap = {}
    for pre, post, typ, w in rows:
        if typ == "chemical":
            chem[(pre, post)] = chem.get((pre, post), 0) + w
        elif typ == "electrical":
            gap.setdefault(frozenset((pre, post)), set()).add(w)
    return chem, gap


def _fmt_pair(p) -> str:
    a = sorted(p)
    return f"{a[0]}--{a[-1]}"


def _compare(a_rows, b_rows) -> dict:
    ca, ga = _edge_dicts(a_rows)
    cb, gb = _edge_dicts(b_rows)
    out = {
        "chem_edges_only_in_a": sorted(f"{p}->{q}:{ca[(p, q)]}" for p, q in ca if (p, q) not in cb),
        "chem_edges_only_in_b": sorted(f"{p}->{q}:{cb[(p, q)]}" for p, q in cb if (p, q) not in ca),
        "chem_weight_differs_a_vs_b": sorted(
            f"{p}->{q}:{ca[(p, q)]}vs{cb[(p, q)]}" for p, q in ca if (p, q) in cb and ca[(p, q)] != cb[(p, q)]
        ),
        "gap_pairs_only_in_a": sorted(f"{_fmt_pair(p)}:{sorted(ga[p])}" for p in ga if p not in gb),
        "gap_pairs_only_in_b": sorted(f"{_fmt_pair(p)}:{sorted(gb[p])}" for p in gb if p not in ga),
        "gap_weight_differs_a_vs_b": sorted(
            f"{_fmt_pair(p)}:{sorted(ga[p])}vs{sorted(gb[p])}" for p in ga if p in gb and ga[p] != gb[p]
        ),
    }
    out["chem_identical"] = not (out["chem_edges_only_in_a"] or out["chem_edges_only_in_b"] or out["chem_weight_differs_a_vs_b"])
    out["gap_unordered_identical"] = not (out["gap_pairs_only_in_a"] or out["gap_pairs_only_in_b"] or out["gap_weight_differs_a_vs_b"])
    out["chem_synapse_sum_a_minus_b"] = sum(ca.values()) - sum(cb.values())
    return out


def record_counts() -> dict:
    """Counts computed from the raw files only, with no renaming or filtering applied.

    Keys are ``<version>_d<dataset>_<quantity>``. Versions: ``wna_csv`` (wheel
    CSV, what Randi used), ``cect_xlsx`` (toolbox/WormWiring xlsx),
    ``nemanode_859641e`` (pre-revision JSON), ``nemanode_baf8ec8``
    (post-revision JSON). Datasets: 7 and 8.

    Row and edge counts:

    - ``rows_<type>``: stored rows (JSON entries) by type. JSON ``typ`` 0 is
      "chemical", 2 is "electrical" (NemaNode docs); any other value would be
      reported as ``typ=<n>``.
    - ``duplicate_keys``: rows sharing (pre, post, type) with another row.
    - ``chem_edges``: chemical rows = ordered (pre, post) pairs.
    - ``chem_self_edges``: chemical rows with pre == post.
    - ``chem_synapse_sum``: sum of chemical weights. Weight is the
      ``synapses`` column (CSV/xlsx) or ``len(syn)`` (JSON; NemaNode's rule).
      A polyadic synapse adds 1 to each postsynaptic partner's edge.
    - JSON only: ``chem_unique_connector_ids`` = distinct connector ids over
      all chemical entries (one per presynaptic site); ``chem_sum_unique_ids_per_edge``
      = per-edge distinct ids, summed; ``chem_entries_with_repeated_id`` =
      entries listing an id more than once; ``chem_syn_value_sum`` = sum of
      the ``syn`` values themselves (differs from ``chem_synapse_sum`` where a
      ``syn`` value is 2); ``chem_entries_with_syn_value_gt1`` lists them.
    - ``gap_rows``: electrical rows as stored. ``gap_unordered_pairs``:
      distinct {a, b}. ``gap_self_pairs``: a == b. ``gap_pairs_in_both_orientations``:
      unordered pairs (a != b) stored as both a->b and b->a.
      ``gap_pairs_one_orientation_only``: a != b stored one way only.
      ``gap_pairs_weight_asymmetric``: pairs whose two stored directions carry
      different weights. ``gap_weight_sum_unordered``: sum over unordered pairs
      of the pair's weight (max over stored directions; equal when symmetric).
      ``gap_rows_pre_lt_post``: rows with pre < post as Python strings.
      JSON only: ``gap_unique_connector_ids``.

    Cells (``cells_*``): the distinct names in pre or post, all row types,
    partitioned by NemaNode ``neurons.json`` ``typ`` only: ``b`` (muscle),
    ``u`` (unknown; NemaNode puts glia, GLR cells and CANR here), any
    neuron code (s/i/m/n combinations), or absent from neurons.json. This is
    NemaNode's labelling, reported as-is; which cells count as neurons is an
    owner decision (Phase 2). ``chem_edges_neuron_coded_both_ends`` and its
    synapse sum restrict to rows whose two ends both have a neuron code.

    ``cmp_d<k>_<a>__vs__<b>``: edge-level comparisons. Chemical edges are
    compared as ordered pairs with their weights; gap junctions as unordered
    pairs with the set of stored weights. Entries are "PRE->POST:w" or
    "A--B:[w]" strings, sorted. ``..._weight_sum_syn_...`` repeats the
    NemaNode pre- vs post-revision comparison with weight = sum of ``syn``.

    ``cells_by_paper_type``: each name is mapped to its class by NemaNode
    ``neurons.json`` ``classes`` and the class to its type by the paper's
    ``_neurons.csv``; names with no such type (absent from neurons.json, or
    class not listed, e.g. CAN, which the authors' tables.py skips) are listed
    in ``cells_without_paper_type_names``.

    Paper tables (``paper_*``): ``_neurons.csv`` class and member counts by
    type and integration; ``synapse_count_matrices.xlsx`` per adult sheet:
    pre columns, post rows (named rows only), nonzero cells, sum, and the
    type labels in sheet order; ``synapse_list.csv`` rows, distinct
    ``syn_id`` and distinct (pre, post) per dataset (all 8), rows with
    size == -1; ``connection_classifications.csv`` rows by value, rows not
    "post-embryonic brain integration" (and how many are self-pairs), and, per
    dataset, how many of those classified connections occur in that dataset's
    synapse list (their sum and the number of datasets are given so a mean
    can be formed). ``cmp_d<k>_paper_matrix__vs__<v>`` and
    ``cmp_d<k>_paper_synapse_list__vs__nemanode_baf8ec8`` compare chemical
    edges only (the paper tables hold no gap junctions); for the synapse list
    the weight is the number of rows per (pre, post), and ``syn_id_sets_equal``
    compares its syn_ids with NemaNode's chemical connector ids.
    """
    raw = RAW_ROOT / SOURCE_ID
    cells = {c["name"]: c for c in json.loads((raw / "nemanode_baf8ec8__neurons.json").read_text(encoding="utf-8"))}
    data = _load_all(raw)
    paper_neurons = _read_csv_dicts(raw / "_neurons.csv")
    paper_type = {r["class"]: r["type"] for r in paper_neurons}
    out: dict = {
        "neurons_json_cells": len(cells),
        "neurons_json_typ_values": {k: v for k, v in sorted(Counter(c["typ"] for c in cells.values()).items())},
    }

    for (version, k), d in sorted(data.items()):
        key = f"{version}_d{k}"
        rows = d["rows"]
        if d["header"] is not None:
            out[f"{key}_header"] = d["header"]
        for fk, fv in sorted(d["facts"].items()):
            out[f"{key}_file_{fk}"] = fv
        types = Counter(r[2] for r in rows)
        out[f"{key}_rows_total"] = len(rows)
        for t, n in sorted(types.items()):
            out[f"{key}_rows_{t}"] = n
        keyc = Counter((r[0], r[1], r[2]) for r in rows)
        out[f"{key}_duplicate_keys"] = sum(v - 1 for v in keyc.values() if v > 1)
        out[f"{key}_weight_min"] = min(r[3] for r in rows)

        names = {r[0] for r in rows} | {r[1] for r in rows}
        groups = _cell_groups(names, cells)
        out[f"{key}_cells_total"] = len(names)
        for g, members in groups.items():
            out[f"{key}_cells_{g}"] = len(members)
        out[f"{key}_cells_typ_u_unknown_names"] = groups["typ_u_unknown"]
        out[f"{key}_cells_absent_from_neurons_json_names"] = groups["absent_from_neurons_json"]
        out[f"{key}_cells_AWC_names"] = sorted(n for n in names if n.startswith("AWC"))
        ptypes = Counter()
        no_paper_type = []
        for n in sorted(names):
            t = paper_type.get(cells[n]["classes"]) if n in cells else None
            if t is None:
                no_paper_type.append(n)
            else:
                ptypes[t] += 1
        out[f"{key}_cells_by_paper_type"] = dict(sorted(ptypes.items()))
        out[f"{key}_cells_without_paper_type_names"] = no_paper_type
        neuron_coded = set(groups["typ_neuron_codes"])

        chem = [r for r in rows if r[2] == "chemical"]
        out[f"{key}_chem_edges"] = len(chem)
        out[f"{key}_chem_self_edges"] = sum(r[0] == r[1] for r in chem)
        out[f"{key}_chem_self_edge_names"] = sorted(f"{r[0]}:{r[3]}" for r in chem if r[0] == r[1])
        out[f"{key}_chem_synapse_sum"] = sum(r[3] for r in chem)
        out[f"{key}_chem_weight_max"] = max(r[3] for r in chem)
        nn = [r for r in chem if r[0] in neuron_coded and r[1] in neuron_coded]
        out[f"{key}_chem_edges_neuron_coded_both_ends"] = len(nn)
        out[f"{key}_chem_synapse_sum_neuron_coded_both_ends"] = sum(r[3] for r in nn)
        out[f"{key}_chem_edges_neuron_coded_both_ends_non_self"] = sum(r[0] != r[1] for r in nn)

        gap = [r for r in rows if r[2] == "electrical"]
        directed = {}
        for pre, post, _, w in gap:
            directed[(pre, post)] = w
        pairs = {frozenset((a, b)) for a, b in directed}
        both = [p for p in pairs if len(p) == 2 and all((a, b) in directed for a in p for b in p if a != b)]
        one = [p for p in pairs if len(p) == 2 and p not in set(both)]
        asym = [p for p in both if len({directed[(a, b)] for a in p for b in p if a != b}) > 1]

        def pair_weight(p):
            if len(p) == 1:
                (a,) = tuple(p)
                return directed[(a, a)]
            ws = [directed[(a, b)] for a in p for b in p if a != b and (a, b) in directed]
            return max(ws)

        out[f"{key}_gap_rows"] = len(gap)
        out[f"{key}_gap_unordered_pairs"] = len(pairs)
        out[f"{key}_gap_self_pairs"] = sum(len(p) == 1 for p in pairs)
        out[f"{key}_gap_pairs_in_both_orientations"] = len(both)
        out[f"{key}_gap_pairs_one_orientation_only"] = len(one)
        out[f"{key}_gap_pairs_weight_asymmetric"] = len(asym)
        out[f"{key}_gap_weight_sum_unordered"] = sum(pair_weight(p) for p in pairs)
        out[f"{key}_gap_rows_pre_lt_post"] = sum(r[0] < r[1] for r in gap)
        absent = set(groups["absent_from_neurons_json"])
        out[f"{key}_gap_pairs_touching_names_absent_from_neurons_json"] = sorted(
            _fmt_pair(p) for p in pairs if p & absent
        )

        if d["entries"] is not None:
            ce = [e for e in d["entries"] if e["typ"] == 0]
            ge = [e for e in d["entries"] if e["typ"] == 2]
            out[f"{key}_chem_unique_connector_ids"] = len({i for e in ce for i in e["ids"]})
            out[f"{key}_chem_syn_value_sum"] = sum(sum(e["syn"]) for e in ce)
            out[f"{key}_chem_entries_with_syn_value_gt1"] = sorted(
                f"{e['pre']}->{e['post']}:len{len(e['syn'])}:sum{sum(e['syn'])}" for e in ce if any(v > 1 for v in e["syn"])
            )
            out[f"{key}_chem_sum_unique_ids_per_edge"] = sum(len(set(e["ids"])) for e in ce)
            out[f"{key}_chem_entries_with_repeated_id"] = sum(len(set(e["ids"])) != len(e["ids"]) for e in ce)
            out[f"{key}_gap_unique_connector_ids"] = len({i for e in ge for i in e["ids"]})
            out[f"{key}_connector_ids_shared_by_chem_and_gap"] = len(
                {i for e in ce for i in e["ids"]} & {i for e in ge for i in e["ids"]}
            )

    comparisons = (
        ("wna_csv", "nemanode_859641e"),
        ("cect_xlsx", "nemanode_baf8ec8"),
        ("wna_csv", "cect_xlsx"),
        ("nemanode_859641e", "nemanode_baf8ec8"),
    )
    for k in DATASETS:
        for a, b in comparisons:
            res = _compare(data[(a, k)]["rows"], data[(b, k)]["rows"])
            for rk, rv in res.items():
                out[f"cmp_d{k}_{a}__vs__{b}_{rk}"] = rv
        # The same NemaNode comparison with weight = sum of syn values instead
        # of len(syn), because the pre-revision files store a few synapses with
        # syn value 2.
        a, b = "nemanode_859641e", "nemanode_baf8ec8"
        res = _compare(_rows_sum_syn(data[(a, k)]["entries"]), _rows_sum_syn(data[(b, k)]["entries"]))
        for rk, rv in res.items():
            out[f"cmp_d{k}_{a}__vs__{b}_weight_sum_syn_{rk}"] = rv

    out.update(_paper_table_counts(raw, data, paper_neurons))
    return out


def _read_csv_dicts(path) -> list[dict]:
    import csv

    with open(path, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def _read_paper_matrix(ws) -> tuple[list[tuple[str, str, str, int]], dict]:
    """Read one sheet of synapse_count_matrices.xlsx as (pre, post, "chemical", count) rows.

    Layout, as written by the authors' export_matrices.py: row 3 holds the
    pre names from column 4 on; column 3 holds the post names from row 5 on;
    rows 1-2 and columns 1-2 hold the "Pre"/"Post" and cell-type labels.
    """
    values = [list(r) for r in ws.iter_rows(values_only=True)]
    pre_names = values[2][3:]
    post_rows = [r for r in values[4:] if r[2] is not None]
    rows = []
    value_types = Counter()
    for r in post_rows:
        for pre, v in zip(pre_names, r[3:]):
            value_types[type(v).__name__] += 1
            if v not in (None, 0):
                rows.append((pre, r[2], "chemical", int(v)))
    facts = {
        "pre_columns": len(pre_names),
        "post_rows": len(post_rows),
        "pre_type_labels": [v for v in values[1][3:] if v is not None],
        "post_type_labels": [r[1] for r in values[4:] if r[1] is not None],
        "cell_value_types": dict(sorted(value_types.items())),
        "nonzero": len(rows),
        "sum": sum(r[3] for r in rows),
    }
    return rows, facts


def _paper_table_counts(raw, data, paper_neurons) -> dict:
    """Counts from the first author's tables (see record_counts for definitions)."""
    import openpyxl

    out: dict = {}
    out["paper_neurons_csv_classes"] = len(paper_neurons)
    out["paper_neurons_csv_members_sum"] = sum(int(r["members"]) for r in paper_neurons)
    out["paper_neurons_csv_classes_by_type"] = dict(sorted(Counter(r["type"] for r in paper_neurons).items()))
    by_type = Counter()
    for r in paper_neurons:
        by_type[r["type"]] += int(r["members"])
    out["paper_neurons_csv_members_by_type"] = dict(sorted(by_type.items()))
    out["paper_neurons_csv_classes_by_integration"] = dict(sorted(Counter(r["integration"] for r in paper_neurons).items()))
    out["paper_neurons_csv_lists_CAN"] = any(r["class"] == "CAN" for r in paper_neurons)

    wb = openpyxl.load_workbook(raw / "synapse_count_matrices.xlsx", read_only=True)
    try:
        out["paper_matrices_sheetnames"] = list(wb.sheetnames)
        for k in DATASETS:
            rows, facts = _read_paper_matrix(wb[f"Dataset{k}"])
            for fk, fv in sorted(facts.items()):
                out[f"paper_matrices_d{k}_{fk}"] = fv
            for other in ("nemanode_baf8ec8", "wna_csv"):
                chem_only = [r for r in data[(other, k)]["rows"] if r[2] == "chemical"]
                res = _compare(rows, chem_only)
                for rk in ("chem_identical", "chem_edges_only_in_a", "chem_edges_only_in_b",
                           "chem_weight_differs_a_vs_b", "chem_synapse_sum_a_minus_b"):
                    out[f"cmp_d{k}_paper_matrix__vs__{other}_{rk}"] = res[rk]
    finally:
        wb.close()

    syn = _read_csv_dicts(raw / "synapse_list.csv")
    out["paper_synapse_list_columns"] = list(syn[0].keys())
    out["paper_synapse_list_rows"] = len(syn)
    datasets = sorted({r["dataset"] for r in syn})
    out["paper_synapse_list_rows_by_dataset"] = {d: sum(r["dataset"] == d for r in syn) for d in datasets}
    out["paper_synapse_list_unique_syn_id_by_dataset"] = {
        d: len({r["syn_id"] for r in syn if r["dataset"] == d}) for d in datasets
    }
    out["paper_synapse_list_pre_post_pairs_by_dataset"] = {
        d: len({(r["pre"], r["post"]) for r in syn if r["dataset"] == d}) for d in datasets
    }
    out["paper_synapse_list_size_minus1_by_dataset"] = {
        d: sum(r["dataset"] == d and r["size"] == "-1" for r in syn) for d in datasets
    }
    for k in DATASETS:
        dk = [r for r in syn if r["dataset"] == f"Dataset{k}"]
        out[f"paper_synapse_list_d{k}_post_is_branch_values"] = dict(sorted(Counter(r["post_is_branch"] for r in dk).items()))
        counts = Counter((r["pre"], r["post"]) for r in dk)
        rows = [(a, b, "chemical", n) for (a, b), n in counts.items()]
        chem_only = [r for r in data[("nemanode_baf8ec8", k)]["rows"] if r[2] == "chemical"]
        res = _compare(rows, chem_only)
        for rk in ("chem_identical", "chem_edges_only_in_a", "chem_edges_only_in_b", "chem_weight_differs_a_vs_b"):
            out[f"cmp_d{k}_paper_synapse_list__vs__nemanode_baf8ec8_{rk}"] = res[rk]
        nn_ids = {str(i) for e in data[("nemanode_baf8ec8", k)]["entries"] if e["typ"] == 0 for i in e["ids"]}
        sl_ids = {r["syn_id"] for r in dk}
        out[f"cmp_d{k}_paper_synapse_list__vs__nemanode_baf8ec8_syn_id_sets_equal"] = nn_ids == sl_ids

    cls = _read_csv_dicts(raw / "connection_classifications.csv")
    out["paper_classifications_columns"] = list(cls[0].keys())
    out["paper_classifications_rows"] = len(cls)
    out["paper_classifications_by_value"] = dict(sorted(Counter(r["classification"] for r in cls).items()))
    postemb = "post-embryonic brain integration"
    classified = {(r["pre"], r["post"]) for r in cls if r["classification"] != postemb}
    out["paper_classifications_rows_not_postembryonic"] = len(classified)
    out["paper_classifications_rows_not_postembryonic_self"] = sum(a == b for a, b in classified)
    present = {d: len({(r["pre"], r["post"]) for r in syn if r["dataset"] == d} & classified) for d in datasets}
    out["paper_classified_connections_present_by_dataset"] = present
    out["paper_classified_connections_present_sum_over_datasets"] = sum(present.values())
    out["paper_classified_connections_present_n_datasets"] = len(present)
    return out


def _rows_sum_syn(entries):
    return [(e["pre"], e["post"], _NEMANODE_TYP.get(e["typ"], f"typ={e['typ']}"), sum(e["syn"])) for e in entries]
