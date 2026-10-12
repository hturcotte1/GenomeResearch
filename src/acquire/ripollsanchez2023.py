"""Ripoll-Sanchez et al. 2023, Neuron 111:3570-3589: the neuropeptidergic connectome of C. elegans.

Three models of neuropeptide (NPP -> GPCR) connectivity are distributed, and
they must be kept separate: short-range (processes in the same bundle),
mid-range (same body region) and long-range (no spatial constraint). The same
group also distributes a monoamine connectome built with the same code.

All matrices are acquired from the first author's GitHub repository
``LidiaRipollSanchez/Neuropeptide-Connectome``. The paper's code statement
points there, and the authors' NemaMod repository README says "For downloading
the data from the paper in csv format go to this repository". The repository
holds THREE successive versions of the three model matrices, and all of them
are acquired because they differ and the paper's own numbers do not all agree
with one version (see docs/provenance/ripollsanchez2023.md):

- ``07072022_neuropeptide_connectome_{short,mid,long}_range_model`` (no file
  extension, no header row or column): the only matrices present at the
  repository's single tag ``Paper`` (commit 36ecbbf, 2023-06-02). Neuron
  order is given by ``26012022_num_neuronID.txt`` from the same commit (the
  README at that tag: "neurons that correspond to each row and column in the
  adjancency matrices"). The network densities quoted in web-search excerpts
  of the paper / preprint (0.3437 short, 0.4429 mid, 0.5929 long; the last
  possibly preprint-only) are reproduced only by this version.
- ``08062023_neuropeptide_connectome_{short,mid,long}_range_model.csv``: added
  2023-11-17, deleted 2024-02-02. Pinned at fb0ba84 (2023-11-21), the last
  commit before the deletion. The README names these files as the data behind
  Figures 1 and 5. Per-neuron in/out/total degrees computed from them equal
  the paper's Table S6 (mmc7) for all 302 neurons, mid- and short-range.
- ``01022024_neuropeptide_connectome_{short,mid,long}_range_model.csv``: the
  current files (HEAD 6689619, 2024-09-20). The README says they "were updated
  on 02/02/2024 with updated scRNAseq data for dmsr-5 and npr-34", i.e. after
  publication (Nov 2023). These are byte-identical (same git blob ids) to the
  copies in openworm/ConnectomeToolbox at ffe5702, which the toolbox loads.

Also acquired:

- ``08062023_monoamine_connectome.csv``: monoamine -> receptor network from
  the same pipeline (``Run_all_analysis_from_paper.m`` writes it alongside the
  neuropeptide matrices), using the 14 monoamine-GPCR pairs in
  ``05062023_Ligand-receptor-interactions_Mon_from_Barry_Bentley.csv``. It is
  NOT the Bentley et al. 2016 file. Byte-identical to the ConnectomeToolbox
  copy. A candidate for owner question Q-009 only.
- ``Table S6. Neuron information.xlsx`` (author repository) and
  ``1-s2.0-S0896627323007560-mmc7.xlsx`` (ConnectomeToolbox). Same cell
  values and formulas in every cell; different bytes. The toolbox copy was
  re-saved in Excel by the toolbox maintainer (its workbook.xml records
  absPath /Users/padraig/git/ConnectomeToolbox/cect/data/, modified
  2024-11-20). Neither is proven byte-identical to the journal's mmc7.

Facts checked by ``record_counts`` that later phases must respect:

- Orientation: ``M[i, j]`` = neuron i (row) expresses the neuropeptide /
  monoamine, neuron j (column) expresses the receptor; i.e. row = sender,
  column = receiver. The authors' ``buildnetwork`` computes
  ``reExp .* neExp`` with NPP expression as a column vector, and mmc7's
  in-degree equals the column sums. NOTE the authors' own code comment (line
  479 of Run_all_analysis_from_paper.m) states the opposite; the code and the
  data agree with each other, the comment does not.
- Weight = number of NPP-GPCR (or monoamine-GPCR) gene pairs from the
  authors' 500 nM EC50 interaction list for which the row neuron expresses
  the ligand and the column neuron the receptor (CeNGEN threshold 4, binary),
  summed over pairs. The diagonal holds autocrine pair counts and equals
  mmc7's "Self-loops" column.
- The authors compute degree and density on the binarised matrix with the
  diagonal removed, EXCEPT that their long-range density keeps the diagonal
  in the edge count (density_dir on the unmasked matrix).
- Names: 302 neurons in the authors' order (not alphabetical), AWCL/AWCR,
  CANL/CANR present, ventral-cord classes zero-padded (DA01 ... VC06; 64
  names).
"""

