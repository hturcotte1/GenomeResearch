"""Phase 4: build the merged edge table.

One row per ordered pair (pre, post) of distinct head neurons. ``pre`` is the
stimulated neuron and ``post`` the responding one; for anatomy, ``pre`` is
presynaptic. Every value comes from a raw file through the readers and the
namespace mappings; nothing is imputed. A value that does not exist is null,
and the row's ``source_flags`` says why.

No pair is classified into channel categories A–E here (brief: "Do NOT
classify anything into categories A–E").

Outputs, in ``data/processed/``:

- ``merged_edges.parquet`` and ``merged_edges.csv``;
- ``merged_edges.columns.json`` (per-column provenance);
- ``merged_edges_exclusions.csv``;
- ``SHA256SUMS``.

The build is deterministic: the same inputs and config give byte-identical
outputs.
"""

from __future__ import annotations

import csv
import hashlib
import io
import json
import math
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

from src.acquire import randi2023
from src.acquire.common import RAW_ROOT, REPO_ROOT
from src.merge import readers
from src.namespace.canonical import canonical_neurons
from src.namespace.mapping import OUT_DIR as NS_DIR

CONFIG_PATH = REPO_ROOT / "config" / "pipeline.json"
OUT_DIR = REPO_ROOT / "data" / "processed"
TABLE = "merged_edges"

STATES = ("connected", "absent_confident", "inconclusive", "observed_all_trials_discarded", "not_observed")
SIGN_MAP = {"+": "excitatory", "-": "inhibitory", "complex": "complex", "no pred": "unknown"}

WHITE_FILES = {
    "n2u": "wna__aconnectome_white_1986_A.csv",
    "jsh": "wna__aconnectome_white_1986_L4.csv",
    "whole": "wna__aconnectome_white_1986_whole.csv",
}
WITVLIET_FILES = {
    "d7": "nemanode_baf8ec8__witvliet_2020_7.json",
    "d8": "nemanode_baf8ec8__witvliet_2020_8.json",
}
NP_FILES = {
    ("08062023", r): f"08062023_neuropeptide_connectome_{r}_range_model.csv" for r in ("short", "mid", "long")
} | {
    ("01022024", r): f"01022024_neuropeptide_connectome_{r}_range_model.csv" for r in ("short", "mid", "long")
}
RS_MONOAMINE = "08062023_monoamine_connectome.csv"


def load_config() -> dict:
    cfg = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    allowed = {
        "randi_release": set(randi2023.ATLAS_RELEASES),
        "awc_policy": {"unresolved", "authors_convention"},
        "bilateral_policy": {"split"},
        "include_self_pairs": {False, True},
        "head_set": {"randi_head188_plus_rmhr", "randi_head188"},
        "white_primary": set(WHITE_FILES),
        "witvliet_version": {"published_baf8ec8"},
        "witvliet_combination": {"sum_d7_d8"},
        "gap_primary": {"white_n2u", "white_jsh", "white_whole"},
        "neuropeptide_version": {"08062023"},
        "monoamine_primary": {"bentley2016"},
        "fenyves_version": {"journal_xlsx"},
    }
    for key, values in allowed.items():
        if cfg[key] not in values:
            raise ValueError(f"config {key}={cfg[key]!r} is not one of {sorted(map(str, values))}"
                             + (" (collapse is documented as not implementable; see docs/namespace-decisions.md §4)"
                                if key == "bilateral_policy" else ""))
    return cfg


# ---------------------------------------------------------------- name mapping

def _name_map(source_id: str) -> dict[str, str]:
    with open(NS_DIR / f"mapping_{source_id}.csv", encoding="utf-8", newline="") as fh:
        return {r["source_name"]: r["canonical_name"] for r in csv.DictReader(fh) if r["status"] == "mapped"}


