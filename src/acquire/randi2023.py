"""Randi et al. 2023, Nature 623:406-414: signal propagation atlas, WT and unc-31.

Two data releases of the atlas are acquired, both published by the first
author, F. Randi:

- ``funatlas.h5``: the 2023-06-28 release (git 827e26b, "updated data after
  fix in export script"), bundled in the ``wormneuroatlas`` 0.0.7.3 wheel on
  PyPI. It reproduces the Nature article's numbers (23,433 measured head
  pairs, 1,310 at q<0.05, 53 strict extrasynaptic candidates).
- ``funatlas_release-2023-06-14.h5``: the previous release (git df07176,
  "updated data"), from the author's GitHub repository. It reproduces the
  arXiv preprint's 23,427. Every unc-31 q-value differs between the two
  releases.

The primary locations (FunCoNN, OSF) are blocked in this environment; see
docs/provenance/randi2023.md.

Facts about the atlas files, established by inspection and partly emitted by
``record_counts``:

- ``neuron_ids`` is a 300-entry, alphabetically sorted |S5 array. Its order
  differs from the package's ``neuron_ids.txt``, so the matrices must be
  indexed with the h5's own ids.
- AWC appears as "AWCON" and "AWCOF" ("AWCOFF" truncated to 5 bytes). There
  is no AWCL/AWCR and no CANL/CANR.
- Matrices are indexed [responding, stimulated]: rows i respond, columns j
  are stimulated (authors' code: "occ1[i,j] is the number of occurrences of
  the response of i following a stimulation of j").
- ``occ1`` counts stimulation/response occurrences, including trials that
  were later discarded. ``len(dFF_all[i, j])`` is the number of retained
  trials, and q is finite exactly when at least one trial was retained.
"""

from __future__ import annotations

import json
from collections import Counter

from .common import RAW_ROOT, ArchiveMember, RemoteFile, acquire_source, verify_pypi_digest
from .distributions import (
    WORMNEUROATLAS_PACKAGE,
    WORMNEUROATLAS_VERSION,
    WORMNEUROATLAS_WHEEL,
)

SOURCE_ID = "randi2023"
CITATION = (
    "Randi F, Sharma AK, Dvali S, Leifer AM. Neural signal propagation atlas of "
    "Caenorhabditis elegans. Nature 623, 406-414 (2023). doi:10.1038/s41586-023-06683-4"
)
PRIMARY_ATLAS = (
    "https://funconn.princeton.edu/ (interactive atlas); machine-readable datasets on OSF "
    "doi:10.17605/OSF.IO/E2SYT (https://osf.io/e2syt/). Which OSF file corresponds to this h5 is UNVERIFIED."
)
PRIMARY_METADATA = (
    "No portal or journal copy known: author package metadata. Byte-identical copy of the ganglia file at "
    "github.com/leiferlab/pumpprobe @1dbc5e0a pumpprobe/aconnectome_ids_ganglia.json (the paper's analysis code)."
)

AUTHOR_REPO = "francescorandi/wormneuroatlas"
RELEASE_2023_06_14_COMMIT = "df07176e2b369d13c683e2361651277fac5d0346"

# The release whose numbers match the Nature article. Later phases read this file.
ATLAS_FILE = "funatlas.h5"
ATLAS_RELEASES = {
    "2023-06-28": "funatlas.h5",
    "2023-06-14": "funatlas_release-2023-06-14.h5",
}

FILES = (
    ArchiveMember(
        archive=WORMNEUROATLAS_WHEEL,
        member="wormneuroatlas/data/funatlas.h5",
        filename="funatlas.h5",
        sha256="53a99055667b853e1d3d6be573ec2613d38c9f6989f302ec38ecd38dd50c7975",
        size=18266176,
        primary_reference=PRIMARY_ATLAS,
        note=(
            "Signal propagation atlas, WT and unc-31, release of 2023-06-28 (time_compiled "
            "2023-06-28_19-52-14; git 827e26b 'updated data after fix in export script', blob fa122efd). "
            "Reproduces the Nature article's counts."
        ),
    ),
    RemoteFile(
        url=(
            f"https://raw.githubusercontent.com/{AUTHOR_REPO}/{RELEASE_2023_06_14_COMMIT}/"
            "wormneuroatlas/data/funatlas.h5"
        ),
        filename="funatlas_release-2023-06-14.h5",
        sha256="f84f1790a6cdf812375e2644122a08e101d7d7c15c99a44a7fb106f7bd1088d6",
        size=18249792,
        distributor=f"GitHub {AUTHOR_REPO} @ {RELEASE_2023_06_14_COMMIT} (first author's repository)",
        origin="secondary",
        primary_reference=PRIMARY_ATLAS,
        git_blob_sha1="247c9d11f814c2e0c011634ed3ca4cda42056c58",
        note=(
            "Earlier release of the same atlas (time_compiled 2023-06-14_08-36-12; git df07176 'updated data'). "
            "Reproduces the arXiv preprint's 23,427. Superseded two weeks later by the 2023-06-28 release, "
            "which changed every unc-31 q-value. Acquired for version comparison only."
        ),
    ),
    ArchiveMember(
        archive=WORMNEUROATLAS_WHEEL,
        member="wormneuroatlas/data/aconnectome_ids_ganglia.json",
        filename="aconnectome_ids_ganglia.json",
        sha256="e754fcb703b39b5f0db977d0b654ba2ac5ce09111f4e19aef3a85fb09ee2e0a2",
        size=5636,
        primary_reference=PRIMARY_METADATA,
        note=(
            "Authors' ganglion assignment. 'head' lists 189 entries, 188 unique (RMHL listed twice, RMHR "
            "absent, AWC named AWCL/AWCR)."
        ),
    ),
    ArchiveMember(
        archive=WORMNEUROATLAS_WHEEL,
        member="wormneuroatlas/data/neuron_ids.txt",
        filename="neuron_ids.txt",
        sha256="e2c7e54af611c1e85aa0705588fcf096ede5f0c28f7fd1d5f0cbec5480b786cc",
        size=2645,
        primary_reference="No portal or journal copy known: author package metadata.",
        note=(
            "Package's 300-id list (no CANL/CANR). Its order differs from funatlas.h5, and it spells AWC "
            "as AWCOFF/AWCON, whereas the h5 has AWCOF/AWCON."
        ),
    ),
)

