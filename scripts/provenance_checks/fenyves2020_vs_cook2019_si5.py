"""Cross-source check: is Fenyves et al. 2020's input connectome Cook et al. 2019 SI 5?

Compares the xlsx's sheet "5. Sign prediction" (data/raw/fenyves2020) with the
"hermaphrodite chemical" sheet of each Cook et al. 2019 SI 5 workbook acquired
by white1986 (data/raw/white1986). Reads only those raw files, makes no network
calls and prints sorted JSON, so the output is deterministic.

Run from the repository root:

    .venv/bin/python scripts/provenance_checks/fenyves2020_vs_cook2019_si5.py

Reading conventions (from the files themselves):

- SI 5 "TITLE AND LEGEND": "For chemical connections, rows give the
  pre-synaptic cell, columns give the post-synaptic cell", and weights are
  "the total number of EM serial sections". Row labels are in column C from
  row 4, column labels in row 3 from column D. Non-integer cells are skipped
  and counted; values under a repeated label pair are added.
- Sheet 5: data rows are rows >= 3 with a non-empty column A; Source = A,
  Target = D, weight = E (synapse count).
- Both sides are restricted to the 302 names of the xlsx's sheet "1. NT expr".
  No name is changed.
"""

from __future__ import annotations

import hashlib
import json
import sys
import warnings
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
FEN = REPO / "data" / "raw" / "fenyves2020" / "journal.pcbi.1007974.s003.xlsx"
SI5 = [
    REPO / "data" / "raw" / "white1986" / "41586_2019_1352_MOESM9_ESM.xlsx",
    REPO / "data" / "raw" / "white1986" / "SI 5 Connectome adjacency matrices.xlsx",
    REPO / "data" / "raw" / "white1986" / "SI 5 Connectome adjacency matrices, corrected July 2020.xlsx",
]


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _fenyves():
    import openpyxl

    wb = openpyxl.load_workbook(FEN, read_only=True, data_only=True)
    s1 = {r[0] for r in wb["1. NT expr"].iter_rows(min_row=2, values_only=True) if r[0] is not None}
    s5 = {}
    for r in wb["5. Sign prediction"].iter_rows(min_row=3, values_only=True):
        if r[0] is not None:
            s5[(r[0], r[3])] = s5.get((r[0], r[3]), 0) + int(r[4])
    wb.close()
    return s1, s5


def _si5(path: Path):
    import openpyxl

    wb = openpyxl.load_workbook(path, read_only=True)
    legend = " ".join(
        str(v) for row in wb["TITLE AND LEGEND"].iter_rows(values_only=True) for v in row if v is not None
    )
    rows = list(wb["hermaphrodite chemical"].iter_rows(values_only=True))
    wb.close()
    col = {j: v for j, v in enumerate(rows[2]) if j >= 3 and v is not None}
    vals, non_int = {}, 0
    for i in range(3, len(rows)):
        r = rows[i]
        pre = r[2] if len(r) > 2 else None
        if pre is None:
            continue
        for j, post in col.items():
            v = r[j] if j < len(r) else None
            if v is None:
                continue
            if not isinstance(v, int) or isinstance(v, bool):
                non_int += 1
                continue
            vals[(pre, post)] = vals.get((pre, post), 0) + v
    return legend, vals, non_int


def main() -> int:
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=UserWarning)
        s1, s5 = _fenyves()
        out = {
            "fenyves_xlsx": {"file": FEN.name, "sha256": _sha256(FEN)},
            "sheet1_names": len(s1),
            "sheet5_pairs": len(s5),
            "sheet5_weight_sum": sum(s5.values()),
            "si5": {},
        }
        restricted = {}
        for path in SI5:
            legend, vals, non_int = _si5(path)
            m = {k: v for k, v in vals.items() if v and k[0] in s1 and k[1] in s1}
            restricted[path.name] = m
            mt = {(b, a): v for (a, b), v in m.items()}
            common = set(m) & set(s5)
            out["si5"][path.name] = {
                "sha256": _sha256(path),
                "legend_says_rows_presynaptic_columns_postsynaptic": (
                    "rows give the pre-synaptic cell, columns give the post-synaptic cell" in legend
                ),
                "legend_says_weights_are_em_serial_sections": "total number of EM serial sections" in legend,
                "non_integer_cells_skipped": non_int,
                "nonzero_pairs_both_names_in_sheet1": len(m),
                "weight_sum_both_names_in_sheet1": sum(m.values()),
                "pairs_only_in_sheet5": len(set(s5) - set(m)),
                "pairs_only_in_si5": len(set(m) - set(s5)),
                "pairs_in_both": len(common),
                "pairs_in_both_with_different_weight": sum(1 for k in common if s5[k] != m[k]),
                "pairs_in_both_with_different_weight_list": sorted(
                    [a, b, s5[(a, b)], m[(a, b)]] for (a, b) in common if s5[(a, b)] != m[(a, b)]
                ),
                "transposed_orientation_pairs_in_both": len(set(mt) & set(s5)),
            }
        names = sorted(restricted)
        out["si5_restricted_matrices_identical_across_files"] = all(
            restricted[n] == restricted[names[0]] for n in names
        )
    print(json.dumps(out, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
