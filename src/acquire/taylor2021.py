"""Taylor et al. 2021, Cell 184:4329-4347: CeNGEN single-cell expression atlas.

The project uses the CeNGEN release labelled "021821", the one Randi et al.
bundle in the `wormneuroatlas` 0.0.7.3 wheel. The primary host
(cengen.org/downloads) is blocked in this environment, so every file here is a
SECONDARY copy; see docs/provenance/taylor2021.md.

Files acquired:

- The four thresholded gene x cell-type matrices of release 021821
  (threshold 1 "liberal" ... threshold 4 "stringent"). Which threshold the
  project uses is an OWNER decision, so all four are kept.
- ``cengen.h5``: the wheel author's float32 conversion of those four CSVs,
  which is what the package's ``Cengen`` class actually reads.
- Seven ``GenesExpressing-*.csv`` CeNGEN web-app exports (threshold 2) that the
  Randi et al. code (``wormneuroatlas`` and ``leiferlab/pumpprobe``) reads for
  innexin, neuropeptide and receptor expression.
- The two CeNGEN tables the Ripoll-Sanchez et al. 2023 neuropeptide connectome
  was built from (threshold 4, and threshold 3 for its sensitivity analysis),
  already expanded by those authors from cell types to 302 neurons.

Facts that later phases must respect, checked by ``record_counts``:

- The threshold CSVs have CRLF line endings, a leading unnamed row-number
  column, then ``gene_name`` and ``Wormbase_ID``, then 128 cell-type columns.
  Rows are genes, columns are cell types. Row ORDER differs between the four
  files (gene SETS are identical), so join on ``Wormbase_ID``, never on row
  position.
- A zero means "not called expressed at this threshold". Non-zero values are
  carried over unchanged across thresholds except for printing precision
  (some values printed with 7 significant digits in one file and 15 in
  another), so compare numerically, not as strings.
- ``cengen.h5`` stores ``tpm_th{1..4}`` TRANSPOSED: [cell type, gene].
- Cell-type columns are CeNGEN types, not neurons and not always canonical
  classes: e.g. AWC_OFF/AWC_ON, ASEL/ASER, IL2_DV/IL2_LR, RMD_DV/RMD_LR,
  RME_DV/RME_LR, VD_DD (one merged column), VC and VC_4_5, VB plus VB01 and
  VB02, DB plus DB01, DA plus DA9, VA plus VA12. No names are changed here.
"""

from __future__ import annotations

import collections
import csv
import io
import re

from .common import RAW_ROOT, ArchiveMember, RemoteFile, acquire_source, verify_pypi_digest
from .distributions import (
    WORMNEUROATLAS_PACKAGE,
    WORMNEUROATLAS_VERSION,
    WORMNEUROATLAS_WHEEL,
)

SOURCE_ID = "taylor2021"
CITATION = (
    "Taylor SR, Santpere G, Weinreb A, Barrett A, Reilly MB, Xu C, Varol E, Oikonomou P, "
    "Glenwinkel L, McWhirter R, Poff A, Basavaraju M, Rafi I, Yemini E, Cook SJ, Abrams A, "
    "Vidal B, Cros C, Tavazoie S, Sestan N, Hammarlund M, Hobert O, Miller DM 3rd. "
    "Molecular topography of an entire nervous system. Cell 184(16), 4329-4347.e23 (2021). "
    "doi:10.1016/j.cell.2021.06.023"
)
PRIMARY = (
    "https://www.cengen.org/downloads/ (CeNGEN portal; thresholded csv files, thresholds 1-4, "
    "release 021821 per the file names); paper doi:10.1016/j.cell.2021.06.023"
)
PRIMARY_APP_EXPORT = (
    "CeNGEN L4 web app (https://cengen.shinyapps.io/L4app/, 'Gene expression by cell type', "
    "threshold 2) as exported by the Randi et al. authors; underlying data: " + PRIMARY
)