def _anat_identity(name: str, awc_policy: str) -> str | None:
    """Name under which a table neuron is looked up in positional (anatomical) datasets."""
    if name in ("AWCON", "AWCOFF"):
        if awc_policy == "authors_convention":
            return {"AWCOFF": "AWCL", "AWCON": "AWCR"}[name]
        return None
    return name


# ---------------------------------------------------------------- kernels

def _kernel_eval(params: np.ndarray, t):
    p = params.reshape(-1, 4)
    t = np.asarray(t, dtype=np.float64)
    out = np.zeros_like(t)
    for g, factor, power_t, _branch in p:
        mult = 1.0 if power_t == 0 else np.power(t, power_t)
        out = out + factor * mult * np.exp(-g * t)
    return out


def kernel_times(params: np.ndarray, time: np.ndarray) -> tuple[float, float, str]:
    """(peak_time, effective_rise_time, status), using the authors' algorithm.

    The algorithm is pumpprobe ``ExponentialConvolution.get_peak_time`` and
    ``get_effective_rise_time``. The peak is the time of max |kernel| on
    ``time``. The rise time is peak time minus the root of kernel(t) = peak/e
    on [0, peak], found by Brent's method. It is NaN when the peak is at the
    end of the axis, or when no sign change brackets the root (the authors'
    code would raise there).
    """
    from scipy.optimize import brentq

    y = _kernel_eval(params, time)
    mi, ma = int(np.argmin(y)), int(np.argmax(y))
    istar = mi if -y[mi] > y[ma] else ma
    tstar = float(time[istar])
    if tstar == 0.0:
        return tstar, 0.0, "ok_peak_at_zero"
    if not tstar < time[-1]:
        return tstar, math.nan, "peak_at_end_of_axis"
    peak = float(y[istar])
    f = lambda t: float(_kernel_eval(params, t)) - peak * math.exp(-1)  # noqa: E731
    a, b = f(0.0), f(tstar)
    if a == 0.0:
        return tstar, tstar, "ok"
    if a * b > 0:
        return tstar, math.nan, "no_sign_change_for_root"
    return tstar, tstar - brentq(f, 0.0, tstar), "ok"


# ---------------------------------------------------------------- per-source matrices

def _anatomy(cfg, head: list[str], excl: list) -> dict:
    """{dataset: {"chem": Counter[(pre,post)], "gap": Counter[frozenset], "covered": set}}."""
    out = {}
    white_map = _name_map("white1986")
    for key, fn in WHITE_FILES.items():
        chem, gap, covered = Counter(), Counter(), set()
        dropped = Counter()
        for e in readers.nemanode_tsv("white1986", fn):
            a, b = white_map.get(e.pre), white_map.get(e.post)
            if a is None or b is None:
                dropped[e.kind] += 1
                continue
            covered.update((a, b))
            if e.kind == "chemical":
                chem[(a, b)] += e.weight
            elif e.kind == "electrical":
                gap[frozenset((a, b))] += e.weight
            else:
                raise ValueError(f"{fn}: unknown edge type {e.kind}")
        for kind, n in sorted(dropped.items()):
            excl.append(["anatomy_edge_non_neuronal_endpoint", "white1986", fn, n,
                         f"{kind} records with a non-neuronal endpoint (muscle/glia/other; see data/interim/namespace/exclusions.csv)"])
        out[f"white_{key}"] = {"chem": chem, "gap": gap, "covered": covered, "file": fn, "source": "white1986"}
    wv_map = _name_map("witvliet2021")
    for key, fn in WITVLIET_FILES.items():
        chem, covered = Counter(), set()
        dropped = Counter()
        for e in readers.nemanode_json("witvliet2021", fn):
            a, b = wv_map.get(e.pre), wv_map.get(e.post)
            if a is None or b is None:
                dropped[e.kind] += 1
                continue
            covered.update((a, b))
            if e.kind == "chemical":
                chem[(a, b)] += e.weight
        for kind, n in sorted(dropped.items()):
            excl.append(["anatomy_edge_non_neuronal_endpoint", "witvliet2021", fn, n,
                         f"{kind} records with a non-neuronal or fragment endpoint"])
        excl.append(["anatomy_gap_not_used", "witvliet2021", fn,
                     sum(1 for e in readers.nemanode_json("witvliet2021", fn) if e.kind == "electrical"),
                     "Witvliet gap junctions were partially annotated and excluded from that paper's analyses; not tabulated (decision Q-W4)"])
        out[f"witvliet_{key}"] = {"chem": chem, "gap": None, "covered": covered, "file": fn, "source": "witvliet2021"}
    return out


