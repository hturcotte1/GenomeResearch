"""Canonical C. elegans hermaphrodite neuron namespace: the single source of truth.

The canonical name set is the WormAtlas-standard list of 302 hermaphrodite
neurons. wormatlas.org is blocked in the build environment, so the list is
assembled from the acquired secondary copies (source ``canonical_neurons``)
and cross-checked:

1. ``IndividualNeurons.csv``: OpenWorm's copy of WormAtlas NeuronNames.htm
   (hermaphrodite and male neurons).
2. ``C. elegans Cell List - WormBase.csv``: its "Neurons (no male-specific
   cells)" column marks the 302 hermaphrodite neurons.

The canonical set is the names in (1) that (2) marks as hermaphrodite neurons.
Three further lists must equal it exactly, or the build fails:

- ``Cells.py`` PREFERRED_HERM_NEURON_NAMES (ConnectomeToolbox);
- owmeta ``neurons.csv``;
- the NemaNode cell table's neuron entries.

Neuron classes come from the NemaNode cell table's ``classes`` field, which
gives White et al.'s 118 classes over the 302.

Two *extension* identities are added for AWC: ``AWCON`` and ``AWCOFF``. These
are functional identities, assigned per animal by odorant-receptor expression;
they are not positions. They exist because the Randi atlas and CeNGEN name AWC
this way, and the per-animal correspondence with AWCL/AWCR is not fixed. How
they relate to AWCL/AWCR is set by ``awc_policy`` (``config/pipeline.json``);
see ``src/namespace/mapping.py``.
"""

from __future__ import annotations

import csv
import io
import json
from dataclasses import dataclass

from src.acquire import canonical_neurons as cn
from src.acquire.common import RAW_ROOT

AWC_EXTENSIONS = ("AWCOFF", "AWCON")


@dataclass(frozen=True)
class CanonicalNeuron:
    name: str
    neuron_class: str
    is_pharyngeal: bool
    is_extension: bool
    nemanode_inhead: int | None
    wormatlas_description: str


def _raw(name: str) -> str:
    return (RAW_ROOT / cn.SOURCE_ID / name).read_bytes().decode("utf-8")


def _wormatlas_neuronnames() -> dict[str, str]:
    """{name: description} from IndividualNeurons.csv (WormAtlas NeuronNames copy)."""
    first, rows = cn._individual_neurons()
    if "wormatlas.org/NeuronNames" not in first:
        raise ValueError("IndividualNeurons.csv no longer states its WormAtlas origin")
    out: dict[str, str] = {}
    for r in rows:
        name = r[0].strip()
        desc = r[3].strip() if len(r) > 3 else ""
        out.setdefault(name, desc)
    return out


def _wormbase_herm_neurons() -> list[str]:
    rows = list(csv.reader(io.StringIO(_raw(cn.F_WB_CSV))))
    header = rows[1]
    col = header.index("Neurons (no male-specific cells)")
    stated_total = int(rows[2][col])
    names = [r[0] for r in rows[3:] if len(r) > col and r[col].strip() == "1"]
    if len(names) != stated_total:
        raise ValueError(f"WormBase.csv neuron column marks {len(names)} names, its total row says {stated_total}")
    return names


def _nemanode_cells() -> dict[str, dict]:
    return {c["name"]: c for c in json.loads(_raw(cn.F_NEMANODE))}


def canonical_neurons() -> list[CanonicalNeuron]:
    """The canonical table, sorted by name. Raises if the cross-checks fail."""
    wa = _wormatlas_neuronnames()
    herm = _wormbase_herm_neurons()
    canon = sorted(n for n in herm if n in wa)
    if len(canon) != len(herm) or len(canon) != 302:
        missing = sorted(set(herm) - set(wa))
        raise ValueError(f"canonical set has {len(canon)} names; WormBase herm neurons absent from WormAtlas copy: {missing}")

    lists = cn._cells_py_lists()
    cells_py = sorted(lists["PREFERRED_HERM_NEURON_NAMES"])
    ow = sorted(r[0].strip() for r in cn._ow_neurons())
    nn = _nemanode_cells()
    nn_neurons = sorted(n for n in canon if n in nn)
    for label, other in (("Cells.py", cells_py), ("owmeta neurons.csv", ow), ("NemaNode", nn_neurons)):
        if other != canon:
            raise ValueError(f"{label} disagrees with the canonical set: "
                             f"extra {sorted(set(other) - set(canon))}, missing {sorted(set(canon) - set(other))}")

    pharyngeal = set(
        lists["PHARYNGEAL_INTERNEURONS"] + lists["PHARYNGEAL_MOTORNEURONS"] + lists["PHARYNGEAL_POLYMODAL_NEURONS"]
    )
    if len(pharyngeal) != 20 or not pharyngeal <= set(canon):
        raise ValueError(f"pharyngeal list is not 20 canonical names: {sorted(pharyngeal)}")

    out = [
        CanonicalNeuron(
            name=n,
            neuron_class=nn[n]["classes"],
            is_pharyngeal=n in pharyngeal,
            is_extension=False,
            nemanode_inhead=nn[n].get("inhead"),
            wormatlas_description=wa[n],
        )
        for n in canon
    ]
    for ext in AWC_EXTENSIONS:
        out.append(
            CanonicalNeuron(
                name=ext,
                neuron_class=nn["AWCL"]["classes"],
                is_pharyngeal=False,
                is_extension=True,
                nemanode_inhead=nn["AWCL"].get("inhead"),
                wormatlas_description="Functional identity of an AWC neuron (str-2 expressing ON / non-expressing OFF); "
                "assigned per animal, not a position. Extension to the WormAtlas list.",
            )
        )
    return sorted(out, key=lambda c: c.name)


def canonical_names(include_extensions: bool = True) -> list[str]:
    return [c.name for c in canonical_neurons() if include_extensions or not c.is_extension]


def classes() -> dict[str, str]:
    return {c.name: c.neuron_class for c in canonical_neurons()}