# --- Ripoll-Sanchez et al. 2023 first-author repository --------------------
# Declared here (not in distributions.py) because only these two files are
# taken from it by this source. Same commit as src/acquire/ripollsanchez2023.py
# pins as its HEAD.
NPC_REPO = "LidiaRipollSanchez/Neuropeptide-Connectome"
NPC_HEAD = "6689619236ba1b4681a9a77b3d918d513416336c"  # 2024-09-20, master head
PRIMARY_RS = (
    "Ripoll-Sanchez et al. 2023, Neuron 111:3570, doi:10.1016/j.neuron.2023.09.043; input data "
    f"in the authors' repository https://github.com/{NPC_REPO} ; underlying expression: " + PRIMARY
)


def _quote(path: str) -> str:
    return path.replace("%", "%25").replace(" ", "%20").replace("&", "%26").replace("#", "%23")


def _npc_file(path: str, *, sha256: str, size: int, git_blob_sha1: str, note: str) -> RemoteFile:
    return RemoteFile(
        url=f"https://raw.githubusercontent.com/{NPC_REPO}/{NPC_HEAD}/{_quote(path)}",
        filename=path.rsplit("/", 1)[-1],
        sha256=sha256,
        size=size,
        distributor=f"GitHub {NPC_REPO} @ {NPC_HEAD} (L. Ripoll-Sanchez, first author of Ripoll-Sanchez et al. 2023)",
        origin="secondary",
        primary_reference=PRIMARY_RS,
        git_blob_sha1=git_blob_sha1,
        note=note,
    )


def _wheel(member: str, *, sha256: str, size: int, note: str, primary: str = PRIMARY) -> ArchiveMember:
    return ArchiveMember(
        archive=WORMNEUROATLAS_WHEEL,
        member=f"wormneuroatlas/data/{member}",
        filename=member,
        sha256=sha256,
        size=size,
        primary_reference=primary,
        note=note,
    )


_SAME_ON_GITHUB = (
    " Byte-identical (same git blob {blob}) to francescorandi/wormneuroatlas @ "
    "b2e13d88b670efcb3438aeacba2ad4bd6c383933 wormneuroatlas/data/{name}."
)
_SAME_IN_PUMPPROBE = " Also byte-identical to leiferlab/pumpprobe @ 1dbc5e0a2b609d54bc9b1c90c73d4e3bf183d3c7 pumpprobe/{name}."

THRESHOLD_FILES = (
    ("cengen_021821_liberal_threshold1.csv", 1),
    ("cengen_021821_medium_threshold2.csv", 2),
    ("cengen_021821_conservative_threshold3.csv", 3),
    ("cengen_021821_stringent_threshold4.csv", 4),
)
SINGLE_GENE_EXPORTS = (
    ("GenesExpressing-daf-2-thrs2.csv", "daf-2"),
    ("GenesExpressing-npr-11-thrs2.csv", "npr-11"),
    ("GenesExpressing-npr-4-thrs2.csv", "npr-4"),
    ("GenesExpressing-pdfr-1-thrs2.csv", "pdfr-1"),
)
MATRIX_EXPORTS = (
    "GenesExpressing-neuropeptide-receptors.csv",
    "GenesExpressing-neuropeptides.csv",
    "GenesExpressing-unc-7-unc-9-inx-_-eat-5-thrs2.csv",
)
RS_TABLES = (
    ("30072020_CENGEN_threshold4_expression_NPP_NPR_MR_LGC_allneurons.csv", 4),
    ("13112020_CENGEN_threshold3_expression_NPP_NPR_MR_LGC_allneurons.csv", 3),
)