def _fenyves() -> tuple[dict, dict]:
    fmap = _name_map("fenyves2020")
    classes, expressed = readers.fenyves_receptor_genes()
    rows = {}
    for r in readers.fenyves_sign_rows():
        a, b = fmap[r["pre"]], fmap[r["post"]]
        nts = [x for x in (r["pre_nt_primary"], r["pre_nt_secondary"]) if x]
        post_genes = expressed.get(r["post"], [])
        matched = []
        for c in r["matched_classes"]:
            genes = [g for g in post_genes if g in classes[c]]
            matched.append(f"{c}:{','.join(genes)}")
        basis = (f"pre_NT={'+'.join(nts) if nts else 'none'}; "
                 f"matched_receptor_classes={'|'.join(matched) if matched else 'none'}")
        if (a, b) in rows:
            raise ValueError(f"duplicate Fenyves row {a}->{b}")
        rows[(a, b)] = {"sign": SIGN_MAP[r["prediction"]], "basis": basis, "synapses": r["synapses"]}
    covered = {fmap[n] for n in expressed}
    return rows, covered


def _neuropeptide() -> dict:
    rmap = _name_map("ripollsanchez2023")
    out = {}
    for (version, rng), fn in NP_FILES.items():
        m = Counter()
        for e in readers.ripoll_matrix(fn):
            m[(rmap[e.pre], rmap[e.post])] += e.weight
        out[(version, rng)] = m
    ma = Counter()
    for e in readers.ripoll_matrix(RS_MONOAMINE):
        ma[(rmap[e.pre], rmap[e.post])] += e.weight
    out["rs_monoamine"] = ma
    return out


def _bentley_monoamine() -> dict:
    bmap = _name_map("bentley2016")
    out: dict = defaultdict(set)
    for e in readers.bentley_edgelist("edgelist_MA.csv"):
        out[(bmap[e.pre], bmap[e.post])].add(e.kind)
    return out


# ---------------------------------------------------------------- build

def head_set(cfg, atlas_ids_canonical: list[str]) -> list[str]:
    g = readers.randi_ganglia()
    raw_ids = readers.randi_atlas(randi2023.ATLAS_RELEASES[cfg["randi_release"]])["ids"]
    rmap = _name_map("randi2023")
    head = {rmap[n] for n in randi2023.head188_ids(raw_ids, g)}
    if cfg["head_set"] == "randi_head188_plus_rmhr":
        head.add("RMHR")
    return sorted(head)


