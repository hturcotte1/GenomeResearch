"""Bentley et al. 2016, PLoS Comput Biol 12(12):e1005283: monoamine and neuropeptide connectomes.

Bentley et al. built two "wireless" layers as directed edge lists. In the
monoamine layer, a neuron that makes a monoamine sends an edge to every neuron
that expresses one of that monoamine's receptors. The neuropeptide layer is
built the same way from peptide and receptor expression. The paper's S1
Dataset (PLOS supporting-information item ``.s004``, a zip) holds the edge
lists. The three copies reachable from this environment are acquired here,
and all are SECONDARY. See docs/provenance/bentley2016.md.

Files and what they are:

1. ``edgelist_MA.csv`` and ``edgelist_NP.csv``, from the pinned
   ConnectomeToolbox commit (``cect/data/``). The toolbox's validation note
   (``cect/validation/BentleyEtAl2016.md``) says these are the files
   ``edge_lists/edgelist_MA.csv`` and ``edge_lists/edgelist_NP.csv``
   extracted from the S1 Dataset zip. The toolbox added them on 2026-06-24
   (commit f052c0d). There is no header. Each row has 4 fields:
   source, target, ligand, receptor.
2. ``esconnectome_monoamines_Bentley_2016.csv`` and
   ``esconnectome_neuropeptides_Bentley_2016.csv``, from the
   ``wormneuroatlas`` 0.0.7.3 wheel. These are the files Randi's package
   loads (``NeuroAtlas.esconn_sources``). Byte relationships, which
   ``record_counts`` checks:
   - Monoamine: one 53-byte header line ("#source neuron, target neuron,
     transmitter, receptor"), followed by exactly the bytes of the toolbox's
     ``edgelist_MA.csv``.
   - Neuropeptide: a 54-byte header line (the same text plus a trailing
     comma), then the toolbox's rows, each with a 5th field appended. The 5th
     field is a receptor sequence name such as "C39E6.6", and it is filled in
     on only some rows. Drop the header and the 5th field and what remains is
     byte-identical to ``edgelist_NP.csv``. The 5th field is absent from the
     toolbox's S1 extraction and from the pumpprobe copy (3. below). In
     GitHub francescorandi/wormneuroatlas the file is first committed on
     2022-12-12 (3eed4b8, at ``wormneuroatlas/``; moved to
     ``wormneuroatlas/data/`` by 5ebe7f4 on 2022-12-13) with the 4-field
     rows only. The 5th field appears on 2022-12-23 (7a7c653), in the same
     commit that adds ``cached_seq_ids.txt``. So it is most likely Randi's
     annotation, not Bentley's; confirming that needs the primary zip.
3. ``pumpprobe__esconnectome_monoamines_Bentley_2016.csv`` and
   ``pumpprobe__esconnectome_neuropeptides_Bentley_2016.csv``, from GitHub
   leiferlab/pumpprobe at the pinned commit (``pumpprobe/``). These are the
   files Randi et al.'s analysis code loads (``Funatlas.esconn_sources``).
   Both have been in that repository, as the same blobs, since 2022-07-15
   (8ceb2cb). Byte relationships, which ``record_counts`` checks:
   - Monoamine: byte-identical to the wheel's monoamine file.
   - Neuropeptide: the wheel's 53-byte monoamine header line (no trailing
     comma), followed by exactly the bytes of the toolbox's
     ``edgelist_NP.csv`` (4 fields, no 5th field).
   The repository also carries both files under
   ``build/lib.linux-x86_64-3.8/pumpprobe/`` as the same blobs; those
   duplicates are not acquired.

Facts later phases must respect (checked by ``record_counts``):

- Orientation: field 1 is the sender (expresses the ligand) and field 2 the
  receiver (expresses the receptor). The wheel header calls them "source" and
  "target"; the toolbox reader calls them pre and post. The monoamine list
  has 18 distinct field-1 names. The paper (web-search excerpt) reports 18
  monoamine-releasing neurons and names RIM as tyramine-releasing and RIC as
  octopamine-releasing. Here the tyramine senders are RIML/RIMR and the
  octopamine senders RICL/RICR. Each (ligand, receptor) block is a complete
  bipartite product of its senders and receivers.
- There is one row per (sender, receiver, ligand, receptor). A neuron pair
  linked through two receptors for the same ligand appears on two rows. The
  paper's totals (1,940 monoamine and 7,035 neuropeptide connections, PLOS
  version, per web-search excerpts) equal the distinct ordered pairs with
  self-pairs excluded; see ``record_counts``.
- Self-rows (sender == receiver) are present: 12 distinct self-pairs in the
  monoamine list and 43 in the neuropeptide list.
- Names: ventral-cord names are NOT zero-padded (VA1, VD13); AWC appears as
  AWCL/AWCR; CANL/CANR appear in the monoamine list. No normalisation is
  applied here.
- Both of Randi's loaders (wormneuroatlas ``NeuroAtlas._get_esconnectome_bentley``
  and pumpprobe ``Funatlas._get_esconnectome_bentley``, the same code) skip
  the first line and build ``esc[target, source]``, i.e. [receiver, sender],
  matching the atlas's [responding, stimulated] convention. Their name lookup
  (``ids_to_ai`` / ``ids_to_i``) returns -1 for a name not in the id list,
  and the loader then indexes with -1 without checking, so such rows land on
  the last id of the sorted list, VD9 under default settings. The wheel's id
  list (``neuron_ids.txt``) has AWCOFF/AWCON and no CANL/CANR, so
  AWCL/AWCR/CANL/CANR rows are affected; pumpprobe's (``aconnectome_ids.txt``)
  has AWCL/AWCR and no CANL/CANR, so only CANL/CANR rows are. The line
  ``if recept[-1] == "\\n": recept = recept[-1]`` sets the receptor to a
  newline on every row whose 4th field ends the line. These effects come
  from a scratch re-implementation; the packages were not executed. Use these
  raw files, not those loaders' matrices; see docs/provenance/bentley2016.md.
"""

