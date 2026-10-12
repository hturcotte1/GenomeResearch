"""Phase 3: reproduce numbers the source papers report, from the acquired raw files.

Each test names the paper figure it reproduces and where that figure was read
(see the source's docs/provenance record). Counts are recomputed here from the
raw files, where practical independently of the acquisition modules.

Numbers that do NOT reproduce are kept as tests marked
``xfail(strict=True)`` with a reason starting "BLOCKER". They stay visible in
every test run, and fail loudly if the mismatch ever disappears. No tolerance
was widened to make anything pass.
"""

from __future__ import annotations

import json
from collections import Counter

import numpy as np
import pytest

from src.acquire.common import RAW_ROOT
from src.acquire.randi2023 import head188_ids
from src.merge import readers
from src.namespace.canonical import canonical_neurons



# ------------------------------------------------------------------ Randi et al. 2023

def _randi_head_counts(filename):
    a = readers.randi_atlas(filename)
    ids = a["ids"]
    idx = [ids.index(n) for n in head188_ids(ids, readers.randi_ganglia())]
    ix = np.ix_(idx, idx)
    q = a["wt"]["q"][ix]
    fin = np.isfinite(q)
    sig = fin & (np.nan_to_num(q, nan=1.0) < 0.05)
    dff = a["wt"]["dFF"][ix]
    return a, ids, fin, sig, dff


def test_randi_nature_measured_pairs_23433_and_connections_1310():
    """Nature 623:406: "1,310 of the 23,433 measured neuron pairs, or 6%, ... q < 0.05"."""
    _, _, fin, sig, _ = _randi_head_counts("funatlas.h5")
    assert int(fin.sum()) == 23433
    assert int(sig.sum()) == 1310
    assert round(100 * 1310 / 23433) == 6


def test_randi_preprint_measured_pairs_23427_from_the_2023_06_14_release():
    """arXiv:2208.04790: "... for 23,427 neuron pairs ... at least once". Reproduced by the earlier release."""
    _, _, fin, _, _ = _randi_head_counts("funatlas_release-2023-06-14.h5")
    assert int(fin.sum()) == 23427


def test_randi_acquired_release_does_not_give_the_preprint_23427():
    """The brief's 23,427 is NOT the acquired 2023-06-28 release's count; the difference is the data release."""
    _, _, fin, _, _ = _randi_head_counts("funatlas.h5")
    assert int(fin.sum()) != 23427


def test_randi_eleven_percent_inhibitory():
    """Nature: "11% of q < 0.05 functional connections are inhibitory"."""
    _, _, _, sig, dff = _randi_head_counts("funatlas.h5")
    inh = int((sig & (np.nan_to_num(dff) < 0)).sum())
    exc = int((sig & (np.nan_to_num(dff) > 0)).sum())
    assert (inh, exc) == (150, 1159)
    assert round(100 * inh / (inh + exc)) == 11


def test_randi_fifty_three_candidate_extrasynaptic_pairs():
    """Nature: "Fifty-three pairs of neurons met their criteria" (WT q<0.05, unc-31 q_eq<0.05, q>0.05; off-diagonal)."""
    a = readers.randi_atlas("funatlas.h5")
    qw, qu, tu = a["wt"]["q"], a["unc31"]["q"], a["unc31"]["q_eq"]
    with np.errstate(invalid="ignore"):
        strict = (qw < 0.05) & (tu < 0.05) & (qu > 0.05) & np.isfinite(qw) & np.isfinite(qu)
    np.fill_diagonal(strict, False)
    assert int(strict.sum()) == 53


# ------------------------------------------------------------------ Fenyves et al. 2020

def test_fenyves_3638_connections_and_20589_synapses():
    """PLoS Comput Biol 16:e1007974: "(3,638 connections and 20,589 synapses total)"."""
    rows = readers.fenyves_sign_rows()
    assert len(rows) == 3638
    assert {r["edge_type"] for r in rows} == {"chemical"}
    assert sum(r["synapses"] for r in rows) == 20589


def test_fenyves_predicted_excitatory_inhibitory_complex_synapses():
    """Paper: "We predicted that 9,070 of the synapses are excitatory and 2,580 are inhibitory, while 3,413 ... complex"."""
    by = Counter()
    for r in readers.fenyves_sign_rows():
        by[r["prediction"]] += r["synapses"]
    assert by["+"] == 9070
    assert by["-"] == 2580
    assert by["complex"] == 3413
    assert by["no pred"] == 5526
    assert round(100 * (20589 - 5526) / 20589) == 73  # "polarities for 73% of all ionotropic chemical synapses"


def test_fenyves_excitatory_inhibitory_ratio_is_the_papers_close_to_4_to_1():
    """The paper's E:I is 'close to 4:1'. The exact synapse-weighted ratio implied by its counts is 9,070/2,580 = 3.5155.

    The owner's brief targets "approximately 4:1". That target is the paper's
    rounding, not a separately reported number. This test asserts the exact
    ratio the reported counts imply, with no tolerance.
    """
    by = Counter()
    for r in readers.fenyves_sign_rows():
        by[r["prediction"]] += r["synapses"]
    assert by["+"] / by["-"] == 9070 / 2580
    assert f"{by['+'] / by['-']:.4f}" == "3.5155"


