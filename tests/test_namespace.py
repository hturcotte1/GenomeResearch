"""Phase 2 validation of the canonical namespace and the per-source mappings."""

import csv
import hashlib

import pytest

from src.namespace import mapping
from src.namespace.canonical import AWC_EXTENSIONS, canonical_neurons

OUT = mapping.OUT_DIR
ALLOWED_MAPPED_RULES = {"alias", "exact", "strip_whitespace", "vnc_zero_padding"}


def _rows(name):
    with open(OUT / name, encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def test_canonical_list_is_the_302_plus_two_awc_identities():
    table = canonical_neurons()
    plain = [c for c in table if not c.is_extension]
    assert len(plain) == 302
    assert sorted(c.name for c in table if c.is_extension) == sorted(AWC_EXTENSIONS)
    assert len({c.neuron_class for c in plain}) == 118
    assert sum(c.is_pharyngeal for c in plain) == 20
    assert len({c.name for c in table}) == len(table)


def test_every_mapping_lands_in_the_canonical_set_by_an_allowed_rule():
    canon = {c.name for c in canonical_neurons()}
    for path in sorted(OUT.glob("mapping_*.csv")):
        if path.name == "mapping_taylor2021_cengen_types.csv":
            continue
        for r in _rows(path.name):
            if r["status"] == "mapped":
                assert r["canonical_name"] in canon, (path.name, r)
                assert r["rule"] in ALLOWED_MAPPED_RULES, (path.name, r)
                assert r["needs_review"] == ("0" if r["rule"] == "exact" else "1"), (path.name, r)
            else:
                assert r["status"] == "excluded" and r["canonical_name"] == "" and r["reason"], (path.name, r)


def test_cengen_types_map_only_to_canonical_names():
    canon = {c.name for c in canonical_neurons()}
    for r in _rows("mapping_taylor2021_cengen_types.csv"):
        members = [m for m in r["members"].split(";") if m]
        assert members and set(members) <= canon, r


def test_no_unrecognised_names_and_every_exclusion_has_a_reason():
    rows = _rows("exclusions.csv")
    assert all(r["reason"] for r in rows)
    assert [r for r in rows if r["rule"] == "unrecognised"] == []


def test_every_neuron_like_name_in_every_source_is_mapped():
    for r in _rows("coverage.csv"):
        assert r["excluded_unrecognised"] == "0", r
        assert r["pct_mapped_of_neuron_like"] == "100.00", r


def test_committed_namespace_artifacts_are_reproducible():
    def digest():
        return {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(OUT.glob("*.csv"))}

    before = digest()
    mapping.build()
    assert digest() == before, "namespace artifacts are stale or non-deterministic; rebuild and commit"
