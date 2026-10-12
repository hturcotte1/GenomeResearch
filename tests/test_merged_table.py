"""Phase 4: structural, provenance and determinism checks on the merged edge table."""

import csv
import hashlib
import json

import pyarrow.parquet as pq
import pytest

from src.acquire.common import RAW_ROOT
from src.merge import build_table
from src.merge.build_table import COLUMN_ORDER, OUT_DIR, STATES, TABLE


@pytest.fixture(scope="module")
def rows():
    return pq.read_table(OUT_DIR / f"{TABLE}.parquet").to_pylist()


def test_shape_and_keys(rows):
    assert list(pq.read_schema(OUT_DIR / f"{TABLE}.parquet").names) == COLUMN_ORDER
    heads = sorted({r["pre"] for r in rows})
    assert len(heads) == 189 and "RMHR" in heads and {"AWCON", "AWCOFF"} <= set(heads)
    assert len(rows) == 189 * 188
    keys = [(r["pre"], r["post"]) for r in rows]
    assert len(set(keys)) == len(keys)
    assert all(a != b for a, b in keys)
    assert keys == sorted(keys)


def test_randi_states_reproduce_the_atlas(rows):
    st = {s: sum(1 for r in rows if r["randi_state_wt"] == s) for s in STATES}
    assert st["connected"] == 1151  # 1,310 minus the 159 self-pairs
    assert sum(r["randi_strict_extrasynaptic_candidate"] for r in rows) == 53
    assert sum(1 for r in rows if r["measured_q_wt"] is not None) == 23433 - 168


def test_tested_and_untested_are_never_conflated(rows):
    for r in rows:
        if r["randi_state_wt"] == "not_observed":
            assert not r["randi_tested"] and r["measured_q_wt"] is None and r["measured_occurrences_wt"] == 0
        else:
            assert r["randi_tested"]
        if r["randi_state_wt"] == "observed_all_trials_discarded":
            assert r["measured_q_wt"] is None and r["measured_n_wt"] == 0 and r["measured_occurrences_wt"] > 0
        if r["measured_q_wt"] is not None:
            assert r["measured_n_wt"] > 0
        if r["measured_sign_wt"] is not None:
            assert r["randi_state_wt"] == "connected"


def test_every_null_anatomical_value_is_explained_by_a_flag(rows):
    for r in rows:
        flags = set(r["source_flags"].split(";")) if r["source_flags"] else set()
        for key in ("white_n2u", "white_jsh", "witvliet_d7", "witvliet_d8"):
            if r[f"anat_chem_{key}"] is None:
                assert f"{key}_not_covered" in flags or "awc_identity_unresolved" in flags, (r["pre"], r["post"], key)
        if r["np_edge_short"] is None or r["monoamine_edge"] is None or r["anat_chem_white_whole"] is None:
            assert "awc_identity_unresolved" in flags


def test_csv_and_parquet_hold_the_same_rows(rows):
    with open(OUT_DIR / f"{TABLE}.csv", encoding="utf-8", newline="") as fh:
        csv_rows = list(csv.DictReader(fh))
    assert len(csv_rows) == len(rows)
    for a, b in zip(rows, csv_rows):
        for c in COLUMN_ORDER:
            v = a[c]
            expected = "" if v is None else ("true" if v is True else "false" if v is False else
                                             repr(v) if isinstance(v, float) else str(v))
            assert b[c] == expected, (a["pre"], a["post"], c)


def test_every_column_has_provenance_with_current_hashes():
    meta = json.loads((OUT_DIR / f"{TABLE}.columns.json").read_text(encoding="utf-8"))
    assert set(COLUMN_ORDER) <= set(meta)
    for c in COLUMN_ORDER:
        m = meta[c]
        assert m["definition"]
        for f in m["files"]:
            manifest = json.loads((RAW_ROOT / m["source_id"] / "MANIFEST.json").read_text(encoding="utf-8"))
            assert {"filename": f["filename"], "sha256": f["sha256"]} in [
                {"filename": e["filename"], "sha256": e["sha256"]} for e in manifest["files"]], (c, f)


def test_build_is_byte_identical_to_the_committed_artifact():
    recorded = (OUT_DIR / "SHA256SUMS").read_text(encoding="utf-8")
    build_table.build()
    rebuilt = "".join(
        f"{hashlib.sha256((OUT_DIR / n).read_bytes()).hexdigest()}  {n}\n"
        for n in sorted(p.name for p in OUT_DIR.iterdir() if p.name.startswith(TABLE))
    )
    assert rebuilt == recorded


def _excluded(source_id, filename, unit):
    with open(OUT_DIR / f"{TABLE}_exclusions.csv", encoding="utf-8", newline="") as fh:
        return sum(int(r["n_records"]) for r in csv.DictReader(fh)
                   if r["source_id"] == source_id and r["file"] == filename
                   and r["category"] in ("awc_identity_unresolved", "out_of_head_scope", "self_pair")
                   and r["reason"].startswith(f"distinct {unit} "))


@pytest.mark.parametrize("key", ["n2u", "jsh", "whole"])
def test_every_white_pair_is_in_the_table_or_logged(rows, key):
    """No silent drops: neuron pairs in a source = pairs with a row value + logged exclusions."""
    from src.merge import readers

    fn = build_table.WHITE_FILES[key]
    names = build_table._name_map("white1986")
    chem, gap = set(), set()
    for e in readers.nemanode_tsv("white1986", fn):
        a, b = names.get(e.pre), names.get(e.post)
        if a is None or b is None or not e.weight:
            continue
        (chem.add((a, b)) if e.kind == "chemical" else gap.add(frozenset((a, b))))
    in_chem = sum(1 for r in rows if (r[f"anat_chem_white_{key}"] or 0) > 0)
    in_gap = sum(1 for r in rows if (r[f"anat_gap_white_{key}"] or 0) > 0 and r["pre"] < r["post"])
    assert in_chem + _excluded("white1986", fn, "ordered chemical") == len(chem)
    assert in_gap + _excluded("white1986", fn, "unordered electrical") == len(gap)


@pytest.mark.parametrize("rng", ["short", "mid", "long"])
def test_every_neuropeptide_pair_is_in_the_table_or_logged(rows, rng):
    from src.merge import readers

    fn = build_table.NP_FILES[("08062023", rng)]
    names = build_table._name_map("ripollsanchez2023")
    pairs = {(names[e.pre], names[e.post]) for e in readers.ripoll_matrix(fn) if e.weight}
    in_table = sum(1 for r in rows if (r[f"np_edge_{rng}"] or 0) > 0)
    assert in_table + _excluded("ripollsanchez2023", fn, "ordered neuropeptide") == len(pairs)