from __future__ import annotations

import json
import re
import zipfile

from .common import RAW_ROOT, RemoteFile, acquire_source

SOURCE_ID = "ripollsanchez2023"
CITATION = (
    "Ripoll-Sánchez L, Watteyne J, Sun H, Fernandez R, Taylor SR, Weinreb A, "
    "Bentley BL, Hammarlund M, Miller DM 3rd, Hobert O, Beets I, Vértes PE, "
    "Schafer WR. The neuropeptidergic connectome of C. elegans. Neuron 111(22), "
    "3570-3589.e5 (2023). doi:10.1016/j.neuron.2023.09.043"
)
PRIMARY_PAPER = "https://www.cell.com/neuron/fulltext/S0896-6273(23)00756-0"
PRIMARY_DATA = (
    "Figshare collection doi:10.6084/m9.figshare.c.6895870.v1 (the paper's data deposit per "
    "its data availability statement, as reported by web search; a newer version is reported "
    "to exist; contents and file correspondence UNVERIFIED, host blocked)"
)
PRIMARY_MMC7 = (
    f"{PRIMARY_PAPER} Supplementary Table S6 'Neuron information', journal file "
    "1-s2.0-S0896627323007560-mmc7.xlsx (Elsevier supplementary host, blocked; the mmc7 <-> "
    "Table S6 correspondence rests on identical cell contents, not on the journal page)"
)

# The first author's repository. Declared here, not in distributions.py,
# because only this source uses it.
NPC_REPO = "LidiaRipollSanchez/Neuropeptide-Connectome"
NPC_HEAD = "6689619236ba1b4681a9a77b3d918d513416336c"  # 2024-09-20, master head ("Create LICENSE")
NPC_PRE_UPDATE = "fb0ba8452aaee88793d731609dcff563d6265ec4"  # 2023-11-21, last commit with the 08062023 matrices
NPC_PAPER_TAG = "36ecbbffc3582a99f49e4a4f81e6a50fa0b9e32f"  # 2023-06-02, the repository's only tag, "Paper"
_ADJ = "Adjacency matrices for networks"

CONNECTOME_TOOLBOX_REPO = "openworm/ConnectomeToolbox"
CONNECTOME_TOOLBOX_COMMIT = "ffe570268b7cffb9329cd009a1bb37d60db2d465"
_TOOLBOX_SAME_BLOB = (
    f" The same git blob id is recorded for cect/data/{{name}} in {CONNECTOME_TOOLBOX_REPO} @ "
    f"{CONNECTOME_TOOLBOX_COMMIT} (checked when pinned), i.e. the toolbox copy has identical bytes."
)


def _quote(path: str) -> str:
    return path.replace("%", "%25").replace(" ", "%20").replace("&", "%26").replace("#", "%23")


def _npc_file(commit: str, path: str, *, sha256: str, size: int, git_blob_sha1: str,
              primary_reference: str, note: str, label: str) -> RemoteFile:
    return RemoteFile(
        url=f"https://raw.githubusercontent.com/{NPC_REPO}/{commit}/{_quote(path)}",
        filename=path.rsplit("/", 1)[-1],
        sha256=sha256,
        size=size,
        distributor=f"GitHub {NPC_REPO} @ {commit} ({label}; L. Ripoll-Sánchez, first author)",
        origin="secondary",
        primary_reference=primary_reference,
        git_blob_sha1=git_blob_sha1,
        note=note,
    )


