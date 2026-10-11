"""Randi et al. 2023, Nature 623:406-414: signal propagation atlas, WT and unc-31.

Acquired from the authors' own redistribution: the `wormneuroatlas` 0.0.7.3
wheel on PyPI, which bundles the atlas as ``data/funatlas.h5``. The primary
locations (funconn.princeton.edu, OSF) are blocked in this environment; see
docs/provenance/randi2023.md.

Facts about funatlas.h5 that later phases must respect, checked by
``record_counts``:

- ``neuron_ids`` is a 300-entry, alphabetically sorted |S5 array. It is NOT in
  the order of the package's ``neuron_ids.txt``, so index the matrices with
  the h5's own ids only.
- AWC appears as "AWCON" and "AWCOF". The second is "AWCOFF" truncated to 5
  bytes. There is no AWCL/AWCR. CANL/CANR are absent.
- Matrices are indexed [responding, stimulated], following the authors' code:
  rows i respond, columns j are stimulated. An entry is a response of i to
  stimulation of j.
"""

from __future__ import annotations

import json

from .common import RAW_ROOT, ArchiveMember, acquire_source, verify_pypi_digest
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
PRIMARY = "https://funconn.princeton.edu/ (atlas portal); raw data https://osf.io/e2syt/"

FILES = (
    ArchiveMember(
        archive=WORMNEUROATLAS_WHEEL,
        member="wormneuroatlas/data/funatlas.h5",
        filename="funatlas.h5",
        sha256="53a99055667b853e1d3d6be573ec2613d38c9f6989f302ec38ecd38dd50c7975",
        size=18266176,
        primary_reference=PRIMARY,
        note="Signal propagation atlas, WT and unc-31. Internal attribute time_compiled=2023-06-28_19-52-14.",
    ),
    ArchiveMember(
        archive=WORMNEUROATLAS_WHEEL,
        member="wormneuroatlas/data/aconnectome_ids_ganglia.json",
        filename="aconnectome_ids_ganglia.json",
        sha256="e754fcb703b39b5f0db977d0b654ba2ac5ce09111f4e19aef3a85fb09ee2e0a2",
        size=5636,
        primary_reference=PRIMARY,
        note="The authors' assignment of neurons to ganglia; its 'head' key defines the 188-neuron head set.",
    ),
    ArchiveMember(
        archive=WORMNEUROATLAS_WHEEL,
        member="wormneuroatlas/data/neuron_ids.txt",
        filename="neuron_ids.txt",
        sha256="e2c7e54af611c1e85aa0705588fcf096ede5f0c28f7fd1d5f0cbec5480b786cc",
        size=2645,
        primary_reference=PRIMARY,
        note="The package's 300-neuron id list (no CANL/CANR). Its order differs from funatlas.h5.",
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
    extra = {f.filename: [f"archive {WORMNEUROATLAS_WHEEL.filename}: {pypi_check}"] for f in FILES}
    return acquire_source(SOURCE_ID, FILES, extra)


def _head_ids_from_ganglia(ganglia: dict) -> list[str]:
    return sorted({n for group in ganglia["head"] for n in ganglia[group]})


def record_counts() -> dict:
    """Counts computed from the raw files only, with no naming decisions applied.

    Two head-set variants are reported side by side, because the ganglia file
    names AWCL/AWCR while the atlas names AWCON/AWCOF:

    - ``head188``: the ganglia head set, with AWCL/AWCR stood in for by the
      atlas's AWCON/AWCOF. This variant reproduces the paper's 23,433 / 1,310.
    - ``head186``: the ganglia head set with AWC dropped, because AWCL/AWCR do
      not occur in the atlas.

    "finite_q" means a q-value exists, which is the authors' own definition of
    a measured pair (their Numbers_script.py). "occ_pos" means at least one
    observation is recorded (occ1 > 0). "self" counts diagonal entries,
    i.e. a neuron's response to its own stimulation.
    """
    import h5py
    import numpy as np

    raw = RAW_ROOT / SOURCE_ID
    ganglia = json.loads((raw / "aconnectome_ids_ganglia.json").read_text(encoding="utf-8"))
    txt_ids = [line.split()[1] for line in (raw / "neuron_ids.txt").read_text(encoding="utf-8").splitlines() if line.strip()]

    out: dict = {}
    with h5py.File(raw / "funatlas.h5", "r") as f:
        ids = [x.decode("utf-8") for x in f["neuron_ids"][:]]
        out["atlas_neuron_ids"] = len(ids)
        out["atlas_ids_alphabetically_sorted"] = ids == sorted(ids)
        out["atlas_ids_same_order_as_neuron_ids_txt"] = ids == txt_ids
        out["atlas_awc_ids"] = sorted(i for i in ids if i.startswith("AWC"))
        out["atlas_time_compiled"] = f.attrs["time_compiled"].decode("utf-8")

        head = _head_ids_from_ganglia(ganglia)
        missing = [n for n in head if n not in ids]
        out["ganglia_head_ids"] = len(head)
        out["ganglia_head_ids_absent_from_atlas"] = missing
        out["ganglia_pharynx_ids"] = len({n for g in ganglia["pharynx"] for n in ganglia[g]})

        variants = {
            "head188": [ids.index(n) for n in head if n in ids] + [ids.index("AWCOF"), ids.index("AWCON")],
            "head186": [ids.index(n) for n in head if n in ids],
            "all300": list(range(len(ids))),
        }
        for s in STRAINS:
            g = f[s]
            out[f"{s}_q_eq_th"] = float(g["q_eq_th"][()])
            q_all = g["q"][:]
            qeq_all = g["q_eq"][:]
            occ_all = g["occ1"][:]
            for vname, idx in variants.items():
                ix = np.ix_(idx, idx)
                q, qeq, occ = q_all[ix], qeq_all[ix], occ_all[ix]
                fin = np.isfinite(q)
                diag = np.eye(len(idx), dtype=bool)
                key = f"{s}_{vname}"
                out[f"{key}_finite_q"] = int(fin.sum())
                out[f"{key}_finite_q_self"] = int((fin & diag).sum())
                out[f"{key}_occ_pos"] = int((occ > 0).sum())
                out[f"{key}_occ_pos_without_finite_q"] = int(((occ > 0) & ~fin).sum())
                out[f"{key}_q_lt_0.05"] = int((fin & (np.nan_to_num(q, nan=1.0) < 0.05)).sum())
                out[f"{key}_q_lt_0.05_self"] = int((fin & diag & (np.nan_to_num(q, nan=1.0) < 0.05)).sum())
                out[f"{key}_q_eq_lt_0.05"] = int((np.isfinite(qeq) & (np.nan_to_num(qeq, nan=1.0) < 0.05)).sum())

        # Pairs measured in both strains (head188, off-diagonal): the only
        # pairs on which a WT-vs-unc-31 comparison is possible at all.
        idx = variants["head188"]
        ix = np.ix_(idx, idx)
        off = ~np.eye(len(idx), dtype=bool)
        fin_wt = np.isfinite(f["wt"]["q"][:][ix])
        fin_u = np.isfinite(f["unc31"]["q"][:][ix])
        out["head188_offdiag_finite_q_both_strains"] = int((fin_wt & fin_u & off).sum())

        # Orientation check. The paper names AVDR->AVDL and M3L->URYVL
        # (stimulated -> responding) as candidate extrasynaptic connections.
        # Under the authors' strict rule they must appear at [responding,
        # stimulated], not transposed.
        qw, qu, tu = f["wt"]["q"][:], f["unc31"]["q"][:], f["unc31"]["q_eq"][:]
        with np.errstate(invalid="ignore"):
            strict = (qw < 0.05) & (tu < 0.05) & (qu > 0.05) & np.isfinite(qw) & np.isfinite(qu)
        out["candidate_extrasynaptic_strict_all300"] = int(strict.sum())
        for stim, resp in (("AVDR", "AVDL"), ("M3L", "URYVL")):
            i, j = ids.index(resp), ids.index(stim)
            out[f"orientation_{stim}_to_{resp}_at_[resp,stim]"] = bool(strict[i, j])
            out[f"orientation_{stim}_to_{resp}_at_[stim,resp]"] = bool(strict[j, i])
    return out