from __future__ import annotations

from collections import Counter, defaultdict

from .common import RAW_ROOT, ArchiveMember, RemoteFile, acquire_source, verify_pypi_digest
from .distributions import (
    WORMNEUROATLAS_PACKAGE,
    WORMNEUROATLAS_VERSION,
    WORMNEUROATLAS_WHEEL,
    connectome_toolbox_file,
)

SOURCE_ID = "bentley2016"
CITATION = (
    "Bentley B, Branicky R, Barnes CL, Chew YL, Yemini E, Bullmore ET, Vértes PE, Schafer WR. "
    "The Multilayer Connectome of Caenorhabditis elegans. PLoS Comput Biol 12(12): e1005283 (2016). "
    "doi:10.1371/journal.pcbi.1005283"
)

PRIMARY = (
    "https://doi.org/10.1371/journal.pcbi.1005283.s004 (PLOS supporting-information item s004, "
    "'S1 Dataset', a zip; per the ConnectomeToolbox validation note it contains "
    "edge_lists/edgelist_MA.csv and edge_lists/edgelist_NP.csv). Also listed in the PLOS figshare "
    "collection https://plos.figshare.com/collections/The_Multilayer_Connectome_of_i_Caenorhabditis_elegans_i_/3647060 . "
    "Not reachable from this environment; byte comparison PENDING."
)

MA_TOOLBOX = "edgelist_MA.csv"
NP_TOOLBOX = "edgelist_NP.csv"
MA_WHEEL = "esconnectome_monoamines_Bentley_2016.csv"
NP_WHEEL = "esconnectome_neuropeptides_Bentley_2016.csv"
MA_PUMPPROBE = "pumpprobe__esconnectome_monoamines_Bentley_2016.csv"
NP_PUMPPROBE = "pumpprobe__esconnectome_neuropeptides_Bentley_2016.csv"

# leiferlab/pumpprobe: Randi et al.'s analysis code, at the same commit white1986 pins
# for aconnectome_ids.txt.
PUMPPROBE_REPO = "leiferlab/pumpprobe"
PUMPPROBE_COMMIT = "1dbc5e0a2b609d54bc9b1c90c73d4e3bf183d3c7"  # 2023-09-20


def _pumpprobe(name: str, filename: str, sha256: str, size: int, blob: str, primary: str, note: str) -> RemoteFile:
    return RemoteFile(
        url=f"https://raw.githubusercontent.com/{PUMPPROBE_REPO}/{PUMPPROBE_COMMIT}/pumpprobe/{name}",
        filename=filename,
        sha256=sha256,
        size=size,
        distributor=f"GitHub {PUMPPROBE_REPO} @ {PUMPPROBE_COMMIT} (Leifer lab; Randi et al. analysis code)",
        origin="secondary",
        primary_reference=primary,
        git_blob_sha1=blob,
        note=note,
    )