def build_rows(cfg: dict) -> tuple[list[str], list[dict], list[list], dict]:
    excl: list[list] = []
    canon = {c.name: c for c in canonical_neurons()}
    release_file = randi2023.ATLAS_RELEASES[cfg["randi_release"]]
    atlas = readers.randi_atlas(release_file)
    rmap = _name_map("randi2023")
    ids = [rmap[n] for n in atlas["ids"]]
    pos = {n: i for i, n in enumerate(ids)}
    head = head_set(cfg, ids)
    for n in head:
        if n not in canon:
            raise ValueError(f"head neuron {n} is not canonical")

    t0, t1, npts = cfg["kernel_time_axis_s"]
    time = np.linspace(float(t0), float(t1), int(npts))

    anat = _anatomy(cfg, head, excl)
    fen, fen_covered = _fenyves()
    npm = _neuropeptide()
    bma = _bentley_monoamine()
    awc = cfg["awc_policy"]

    rows = []
    kstat = Counter()
    for pre in head:
        for post in head:
            if pre == post and not cfg["include_self_pairs"]:
                continue
            flags = []
            row = {"pre": pre, "post": post,
                   "pre_class": canon[pre].neuron_class, "post_class": canon[post].neuron_class}
            # --- Randi: matrices are [responding=post, stimulated=pre]
            i, j = pos.get(post), pos.get(pre)
            for s in ("wt", "unc31"):
                d = atlas[s]
                if i is None or j is None:
                    occ, ntr, q, qeq, dff = 0, 0, math.nan, math.nan, math.nan
                else:
                    occ, ntr = int(d["occ1"][i, j]), int(d["n_trials"][i, j])
                    q, qeq, dff = float(d["q"][i, j]), float(d["q_eq"][i, j]), float(d["dFF"][i, j])
                if occ == 0:
                    state = "not_observed"
                elif not math.isfinite(q):
                    state = "observed_all_trials_discarded"
                elif q < 0.05:
                    state = "connected"
                elif math.isfinite(qeq) and qeq < 0.05:
                    state = "absent_confident"
                else:
                    state = "inconclusive"
                if state == "connected" and math.isfinite(qeq) and qeq < 0.05:
                    flags.append(f"{s}_q_and_q_eq_both_below_0.05")
                sign = None
                if state == "connected":
                    sign = "excitatory" if dff > 0 else "inhibitory" if dff < 0 else "undefined"
                    if sign == "undefined":
                        flags.append(f"{s}_connected_but_mean_dFF_undefined")
                row[f"randi_state_{s}"] = state
                row[f"measured_sign_{s}"] = sign
                row[f"measured_amplitude_{s}"] = dff if math.isfinite(dff) else None
                row[f"measured_n_{s}"] = ntr
                row[f"measured_occurrences_{s}"] = occ
                row[f"measured_q_{s}"] = q if math.isfinite(q) else None
                row[f"measured_q_eq_{s}"] = qeq if math.isfinite(qeq) else None
                if s == "wt":
                    peak, rise, status = (None, None, "no_kernel")
                    if i is not None and j is not None and len(d["kernels"][i, j]):
                        peak, rise, status = kernel_times(np.asarray(d["kernels"][i, j], dtype=np.float64), time)
                        rise = rise if math.isfinite(rise) else None
                    kstat[status] += 1
                    if status in ("peak_at_end_of_axis", "no_sign_change_for_root"):
                        flags.append(f"wt_latency_undefined_{status}")
                    row["measured_latency_wt"] = rise
                    row["measured_peak_time_wt"] = peak
            row["randi_tested"] = row["measured_occurrences_wt"] > 0
            a, b = row["measured_amplitude_wt"], row["measured_amplitude_unc31"]
            row["unc31_delta"] = a - b if a is not None and b is not None else None
            qw, qu, tu = row["measured_q_wt"], row["measured_q_unc31"], row["measured_q_eq_unc31"]
            row["randi_strict_extrasynaptic_candidate"] = bool(
                qw is not None and qu is not None and tu is not None and qw < 0.05 and tu < 0.05 and qu > 0.05)

            # --- positional datasets
            ap, aq = _anat_identity(pre, awc), _anat_identity(post, awc)
            if ap is None or aq is None:
                flags.append("awc_identity_unresolved")
            for key, ds in anat.items():
                ok = ap is not None and aq is not None and ap in ds["covered"] and aq in ds["covered"]
                if ap is not None and aq is not None and not ok:
                    flags.append(f"{key}_not_covered")
                row[f"anat_chem_{key}"] = ds["chem"].get((ap, aq), 0.0) if ok else None
                if ds["gap"] is not None:
                    row[f"anat_gap_{key}"] = ds["gap"].get(frozenset((ap, aq)), 0.0) if ok else None
            row["anat_chem_white"] = row[f"anat_chem_white_{cfg['white_primary']}"]
            w7, w8 = row["anat_chem_witvliet_d7"], row["anat_chem_witvliet_d8"]
            row["anat_chem_witvliet"] = w7 + w8 if w7 is not None and w8 is not None else None
            row["anat_gap"] = row[f"anat_gap_{cfg['gap_primary']}"]

            # --- predicted sign (Fenyves)
            if ap is None or aq is None:
                row["predicted_sign"] = row["predicted_sign_basis"] = row["predicted_sign_connectome_synapses"] = None
            elif (ap, aq) in fen:
                f = fen[(ap, aq)]
                row["predicted_sign"], row["predicted_sign_basis"] = f["sign"], f["basis"]
                row["predicted_sign_connectome_synapses"] = f["synapses"]
            else:
                row["predicted_sign"] = row["predicted_sign_basis"] = None
                row["predicted_sign_connectome_synapses"] = 0 if (ap in fen_covered and aq in fen_covered) else None
                flags.append("no_chemical_connection_in_fenyves_connectome")

            # --- extrasynaptic layers (whole-animal matrices; every canonical neuron covered)
            for rng in ("short", "mid", "long"):
                v23 = npm[("08062023", rng)].get((ap, aq), 0) if ap and aq else None
                v24 = npm[("01022024", rng)].get((ap, aq), 0) if ap and aq else None
                row[f"np_edge_{rng}"] = int(v23) if v23 is not None else None
                row[f"np_edge_{rng}_v2024"] = int(v24) if v24 is not None else None
            if ap and aq:
                lig = sorted(bma.get((ap, aq), ()))
                row["monoamine_edge"] = ";".join(lig) if lig else "none"
                row["monoamine_edge_rs2023"] = int(npm["rs_monoamine"].get((ap, aq), 0))
            else:
                row["monoamine_edge"] = row["monoamine_edge_rs2023"] = None
            row["source_flags"] = ";".join(sorted(set(flags)))
            rows.append(row)

    # self-pairs and out-of-scope measurements: logged, never silently dropped
    if not cfg["include_self_pairs"]:
        for n in head:
            i = pos.get(n)
            occ = int(atlas["wt"]["occ1"][i, i]) if i is not None else 0
            excl.append(["self_pair", "randi2023", release_file, 1,
                         f"{n}->{n}: self-pairs excluded by config include_self_pairs=false (WT occ1={occ})"])
    head_idx = [pos[n] for n in head if n in pos]
    fin = np.isfinite(atlas["wt"]["q"])
    mask = np.zeros_like(fin)
    mask[np.ix_(head_idx, head_idx)] = True
    excl.append(["out_of_head_scope", "randi2023", release_file, int((fin & ~mask).sum()),
                 "WT measured pairs involving at least one non-head neuron (Rule 6: head only)"])
    return head, rows, excl, {"kernel_status": dict(sorted(kstat.items())), "release_file": release_file}