_V2024 = "01022024"
_V2023 = "08062023"
_V2022 = "07072022"
RANGES = ("short", "mid", "long")
VERSIONS = (_V2022, _V2023, _V2024)

_PINS = {
    (_V2024, "short"): ("10c5739462fea24e9221753e2fe02ab466fd4927", 185765, "ee630f66dbb78a49d1818bd5209f1f9a0ee46400c061126e30d0d0a4b9d2e44d"),
    (_V2024, "mid"): ("17672bb56d4e828b86c8854319bf9ed2fb97632d", 185866, "97569885d58d947c2526e6ecc26c8b191b074d1b065f4da224102298203ad141"),
    (_V2024, "long"): ("d1b7e6539df4a2acd6cabbaa0ebdf632f2651747", 186132, "57ebc0919860bafcb866e63f5ae06b8b5d59427897d8bd230b4461bfa833f6fe"),
    (_V2023, "short"): ("6acbee7ed59273f80ef5f972f4452810d5891dd5", 185773, "7a9fd18305c4f145c51881ed145e09b442acd8cfda2836c0e87c1bce48c0c1a1"),
    (_V2023, "mid"): ("7c24a9dfd7bfc29feaf0887b47fb6015d984b3e8", 185874, "e2b5f3ae7a760933e47e5c5bc449c915df11e537c2fa33e30728745a49b78cd4"),
    (_V2023, "long"): ("e229d102823d788d995e0355160c93b0d88ee575", 186152, "cd3769c27427e972216e6faf7f3cb924fcc4e3e052586bf8f695f694bbcc0b3d"),
    (_V2022, "short"): ("ce6aca4934fc6b0c2f3a1e7b7aa7ec7465d3e7c0", 182735, "598cc7d2bba39862e20882fee2365eba9e42c5856d083e57882695f9e8a8f719"),
    (_V2022, "mid"): ("9b5176395cc90363ff108800e8241b805a73ef71", 182832, "7a8434d6cca231bdb78cb6ce43f37f5befd953f7d8599dd3b900395323872c18"),
    (_V2022, "long"): ("73cb72b52fe7ec99f2d75d2f9e4947fe6474836c", 183108, "4da3a7b558b9ae02aedd39eb154cfee09a2ce2b35da5674856703bf39148af2f"),
}
_COMMIT = {_V2024: NPC_HEAD, _V2023: NPC_PRE_UPDATE, _V2022: NPC_PAPER_TAG}
_VERSION_NOTE = {
    _V2024: ("POST-PUBLICATION version: README says the matrices 'were updated on 02/02/2024 with "
             "updated scRNAseq data for dmsr-5 and npr-34'. Header row and column, 302 neurons, "
             "row = sender (ligand), column = receiver (receptor)."),
    _V2023: ("Version present 2023-11-17 to 2024-02-02, named in the README as the data behind "
             "Figs 1 and 5; its per-neuron degrees equal Table S6/mmc7 exactly. Header row and "
             "column, 302 neurons, row = sender (ligand), column = receiver (receptor)."),
    _V2022: ("Version at the repository's only tag 'Paper' (2023-06-02); no header row or column, "
             "no file extension; neuron order from 26012022_num_neuronID.txt at the same commit. "
             "Reproduces the paper's quoted densities. Row = sender, column = receiver."),
}


def _matrix_name(version: str, rng: str) -> str:
    base = f"{version}_neuropeptide_connectome_{rng}_range_model"
    return base if version == _V2022 else base + ".csv"