FILES = (
    connectome_toolbox_file(
        "cect/data/edgelist_MA.csv",
        sha256="5a206a6743479f4ae11eb82456378051c5d9aeb56ea5c1f82b121671c7fa2aa3",
        size=66718,
        git_blob_sha1="a83c4b617244d2fd29b8890bfe87f59b6aad9aa7",
        primary_reference=PRIMARY + " Corresponds to edge_lists/edgelist_MA.csv in the zip (per the toolbox).",
        note=(
            "Monoamine edge list: 2,626 rows of source,target,ligand,receptor; no header; LF. "
            "Added to the toolbox 2026-06-24 (commit f052c0d) as an extraction of the S1 Dataset zip."
        ),
    ),
    connectome_toolbox_file(
        "cect/data/edgelist_NP.csv",
        sha256="bec5f0c9526db1523ed73fb6a8b386de95d48a2fd5eae75a9a4889758102389b",
        size=202657,
        git_blob_sha1="7c23acadf96bccaf77718210c7fc1bd372c59727",
        primary_reference=PRIMARY + " Corresponds to edge_lists/edgelist_NP.csv in the zip (per the toolbox).",
        note=(
            "Neuropeptide edge list: 8,931 rows of source,target,peptide,receptor; no header; LF. "
            "Added to the toolbox 2026-06-24 (commit f052c0d) as an extraction of the S1 Dataset zip."
        ),
    ),
    ArchiveMember(
        archive=WORMNEUROATLAS_WHEEL,
        member="wormneuroatlas/data/esconnectome_monoamines_Bentley_2016.csv",
        filename=MA_WHEEL,
        sha256="16a1527028c6d8eece4d8a2d792e5a19cc416650e45066612180c42adc83654e",
        size=66771,
        primary_reference=PRIMARY
        + " Content: edge_lists/edgelist_MA.csv (per the toolbox) behind a header line not in the toolbox's extraction.",
        note=(
            "The monoamine file Randi's wormneuroatlas package loads (NeuroAtlas.esconn_sources). Equals a "
            "53-byte '#source neuron, ...' header line followed by the exact bytes of the toolbox's "
            "edgelist_MA.csv. Byte-identical to the pumpprobe copy."
        ),
    ),
    ArchiveMember(
        archive=WORMNEUROATLAS_WHEEL,
        member="wormneuroatlas/data/esconnectome_neuropeptides_Bentley_2016.csv",
        filename=NP_WHEEL,
        sha256="0abea9f09112e5d7af88823dd6e4ef91f181af7e919ce997fa12356c92c99e64",
        size=217695,
        primary_reference=PRIMARY
        + " Content: edge_lists/edgelist_NP.csv (per the toolbox) behind a header line, with a 5th field "
        "that is not in the toolbox's extraction.",
        note=(
            "The neuropeptide file Randi's wormneuroatlas package loads. 54-byte header line + the toolbox's "
            "8,931 rows, each with a 5th field appended (a receptor sequence name, filled on only some rows). "
            "That field is absent from the toolbox's S1 extraction, from the pumpprobe copy (blob 190868bd), "
            "and from that same blob in GitHub francescorandi/wormneuroatlas from its first commit of the file "
            "(3eed4b8, 2022-12-12; moved to data/ by 5ebe7f4, 2022-12-13); it appears in commit 7a7c653 "
            "(2022-12-23)."
        ),
    ),
    _pumpprobe(
        "esconnectome_monoamines_Bentley_2016.csv",
        MA_PUMPPROBE,
        sha256="16a1527028c6d8eece4d8a2d792e5a19cc416650e45066612180c42adc83654e",
        size=66771,
        blob="eaa17360c76e311ad690f68395537d1f7628c4e5",
        primary=PRIMARY
        + " Content: edge_lists/edgelist_MA.csv (per the toolbox) behind a header line not in the toolbox's extraction.",
        note=(
            "The monoamine file Randi et al.'s analysis code loads (pumpprobe Funatlas.esconn_sources). "
            "Byte-identical to the wheel's esconnectome_monoamines_Bentley_2016.csv (53-byte header line + "
            "toolbox edgelist_MA.csv). Same blob in pumpprobe since 8ceb2cb (2022-07-15). The copy at "
            "build/lib.linux-x86_64-3.8/pumpprobe/ is the same blob and is not acquired."
        ),
    ),
    _pumpprobe(
        "esconnectome_neuropeptides_Bentley_2016.csv",
        NP_PUMPPROBE,
        sha256="b8544d2bc947d0dc2ddf510f141f06b90acae2e39fea49f4cf7ec13c3f59de6f",
        size=202710,
        blob="190868bd841ccf4b2f671fb83396a9d9ca193a7e",
        primary=PRIMARY
        + " Content: edge_lists/edgelist_NP.csv (per the toolbox) behind a header line not in the toolbox's extraction.",
        note=(
            "The neuropeptide file Randi et al.'s analysis code loads (pumpprobe Funatlas.esconn_sources). "
            "The 53-byte monoamine-style header line (no trailing comma) + exactly the bytes of the toolbox's "
            "edgelist_NP.csv: 4 fields, no 5th field, so NOT the wheel's version. Same blob in pumpprobe since "
            "8ceb2cb (2022-07-15), and the first wormneuroatlas version of the file (3eed4b8). The copy at "
            "build/lib.linux-x86_64-3.8/pumpprobe/ is the same blob and is not acquired."
        ),
    ),
)


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