STRAINS = ("wt", "unc31")


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


def ganglia_head_entries(ganglia: dict) -> list[str]:
    """The ganglia file's 'head' entries in file order, duplicates kept."""
    return [n for group in ganglia["head"] for n in ganglia[group]]


def head188_ids(atlas_ids: list[str], ganglia: dict) -> list[str]:
    """The authors' head set as the paper's counts use it.

    These are the unique ganglia 'head' names present in the atlas, plus the
    atlas's AWCOF/AWCON standing in for the ganglia file's AWCL/AWCR. The
    authors' analysis code (pumpprobe Funatlas.approximate_ids) maps AWCOFF to
    AWCL and AWCON to AWCR, which yields exactly this set. Returned sorted.
    """
    head = sorted(set(ganglia_head_entries(ganglia)))
    return sorted([n for n in head if n in atlas_ids] + ["AWCOF", "AWCON"])


def _release_counts(path, ganglia: dict) -> dict:
    import h5py
    import numpy as np

    out: dict = {}
    with h5py.File(path, "r") as f:
        ids = [x.decode("utf-8") for x in f["neuron_ids"][:]]
        out["atlas_neuron_ids"] = len(ids)
        out["atlas_ids_alphabetically_sorted"] = ids == sorted(ids)
        out["atlas_awc_ids"] = sorted(i for i in ids if i.startswith("AWC"))
        out["atlas_time_compiled"] = f.attrs["time_compiled"].decode("utf-8")
        head = sorted(set(ganglia_head_entries(ganglia)))
        variants = {
            "head188": [ids.index(n) for n in head188_ids(ids, ganglia)],
            "head186": [ids.index(n) for n in head if n in ids],
            "all300": list(range(len(ids))),
        }
        for s in STRAINS:
            g = f[s]
            out[f"{s}_q_eq_th"] = float(g["q_eq_th"][()])
            q_all, qeq_all, occ_all, dff_all = g["q"][:], g["q_eq"][:], g["occ1"][:], g["dFF"][:]
            ntrials_all = np.vectorize(len, otypes=[int])(g["dFF_all"][:])
            for vname, idx in variants.items():
                ix = np.ix_(idx, idx)
                q, qeq, occ, ntr, dff = q_all[ix], qeq_all[ix], occ_all[ix], ntrials_all[ix], dff_all[ix]
                fin = np.isfinite(q)
                diag = np.eye(len(idx), dtype=bool)
                sig = fin & (np.nan_to_num(q, nan=1.0) < 0.05)
                key = f"{s}_{vname}"
                out[f"{key}_finite_q"] = int(fin.sum())
                out[f"{key}_finite_q_self"] = int((fin & diag).sum())
                out[f"{key}_occ_pos"] = int((occ > 0).sum())
                out[f"{key}_occ_pos_without_finite_q"] = int(((occ > 0) & ~fin).sum())
                out[f"{key}_retained_trials_pos"] = int((ntr > 0).sum())
                out[f"{key}_finite_q_iff_retained_trials"] = bool(np.array_equal(fin, ntr > 0))
                out[f"{key}_q_lt_0.05"] = int(sig.sum())
                out[f"{key}_q_lt_0.05_self"] = int((sig & diag).sum())
                out[f"{key}_q_lt_0.05_dFF_neg"] = int((sig & (np.nan_to_num(dff, nan=0.0) < 0)).sum())
                out[f"{key}_q_lt_0.05_dFF_pos"] = int((sig & (np.nan_to_num(dff, nan=0.0) > 0)).sum())
                out[f"{key}_q_lt_0.05_dFF_nan"] = int((sig & np.isnan(dff)).sum())
                out[f"{key}_q_eq_lt_0.05"] = int((np.isfinite(qeq) & (np.nan_to_num(qeq, nan=1.0) < 0.05)).sum())

        idx = variants["head188"]
        ix = np.ix_(idx, idx)
        off = ~np.eye(len(idx), dtype=bool)
        fin_wt = np.isfinite(f["wt"]["q"][:][ix])
        fin_u = np.isfinite(f["unc31"]["q"][:][ix])
        out["head188_offdiag_finite_q_both_strains"] = int((fin_wt & fin_u & off).sum())

        # Strict "candidate purely extrasynaptic" rule of the authors
        # (wt_unc31_differences.py): WT q<0.05, unc-31 q_eq<0.05 and unc-31 q>0.05.
        qw, qu, tu = f["wt"]["q"][:], f["unc31"]["q"][:], f["unc31"]["q_eq"][:]
        with np.errstate(invalid="ignore"):
            strict = (qw < 0.05) & (tu < 0.05) & (qu > 0.05) & np.isfinite(qw) & np.isfinite(qu)
        out["candidate_extrasynaptic_strict_all300"] = int(strict.sum())
        out["candidate_extrasynaptic_strict_all300_self"] = int(np.diag(strict).sum())
        out["candidate_extrasynaptic_strict_all300_offdiag"] = int(strict.sum() - np.diag(strict).sum())
        # Orientation check: the paper names AVDR->AVDL and M3L->URYVL
        # (stimulated -> responding) as candidates.
        for stim, resp in (("AVDR", "AVDL"), ("M3L", "URYVL")):
            i, j = ids.index(resp), ids.index(stim)
            out[f"orientation_{stim}_to_{resp}_at_[resp,stim]"] = bool(strict[i, j])
            out[f"orientation_{stim}_to_{resp}_at_[stim,resp]"] = bool(strict[j, i])
        r = ids.index("RMHR")
        out["RMHR_finite_q_any_strain"] = int(
            sum(int(np.isfinite(f[s]["q"][:][r, :]).sum() + np.isfinite(f[s]["q"][:][:, r]).sum()) for s in STRAINS)
        )
    return out