def _matrix_file(version: str, rng: str) -> RemoteFile:
    blob, size, sha = _PINS[(version, rng)]
    name = _matrix_name(version, rng)
    note = f"{rng}-range model. " + _VERSION_NOTE[version]
    if version == _V2024:
        note += _TOOLBOX_SAME_BLOB.format(name=name)
    label = {_V2024: "master head", _V2023: "last commit before the 2024-02-02 update", _V2022: "tag 'Paper'"}[version]
    return _npc_file(
        _COMMIT[version], f"{_ADJ}/{name}", sha256=sha, size=size, git_blob_sha1=blob,
        primary_reference=PRIMARY_DATA, note=note, label=label,
    )


FILES = (
    *(_matrix_file(v, r) for v in (_V2024, _V2023, _V2022) for r in RANGES),
    _npc_file(
        NPC_PAPER_TAG, "26012022_num_neuronID.txt",
        sha256="0f3a73e4f3cda8c9693c75f3c8df18c5b51dd64da6b05a840df7fb18827f954b",
        size=2933, git_blob_sha1="698102a1340e8bac054e0e286fe0a18e1038dce1",
        primary_reference=PRIMARY_DATA, label="tag 'Paper'",
        note=("Neuron order for the matrices (tab-separated nodeID, nodeLabel; header line LF, "
              "data lines CRLF, no final newline). Same blob at HEAD as 'Scripts & data/26012022_num_neuronID.txt'. "
              "The only source of row/column labels for the headerless 07072022 matrices."),
    ),
    _npc_file(
        NPC_HEAD, f"{_ADJ}/08062023_monoamine_connectome.csv",
        sha256="629c99a54190940be954b5281fb414553dcb2e4913ced34f355aab27b3c9650f",
        size=185444, git_blob_sha1="7a9db13b346963f8a564836e2b64254684724271",
        primary_reference=PRIMARY_DATA, label="master head",
        note=("Monoamine -> GPCR network (serotonin, dopamine, octopamine, tyramine; 14 ligand-receptor "
              "pairs from '05062023_Ligand-receptor-interactions_Mon_from_Barry_Bentley.csv'), built by the "
              "same code as the neuropeptide matrices, no spatial constraint. Unchanged since 2023-11-17. "
              "NOT the Bentley et al. 2016 file. Candidate for owner question Q-009 only."
              + _TOOLBOX_SAME_BLOB.format(name="08062023_monoamine_connectome.csv")),
    ),
    _npc_file(
        NPC_HEAD, "Supplementary Tables/Table S6. Neuron information.xlsx",
        sha256="8cc3817a0efa76347688331c1a34f940bacab5941b4b205f9ce517382ed90f04",
        size=36794, git_blob_sha1="913c96f69ff849a76084c2977b18f68bd7b3c139",
        primary_reference=PRIMARY_MMC7, label="master head",
        note=("The author's copy of Table S6 'Neuron information' (one sheet, 302 neurons: type, segment, "
              "degree/in/out at EC50 500 nM for mid- and short-range, rich club formulas, cluster, self-loops). "
              "Unchanged since 2023-11-20; docProps modified 2023-11-14. Cell values and formulas identical "
              "to the toolbox's mmc7.xlsx; bytes differ."),
    ),
    RemoteFile(
        url=(f"https://raw.githubusercontent.com/{CONNECTOME_TOOLBOX_REPO}/{CONNECTOME_TOOLBOX_COMMIT}/"
             "cect/data/1-s2.0-S0896627323007560-mmc7.xlsx"),
        filename="1-s2.0-S0896627323007560-mmc7.xlsx",
        sha256="df379d1eff235b8c7289162048de593b79c94e9bd7cd0e724014e7f92a340654",
        size=36734,
        distributor=f"GitHub {CONNECTOME_TOOLBOX_REPO} @ {CONNECTOME_TOOLBOX_COMMIT}",
        origin="secondary",
        primary_reference=PRIMARY_MMC7,
        git_blob_sha1="5dd66158db8b855a59e6f37ebe742c991e3d0097",
        note=("Named as the journal's supplementary file mmc7 (= Table S6 'Neuron information'). Re-saved in "
              "Excel by the toolbox maintainer: workbook.xml absPath /Users/padraig/git/ConnectomeToolbox/cect/data/, "
              "docProps modified 2024-11-20 by 'Microsoft Office User'. Same cell values and formulas as the "
              "author's 'Table S6. Neuron information.xlsx'."),
    ),
)