def _read(filename: str) -> tuple[dict, str | None, list[list[str]], bytes]:
    """Split one file into (byte facts, header line or None, data rows as raw fields, raw bytes).

    A first line that starts with "#" is treated as a header. Fields are split
    on "," with no stripping and no other change.
    """
    data = (RAW_ROOT / SOURCE_ID / filename).read_bytes()
    text = data.decode("ascii")
    lines = text.split("\n")
    final_newline = lines[-1] == ""
    if final_newline:
        lines = lines[:-1]
    header = lines[0] if lines and lines[0].startswith("#") else None
    body = lines[1:] if header is not None else lines
    rows = [line.split(",") for line in body]
    facts = {
        "bytes": len(data),
        "crlf_count": text.count("\r\n"),
        "cr_count": text.count("\r"),
        "ends_with_newline": final_newline,
        "header_line": header,
        "data_rows": len(rows),
        "fields_per_data_row": {str(k): v for k, v in sorted(Counter(len(r) for r in rows).items())},
    }
    return facts, header, rows, data


def _network_counts(rows: list[list[str]], list_sources: bool) -> dict:
    """Counts over the first four fields (source, target, ligand, receptor) of each row."""
    quads = [tuple(r[:4]) for r in rows]
    pairs_all = {(s, t) for s, t, _, _ in quads}
    pairs_off = {p for p in pairs_all if p[0] != p[1]}
    sources = {s for s, _, _, _ in quads}
    targets = {t for _, t, _, _ in quads}

    by_lig: dict[str, list] = defaultdict(list)
    by_lr: dict[tuple, list] = defaultdict(list)
    ligs_of_pair: dict[tuple, set] = defaultdict(set)
    for q in quads:
        by_lig[q[2]].append(q)
        by_lr[(q[2], q[3])].append(q)
        ligs_of_pair[(q[0], q[1])].add(q[2])

    lig_out = {}
    for lig in sorted(by_lig):
        qs = by_lig[lig]
        p = {(s, t) for s, t, _, _ in qs}
        srcs = {s for s, _, _, _ in qs}
        tgts = {t for _, t, _, _ in qs}
        d = {
            "rows": len(qs),
            "ordered_pairs_incl_self": len(p),
            "ordered_pairs_excl_self": sum(1 for a, b in p if a != b),
            "self_neurons": sorted(a for a, b in p if a == b),
            "receptors": sorted({q[3] for q in qs}),
            "n_sources": len(srcs),
            "n_targets": len(tgts),
            "n_neurons": len(srcs | tgts),
        }
        if list_sources:
            d["sources"] = sorted(srcs)
        lig_out[lig] = d

    lr_out = {}
    for lig, rec in sorted(by_lr):
        qs = by_lr[(lig, rec)]
        p = {(s, t) for s, t, _, _ in qs}
        srcs = {s for s, _, _, _ in qs}
        tgts = {t for _, t, _, _ in qs}
        lr_out[f"{lig} -> {rec}"] = {
            "rows": len(qs),
            "ordered_pairs": len(p),
            "self_pairs": sum(1 for a, b in p if a == b),
            "n_sources": len(srcs),
            "n_targets": len(tgts),
            "complete_bipartite_sources_x_targets": len(p) == len(srcs) * len(tgts),
        }

    rows_per_pair = Counter(Counter((s, t) for s, t, _, _ in quads).values())
    return {
        "rows": len(quads),
        "distinct_rows": len(set(quads)),
        "fields_with_surrounding_whitespace_or_empty": sum(
            1 for q in quads for x in q if x != x.strip() or x == ""
        ),
        "ligands": sorted(by_lig),
        "receptors": sorted({q[3] for q in quads}),
        "n_ligand_receptor_combinations": len(by_lr),
        "ordered_pairs_incl_self": len(pairs_all),
        "ordered_pairs_excl_self": len(pairs_off),
        "sum_over_ligands_of_ordered_pairs_excl_self": sum(v["ordered_pairs_excl_self"] for v in lig_out.values()),
        "self_pairs": len(pairs_all) - len(pairs_off),
        "self_rows": sum(1 for s, t, _, _ in quads if s == t),
        "ordered_pairs_with_more_than_one_ligand": sum(1 for v in ligs_of_pair.values() if len(v) > 1),
        "rows_per_ordered_pair_histogram": {str(k): v for k, v in sorted(rows_per_pair.items())},
        "n_neurons": len(sources | targets),
        "n_neurons_in_non_self_edges": len({n for p in pairs_off for n in p}),
        "n_sources": len(sources),
        "n_targets": len(targets),
        "n_both_source_and_target": len(sources & targets),
        "sources_never_targets": sorted(sources - targets),
        "by_ligand": lig_out,
        "by_ligand_receptor": lr_out,
    }