FILES = (
    _wheel(
        "cengen_021821_liberal_threshold1.csv",
        sha256="74ac7e400f3f841d8784946db67bdbc211598c8682020ef57730b29e564e0cb6",
        size=14921760,
        note="CeNGEN release 021821, threshold 1 (most permissive). Genes x 128 cell types; 0 = not called "
        "expressed, >0 = expression value (TPM per cengen.org)."
        + _SAME_ON_GITHUB.format(blob="c2a1e19165841b5d560c2868a05a30a566c948fa", name="cengen_021821_liberal_threshold1.csv"),
    ),
    _wheel(
        "cengen_021821_medium_threshold2.csv",
        sha256="de03fc03cacdf4c1aa7ffd7565df89135ed72eab68d0b3cf03f542932abc63c8",
        size=13555783,
        note="CeNGEN release 021821, threshold 2 (medium; cengen.org's recommended default)."
        + _SAME_ON_GITHUB.format(blob="8f607c34d578c1856308d9f946d02ef013ee2765", name="cengen_021821_medium_threshold2.csv"),
    ),
    _wheel(
        "cengen_021821_conservative_threshold3.csv",
        sha256="2454624b7b0409b8ce62c5687c431e0c9b9dd5f38148e0bc9b0fb48c26887236",
        size=11612055,
        note="CeNGEN release 021821, threshold 3 (more conservative)."
        + _SAME_ON_GITHUB.format(blob="e7ae755fa5c9c3a1d0adbd3cb226240361cdb00a", name="cengen_021821_conservative_threshold3.csv"),
    ),
    _wheel(
        "cengen_021821_stringent_threshold4.csv",
        sha256="478791be7f43d46e11cb751cf12016ae517d59b34db3325f29703646853df875",
        size=9818818,
        note="CeNGEN release 021821, threshold 4 (most stringent; the package's default th=4, and the "
        "threshold Ripoll-Sanchez et al. used)."
        + _SAME_ON_GITHUB.format(blob="cd18e969c1f862eeb754a20065553666f407f3b8", name="cengen_021821_stringent_threshold4.csv"),
    ),
    _wheel(
        "cengen.h5",
        sha256="d8e6f6f2a25e05211676cfd9c3dd18b8a8bb5c3db4d673fd87b61ed91637ed23",
        size=32852608,
        note="Derived by the wheel author from the four 021821 CSVs (scripts/build_datasets/"
        "cengen_make_h5_from_csv.py in francescorandi/wormneuroatlas): tpm_th{1..4} = float32 of the CSV "
        "values, TRANSPOSED to [cell type, gene]. This is what wormneuroatlas.Cengen reads."
        + _SAME_ON_GITHUB.format(blob="cef51ed6f9996ed9963c5d34cbc32a1518e8a91b", name="cengen.h5"),
    ),
    _wheel(
        "GenesExpressing-daf-2-thrs2.csv",
        sha256="bf2d2e920ad018a1993948f115ba9d7d8b2f11f7f8274f8e858ee423f020683b",
        size=1905,
        primary=PRIMARY_APP_EXPORT,
        note="CeNGEN app export: cell types expressing daf-2 at threshold 2, values to 3 decimals."
        + _SAME_ON_GITHUB.format(blob="b7011ae72a5b41d65155af45a1339941326cca13", name="GenesExpressing-daf-2-thrs2.csv")
        + _SAME_IN_PUMPPROBE.format(name="GenesExpressing-daf-2-thrs2.csv"),
    ),
    _wheel(
        "GenesExpressing-npr-11-thrs2.csv",
        sha256="37e5fadb7c00f4b382388172a28afca631132bced87c3c0f57a0619230000f73",
        size=652,
        primary=PRIMARY_APP_EXPORT,
        note="CeNGEN app export: cell types expressing npr-11 at threshold 2 (read by pumpprobe RID figure "
        "scripts)." + _SAME_ON_GITHUB.format(blob="c9230d0f5f8faf3b4246ae7c47b3ea1866ad1c66", name="GenesExpressing-npr-11-thrs2.csv")
        + _SAME_IN_PUMPPROBE.format(name="GenesExpressing-npr-11-thrs2.csv"),
    ),
    _wheel(
        "GenesExpressing-npr-4-thrs2.csv",
        sha256="20df91002182487d6bb6e24dff82324ff4281a21b0f552dae7c3fe1634e93a8a",
        size=1294,
        primary=PRIMARY_APP_EXPORT,
        note="CeNGEN app export: cell types expressing npr-4 at threshold 2 (read by pumpprobe RID figure "
        "scripts)." + _SAME_ON_GITHUB.format(blob="38f7afd37c7223b7c251f9b4710c742acd8e270b", name="GenesExpressing-npr-4-thrs2.csv")
        + _SAME_IN_PUMPPROBE.format(name="GenesExpressing-npr-4-thrs2.csv"),
    ),
    _wheel(
        "GenesExpressing-pdfr-1-thrs2.csv",
        sha256="1a0523ddf5633e21a9fc7dcbb0daad4047c3ed67d1e8bf910717d76676ff7515",
        size=1999,
        primary=PRIMARY_APP_EXPORT,
        note="CeNGEN app export: cell types expressing pdfr-1 at threshold 2 (read by pumpprobe RID figure "
        "scripts)." + _SAME_ON_GITHUB.format(blob="ae25011375351f7e2b4b6e5a348a6c7ae1d2c7a2", name="GenesExpressing-pdfr-1-thrs2.csv")
        + _SAME_IN_PUMPPROBE.format(name="GenesExpressing-pdfr-1-thrs2.csv"),
    ),
    _wheel(
        "GenesExpressing-neuropeptide-receptors.csv",
        sha256="1e88e1047a8a8ecd545907f7336212889e59d8dd1ff4ce9731d9c3bf935087c9",
        size=80763,
        primary=PRIMARY_APP_EXPORT,
        note="CeNGEN app export: 141 receptor genes x 128 cell types, threshold 2 (NeuroAtlas/Funatlas "
        "fname_neuropeptide_receptors). One row (F59D12.1) carries a sequence name in the WormBase-ID column."
        + _SAME_ON_GITHUB.format(blob="848f504fae31f9c5050c339f70fffb4968a57c25", name="GenesExpressing-neuropeptide-receptors.csv")
        + _SAME_IN_PUMPPROBE.format(name="GenesExpressing-neuropeptide-receptors.csv"),
    ),
    _wheel(
        "GenesExpressing-neuropeptides.csv",
        sha256="6f47ec2b853d4aa3433ea98b75253024f01c585c60be01fa45a27fb9ec99a07b",
        size=63665,
        primary=PRIMARY_APP_EXPORT,
        note="CeNGEN app export: 137 neuropeptide genes x 128 cell types, threshold 2 (NeuroAtlas/Funatlas "
        "fname_neuropeptides)."
        + _SAME_ON_GITHUB.format(blob="16ad3744224f52e3fd7ac720d1ee66069b65453b", name="GenesExpressing-neuropeptides.csv")
        + _SAME_IN_PUMPPROBE.format(name="GenesExpressing-neuropeptides.csv"),
    ),
    _wheel(
        "GenesExpressing-unc-7-unc-9-inx-_-eat-5-thrs2.csv",
        sha256="ac96905ac5d89068412966cd8e6ab0bca653fe3d94394b7aec44b22fb2bb7954",
        size=12761,
        primary=PRIMARY_APP_EXPORT,
        note="CeNGEN app export: 21 innexin genes x 128 cell types, threshold 2 (NeuroAtlas/Funatlas "
        "fname_innexins). UTF-8 BOM; AWC columns named AWCOFF/AWCON here, AWC_OFF/AWC_ON elsewhere."
        + _SAME_ON_GITHUB.format(blob="2ccf9f9eb6c74cace0c14645be24aa0112bf929b", name="GenesExpressing-unc-7-unc-9-inx-_-eat-5-thrs2.csv")
        + _SAME_IN_PUMPPROBE.format(name="GenesExpressing-unc-7-unc-9-inx-_-eat-5-thrs2.csv"),
    ),
    _npc_file(
        "Scripts & data/30072020_CENGEN_threshold4_expression_NPP_NPR_MR_LGC_allneurons.csv",
        sha256="b3055e3e954273a9f15e9ad288f3d7e0f14f6a5ad7c2580861cf7a7750f4f3e5",
        size=354171,
        git_blob_sha1="4401afd4815514a75e9da7e0de936fe7a8aac0f0",
        note="Ripoll-Sanchez et al.'s CeNGEN threshold-4 input (362 WormBase genes x 302 neurons, ';'-separated, "
        "CRLF). Values equal the 021821 threshold-4 matrix (record_counts checks this); cell types were "
        "expanded to neurons by those authors.",
    ),
    _npc_file(
        "Sensitivity Analysis/Input data/13112020_CENGEN_threshold3_expression_NPP_NPR_MR_LGC_allneurons.csv",
        sha256="72fdc4f4c617d70c1606d7d6d8fd9e7c2d53514478669c770f00d43327df5b80",
        size=394413,
        git_blob_sha1="d26fca9c52c95ef47e5f90330b0b7865236fee53",
        note="Ripoll-Sanchez et al.'s CeNGEN threshold-3 input for their sensitivity analysis (362 genes x 302 "
        "neurons, ';'-separated, UTF-8 BOM). Values equal the 021821 threshold-3 matrix (record_counts checks this).",
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


# ---------------------------------------------------------------------------
# Record counts
# ---------------------------------------------------------------------------

# Values are compared numerically with this relative tolerance, because the
# same number is printed with different precision in different files (down to
# 7 significant digits). Zero/non-zero status must agree exactly.
REL_TOL = 1e-5
_WBGENE = re.compile(r"WBGene\d{8}")


def _read_text_table(path, delimiter=","):
    raw = path.read_bytes()
    facts = {
        "bytes": len(raw),
        "utf8_bom": raw.startswith(b"\xef\xbb\xbf"),
        "crlf_line_ends": raw.count(b"\r\n"),
        "lf_only_line_ends": raw.count(b"\n") - raw.count(b"\r\n"),
        "ends_with_newline": raw.endswith(b"\n"),
    }
    text = raw.decode("utf-8-sig")
    rows = list(csv.reader(io.StringIO(text, newline=""), delimiter=delimiter))
    return facts, rows


def _close(a, b):
    """Elementwise: same zero status and |a-b| <= REL_TOL*|b|."""
    import numpy as np

    return ((a == 0) == (b == 0)) & (np.abs(a - b) <= REL_TOL * np.abs(b))


def _load_thresholds(raw):
    import numpy as np

    out = {}
    for name, th in THRESHOLD_FILES:
        facts, rows = _read_text_table(raw / name)
        header, body = rows[0], rows[1:]
        vals = np.array([[float(x) for x in r[3:]] for r in body], dtype=np.float64)
        out[th] = {
            "name": name,
            "facts": facts,
            "header": header,
            "body": body,
            "celltypes": header[3:],
            "names": [r[1] for r in body],
            "wbids": [r[2] for r in body],
            "vals": vals,
            "row_of_wbid": {r[2]: i for i, r in enumerate(body)},
            "row_of_name": {r[1]: i for i, r in enumerate(body)},
        }
    return out


def _threshold_file_counts(t):
    import numpy as np

    v = t["vals"]
    body = t["body"]
    nz = v != 0
    col_sums = v.sum(axis=0)
    col_nz = nz.sum(axis=0)
    ct = t["celltypes"]
    return {
        **t["facts"],
        "header_first3": t["header"][:3],
        "n_gene_rows": len(body),
        "n_celltype_columns": len(ct),
        "row_lengths": sorted(collections.Counter(len(r) for r in body).items()),
        "first_column_is_1_to_n": [r[0] for r in body] == [str(i) for i in range(1, len(body) + 1)],
        "n_unique_gene_name": len(set(t["names"])),
        "n_unique_wormbase_id": len(set(t["wbids"])),
        "n_wormbase_id_not_WBGene_pattern": sum(1 for w in t["wbids"] if not _WBGENE.fullmatch(w)),
        "n_gene_names_containing_period": sum(1 for n in t["names"] if "." in n),
        "n_cells": int(v.size),
        "n_nonzero": int(nz.sum()),
        "n_zero": int((~nz).sum()),
        "n_negative": int((v < 0).sum()),
        "n_non_finite": int((~np.isfinite(v)).sum()),
        "n_nonzero_below_1": int(((v > 0) & (v < 1)).sum()),
        "min_nonzero": float(v[nz].min()),
        "max_value": float(v.max()),
        "n_rows_all_zero": int((~nz.any(axis=1)).sum()),
        "n_columns_all_zero": int((~nz.any(axis=0)).sum()),
        "celltype_column_sum_min": round(float(col_sums.min()), 3),
        "celltype_column_sum_max": round(float(col_sums.max()), 3),
        "celltype_nonzero_genes_min": [int(col_nz.min()), ct[int(col_nz.argmin())]],
        "celltype_nonzero_genes_max": [int(col_nz.max()), ct[int(col_nz.argmax())]],
    }


def _cross_threshold_counts(ths):
    import numpy as np

    out = {}
    base = ths[1]
    out["celltype_columns_identical_in_all_four"] = all(ths[k]["celltypes"] == base["celltypes"] for k in ths)
    out["wormbase_id_sets_identical_in_all_four"] = all(set(ths[k]["wbids"]) == set(base["wbids"]) for k in ths)
    pairs = {k: set(zip(ths[k]["wbids"], ths[k]["names"])) for k in ths}
    out["wbid_name_pairs_identical_in_all_four"] = all(pairs[k] == pairs[1] for k in ths)
    out["row_order_identical_to_threshold1"] = {f"th{k}": ths[k]["wbids"] == base["wbids"] for k in sorted(ths)}

    for loose, strict in ((1, 2), (2, 3), (3, 4), (1, 4)):
        a, b = ths[loose], ths[strict]
        order = [a["row_of_wbid"][w] for w in b["wbids"]]  # align a's rows to b's order
        va = a["vals"][order]
        vb = b["vals"]
        nza, nzb = va != 0, vb != 0
        both = nza & nzb
        sa = [a["body"][i] for i in order]
        sb = b["body"]
        n_str_same = 0
        for ra, rb in zip(sa, sb):
            for x, y in zip(ra[3:], rb[3:]):
                if y != "0" and x != "0" and x == y:
                    n_str_same += 1
        with np.errstate(divide="ignore", invalid="ignore"):
            rel = np.where(both, np.abs(va - vb) / np.abs(vb), 0.0)
        out[f"th{strict}_vs_th{loose}"] = {
            "nonzero_in_strict_subset_of_nonzero_in_loose": bool(np.all(~nzb | nza)),
            "n_nonzero_in_both": int(both.sum()),
            "n_nonzero_only_in_loose": int((nza & ~nzb).sum()),
            "n_nonzero_both_string_identical": n_str_same,
            "n_nonzero_both_numerically_different": int((both & (va != vb)).sum()),
            "max_relative_difference_where_both_nonzero": float(f"{rel.max():.3e}"),
        }
    return out


def _h5_counts(raw, ths):
    import h5py
    import numpy as np

    out = {}
    with h5py.File(raw / "cengen.h5", "r") as f:
        datasets = {}
        f.visititems(lambda n, o: datasets.__setitem__(n, [list(o.shape), str(o.dtype)]) if isinstance(o, h5py.Dataset) else None)
        out["datasets"] = dict(sorted(datasets.items()))
        out["n_file_attrs"] = len(f.attrs)
        ids = [x.decode("utf-8") for x in f["neuron_ids"][:]]
        out["neuron_ids_equal_csv_celltype_header"] = ids == ths[1]["celltypes"]
        for th in sorted(ths):
            t = ths[th]
            names = [x.decode("utf-8") for x in f[f"gene_names_th{th}"][:]]
            wbids = [x.decode("utf-8") for x in f[f"gene_wbids_th{th}"][:]]
            tpm = f[f"tpm_th{th}"][:]
            out[f"th{th}"] = {
                "gene_names_equal_csv_row_order": names == t["names"],
                "gene_wbids_equal_csv_row_order": wbids == t["wbids"],
                "tpm_shape_is_celltype_by_gene": list(tpm.shape) == [len(t["celltypes"]), len(t["wbids"])],
                "tpm_equals_float32_of_csv_transposed": bool(np.array_equal(tpm, t["vals"].T.astype(np.float32))),
                "tpm_n_nonzero": int((tpm != 0).sum()),
            }
    return out


def _single_gene_export_counts(raw, ths, name, gene):
    import numpy as np

    facts, rows = _read_text_table(raw / name)
    header, body = rows[0], rows[1:]
    listed = {r[1]: float(r[2]) for r in body}
    out = {**facts, "header": header, "n_rows": len(body), "gene_taken_from_filename": gene}
    ct = ths[2]["celltypes"]
    out["listed_celltypes_not_in_021821_header"] = sorted(c for c in listed if c not in ct)
    out["values_sorted_descending"] = all(float(body[i][2]) >= float(body[i + 1][2]) for i in range(len(body) - 1))
    out["gene_name_present_in_021821"] = gene in ths[2]["row_of_name"]
    if out["gene_name_present_in_021821"]:
        for th in sorted(ths):
            t = ths[th]
            row = t["vals"][t["row_of_name"][gene]]
            nz = {c for c, x in zip(t["celltypes"], row) if x != 0}
            out[f"listed_set_equals_021821_nonzero_set_th{th}"] = set(listed) == nz
        row2 = dict(zip(ct, ths[2]["vals"][ths[2]["row_of_name"][gene]]))
        diffs = [abs(x - row2[c]) for c, x in listed.items() if c in row2]
        out["max_abs_difference_vs_th2"] = float(f"{max(diffs):.3e}") if diffs else None
    return out


def _matrix_export_counts(raw, ths, name):
    import numpy as np

    facts, rows = _read_text_table(raw / name)
    header, body = rows[0], rows[1:]
    cols = header[4:]
    ct = ths[2]["celltypes"]
    out = {
        **facts,
        "header_first4": header[:4],
        "n_gene_rows": len(body),
        "n_celltype_columns": len(cols),
        "row_lengths": sorted(collections.Counter(len(r) for r in body).items()),
        "threshold_column_values": sorted(collections.Counter(r[3] for r in body).items()),
        "export_columns_not_in_021821_header": sorted(c for c in cols if c not in ct),
        "021821_columns_not_in_export_header": sorted(c for c in ct if c not in cols),
        "n_nonzero": sum(1 for r in body for x in r[4:] if float(x) != 0),
    }
    shared = [c for c in cols if c in ct]
    ei = [cols.index(c) for c in shared]
    out["n_columns_compared_by_exact_name"] = len(shared)
    absent = []
    match_counts = {f"th{th}": 0 for th in sorted(ths)}
    for r in body:
        wb = r[2]
        if wb not in ths[2]["row_of_wbid"]:
            vals = np.array([float(x) for x in r[4:]])
            absent.append([r[1], wb, int((vals != 0).sum())])
            continue
        vals = np.array([float(r[4 + j]) for j in ei])
        for th in sorted(ths):
            t = ths[th]
            ref = t["vals"][t["row_of_wbid"][wb]][[ct.index(c) for c in shared]]
            if bool(np.all(_close(vals, ref))):
                match_counts[f"th{th}"] += 1
    out["rows_whose_id_column_is_not_a_021821_wormbase_id"] = sorted(absent)
    out["rows_equal_to_021821_row_same_wbid"] = match_counts
    # For rows whose id is not found, look for 021821 th2 rows with identical values (no name matching).
    found = {}
    if absent and not out["export_columns_not_in_021821_header"]:
        t = ths[2]
        idx = [ct.index(c) for c in cols]
        ref = t["vals"][:, idx]
        for gname, wb, _ in absent:
            r = next(rr for rr in body if rr[1] == gname and rr[2] == wb)
            vals = np.array([float(x) for x in r[4:]])
            hit = np.flatnonzero(np.all(_close(vals[None, :], ref), axis=1))
            found[gname] = sorted([t["names"][i], t["wbids"][i]] for i in hit)
    out["absent_rows_value_identical_th2_rows"] = dict(sorted(found.items()))
    return out


def _rs_table_counts(raw, ths, name, stated_th):
    import numpy as np

    facts, rows = _read_text_table(raw / name, delimiter=";")
    header, body = rows[0], rows[1:]
    neurons = header[1:]
    genes = [r[0] for r in body]
    vals = np.array([[float(x) for x in r[1:]] for r in body], dtype=np.float64)
    out = {
        **facts,
        "delimiter": ";",
        "header_first_cell": header[0],
        "n_gene_rows": len(body),
        "n_neuron_columns": len(neurons),
        "n_unique_neuron_columns": len(set(neurons)),
        "neuron_columns": neurons,
        "row_lengths": sorted(collections.Counter(len(r) for r in body).items()),
        "n_row_ids_matching_WBGene_pattern": sum(1 for g in genes if _WBGENE.fullmatch(g)),
        "n_row_ids_present_in_021821": sum(1 for g in genes if g in ths[2]["row_of_wbid"]),
        "n_cells": int(vals.size),
        "n_nonzero": int((vals != 0).sum()),
        "threshold_in_filename": stated_th,
    }
    present = [i for i, g in enumerate(genes) if g in ths[2]["row_of_wbid"]]
    a = vals[present]  # genes x neurons
    per_th = {}
    for th in sorted(ths):
        t = ths[th]
        b = t["vals"][[t["row_of_wbid"][genes[i]] for i in present]]  # genes x celltypes
        m = np.zeros((a.shape[1], b.shape[1]), dtype=bool)  # neurons x celltypes
        for j in range(b.shape[1]):
            m[:, j] = np.all(_close(a, b[:, j : j + 1]), axis=0)
        nmatch = m.sum(axis=1)
        entry = {
            "n_neurons_matching_exactly_one_celltype_column": int((nmatch == 1).sum()),
            "n_neurons_matching_no_column": int((nmatch == 0).sum()),
            "n_neurons_matching_several_columns": int((nmatch > 1).sum()),
        }
        if (nmatch == 1).sum() > 0:
            entry["neuron_to_matching_021821_column"] = {
                n: [t["celltypes"][j] for j in np.flatnonzero(m[i])] for i, n in sorted(enumerate(neurons), key=lambda x: x[1])
            }
            used = set(np.flatnonzero(m.any(axis=0)).tolist())
            entry["021821_columns_matched_by_no_neuron"] = [c for j, c in enumerate(t["celltypes"]) if j not in used]
        per_th[f"th{th}"] = entry
    out["value_match_against_021821"] = per_th
    return out


def record_counts() -> dict:
    """Counts computed from the raw files only, with no naming decisions applied.

    Definitions (one block per file, plus cross-file checks):

    - Threshold CSVs: ``n_gene_rows`` = data rows (genes); ``n_celltype_columns``
      = header fields after the first three (``""``, ``gene_name``,
      ``Wormbase_ID``); ``n_nonzero`` = cells whose value parses to a number
      other than 0; ``n_rows_all_zero`` = genes with no non-zero cell type;
      ``celltype_column_sum_*`` = per-cell-type sum of all values (for a TPM
      table the unthresholded sum would be 1e6); ``celltype_nonzero_genes_*``
      = [count, cell type] with the fewest / most non-zero genes.
    - ``celltype_columns``: the 128 header names, in file order, unchanged.
    - ``cross_threshold``: rows are aligned by Wormbase_ID (never by position,
      which differs). ``nonzero_in_strict_subset_of_nonzero_in_loose`` checks
      nesting; ``n_nonzero_both_*`` compare values present in both files as
      strings and as numbers.
    - ``cengen.h5``: checks that each ``tpm_thN`` equals the float32 cast of
      the CSV matrix transposed to [cell type, gene], with the same gene order.
    - App exports: for single-gene exports, whether the listed cell types equal
      the gene's non-zero cell types in each 021821 file (gene taken from the
      file name, matched to ``gene_name`` exactly). For matrix exports, rows
      are matched by the WormBase ID column and compared on columns with
      exactly the same name (relative tolerance ``REL_TOL``); rows whose id is
      not a 021821 WormBase ID are listed, with any th2 row of identical
      values.
    - Ripoll-Sanchez tables: each of the 302 neuron columns is compared with
      every 021821 cell-type column, at every threshold, over all 362 genes
      (same zero pattern, values within ``REL_TOL``). The matching columns
      are reported as found; this is a value match, not a naming rule.
    """
    raw = RAW_ROOT / SOURCE_ID
    ths = _load_thresholds(raw)
    out: dict = {
        "celltype_columns": ths[1]["celltypes"],
        "celltype_columns_containing_underscore": [c for c in ths[1]["celltypes"] if "_" in c],
        "celltype_columns_containing_digit": [c for c in ths[1]["celltypes"] if any(ch.isdigit() for ch in c)],
        "compare_rel_tol": REL_TOL,
    }
    for th in sorted(ths):
        out[ths[th]["name"]] = _threshold_file_counts(ths[th])
    out["cross_threshold"] = _cross_threshold_counts(ths)
    out["cengen.h5"] = _h5_counts(raw, ths)
    for name, gene in SINGLE_GENE_EXPORTS:
        out[name] = _single_gene_export_counts(raw, ths, name, gene)
    for name in MATRIX_EXPORTS:
        out[name] = _matrix_export_counts(raw, ths, name)
    for name, th in RS_TABLES:
        out[name] = _rs_table_counts(raw, ths, name, th)
    return out