MONOAMINE = "08062023_monoamine_connectome.csv"
NEURON_ID_FILE = "26012022_num_neuronID.txt"
TABLE_S6_AUTHOR = "Table S6. Neuron information.xlsx"
TABLE_S6_TOOLBOX = "1-s2.0-S0896627323007560-mmc7.xlsx"


def acquire() -> list[dict]:
    return acquire_source(SOURCE_ID, FILES)


# ---------------------------------------------------------------------------
# Record counts
# ---------------------------------------------------------------------------

def _read_bytes(name: str) -> bytes:
    return (RAW_ROOT / SOURCE_ID / name).read_bytes()


def _line_ending_facts(raw: bytes) -> dict:
    crlf = raw.count(b"\r\n")
    return {
        "bytes": len(raw),
        "crlf": crlf,
        "lf_only": raw.count(b"\n") - crlf,
        "utf8_bom": raw.startswith(b"\xef\xbb\xbf"),
        "ends_with_newline": raw.endswith(b"\n"),
    }


def _neuron_ids() -> list[str]:
    text = _read_bytes(NEURON_ID_FILE).decode("utf-8")
    lines = [ln for ln in text.splitlines() if ln.strip()]
    return [ln.split("\t")[1].strip() for ln in lines[1:]]


def _load_matrix(name: str):
    """Return (labels or None, row labels or None, int matrix, header cell or None)."""
    import csv
    import io

    import numpy as np

    rows = list(csv.reader(io.StringIO(_read_bytes(name).decode("utf-8"))))
    try:
        float(rows[0][0])
        has_header = False
    except ValueError:
        has_header = True
    if has_header:
        cols = rows[0][1:]
        body = rows[1:]
        rlab = [r[0] for r in body]
        vals = [r[1:] for r in body]
        corner = rows[0][0]
    else:
        cols = rlab = corner = None
        vals = rows
    widths = sorted({len(v) for v in vals})
    m = np.array([[float(t) for t in v] for v in vals])
    if not np.all(m == np.round(m)):
        raise ValueError(f"{name}: non-integer weights")
    return cols, rlab, m.astype(np.int64), corner, widths


def _matrix_facts(m, labels: list[str]) -> dict:
    import numpy as np

    n = m.shape[0]
    nz = m != 0
    diag = np.eye(n, dtype=bool)
    off = nz & ~diag
    k_off, k_all = int(off.sum()), int(nz.sum())
    pairs = n * (n - 1)
    w = m[off]
    hist = {str(k): int(v) for k, v in sorted(zip(*np.unique(m[nz], return_counts=True)))}
    return {
        "shape": [int(m.shape[0]), int(m.shape[1])],
        "min_weight": int(m.min()),
        "max_weight": int(m.max()),
        "nonzero_total": k_all,
        "nonzero_offdiag": k_off,
        "nonzero_diag": int((nz & diag).sum()),
        "weight_sum_offdiag": int(w.sum()),
        "weight_sum_diag": int(np.diag(m).sum()),
        "offdiag_edges_weight_eq_1": int((w == 1).sum()),
        "reciprocal_offdiag_ordered_pairs": int((off & off.T).sum()),
        "symmetric_matrix": bool(np.array_equal(m, m.T)),
        "nonzero_weight_histogram": hist,
        "rows_with_offdiag_edges": int(off.any(axis=1).sum()),
        "cols_with_offdiag_edges": int(off.any(axis=0).sum()),
        "density_offdiag_over_n(n-1)": round(k_off / pairs, 6),
        "density_alltotal_over_n(n-1)": round(k_all / pairs, 6),
        "density_alltotal_over_n2": round(k_all / (n * n), 6),
    }