COLUMN_ORDER = [
    "pre", "post", "pre_class", "post_class",
    "randi_tested", "randi_state_wt", "randi_state_unc31",
    "measured_sign_wt", "measured_amplitude_wt", "measured_latency_wt", "measured_peak_time_wt",
    "measured_n_wt", "measured_occurrences_wt", "measured_q_wt", "measured_q_eq_wt",
    "measured_sign_unc31", "measured_amplitude_unc31", "measured_n_unc31", "measured_occurrences_unc31",
    "measured_q_unc31", "measured_q_eq_unc31",
    "unc31_delta", "randi_strict_extrasynaptic_candidate",
    "anat_chem_white", "anat_chem_witvliet", "anat_gap",
    "anat_chem_white_n2u", "anat_chem_white_jsh", "anat_chem_white_whole",
    "anat_gap_white_n2u", "anat_gap_white_jsh", "anat_gap_white_whole",
    "anat_chem_witvliet_d7", "anat_chem_witvliet_d8",
    "predicted_sign", "predicted_sign_basis", "predicted_sign_connectome_synapses",
    "np_edge_short", "np_edge_mid", "np_edge_long",
    "np_edge_short_v2024", "np_edge_mid_v2024", "np_edge_long_v2024",
    "monoamine_edge", "monoamine_edge_rs2023",
    "source_flags",
]

