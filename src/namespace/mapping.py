"""Map every neuron name in every source onto the canonical namespace.

Rules are applied in this fixed order, and the first match wins. Each one is
explicit and inspectable; there is NO fuzzy or similarity matching anywhere:

1. ``alias``: an entry in ``config/namespace/aliases.csv`` for this
   (source, name).
2. ``exact``: the name is a canonical name (including the AWCON/AWCOFF
   extension identities).
3. ``strip_whitespace``: the name with surrounding whitespace removed is
   canonical.
4. ``vnc_zero_padding``: AS/DA/DB/DD/VA/VB/VC/VD followed by a zero-padded
   number (e.g. VB01) becomes the unpadded canonical name (VB1). This is the
   only pattern rule.

Every name that matches none of these is *excluded*, with a reason. The
reason is "non-neuronal cell" when a cell table classifies the name as one:
the NemaNode cell table (type b = body wall muscle, u = other non-neuron),
the WormAtlas complete cell list, or ``config/namespace/non_neuronal_names.csv``
for pseudo-nodes. Otherwise the reason is "UNRECOGNISED".

CeNGEN cell types are class-level, so they map one-to-many. A type maps to
the members of the canonical class of the same name, or else to the explicit
entry in ``config/namespace/cengen_types.csv``.

Outputs are written to ``data/interim/namespace/`` by ``build()``.
"""

from __future__ import annotations

import csv
import io
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

from src.acquire.common import RAW_ROOT, REPO_ROOT
from src.merge import readers
from src.namespace.canonical import canonical_neurons

CONFIG_DIR = REPO_ROOT / "config" / "namespace"
OUT_DIR = REPO_ROOT / "data" / "interim" / "namespace"
_VNC_PADDED = re.compile(r"^(AS|DA|DB|DD|VA|VB|VC|VD)0(\d)$")

RULE_ORDER = ("alias", "exact", "strip_whitespace", "vnc_zero_padding")