def _diff_facts(a, b, labels: list[str]) -> dict:
    import numpy as np

    d = a != b
    ba, bb = a != 0, b != 0
    rows = sorted({labels[i] for i in np.where(d.any(axis=1))[0]})
    return {
        "cells_differ": int(d.sum()),
        "edges_gained": int((~ba & bb).sum()),
        "edges_lost": int((ba & ~bb).sum()),
        "diag_cells_differ": int(np.diag(d).sum()),
        "rows_touched": len(rows),
        "rows_touched_names": rows,
        "cols_touched": int(d.any(axis=0).sum()),
    }


def _table_s6(name: str, data_only: bool):
    import openpyxl

    wb = openpyxl.load_workbook(RAW_ROOT / SOURCE_ID / name, data_only=data_only)
    ws = wb.worksheets[0]
    return wb, [[c.value for c in row] for row in ws.iter_rows()]


def _xlsx_meta(name: str) -> dict:
    wb, _ = _table_s6(name, data_only=False)
    with zipfile.ZipFile(RAW_ROOT / SOURCE_ID / name) as zf:
        wbxml = zf.read("xl/workbook.xml").decode("utf-8")
    m = re.search(r'absPath url="([^"]*)"', wbxml)
    p = wb.properties
    return {
        "sheets": list(wb.sheetnames),
        "creator": p.creator,
        "created": p.created.isoformat() if p.created else None,
        "last_modified_by": p.lastModifiedBy,
        "modified": p.modified.isoformat() if p.modified else None,
        "workbook_abs_path": m.group(1) if m else None,
    }