def record_counts() -> dict:
    """Counts computed from the six raw files only, with no names changed.

    Definitions:

    - ``files``: per file, the byte size, CR/CRLF counts, whether it ends with
      a newline, the header line (a first line starting with "#"), the number
      of data rows, and a histogram of fields per data row.
    - ``relationships``: byte-level relations between the toolbox, wheel and
      pumpprobe copies, checked directly on the bytes. Keys starting
      ``ma_wheel`` / ``np_wheel`` compare the wheel copies with the toolbox;
      keys starting ``ma_pumpprobe`` / ``np_pumpprobe`` compare the pumpprobe
      copies with the toolbox and the wheel.
    - ``networks.monoamine`` / ``networks.neuropeptide``: computed
      separately from each copy (toolbox, wheel, pumpprobe), using the first
      four fields of every data row: (source, target, ligand, receptor).
      Ligand = field 3 (a monoamine name, or a neuropeptide gene). If all
      copies give identical counts, they are printed once and
      ``computed_from`` lists every file; otherwise each differing copy is
      printed under its own key.
      - A "row" is one (source, target, ligand, receptor) line.
      - An "ordered pair" is a distinct (source, target).
      - "incl_self" counts pairs with source == target; "excl_self" omits
        them.
      - Per ligand, ordered pairs are de-duplicated across that ligand's
        receptors. This is the paper's stated monoamine rule: "Neurons
        expressing multiple receptors for a single monoamine receive a
        single edge from each sending neuron."
      - "self_pairs" counts distinct neurons with a self-row. "self_rows"
        counts self-rows including their receptor multiplicity.
      - ``n_sources`` / ``n_targets`` = distinct names in field 1 / field 2
        (senders / receivers); ``n_neurons`` = distinct names in field 1 ∪
        field 2, as raw strings.
      Each alternative edge definition is reported side by side; none is
      chosen.
    - ``neuron_names``: the sorted raw names in each network, taken from the
      toolbox copy, plus whether the wheel and pumpprobe copies have exactly
      the same names.
    - ``np_wheel_fifth_field``: what the wheel neuropeptide file's extra 5th
      field holds, per ligand -> receptor (value -> rows; "" = empty).
    """
    out: dict = {"files": {}, "relationships": {}, "networks": {}, "neuron_names": {}}
    parsed = {}
    for fn in (MA_TOOLBOX, NP_TOOLBOX, MA_WHEEL, NP_WHEEL, MA_PUMPPROBE, NP_PUMPPROBE):
        facts, header, rows, data = _read(fn)
        out["files"][fn] = facts
        parsed[fn] = (header, rows, data)

    _, _, ma_tb = parsed[MA_TOOLBOX]
    _, _, np_tb = parsed[NP_TOOLBOX]
    ma_w_header, _, ma_w = parsed[MA_WHEEL]
    np_w_header, np_w_rows, np_w = parsed[NP_WHEEL]
    ma_pp_header, _, ma_pp = parsed[MA_PUMPPROBE]
    np_pp_header, _, np_pp = parsed[NP_PUMPPROBE]

    ma_w_after_first_line = ma_w.split(b"\n", 1)[1]
    np_w_after_first_line = np_w.split(b"\n", 1)[1].decode("ascii")
    np_w_first4 = "".join(",".join(line.split(",")[:4]) + "\n" for line in np_w_after_first_line.split("\n")[:-1])
    ma_pp_after_first_line = ma_pp.split(b"\n", 1)[1]
    np_pp_after_first_line = np_pp.split(b"\n", 1)[1]
    rel = out["relationships"]
    rel["ma_wheel_first_line_bytes"] = len(ma_w) - len(ma_w_after_first_line)
    rel["ma_wheel_after_first_line_equals_toolbox_bytes"] = ma_w_after_first_line == ma_tb
    rel["np_wheel_first_line_bytes"] = len(np_w) - len(np_w_after_first_line.encode("ascii"))
    rel["np_wheel_after_first_line_fields_1_to_4_equals_toolbox_bytes"] = np_w_first4.encode("ascii") == np_tb
    rel["np_wheel_after_first_line_equals_toolbox_bytes"] = np_w_after_first_line.encode("ascii") == np_tb
    rel["ma_wheel_header"] = ma_w_header
    rel["np_wheel_header"] = np_w_header
    rel["ma_pumpprobe_equals_wheel_bytes"] = ma_pp == ma_w
    rel["ma_pumpprobe_first_line_bytes"] = len(ma_pp) - len(ma_pp_after_first_line)
    rel["ma_pumpprobe_after_first_line_equals_toolbox_bytes"] = ma_pp_after_first_line == ma_tb
    rel["ma_pumpprobe_header"] = ma_pp_header
    rel["np_pumpprobe_equals_wheel_bytes"] = np_pp == np_w
    rel["np_pumpprobe_first_line_bytes"] = len(np_pp) - len(np_pp_after_first_line)
    rel["np_pumpprobe_after_first_line_equals_toolbox_bytes"] = np_pp_after_first_line == np_tb
    rel["np_pumpprobe_after_first_line_equals_wheel_after_first_line_fields_1_to_4"] = (
        np_pp_after_first_line == np_w_first4.encode("ascii")
    )
    rel["np_pumpprobe_header"] = np_pp_header
    rel["np_pumpprobe_header_equals_ma_wheel_header"] = np_pp_header == ma_w_header

    for label, copies, list_sources in (
        ("monoamine", (MA_TOOLBOX, MA_WHEEL, MA_PUMPPROBE), True),
        ("neuropeptide", (NP_TOOLBOX, NP_WHEEL, NP_PUMPPROBE), False),
    ):
        counts = {fn: _network_counts(parsed[fn][1], list_sources) for fn in copies}
        reference = counts[copies[0]]
        same = [fn for fn in copies if counts[fn] == reference]
        rel[f"{label}_network_counts_identical_across_copies"] = len(same) == len(copies)
        out["networks"][label] = {"computed_from": same, **reference}
        for fn in copies:
            if fn not in same:
                out["networks"][f"{label}__{fn}"] = {"computed_from": [fn], **counts[fn]}

    for label, copies in (
        ("monoamine", (MA_TOOLBOX, MA_WHEEL, MA_PUMPPROBE)),
        ("neuropeptide", (NP_TOOLBOX, NP_WHEEL, NP_PUMPPROBE)),
    ):
        names = {fn: sorted({r[0] for r in parsed[fn][1]} | {r[1] for r in parsed[fn][1]}) for fn in copies}
        out["neuron_names"][label] = {
            "from_file": copies[0],
            "names": names[copies[0]],
            "identical_in_wheel_copy": names[copies[1]] == names[copies[0]],
            "identical_in_pumpprobe_copy": names[copies[2]] == names[copies[0]],
        }

    fifth: dict[str, Counter] = defaultdict(Counter)
    for r in np_w_rows:
        fifth[f"{r[2]} -> {r[3]}"][r[4] if len(r) > 4 else "<missing>"] += 1
    out["np_wheel_fifth_field"] = {
        "rows_nonempty": sum(1 for r in np_w_rows if len(r) > 4 and r[4] != ""),
        "rows_empty": sum(1 for r in np_w_rows if len(r) > 4 and r[4] == ""),
        "by_ligand_receptor": {k: dict(sorted(v.items())) for k, v in sorted(fifth.items())},
    }
    return out