# ------------------------------------------------------------------ White-lineage connectome (Varshney 2011 consolidation)

def _varshney_rows():
    import xlrd

    book = xlrd.open_workbook(str(RAW_ROOT / "white1986" / "NeuronConnect.xls"))
    sh = book.sheet_by_index(0)
    rows = []
    for i in range(1, sh.nrows):
        n1, n2, typ, nbr = (sh.cell_value(i, j) for j in range(4))
        rows.append((str(n1), str(n2), str(typ), int(nbr)))
    return rows


def test_varshney_published_counts():
    """Varshney et al. 2011 (arXiv:0907.2373): 279 neurons, 2194 directed chemical connections,
    514 gap-junction connections, 890 gap junctions, 1410 neuromuscular junctions."""
    rows = _varshney_rows()
    chem = Counter()
    for n1, n2, t, w in rows:
        if t in ("S", "Sp"):
            chem[(n1.upper(), n2.upper())] += w
    assert sum(1 for v in chem.values() if v > 0) == 2194
    ej = {}
    for n1, n2, t, w in rows:
        if t == "EJ":
            key = tuple(sorted((n1, n2)))
            ej[key] = max(ej.get(key, 0), w)
    assert sum(1 for k in ej if k[0] != k[1]) == 514
    assert sum(ej.values()) == 890  # includes the 3 self-pairs (RIBL, RIBR, VA08)
    assert sum(w for _, _, t, w in rows if t == "NMJ") == 1410
    names = {n for n1, n2, t, w in rows if t != "NMJ" and w > 0 for n in (n1, n2) if n.isupper()}
    assert len(names) == 279


@pytest.mark.xfail(strict=True, reason="BLOCKER: Varshney 2011 reports 6393 chemical synapses; NeuronConnect.xls and the authors' own .mat sum to 6394")
def test_varshney_published_chemical_synapses_6393():
    """BLOCKER: Varshney et al. report 6393 chemical synapses. The acquired NeuronConnect.xls sums to 6394,
    and so does the authors' own released matrix (lrvarshney/elegans ConnOrdered_040903.mat, per the
    Phase 1 verifier). The paper figure conflicts with the authors' released data. Unresolved."""
    rows = _varshney_rows()
    assert sum(w for _, _, t, w in rows if t in ("S", "Sp")) == 6393


@pytest.mark.xfail(strict=True, reason="BLOCKER: Cook 2019 reports 4,887 herm chemical edges; all SI 5 workbooks have 4,879 nonzero cells")
def test_cook2019_hermaphrodite_chemical_edges_4887():
    """BLOCKER: Cook et al. 2019 report 4,887 hermaphrodite chemical edges; every SI 5 workbook
    (Nature ESM, WormWiring original, July 2020 correction) has 4,879 nonzero cells. Not used by
    the merged table (Cook 2019 is an acquired alternative, not a default)."""
    from src.acquire import white1986

    counts = white1986._cook_counts(RAW_ROOT / "white1986" / "41586_2019_1352_MOESM9_ESM.xlsx")[0]["per_sheet"]
    assert counts["hermaphrodite chemical"]["nonzero_cells"] == 4887


# ------------------------------------------------------------------ Witvliet et al. 2021

@pytest.mark.parametrize("dataset, edges, synapses", [(7, 2202, 7467), (8, 2186, 7970)])
def test_witvliet_published_adult_chemical_counts(dataset, edges, synapses):
    """Witvliet et al. 2021, author's supplementary synapse-count tables (dwitvliet/nature2021):
    dataset 7: 2,202 connections / 7,467 synapses; dataset 8: 2,186 / 7,970."""
    e = [x for x in readers.nemanode_json("witvliet2021", f"nemanode_baf8ec8__witvliet_2020_{dataset}.json")
         if x.kind == "chemical"]
    pairs = Counter()
    for x in e:
        pairs[(x.pre, x.post)] += x.weight
    assert len(pairs) == edges
    assert sum(pairs.values()) == synapses


# ------------------------------------------------------------------ Ripoll-Sánchez et al. 2023

def _degrees(filename):
    import csv
    import io

    rows = list(csv.reader(io.StringIO((RAW_ROOT / "ripollsanchez2023" / filename).read_text(encoding="utf-8"))))
    labels = rows[0][1:]
    m = np.array([[float(v) for v in r[1:]] for r in rows[1:]])
    off = m.copy()
    np.fill_diagonal(off, 0)
    b = off > 0
    return labels, b.sum(axis=1), b.sum(axis=0), m