ARROW_TYPES = {
    "bool": ["randi_tested", "randi_strict_extrasynaptic_candidate"],
    "int64": ["measured_n_wt", "measured_occurrences_wt", "measured_n_unc31", "measured_occurrences_unc31",
              "predicted_sign_connectome_synapses", "np_edge_short", "np_edge_mid", "np_edge_long",
              "np_edge_short_v2024", "np_edge_mid_v2024", "np_edge_long_v2024", "monoamine_edge_rs2023"],
    "float64": ["measured_amplitude_wt", "measured_latency_wt", "measured_peak_time_wt", "measured_q_wt",
                "measured_q_eq_wt", "measured_amplitude_unc31", "measured_q_unc31", "measured_q_eq_unc31",
                "unc31_delta", "anat_chem_white", "anat_chem_witvliet", "anat_gap",
                "anat_chem_white_n2u", "anat_chem_white_jsh", "anat_chem_white_whole",
                "anat_gap_white_n2u", "anat_gap_white_jsh", "anat_gap_white_whole",
                "anat_chem_witvliet_d7", "anat_chem_witvliet_d8"],
}


def _csv_value(v) -> str:
    if v is None:
        return ""
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, float):
        if not math.isfinite(v):
            raise ValueError("non-finite float reached the writer")
        return repr(v)
    return str(v)


def write_outputs(rows: list[dict], excl: list[list], columns_meta: dict) -> dict:
    import pyarrow as pa
    import pyarrow.parquet as pq

    if set(rows[0]) != set(COLUMN_ORDER):
        raise ValueError(f"column mismatch: {sorted(set(rows[0]) ^ set(COLUMN_ORDER))}")
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    types = {c: t for t, cols in ARROW_TYPES.items() for c in cols}
    arrays, fields = [], []
    for c in COLUMN_ORDER:
        t = {"bool": pa.bool_(), "int64": pa.int64(), "float64": pa.float64()}.get(types.get(c, ""), pa.string())
        arrays.append(pa.array([r[c] for r in rows], type=t))
        fields.append(pa.field(c, t))
    table = pa.Table.from_arrays(arrays, schema=pa.schema(fields))
    pq.write_table(table, OUT_DIR / f"{TABLE}.parquet", compression="zstd", compression_level=9,
                   use_dictionary=False, write_statistics=True, data_page_version="2.0")

    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\n")
    w.writerow(COLUMN_ORDER)
    for r in rows:
        w.writerow([_csv_value(r[c]) for c in COLUMN_ORDER])
    (OUT_DIR / f"{TABLE}.csv").write_text(buf.getvalue(), encoding="utf-8")

    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\n")
    w.writerow(["category", "source_id", "file", "n_records", "reason"])
    w.writerows(sorted(excl))
    (OUT_DIR / f"{TABLE}_exclusions.csv").write_text(buf.getvalue(), encoding="utf-8")

    (OUT_DIR / f"{TABLE}.columns.json").write_text(json.dumps(columns_meta, indent=2, sort_keys=True) + "\n",
                                                  encoding="utf-8")
    sums = {}
    for name in sorted(p.name for p in OUT_DIR.iterdir() if p.name.startswith(TABLE)):
        sums[name] = hashlib.sha256((OUT_DIR / name).read_bytes()).hexdigest()
    (OUT_DIR / "SHA256SUMS").write_text("".join(f"{h}  {n}\n" for n, h in sorted(sums.items())), encoding="utf-8")
    return sums


def _file_sha(source: str, filename: str) -> str:
    m = json.loads((RAW_ROOT / source / "MANIFEST.json").read_text(encoding="utf-8"))
    return next(e["sha256"] for e in m["files"] if e["filename"] == filename)