def _read_csv(path: Path) -> list[dict]:
    with open(path, encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def _write_csv(path: Path, header: list[str], rows: list[list]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\n")
    w.writerow(header)
    w.writerows(rows)
    path.write_text(buf.getvalue(), encoding="utf-8")


# ---------------------------------------------------------------- vocabularies

def _edge_names(edges) -> Counter:
    c: Counter = Counter()
    for e in edges:
        c[e.pre] += 1
        c[e.post] += 1
    return c


def vocabularies() -> list[tuple[str, str, Counter]]:
    """(source_id, file label, Counter of name -> occurrences) for every name-bearing file used later."""
    out: list[tuple[str, str, Counter]] = []
    for fn in ("funatlas.h5", "funatlas_release-2023-06-14.h5"):
        out.append(("randi2023", f"{fn}:neuron_ids", Counter(readers.randi_atlas(fn)["ids"])))
    g = readers.randi_ganglia()
    out.append(("randi2023", "aconnectome_ids_ganglia.json:head",
                Counter(n for grp in g["head"] for n in g[grp])))
    for fn in ("wna__aconnectome_white_1986_A.csv", "wna__aconnectome_white_1986_L4.csv",
               "wna__aconnectome_white_1986_whole.csv"):
        out.append(("white1986", fn, _edge_names(readers.nemanode_tsv("white1986", fn))))
    for fn in ("nemanode_baf8ec8__witvliet_2020_7.json", "nemanode_baf8ec8__witvliet_2020_8.json"):
        out.append(("witvliet2021", fn, _edge_names(readers.nemanode_json("witvliet2021", fn))))
    rows = readers.fenyves_sign_rows()
    c = Counter()
    for r in rows:
        c[r["pre"]] += 1
        c[r["post"]] += 1
    out.append(("fenyves2020", f"{readers.FENYVES_XLSX}:5. Sign prediction", c))
    _, expressed = readers.fenyves_receptor_genes()
    out.append(("fenyves2020", f"{readers.FENYVES_XLSX}:3. Receptor Gene expression", Counter({k: 1 for k in expressed})))
    for fn in ("08062023_neuropeptide_connectome_short_range_model.csv",
               "08062023_neuropeptide_connectome_mid_range_model.csv",
               "08062023_neuropeptide_connectome_long_range_model.csv",
               "01022024_neuropeptide_connectome_short_range_model.csv",
               "01022024_neuropeptide_connectome_mid_range_model.csv",
               "01022024_neuropeptide_connectome_long_range_model.csv",
               "08062023_monoamine_connectome.csv"):
        cols, rows_ = readers.ripoll_labels(fn)
        if cols != rows_:
            raise ValueError(f"{fn}: row and column labels differ")
        out.append(("ripollsanchez2023", fn, Counter(cols)))
    for fn in ("edgelist_MA.csv", "edgelist_NP.csv"):
        out.append(("bentley2016", fn, _edge_names(readers.bentley_edgelist(fn))))
    return out


# ---------------------------------------------------------------- classification data

def _aliases() -> dict[tuple[str, str], tuple[str, str]]:
    return {(r["source_id"], r["source_name"]): (r["canonical_name"], r["reason"])
            for r in _read_csv(CONFIG_DIR / "aliases.csv")}


def _non_neuronal_explicit() -> dict[str, str]:
    path = CONFIG_DIR / "non_neuronal_names.csv"
    return {r["name"]: r["reason"] for r in _read_csv(path)} if path.exists() else {}


def _nemanode_types() -> dict[str, str]:
    cells = json.loads((RAW_ROOT / "canonical_neurons" / "nemanode_da8ca7e__neurons.json").read_text(encoding="utf-8"))
    return {c["name"]: c["typ"] for c in cells}


def _wormatlas_cells() -> set[str]:
    text = (RAW_ROOT / "canonical_neurons" / "C. elegans Cell List - WormAtlas.tsv").read_text(encoding="utf-8")
    return {ln.split("\t")[0].strip() for ln in text.splitlines()[1:] if ln.strip()}


def classify(source_id: str, name: str, canon: set[str], aliases, nn_types, wa_cells, explicit) -> dict:
    """Apply the rules to one (source, name). Returns a mapping record."""
    if (source_id, name) in aliases:
        target, reason = aliases[(source_id, name)]
        if target not in canon:
            raise ValueError(f"alias {source_id}:{name} -> {target} is not canonical")
        return {"status": "mapped", "canonical_name": target, "rule": "alias", "reason": reason}
    if name in canon:
        return {"status": "mapped", "canonical_name": name, "rule": "exact", "reason": ""}
    stripped = name.strip()
    if stripped != name and stripped in canon:
        return {"status": "mapped", "canonical_name": stripped, "rule": "strip_whitespace",
                "reason": "surrounding whitespace in the source file"}
    m = _VNC_PADDED.match(stripped)
    if m and (m.group(1) + m.group(2)) in canon:
        return {"status": "mapped", "canonical_name": m.group(1) + m.group(2), "rule": "vnc_zero_padding",
                "reason": "zero-padded ventral-cord number"}
    if stripped in explicit:
        return {"status": "excluded", "canonical_name": "", "rule": "non_neuronal",
                "reason": f"non-neuronal or pseudo-node: {explicit[stripped]} (config/namespace/non_neuronal_names.csv)"}
    t = nn_types.get(stripped)
    if t == "b":
        return {"status": "excluded", "canonical_name": "", "rule": "non_neuronal",
                "reason": "body wall muscle (NemaNode cell table type b)"}
    if t == "u":
        return {"status": "excluded", "canonical_name": "", "rule": "non_neuronal",
                "reason": "non-neuronal cell (NemaNode cell table type u)"}
    if stripped in wa_cells:
        return {"status": "excluded", "canonical_name": "", "rule": "non_neuronal",
                "reason": "non-neuronal cell (WormAtlas complete cell list, not a hermaphrodite neuron)"}
    return {"status": "excluded", "canonical_name": "", "rule": "unrecognised", "reason": "UNRECOGNISED"}


def cengen_mapping(canon_table) -> list[dict]:
    """One record per CeNGEN cell type: its canonical member neurons and the rule used."""
    by_class: dict[str, list[str]] = defaultdict(list)
    for c in canon_table:
        by_class[c.neuron_class].append(c.name)
    explicit = {r["cengen_type"]: (r["members"].split(";"), r["reason"])
                for r in _read_csv(CONFIG_DIR / "cengen_types.csv")}
    canon = {c.name for c in canon_table}
    out = []
    for t in readers.cengen_types():
        if t in explicit:
            members, reason = explicit[t]
            rule = "explicit_table"
        elif t in by_class and not any(c.is_extension for c in canon_table if c.name in by_class[t]):
            members, reason, rule = by_class[t], "CeNGEN type name equals the canonical (NemaNode) class name", "class_name"
        else:
            members, reason, rule = [], "UNRECOGNISED cell type", "unrecognised"
        bad = [m for m in members if m not in canon]
        if bad:
            raise ValueError(f"CeNGEN type {t} maps to non-canonical names {bad}")
        out.append({"cengen_type": t, "members": sorted(members), "rule": rule, "reason": reason})
    return out


# ---------------------------------------------------------------- build

def build() -> dict:
    """Write all namespace artifacts to data/interim/namespace/ and return a summary."""
    table = canonical_neurons()
    canon = {c.name for c in table}
    plain = {c.name for c in table if not c.is_extension}
    aliases, explicit = _aliases(), _non_neuronal_explicit()
    nn_types, wa_cells = _nemanode_types(), _wormatlas_cells()

    _write_csv(OUT_DIR / "canonical_neurons.csv",
               ["name", "neuron_class", "is_pharyngeal", "is_extension", "nemanode_inhead", "wormatlas_description"],
               [[c.name, c.neuron_class, int(c.is_pharyngeal), int(c.is_extension),
                 "" if c.nemanode_inhead is None else c.nemanode_inhead, c.wormatlas_description] for c in table])

    vocab = vocabularies()
    per_source: dict[str, dict[str, dict]] = defaultdict(dict)
    coverage_rows = []
    for source_id, label, counts in vocab:
        mapped = excl_nn = excl_unrec = 0
        covered = set()
        for name, n in counts.items():
            rec = per_source[source_id].get(name)
            if rec is None:
                rec = classify(source_id, name, canon, aliases, nn_types, wa_cells, explicit)
                rec = {**rec, "files": set(), "n_occurrences": 0}
                per_source[source_id][name] = rec
            rec["files"].add(label)
            rec["n_occurrences"] += n
            if rec["status"] == "mapped":
                mapped += 1
                covered.add(rec["canonical_name"])
            elif rec["rule"] == "unrecognised":
                excl_unrec += 1
            else:
                excl_nn += 1
        neuron_like = mapped + excl_unrec
        coverage_rows.append([
            source_id, label, len(counts), mapped, excl_nn, excl_unrec,
            f"{100.0 * mapped / neuron_like:.2f}" if neuron_like else "",
            len(covered & plain), f"{100.0 * len(covered & plain) / len(plain):.2f}",
            ";".join(sorted(covered - plain)),
        ])

    exclusions = []
    review = []
    for source_id in sorted(per_source):
        rows = []
        for name in sorted(per_source[source_id]):
            r = per_source[source_id][name]
            needs_review = int(r["status"] == "mapped" and r["rule"] != "exact")
            rows.append([name, ";".join(sorted(r["files"])), r["n_occurrences"], r["status"],
                         r["canonical_name"], r["rule"], needs_review, r["reason"]])
            if r["status"] == "excluded":
                exclusions.append([source_id, name, ";".join(sorted(r["files"])), r["n_occurrences"], r["rule"], r["reason"]])
            if needs_review:
                review.append([source_id, name, r["canonical_name"], r["rule"], r["reason"]])
        _write_csv(OUT_DIR / f"mapping_{source_id}.csv",
                   ["source_name", "files", "n_occurrences", "status", "canonical_name", "rule", "needs_review", "reason"],
                   rows)

    cg = cengen_mapping(table)
    _write_csv(OUT_DIR / "mapping_taylor2021_cengen_types.csv", ["cengen_type", "members", "n_members", "rule", "reason"],
               [[r["cengen_type"], ";".join(r["members"]), len(r["members"]), r["rule"], r["reason"]] for r in cg])
    cg_cov = {m for r in cg for m in r["members"]}
    coverage_rows.append([
        "taylor2021", "cengen_021821 cell types (one-to-many)", len(cg),
        sum(1 for r in cg if r["rule"] != "unrecognised"), 0, sum(1 for r in cg if r["rule"] == "unrecognised"),
        f"{100.0 * sum(1 for r in cg if r['rule'] != 'unrecognised') / len(cg):.2f}",
        len(cg_cov & plain), f"{100.0 * len(cg_cov & plain) / len(plain):.2f}", ";".join(sorted(cg_cov - plain)),
    ])
    for r in cg:
        if r["rule"] == "unrecognised":
            exclusions.append(["taylor2021", r["cengen_type"], "cengen_021821 cell types", 1, "unrecognised", r["reason"]])
        elif r["rule"] == "explicit_table":
            review.append(["taylor2021", r["cengen_type"], ";".join(r["members"]), r["rule"], r["reason"]])

    _write_csv(OUT_DIR / "exclusions.csv", ["source_id", "source_name", "files", "n_occurrences", "rule", "reason"],
               sorted(exclusions))
    _write_csv(OUT_DIR / "needs_review.csv", ["source_id", "source_name", "canonical_name", "rule", "reason"],
               sorted(review))
    _write_csv(OUT_DIR / "coverage.csv",
               ["source_id", "file", "distinct_names", "mapped", "excluded_non_neuronal", "excluded_unrecognised",
                "pct_mapped_of_neuron_like", "canonical_302_covered", "pct_canonical_302_covered", "extension_ids_covered"],
               coverage_rows)
    return {
        "sources": sorted(per_source) + ["taylor2021"],
        "exclusions": len(exclusions),
        "unrecognised": sum(1 for e in exclusions if e[4] == "unrecognised"),
        "needs_review": len(review),
    }


if __name__ == "__main__":
    print(json.dumps(build(), indent=2, sort_keys=True))