def record_counts() -> dict:
    """Counts computed from the raw files only.

    Per release (keys prefixed ``release_<date>__``), two head-set variants
    are reported side by side:

    - ``head188``: the authors' head set, with the atlas's AWCON/AWCOF
      standing in for the ganglia file's AWCL/AWCR. This is the one naming
      substitution; it follows the authors' analysis code and reproduces the
      paper's counts.
    - ``head186``: the same set with AWC dropped.

    Definitions:

    - "finite_q" = a q-value exists (the authors' "measured", from
      Numbers_script.py), diagonal included.
    - "self" = diagonal entries (a neuron's response to its own stimulation).
    - "occ_pos" = occ1 > 0.
    - "retained_trials_pos" = len(dFF_all) > 0.
    - dFF sign counts use the h5 mean dF/F.
    """
    import h5py

    raw = RAW_ROOT / SOURCE_ID
    ganglia = json.loads((raw / "aconnectome_ids_ganglia.json").read_text(encoding="utf-8"))
    txt_ids = [
        line.split()[1]
        for line in (raw / "neuron_ids.txt").read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    entries = ganglia_head_entries(ganglia)
    all_ganglia_ids = {n for k, v in ganglia.items() if k not in ("head", "pharynx") for n in v}

    out: dict = {}
    out["ganglia_head_entries_raw"] = len(entries)
    out["ganglia_head_ids"] = len(set(entries))
    out["ganglia_head_duplicate_entries"] = sorted(n for n, c in Counter(entries).items() if c > 1)
    out["ganglia_pharynx_ids"] = len({n for g in ganglia["pharynx"] for n in ganglia[g]})

    with h5py.File(raw / ATLAS_FILE, "r") as f:
        ids = [x.decode("utf-8") for x in f["neuron_ids"][:]]
    out["ganglia_head_ids_absent_from_atlas"] = sorted(n for n in set(entries) if n not in ids)
    out["atlas_ids_absent_from_ganglia"] = sorted(set(ids) - all_ganglia_ids)
    out["ganglia_ids_absent_from_atlas"] = sorted(all_ganglia_ids - set(ids))
    out["neuron_ids_txt_count"] = len(txt_ids)
    out["neuron_ids_txt_same_order_as_atlas"] = txt_ids == ids
    out["neuron_ids_txt_minus_atlas"] = sorted(set(txt_ids) - set(ids))
    out["atlas_minus_neuron_ids_txt"] = sorted(set(ids) - set(txt_ids))

    for release, filename in ATLAS_RELEASES.items():
        for k, v in _release_counts(raw / filename, ganglia).items():
            out[f"release_{release}__{k}"] = v
    return out