def _table_s6():
    import openpyxl

    wb = openpyxl.load_workbook(RAW_ROOT / "ripollsanchez2023" / "1-s2.0-S0896627323007560-mmc7.xlsx",
                                read_only=True, data_only=True)
    ws = wb["Neuron information"]
    out = {}
    for r in ws.iter_rows(min_row=3, values_only=True):
        if r[0] is None:
            continue
        out[str(r[0])] = {"deg_mid": r[4], "deg_short": r[5], "in_mid": r[6], "in_short": r[7],
                          "out_mid": r[8], "out_short": r[9]}
    wb.close()
    return out


@pytest.mark.parametrize("model", ["short", "mid"])
def test_ripoll_2023_matrices_reproduce_table_s6_degrees(model):
    """Neuron 111:3570, Table S6 'Neuron information': per-neuron in/out/total degree at EC50 500 nM."""
    labels, out_deg, in_deg, _ = _degrees(f"08062023_neuropeptide_connectome_{model}_range_model.csv")
    s6 = _table_s6()
    assert len(labels) == 302 and set(labels) == set(s6)
    for i, n in enumerate(labels):
        assert in_deg[i] == s6[n][f"in_{model}"], n
        assert out_deg[i] == s6[n][f"out_{model}"], n
        assert in_deg[i] + out_deg[i] == s6[n][f"deg_{model}"], n


def test_ripoll_rich_clubs_156_and_166():
    """Paper: rich club of 156 neurons (166 in a mid-range network); Table S6 thresholds 203 / 251."""
    s6 = _table_s6()
    assert sum(1 for v in s6.values() if v["deg_short"] >= 203) == 156
    assert sum(1 for v in s6.values() if v["deg_mid"] >= 251) == 166


@pytest.mark.parametrize("model, density", [("short", "0.3437"), ("mid", "0.4429")])
def test_ripoll_preprint_era_matrices_reproduce_text_densities(model, density):
    """Paper text densities 0.3437 (short) and 0.4429 (mid) are reproduced by the 07072022 matrices."""
    import csv
    import io

    text = (RAW_ROOT / "ripollsanchez2023" / f"07072022_neuropeptide_connectome_{model}_range_model").read_text(encoding="utf-8")
    m = np.array([[float(v) for v in r] for r in csv.reader(io.StringIO(text))])
    np.fill_diagonal(m, 0)
    assert f"{(m > 0).sum() / (302 * 301):.4f}" == density


@pytest.mark.xfail(strict=True, reason="BLOCKER: 08062023 matrices reproduce Table S6 but not the text densities (0.3444/0.4439 vs 0.3437/0.4429)")
@pytest.mark.parametrize("model, density", [("short", "0.3437"), ("mid", "0.4429")])
def test_ripoll_tabulated_2023_matrices_reproduce_text_densities(model, density):
    """BLOCKER: the 08062023 matrices used in the merged table reproduce Table S6 exactly but not the
    densities quoted in the text (they give 0.3444 / 0.4439). No single released version reproduces
    every published number (Phase 1 ripollsanchez2023 provenance)."""
    _, _, _, m = _degrees(f"08062023_neuropeptide_connectome_{model}_range_model.csv")
    np.fill_diagonal(m, 0)
    assert f"{(m > 0).sum() / (302 * 301):.4f}" == density


@pytest.mark.xfail(strict=True, reason="BLOCKER: Ripoll-Sanchez quote monoamine density 0.0236; 08062023_monoamine_connectome.csv gives 0.0315")
def test_ripoll_monoamine_network_density_0_0236():
    """BLOCKER: Ripoll-Sánchez et al. quote a monoamine network density of 0.0236; the acquired
    08062023_monoamine_connectome.csv gives 0.0315 (2,866 off-diagonal edges)."""
    _, _, _, m = _degrees("08062023_monoamine_connectome.csv")
    np.fill_diagonal(m, 0)
    assert f"{(m > 0).sum() / (302 * 301):.4f}" == "0.0236"


# ------------------------------------------------------------------ Bentley et al. 2016

def test_bentley_monoamine_and_neuropeptide_connection_counts():
    """PLoS Comput Biol 12:e1005283: "1940 monoamine connections"; neuropeptide network "239 neurons ...
    with 7035 connections"; 18 monoamine-releasing neurons."""
    ma = readers.bentley_edgelist("edgelist_MA.csv")
    np_ = readers.bentley_edgelist("edgelist_NP.csv")
    assert len({(e.pre, e.post) for e in ma if e.pre != e.post}) == 1940
    assert len({e.pre for e in ma}) == 18
    assert len({(e.pre, e.post) for e in np_ if e.pre != e.post}) == 7035
    assert len({e.pre for e in np_} | {e.post for e in np_}) == 239


# ------------------------------------------------------------------ canonical list (White et al. 1986)

def test_white1986_302_neurons_in_118_classes():
    """White et al. 1986 abstract: "a total complement of 302 neurons" grouped into 118 classes."""
    plain = [c for c in canonical_neurons() if not c.is_extension]
    assert len(plain) == 302
    assert len({c.neuron_class for c in plain}) == 118