def columns_metadata(cfg: dict, release_file: str) -> dict:
    from src.acquire import bentley2016, fenyves2020, ripollsanchez2023, white1986, witvliet2021

    def src(source_id, files, citation, definition, decision=""):
        return {"source_id": source_id,
                "files": [{"filename": f, "sha256": _file_sha(source_id, f)} for f in files],
                "paper": citation, "definition": definition, "decision": decision}

    R = randi2023.CITATION
    meta = {
        "_table": {
            "row": "one ordered pair (pre, post) of distinct head neurons; pre = stimulated / presynaptic / sender, post = responding / postsynaptic / receiver",
            "head_set": cfg["head_set"],
            "config": cfg,
            "nulls": "null = value does not exist for this pair (see source_flags); 0 = measured/reconstructed absence",
        },
        "pre": src("canonical_neurons", ["IndividualNeurons.csv", "C. elegans Cell List - WormBase.csv"],
                   "White et al. 1986 nomenclature via WormAtlas (OpenWorm copies)", "canonical neuron name (src/namespace/canonical.py); AWCON/AWCOFF are extension identities"),
        "pre_class": src("canonical_neurons", ["nemanode_da8ca7e__neurons.json"], "NemaNode cell table (Witvliet et al. 2021 portal)", "neuron class of pre (118 classes)"),
    }
    meta["post"] = dict(meta["pre"], definition="canonical neuron name of the responding/postsynaptic neuron")
    meta["post_class"] = dict(meta["pre_class"], definition="neuron class of post")
    rfiles = [release_file, "aconnectome_ids_ganglia.json"]
    rdef = {
        "randi_tested": "WT: pair observed at least once (occ1[post, pre] > 0)",
        "randi_state_wt": "connected (q<0.05) | absent_confident (q_eq<0.05) | inconclusive | observed_all_trials_discarded (occ1>0, no retained trial, no q) | not_observed (occ1=0)",
        "randi_state_unc31": "as randi_state_wt, unc-31 strain",
        "measured_sign_wt": "sign of mean dF/F when randi_state_wt=connected: excitatory (>0) | inhibitory (<0) | undefined (NaN); null otherwise",
        "measured_amplitude_wt": "mean dF/F over retained trials (h5 wt/dFF[post, pre]); null if no retained trial",
        "measured_latency_wt": "effective rise time (s) of the atlas kernel for the pair: authors' get_effective_rise_time on a 0-200 s / 1000-point axis; null if no kernel or undefined (see source_flags)",
        "measured_peak_time_wt": "time (s) of max |kernel| on the same axis",
        "measured_n_wt": "number of retained trials, len(dFF_all)",
        "measured_occurrences_wt": "occ1: stimulation/response occurrences including discarded trials",
        "measured_q_wt": "q-value for functional connection (h5 wt/q)",
        "measured_q_eq_wt": "q-value of the equivalence (TOST) test for non-connection (h5 wt/q_eq)",
        "unc31_delta": "measured_amplitude_wt - measured_amplitude_unc31 when both exist",
        "randi_strict_extrasynaptic_candidate": "authors' rule (wt_unc31_differences.py): WT q<0.05 and unc-31 q_eq<0.05 and unc-31 q>0.05",
    }
    for c, d in rdef.items():
        meta[c] = src("randi2023", rfiles, R, d, "D-013; Q-002")
    for c in ("measured_sign", "measured_amplitude", "measured_n", "measured_occurrences", "measured_q", "measured_q_eq"):
        meta[f"{c}_unc31"] = src("randi2023", rfiles, R, rdef[f"{c}_wt"] + " (unc-31 strain)", "D-013; Q-002")
    for key, fn in WHITE_FILES.items():
        meta[f"anat_chem_white_{key}"] = src("white1986", [fn], white1986.CITATION,
                                             f"chemical synapse count pre->post in NemaNode {key} export; null if either neuron absent from the dataset", "Q-007")
        meta[f"anat_gap_white_{key}"] = src("white1986", [fn], white1986.CITATION,
                                            f"gap-junction count for the unordered pair in NemaNode {key} export (each pair listed once); null if not covered", "Q-W4")
    for key, fn in WITVLIET_FILES.items():
        meta[f"anat_chem_witvliet_{key}"] = src("witvliet2021", [fn], witvliet2021.CITATION,
                                                f"chemical synapse records pre->post, published Witvliet {key}; null if not covered", "Q-W1")
    meta["anat_chem_white"] = dict(meta[f"anat_chem_white_{cfg['white_primary']}"], decision="Q-007 (primary = " + cfg["white_primary"] + ")")
    meta["anat_gap"] = dict(meta[f"anat_gap_{cfg['gap_primary']}"], decision="Q-W4 (primary = " + cfg["gap_primary"] + ")")
    meta["anat_chem_witvliet"] = src("witvliet2021", list(WITVLIET_FILES.values()), witvliet2021.CITATION,
                                     "anat_chem_witvliet_d7 + anat_chem_witvliet_d8; null unless both datasets cover both neurons", "Q-W3")
    fx = [readers.FENYVES_XLSX]
    meta["predicted_sign"] = src("fenyves2020", fx, fenyves2020.CITATION,
                                 "excitatory | inhibitory | complex | unknown (Fenyves 'no pred'); null when Fenyves's connectome has no chemical connection pre->post", "Q-008")
    meta["predicted_sign_basis"] = src("fenyves2020", fx, fenyves2020.CITATION,
                                       "presynaptic transmitter(s) and matched receptor classes with the postsynaptic genes expressed in each", "Q-008")
    meta["predicted_sign_connectome_synapses"] = src("fenyves2020", fx, fenyves2020.CITATION,
                                                     "synapse count of the pair in the WormWiring connectome Fenyves used (0 = none)", "Q-008")
    for rng in ("short", "mid", "long"):
        meta[f"np_edge_{rng}"] = src("ripollsanchez2023", [NP_FILES[("08062023", rng)]], ripollsanchez2023.CITATION,
                                     f"number of NPP-GPCR pairs supporting pre->post, {rng}-range model, 2023 (Table S6) version; 0 = no edge", "Q-RS-1")
        meta[f"np_edge_{rng}_v2024"] = src("ripollsanchez2023", [NP_FILES[("01022024", rng)]], ripollsanchez2023.CITATION,
                                           f"as np_edge_{rng}, authors' 2024-02-02 post-publication update", "Q-RS-1")
    meta["monoamine_edge"] = src("bentley2016", ["edgelist_MA.csv"], bentley2016.CITATION,
                                 "';'-joined sorted monoamines (dopamine, octopamine, serotonin, tyramine) with an edge pre->post; 'none' if no edge", "Q-009")
    meta["monoamine_edge_rs2023"] = src("ripollsanchez2023", [RS_MONOAMINE], ripollsanchez2023.CITATION,
                                        "weight of pre->post in the Ripoll-Sanchez 08062023 monoamine-GPCR network; 0 = no edge", "Q-009")
    meta["source_flags"] = {"source_id": "derived", "files": [], "paper": "",
                            "definition": "';'-joined row-specific flags explaining nulls and caveats (e.g. awc_identity_unresolved, white_n2u_not_covered, no_chemical_connection_in_fenyves_connectome)",
                            "decision": ""}
    return meta


def build() -> dict:
    cfg = load_config()
    head, rows, excl, info = build_rows(cfg)
    meta = columns_metadata(cfg, info["release_file"])
    missing = set(COLUMN_ORDER) - set(meta)
    if missing:
        raise ValueError(f"columns without provenance: {sorted(missing)}")
    sums = write_outputs(rows, excl, meta)
    return {"rows": len(rows), "head_neurons": len(head), "kernel_status": info["kernel_status"], "sha256": sums}


if __name__ == "__main__":
    print(json.dumps(build(), indent=2, sort_keys=True))