def record_counts() -> dict:
    """Counts computed from the raw files only, with no naming normalisation or filtering.

    Matrices (keys ``np_<version>_<range>`` and ``monoamine_08062023``):

    - ``shape``; ``nonzero_total`` = nonzero cells; ``nonzero_offdiag`` =
      nonzero cells off the diagonal = directed edges i -> j, i != j;
      ``nonzero_diag`` = nonzero diagonal cells (autocrine / self-loops),
      counted separately.
    - Weights: integer counts. ``weight_sum_*`` sums them; the histogram is
      over nonzero cells (diagonal included). ``offdiag_edges_weight_eq_1``
      counts edges carried by exactly one ligand-receptor pair.
    - Densities, three definitions side by side, n = 302:
      ``density_offdiag_over_n(n-1)`` (the authors' definition for the short
      and mid models: binarised, self-loops removed); ``density_alltotal_over_n(n-1)``
      (what the authors' code computes for the long-range model, which it
      passes to density_dir with the diagonal kept); ``density_alltotal_over_n2``.
    - ``labels_*``: header facts. ``header_equals_row_labels`` and
      ``header_equals_num_neuronID_order`` compare label lists exactly. The
      07072022 files have no header; their labels are taken positionally from
      26012022_num_neuronID.txt (the authors' documented order).

    For the monoamine matrix, ``rows_with_offdiag_edges_names`` lists the
    rows (senders) that have at least one off-diagonal edge.

    Version differences (``diff_<range>_<old>_vs_<new>``): cells that differ,
    edges gained/lost (zero <-> nonzero), rows/columns containing any change,
    and the sorted names of the changed rows (rows = senders).

    Table S6 (``tableS6_*``):

    - ``author_vs_toolbox_cells_differ_{formulas,values}``: cells whose
      content differs between the author's and the toolbox's xlsx, read with
      formulas and with cached values.
    - ``degree_check_<version>_<range>``: for each of the 302 neurons, the
      in-degree, out-degree and degree computed from the binarised matrix
      with the diagonal removed, compared to Table S6's columns "In-degree",
      "Out-degree", "Degree (EC50 500nM)" for that range. Two orientations are
      reported: ``rows_are_senders`` (in-degree = column sum) and
      ``rows_are_receivers`` (in-degree = row sum). Each gives the number of
      neurons matching exactly, the largest absolute difference and the
      signed sum of differences (computed minus table).
    - ``selfloops_check_<version>_<range>``: neurons whose diagonal value
      equals Table S6's "Self-loops" column.
    - ``rich_club_<range>``: neurons whose Table S6 degree meets the
      threshold written in the table's own rich-club formula, and, per
      version, the same count using degrees computed from the matrix.
    """
    import numpy as np

    out: dict = {}
    ids = _neuron_ids()
    out["num_neuronID_entries"] = len(ids)
    out["num_neuronID_distinct"] = len(set(ids))
    out["num_neuronID_file"] = _line_ending_facts(_read_bytes(NEURON_ID_FILE))
    out["neuron_ids_zero_padded"] = sorted(n for n in ids if re.fullmatch(r"[A-Z]+0\d", n))
    out["neuron_ids_awc_can"] = sorted(n for n in ids if n.startswith(("AWC", "CAN")))
    out["neuron_ids_alphabetically_sorted"] = ids == sorted(ids)

    mats: dict = {}
    names = [(f"np_{v}_{r}", _matrix_name(v, r)) for v in VERSIONS for r in RANGES]
    names.append(("monoamine_08062023", MONOAMINE))
    for key, fname in names:
        cols, rlab, m, corner, widths = _load_matrix(fname)
        facts = {"file": _line_ending_facts(_read_bytes(fname)), "row_widths": widths}
        if cols is None:
            facts["labels"] = {"has_header": False, "labels_from": NEURON_ID_FILE}
            labels = ids
        else:
            facts["labels"] = {
                "has_header": True,
                "corner_cell": corner,
                "n_labels": len(cols),
                "n_distinct_labels": len(set(cols)),
                "header_equals_row_labels": cols == rlab,
                "header_equals_num_neuronID_order": cols == ids,
            }
            labels = cols
        if len(labels) != m.shape[0] or m.shape[0] != m.shape[1]:
            raise ValueError(f"{fname}: shape {m.shape} vs {len(labels)} labels")
        facts.update(_matrix_facts(m, labels))
        if key.startswith("monoamine"):
            off = (m != 0) & ~np.eye(m.shape[0], dtype=bool)
            facts["rows_with_offdiag_edges_names"] = sorted(labels[i] for i in np.where(off.any(axis=1))[0])
        out[key] = facts
        mats[key] = (labels, m)

    for r in RANGES:
        for old, new in ((_V2022, _V2023), (_V2023, _V2024), (_V2022, _V2024)):
            la, a = mats[f"np_{old}_{r}"]
            lb, b = mats[f"np_{new}_{r}"]
            if la != lb:
                out[f"diff_{r}_{old}_vs_{new}"] = "labels differ; not compared"
                continue
            out[f"diff_{r}_{old}_vs_{new}"] = _diff_facts(a, b, la)
    out["diag_identical_across_all_np_matrices"] = all(
        np.array_equal(np.diag(mats[k][1]), np.diag(mats["np_08062023_short"][1]))
        for k in mats if k.startswith("np_")
    )

    # Table S6: author copy vs toolbox copy.
    for mode, data_only in (("formulas", False), ("values", True)):
        _, ta = _table_s6(TABLE_S6_AUTHOR, data_only)
        _, tb = _table_s6(TABLE_S6_TOOLBOX, data_only)
        n = 0
        for i in range(max(len(ta), len(tb))):
            ra = ta[i] if i < len(ta) else []
            rb = tb[i] if i < len(tb) else []
            for j in range(max(len(ra), len(rb))):
                if (ra[j] if j < len(ra) else None) != (rb[j] if j < len(rb) else None):
                    n += 1
        out[f"tableS6_author_vs_toolbox_cells_differ_{mode}"] = n
    out["tableS6_author_xlsx_meta"] = _xlsx_meta(TABLE_S6_AUTHOR)
    out["tableS6_toolbox_mmc7_xlsx_meta"] = _xlsx_meta(TABLE_S6_TOOLBOX)

    _, vals = _table_s6(TABLE_S6_TOOLBOX, data_only=True)
    _, forms = _table_s6(TABLE_S6_TOOLBOX, data_only=False)
    out["tableS6_header_row1"] = [str(x) if x is not None else None for x in vals[0][:14]]
    out["tableS6_header_row2"] = [str(x) if x is not None else None for x in vals[1][:14]]
    body = [row for row in vals[2:] if row[0] is not None]
    fbody = [row for row in forms[2:] if row[0] is not None]
    out["tableS6_neuron_rows"] = len(body)
    t_names = [row[0] for row in body]
    out["tableS6_names_equal_num_neuronID_order"] = t_names == ids
    out["tableS6_id_column_is_1_to_n"] = [row[1] for row in body] == list(range(1, len(body) + 1))
    col = {"deg_mid": 4, "deg_short": 5, "in_mid": 6, "in_short": 7, "out_mid": 8, "out_short": 9, "self": 13}
    tab = {k: np.array([row[c] for row in body], dtype=np.int64) for k, c in col.items()}
    out["tableS6_degree_equals_in_plus_out"] = {
        r: int((tab[f"deg_{r}"] == tab[f"in_{r}"] + tab[f"out_{r}"]).sum()) for r in ("mid", "short")
    }
    out["tableS6_cluster_counts"] = {str(k): v for k, v in sorted(_count(row[12] for row in body).items())}
    rc_thr = {}
    for r, c in (("mid", 10), ("short", 11)):
        thr = {int(x) for x in (re.search(r">=(\d+)", str(row[c])).group(1) for row in fbody)}
        if len(thr) != 1:
            raise ValueError(f"Table S6 rich-club formula thresholds not unique for {r}: {thr}")
        rc_thr[r] = thr.pop()
        cached_yes = sum(1 for row in body if row[c] == "Yes")
        out[f"rich_club_{r}"] = {
            "formula_threshold_degree_ge": rc_thr[r],
            "tableS6_cached_yes": cached_yes,
            "tableS6_degree_ge_threshold": int((tab[f"deg_{r}"] >= rc_thr[r]).sum()),
        }

    for v in VERSIONS:
        for r in RANGES:
            labels, m = mats[f"np_{v}_{r}"]
            out[f"selfloops_check_{v}_{r}"] = int((np.diag(m) == tab["self"]).sum())
            if r == "long":
                continue
            b = (m != 0).astype(np.int64)
            np.fill_diagonal(b, 0)
            colsum, rowsum = b.sum(axis=0), b.sum(axis=1)
            res = {"labels_equal_tableS6_names": labels == t_names}
            for orient, (indeg, outdeg) in (("rows_are_senders", (colsum, rowsum)),
                                            ("rows_are_receivers", (rowsum, colsum))):
                o = {}
                for q, computed in (("in", indeg), ("out", outdeg), ("degree", indeg + outdeg)):
                    d = computed - tab[f"{'deg' if q == 'degree' else q}_{r}"]
                    o[q] = {
                        "exact_match": int((d == 0).sum()),
                        "max_abs_diff": int(np.abs(d).max()),
                        "sum_diff": int(d.sum()),
                    }
                res[orient] = o
            out[f"degree_check_{v}_{r}"] = res
            out[f"rich_club_{r}"][f"computed_{v}_degree_ge_threshold"] = int(
                ((colsum + rowsum) >= rc_thr[r]).sum()
            )
    # Round-trip through JSON to guarantee plain values.
    return json.loads(json.dumps(out, sort_keys=True))


def _count(items) -> dict:
    c: dict = {}
    for x in items:
        c[x] = c.get(x, 0) + 1
    return c
