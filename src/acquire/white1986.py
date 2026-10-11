"""White et al. 1986 anatomical connectome, in every reachable White-lineage variant.

"White 1986" is not one dataset (owner question Q-007). White et al. reconstructed
two head series, N2U (adult hermaphrodite) and JSH (L4), plus partial ventral
cord and tail series. Every machine-readable version in circulation is a later
compilation or re-annotation of those EM series. This module acquires each
variant an owner could select for ``anat_chem_white`` / ``anat_gap``, and
records what each one is. It does not choose one.

Variants acquired (all SECONDARY copies; see docs/provenance/white1986.md):

1. NemaNode exports, as bundled in the ``wormneuroatlas`` 0.0.7.3 wheel
   (``wna__aconnectome_white_1986_{whole,A,L4}.csv``). These are what Randi et
   al.'s code loads: ``aconn_sources`` type ``whiteA`` loads the **_whole**
   file (not ``_A``), and type ``whiteL4`` loads ``_L4``. ``_A`` is shipped
   but loaded by no code in the wheel or in leiferlab/pumpprobe.
   - ``_A`` = NemaNode dataset ``white_1986_n2u`` and ``_L4`` = NemaNode
     ``white_1986_jsh``: Durbin's 1987 compilation of the N2U / JSH head
     series, with muscle synapses re-annotated by the Zhen lab.
   - ``_whole`` = NemaNode ``white_1986_whole`` ("White et al., 1986
     compilation"): somatic data as compiled by Varshney et al. 2011 plus
     pharynx (Albertson & Thomson 1976). It is a multi-animal compilation,
     not one individual.
2. The NemaNode source JSON for those three datasets, from the Zhen lab's
   repository ``zhenlab-ltri/NemaNode`` at commit da8ca7e, and NemaNode's cell
   table. ``record_counts`` re-derives the CSV export from these with
   NemaNode's own rules and checks that it equals the wheel CSVs.
3. ConnectomeToolbox copies: ``white_1986_jsh.csv`` / ``white_1986_n2u.csv``
   (byte-identical to wheel ``_L4`` / ``_A``) and
   ``cect__aconnectome_white_1986_{whole,A,L4}.csv`` (CRLF re-encodings of the
   wheel files; ``_A`` also has a space-separated header and a final newline).
4. Durbin 1987 ``neurodata.txt`` (both series, per-direction records) and the
   toolbox's edited ``neurodata_updated.txt``.
5. Varshney et al. 2011 ``NeuronConnect.xls`` (somatic, 279-neuron
   re-compilation). A separate paper; attributed to it, not to White.
6. Cook et al. 2019 SI 5 adjacency matrices: the Nature supplement and the two
   WormWiring versions (original, corrected July 2020). A separate paper that
   re-annotated White's prints; weights are EM-section counts, not synapse
   counts.
7. ``aconnectome.json`` (wheel) with its index ``aconnectome_ids.txt`` (from
   leiferlab/pumpprobe): an older, undocumented "white" matrix that Randi et
   al.'s code no longer loads (commented out in pumpprobe's ``aconn_sources``).

Facts later phases must respect (each checked by ``record_counts``):

- Orientation. NemaNode CSVs: ``pre<TAB>post<TAB>type<TAB>synapses``,
  chemical rows are pre -> post. Durbin: ``Send``/``Send_joint`` rows are
  first-name -> second-name, ``Receive``/``Receive_joint`` rows are
  second-name -> first-name. Varshney: ``S``/``Sp`` are Neuron 1 -> Neuron 2,
  ``R``/``Rp`` are Neuron 2 -> Neuron 1. Cook: rows presynaptic, columns
  postsynaptic. aconnectome.json: ``chemical[i][j]`` is ids[i] -> ids[j]
  (pumpprobe Anatlas transposes it to [to, from]).
- Gap-junction encoding differs. NemaNode CSVs list each unordered pair ONCE,
  in arbitrary orientation, with self-pairs (e.g. RIBL-RIBL). NemaNode JSON,
  Durbin, Varshney, Cook "symmetric" sheets and aconnectome.json list both
  directions (double-counted if summed). Cook "asymmetric" sheets list each
  pair once, except 3 hermaphrodite and 2 male pairs listed both ways in the
  as-published files (fixed in the July 2020 correction). Randi's loader
  symmetrises with max().
- Names are as the distributor wrote them: zero-padded (VA01, Varshney/Cook)
  vs not (VA1, NemaNode/Durbin); AWCL/AWCR; lower-case quirks (``avfl``/``avfr``
  in Varshney); muscle pseudo-nodes (``BWM-DL01``..., ``LegacyBodyWallMuscles``,
  ``mu_bod``, ``NMJ``); glia/other (``CEPsh*``, ``hyp``, ``pm1``).
"""

from __future__ import annotations

import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from urllib.parse import quote

from .common import RAW_ROOT, ArchiveMember, RemoteFile, acquire_source, verify_pypi_digest
from .distributions import (
    WORMNEUROATLAS_PACKAGE,
    WORMNEUROATLAS_VERSION,
    WORMNEUROATLAS_WHEEL,
    connectome_toolbox_file,
)

SOURCE_ID = "white1986"
CITATION = (
    "White JG, Southgate E, Thomson JN, Brenner S. The structure of the nervous "
    "system of the nematode Caenorhabditis elegans. Phil Trans R Soc Lond B 314, "
    "1-340 (1986). doi:10.1098/rstb.1986.0056"
)
# Separate papers whose files are acquired here; each file's note says which applies.
RELATED_CITATIONS = {
    "durbin1987": (
        "Durbin RM. Studies on the development and organisation of the nervous system of "
        "Caenorhabditis elegans. PhD thesis, University of Cambridge (1987)."
    ),
    "varshney2011": (
        "Varshney LR, Chen BL, Paniagua E, Hall DH, Chklovskii DB. Structural properties of the "
        "Caenorhabditis elegans neuronal network. PLoS Comput Biol 7(2), e1001066 (2011). "
        "doi:10.1371/journal.pcbi.1001066"
    ),
    "cook2019": (
        "Cook SJ, Jarrell TA, Brittin CA, et al. Whole-animal connectomes of both "
        "Caenorhabditis elegans sexes. Nature 571, 63-71 (2019). doi:10.1038/s41586-019-1352-7"
    ),
    "albertson1976": (
        "Albertson DG, Thomson JN. The pharynx of Caenorhabditis elegans. Phil Trans R Soc "
        "Lond B 275, 299-325 (1976). doi:10.1098/rstb.1976.0085"
    ),
    "randi2023": (
        "Randi F, Sharma AK, Dvali S, Leifer AM. Neural signal propagation atlas of "
        "Caenorhabditis elegans. Nature 623, 406-414 (2023). doi:10.1038/s41586-023-06683-4"
    ),
}

_NEMANODE_SITE = "https://nemanode.org/ (connectivity download)"
PRIMARY_N2U = (
    f"{_NEMANODE_SITE}, dataset id white_1986_n2u ('White et al., 1986, N2U (adult)'); "
    "underlying data: White et al. 1986 doi:10.1098/rstb.1986.0056, compiled by Durbin 1987 "
    "(https://www.wormatlas.org/neurodata.txt), muscles re-annotated by the Zhen lab"
)
PRIMARY_JSH = (
    f"{_NEMANODE_SITE}, dataset id white_1986_jsh ('White et al., 1986, JSH (L4)'); "
    "underlying data: White et al. 1986 doi:10.1098/rstb.1986.0056, compiled by Durbin 1987 "
    "(https://www.wormatlas.org/neurodata.txt), muscles re-annotated by the Zhen lab"
)
PRIMARY_WHOLE = (
    f"{_NEMANODE_SITE}, dataset id white_1986_whole ('White et al., 1986 compilation (adult)'); "
    "underlying data: somatic White et al. 1986 as compiled by Varshney et al. 2011 "
    "(doi:10.1371/journal.pcbi.1001066), pharynx Albertson & Thomson 1976 (doi:10.1098/rstb.1976.0085)"
)
PRIMARY_DURBIN = (
    "https://www.wormatlas.org/neurodata.txt (readme https://www.wormatlas.org/neurodata_readme.txt); "
    "Durbin 1987 thesis https://www.wormatlas.org/Durbin/durbinthesis.pdf"
)
PRIMARY_VARSHNEY = (
    "https://www.wormatlas.org/images/NeuronConnect.xls (Varshney et al. 2011, "
    "doi:10.1371/journal.pcbi.1001066; per the toolbox's cect/validation/VarshneyEtAl2011.md)"
)
PRIMARY_COOK_NATURE = (
    "https://static-content.springer.com/esm/art%3A10.1038%2Fs41586-019-1352-7/MediaObjects/"
    "41586_2019_1352_MOESM9_ESM.xlsx (Cook et al. 2019 Nature, Supplementary Information 5)"
)
PRIMARY_COOK_WW = "https://wormwiring.org/si/SI%205%20Connectome%20adjacency%20matrices.xlsx (Emmons lab, WormWiring)"
PRIMARY_COOK_WW_2020 = (
    "https://wormwiring.org/si/SI%205%20Connectome%20adjacency%20matrices,%20corrected%20July%202020.xlsx "
    "(Emmons lab, WormWiring)"
)

# leiferlab/pumpprobe: Randi et al.'s analysis code. Only the id list that
# indexes aconnectome.json is taken from it.
PUMPPROBE_REPO = "leiferlab/pumpprobe"
PUMPPROBE_COMMIT = "1dbc5e0a2b609d54bc9b1c90c73d4e3bf183d3c7"  # 2023-09-20

# zhenlab-ltri/NemaNode: the source data of nemanode.org. White files last
# changed at da8ca7e; the same blobs are at master head 6b7ca03 (2022-03-16).
NEMANODE_REPO = "zhenlab-ltri/NemaNode"
NEMANODE_COMMIT = "da8ca7e2fc0eece4b21c30625880b41f39961c76"  # 2020-05-22, D. Witvliet
_NN_DIR = "src/server/populate-db/raw-data"


def _wheel(member: str, filename: str, sha256: str, size: int, primary: str, note: str) -> ArchiveMember:
    return ArchiveMember(
        archive=WORMNEUROATLAS_WHEEL,
        member=f"wormneuroatlas/data/{member}",
        filename=filename,
        sha256=sha256,
        size=size,
        primary_reference=primary,
        note=note,
    )


def _toolbox(path: str, filename: str, sha256: str, size: int, blob: str, primary: str, note: str) -> RemoteFile:
    # The toolbox helper puts ``path`` into the URL verbatim, so spaces and
    # commas are percent-encoded here.
    return connectome_toolbox_file(
        quote(path),
        filename=filename,
        sha256=sha256,
        size=size,
        git_blob_sha1=blob,
        primary_reference=primary,
        note=note,
    )


def _nemanode(path: str, filename: str, sha256: str, size: int, blob: str, primary: str, note: str) -> RemoteFile:
    return RemoteFile(
        url=f"https://raw.githubusercontent.com/{NEMANODE_REPO}/{NEMANODE_COMMIT}/{_NN_DIR}/{path}",
        filename=filename,
        sha256=sha256,
        size=size,
        distributor=f"GitHub {NEMANODE_REPO} @ {NEMANODE_COMMIT} (Zhen lab; source data of nemanode.org)",
        origin="secondary",
        primary_reference=primary,
        git_blob_sha1=blob,
        note=note,
    )


FILES = (
    # --- wormneuroatlas 0.0.7.3 wheel: what Randi et al. loaded ---------------
    _wheel(
        "aconnectome_white_1986_whole.csv",
        "wna__aconnectome_white_1986_whole.csv",
        "768d2b16557d768b51f81548f630adb45d76c1f99586e8fd4c90279293cc9dae",
        64492,
        PRIMARY_WHOLE,
        "LOADED by Randi et al. as aconn_sources type 'whiteA' (pumpprobe Funatlas.py and wormneuroatlas "
        "NeuroAtlas.py). NemaNode export of white_1986_whole: Varshney 2011 somatic compilation + pharynx. "
        "Tab-separated, LF, no final newline. Byte-identical to leiferlab/pumpprobe@1dbc5e0a pumpprobe/.",
    ),
    _wheel(
        "aconnectome_white_1986_L4.csv",
        "wna__aconnectome_white_1986_L4.csv",
        "afe7a37a5bae62630a773b5e7815a408e3a72063caf0ed49ecc91e213077fb12",
        39065,
        PRIMARY_JSH,
        "LOADED by Randi et al. as aconn_sources type 'whiteL4'. NemaNode export of white_1986_jsh (JSH, L4, "
        "head). Byte-identical to toolbox white_1986_jsh.csv and to pumpprobe's copy.",
    ),
    _wheel(
        "aconnectome_white_1986_A.csv",
        "wna__aconnectome_white_1986_A.csv",
        "6b63f6c0281b7bbc3be75fa3962e26caa020ddf3756bfc8dd9aad6577655fc16",
        41889,
        PRIMARY_N2U,
        "Shipped in the wheel but NOT loaded by any code in wormneuroatlas or pumpprobe (type 'whiteA' loads "
        "_whole). NemaNode export of white_1986_n2u (N2U, adult, head). Byte-identical to toolbox "
        "white_1986_n2u.csv.",
    ),
    _wheel(
        "aconnectome.json",
        "aconnectome.json",
        "8d45df9db673ec2a03bd0ab1bd3980d16b6305920adf2332dc80b4cb5f5fb29e",
        902866,
        "No primary identified. Undocumented 300x300 matrices (chemical, chemical_sign, electrical) used by "
        "pumpprobe Anatlas source 'white'; the matching 'white' entry in Funatlas.aconn_sources is commented "
        "out. Index: aconnectome_ids.txt from leiferlab/pumpprobe (not in the wheel).",
        "NOT used by Randi et al.'s published analysis. Electrical matrix equals Varshney 2011 EJ; chemical "
        "matrix looks like Varshney 2011 with Sp overwriting S instead of adding (see provenance doc).",
    ),
    RemoteFile(
        url=f"https://raw.githubusercontent.com/{PUMPPROBE_REPO}/{PUMPPROBE_COMMIT}/pumpprobe/aconnectome_ids.txt",
        filename="aconnectome_ids.txt",
        sha256="bfcde4c0ccaadce2f69f44c858caddd7c6f5b27aaac878975042b19fa3f7442d",
        size=2641,
        distributor=f"GitHub {PUMPPROBE_REPO} @ {PUMPPROBE_COMMIT} (Leifer lab; Randi et al. analysis code)",
        origin="secondary",
        primary_reference=f"https://github.com/{PUMPPROBE_REPO} (authors' own repository; no other copy known)",
        git_blob_sha1="1bb809e9eeee15926c0cb850f3dc1ca05e051d80",
        note="300 lines 'index<TAB>name' giving the row/column order of aconnectome.json (pumpprobe Anatlas). "
        "Uses AWCL/AWCR.",
    ),
    # --- NemaNode source data (Zhen lab repository) ---------------------------
    _nemanode(
        "connections/white_1986_n2u.json",
        f"nemanode_{NEMANODE_COMMIT[:7]}__white_1986_n2u.json",
        "ba949e1e1766020009d0db38aa3182b245aa6242bb0359a253cd65d0a6b9a5d4",
        284796,
        "6aafc974cd97be8cc43653bde6b81935a8266858",
        PRIMARY_N2U,
        "NemaNode source records for white_1986_n2u (both gap-junction directions, per-synapse ids). "
        "Same blob at master head 6b7ca03. Differs from the pre-da8ca7e blob (859641e) in 2 chemical edges.",
    ),
    _nemanode(
        "connections/white_1986_jsh.json",
        f"nemanode_{NEMANODE_COMMIT[:7]}__white_1986_jsh.json",
        "ac251c32cfbc3f3ee5add0f4f566c3006b715553e822210cc4ec9f1fc9816dd4",
        271999,
        "3f54979ca00c210b37f205c77e69cab4810a464e",
        PRIMARY_JSH,
        "NemaNode source records for white_1986_jsh. Same blob at master head 6b7ca03. Differs from the "
        "pre-da8ca7e blob (859641e) in 5 chemical edges.",
    ),
    _nemanode(
        "connections/white_1986_whole.json",
        f"nemanode_{NEMANODE_COMMIT[:7]}__white_1986_whole.json",
        "fe7ff4a6529ccb9d13183e665644e30ad8aded887c64b24732808757bddae41d",
        375599,
        "75a28a2706b0834dca9420343f57213e83ce3894",
        PRIMARY_WHOLE,
        "NemaNode source records for white_1986_whole (Varshney 2011 + pharynx). Same blob from 859641e "
        "through master head 6b7ca03. Contains pharyngeal targets the CSV export drops.",
    ),
    _nemanode(
        "neurons.json",
        f"nemanode_{NEMANODE_COMMIT[:7]}__neurons.json",
        "c780e0b7cab28b311a7e0916a7b8e37b9cf72de152712bd4a5eb29fd9d595492",
        58575,
        "81da4572b20674dcc852cfa9fd041e66a3c7a73c",
        f"{_NEMANODE_SITE}; NemaNode cell table",
        "NemaNode cell table. Its names define which rows NemaNode's CSV export keeps "
        "(src/server/db/download-data.js). Same blob as witvliet2021's nemanode_baf8ec8__neurons.json.",
    ),
    # --- ConnectomeToolbox copies ---------------------------------------------
    _toolbox(
        "cect/data/white_1986_jsh.csv",
        "white_1986_jsh.csv",
        "afe7a37a5bae62630a773b5e7815a408e3a72063caf0ed49ecc91e213077fb12",
        39065,
        "15577df82afdc9c842ae2a661bbd2ad55651dece",
        PRIMARY_JSH,
        "NemaNode-named copy; read by no toolbox reader. Byte-identical to wheel _L4 and to "
        "Nondairy-Creamer/Creamer_LDS_2026 anatomical_data/worm_connectomes/white_1986_jsh.csv, which its "
        "README says was downloaded from NemaNode on 2025-11-01.",
    ),
    _toolbox(
        "cect/data/white_1986_n2u.csv",
        "white_1986_n2u.csv",
        "6b63f6c0281b7bbc3be75fa3962e26caa020ddf3756bfc8dd9aad6577655fc16",
        41889,
        "945003a9949c73c98bd2ad90003ac5fd16f693d8",
        PRIMARY_N2U,
        "NemaNode-named copy; read by no toolbox reader. Byte-identical to wheel _A and to the Creamer "
        "repository's NemaNode download (2025-11-01).",
    ),
    _toolbox(
        "cect/data/aconnectome_white_1986_whole.csv",
        "cect__aconnectome_white_1986_whole.csv",
        "c8aac78756b71f6337629951e5f4211448e85d148f6db9b367b2cd0450bb403a",
        67453,
        "3b96800baa602180a6a49f704695df37df775586",
        PRIMARY_WHOLE,
        "Toolbox copy of the wheel file (per cect/validation/WhiteEtAl1986.md, copied from wormneuroatlas). "
        "Equals wna__ copy after CRLF->LF. Read by toolbox readers White_whole / WhiteDataReader.",
    ),
    _toolbox(
        "cect/data/aconnectome_white_1986_L4.csv",
        "cect__aconnectome_white_1986_L4.csv",
        "f2b709afa7b7997dff7482999af189971f79203f9df1db184a37ced86cb0127d",
        40834,
        "aadcc1ff705708af4b8248e18486f75d8863d329",
        PRIMARY_JSH,
        "Toolbox copy; equals wna__ copy after CRLF->LF. Read by toolbox reader White_L4.",
    ),
    _toolbox(
        "cect/data/aconnectome_white_1986_A.csv",
        "cect__aconnectome_white_1986_A.csv",
        "09284a374c3c30f6c806ea4dbbbb33da2e735d1891893a3f1fd65ada1e565123",
        43790,
        "442f160c9a10830c7d75a238528a2ed1f648f467",
        PRIMARY_N2U,
        "Toolbox copy; CRLF, header 'pre post type synapses' with spaces not tabs, final newline added. "
        "Data rows equal the wna__ copy. Read by toolbox reader White_A.",
    ),
    _toolbox(
        "cect/data/neurodata.txt",
        "neurodata.txt",
        "e4cd6f02499a8cce7b780fa11076645b443ba509001782ae5844ff0b4d27b56c",
        223795,
        "b137a51be4011b138dc81e3b40fd5153b5e42a6c",
        PRIMARY_DURBIN,
        "Durbin 1987 (separate work: thesis) compilation of White's N2U and JSH series, unedited per the "
        "toolbox. One record lacks its series field.",
    ),
    _toolbox(
        "cect/data/neurodata_updated.txt",
        "neurodata_updated.txt",
        "d420e9472e2cd2d62b3ed78211cc3e56a90e1e6ccbb00fab442b464bd30c1f37",
        226307,
        "da9ff80371b713f1609e2967064c44bb6c0b23ba",
        "No primary: OpenWorm ConnectomeToolbox edit of neurodata.txt (cect/validation/WhiteEtAl1986.md lists "
        "the 3 edits). Original: " + PRIMARY_DURBIN,
        "Toolbox-edited derivative of neurodata.txt: blank series set to N2U, 19 missing reverse gap-junction "
        "records added, RIML->AVAR gap weight 5->6. Not a published dataset.",
    ),
    _toolbox(
        "cect/data/NeuronConnect.xls",
        "NeuronConnect.xls",
        "b5e32612967ff277c91ba37463bd03a85678bd8e65a4861abc6516323b6ff5f3",
        518144,
        "898ba5408669a4c27467554591dd69c73b571b41",
        PRIMARY_VARSHNEY,
        "Varshney et al. 2011 (separate paper) re-compilation of White's somatic wiring with ~600 updates. "
        "One sheet 'NeuronConnect.csv': Neuron 1, Neuron 2, Type (S, Sp, R, Rp, EJ, NMJ), Nbr.",
    ),
    _toolbox(
        "cect/data/41586_2019_1352_MOESM9_ESM.xlsx",
        "41586_2019_1352_MOESM9_ESM.xlsx",
        "86d3f24c77752b1f7df4b26cdf9583461fe7e8fc76f86d2d81b3879cdaa0e389",
        4172457,
        "b7a225693bde9aa198f39c69561c37e6a53b3892",
        PRIMARY_COOK_NATURE,
        "Cook et al. 2019 (separate paper) Nature SI 5 as published. Weights are EM serial-section counts. "
        "Hermaphrodite sheets identical in value to the WormWiring original.",
    ),
    _toolbox(
        "cect/data/SI 5 Connectome adjacency matrices.xlsx",
        "SI 5 Connectome adjacency matrices.xlsx",
        "559989daa02cd9a76e9266537a6b80bfd47d338cb5d397d11296288629df364a",
        4367796,
        "9e4f34968eb0f9436ab351c44c34a13a06379d07",
        PRIMARY_COOK_WW,
        "Cook et al. 2019 SI 5, WormWiring copy. Hermaphrodite values identical to the Nature file; male sheets "
        "rename ray structural cells R*st* -> R*sh* and one row RMFL -> RMFR (duplicate).",
    ),
    _toolbox(
        "cect/data/SI 5 Connectome adjacency matrices, corrected July 2020.xlsx",
        "SI 5 Connectome adjacency matrices, corrected July 2020.xlsx",
        "1f4fdbf84746b69b49a8da0816f52787860ce349b638dce37924ba80f90c70c9",
        4188190,
        "4d53c16e9a07c1ecfd068a02b39ccffd6b8a3eaa",
        PRIMARY_COOK_WW_2020,
        "Cook et al. 2019 SI 5, WormWiring 'corrected July 2020'. Gap-junction corrections (e.g. PVDL/R-hmc "
        "400 added, BDUL/R-PLML/R 23 removed); adds hmc column and 'int' row/column. Used by the toolbox.",
    ),
)

_WHEEL_FILES = {f.filename for f in FILES if isinstance(f, ArchiveMember)}


def acquire() -> list[dict]:
    pypi_check = verify_pypi_digest(
        WORMNEUROATLAS_PACKAGE,
        WORMNEUROATLAS_VERSION,
        WORMNEUROATLAS_WHEEL.filename,
        WORMNEUROATLAS_WHEEL.sha256,
    )
    extra = {name: [f"archive {WORMNEUROATLAS_WHEEL.filename}: {pypi_check}"] for name in _WHEEL_FILES}
    return acquire_source(SOURCE_ID, FILES, extra)


# ---------------------------------------------------------------------------
# Record counts
# ---------------------------------------------------------------------------

_PLAIN_NAME = re.compile(r"[A-Z0-9]+")


def _nonplain(names) -> list[str]:
    """Names containing anything other than A-Z and 0-9 (a lexical test only)."""
    return sorted(n for n in names if not _PLAIN_NAME.fullmatch(n))


def _line_info(raw: bytes) -> dict:
    n_crlf = raw.count(b"\r\n")
    n_lf = raw.count(b"\n")
    n_cr = raw.count(b"\r")
    if n_cr == 0:
        term = "LF"
    elif n_crlf == n_lf == n_cr:
        term = "CRLF"
    else:
        term = "mixed"
    return {"bytes": len(raw), "line_terminator": term, "ends_with_newline": raw.endswith(b"\n")}


def _electrical_stats(rows: dict) -> dict:
    """``rows`` maps an ordered (a, b) to its weight, as listed in the file."""
    self_rows = {k: v for k, v in rows.items() if k[0] == k[1]}
    with_rev = [k for k in rows if k[0] != k[1] and (k[1], k[0]) in rows]
    unequal = sorted(f"{a}|{b}" for (a, b) in with_rev if rows[(a, b)] != rows[(b, a)] and a < b)
    pairs = {frozenset(k) for k in rows}
    pair_max = {}
    for (a, b), v in rows.items():
        key = frozenset((a, b))
        pair_max[key] = max(pair_max.get(key, 0), v)
    return {
        "rows": len(rows),
        "weight_sum_over_rows": sum(rows.values()),
        "self_rows": len(self_rows),
        "self_weight": sum(self_rows.values()),
        "rows_whose_reverse_is_also_listed": len(with_rev),
        "rows_without_reverse": sum(1 for k in rows if k[0] != k[1] and (k[1], k[0]) not in rows),
        "pairs_listed_both_ways_with_unequal_weight": unequal,
        "unordered_pairs_incl_self": len(pairs),
        "unordered_pairs_excl_self": sum(1 for p in pairs if len(p) == 2),
        "weight_sum_over_unordered_pairs_taking_max_direction": sum(pair_max.values()),
    }


# --- NemaNode-format tab-separated exports ----------------------------------

def _read_nemanode_tsv(path: Path):
    raw = path.read_bytes()
    text = raw.decode("ascii").replace("\r\n", "\n")
    lines = text.split("\n")
    if lines and lines[-1] == "":
        lines = lines[:-1]
    header = lines[0]
    rows = [line.split("\t") for line in lines[1:]]
    return raw, header, rows


def _nemanode_tsv_counts(path: Path) -> dict:
    """Counts for a NemaNode export: header, then ``pre post type synapses`` rows.

    - ``chemical.rows``: rows of type chemical; each is one ordered pre->post
      pair (no duplicate keys, no zero weights; both checked).
    - ``chemical.weight_sum``: sum of ``synapses`` over chemical rows.
    - ``chemical.rows_post_BWM_prefixed`` / ``rows_post_LegacyBodyWallMuscles``:
      rows whose post name is a NemaNode muscle node (lexical match only).
    - ``chemical.rows_both_names_plain``: rows where both names are only A-Z0-9
      (lexical; excludes BWM-*, CEPsh*, pm*, LegacyBodyWallMuscles).
    - ``electrical``: see ``_electrical_stats``. NemaNode lists each gap-junction
      pair once, so ``weight_sum_over_rows`` is the single-counted total and
      ``weight_if_mirrored_into_both_directions`` (2*sum - self) is what a
      symmetric matrix built from it sums to.
    """
    raw, header, rows = _read_nemanode_tsv(path)
    out = _line_info(raw)
    out["header"] = header
    out["header_fields_tab_split"] = header.split("\t")
    out["data_rows"] = len(rows)
    out["rows_by_field_count"] = {str(k): v for k, v in sorted(Counter(len(r) for r in rows).items())}
    out["rows_by_type"] = dict(sorted(Counter(r[2] for r in rows).items()))
    keys = Counter((r[0], r[1], r[2]) for r in rows)
    out["duplicate_pre_post_type_keys"] = sum(1 for v in keys.values() if v > 1)
    out["rows_with_weight_le_0"] = sum(1 for r in rows if int(r[3]) <= 0)
    names = {r[0] for r in rows} | {r[1] for r in rows}
    out["distinct_names"] = len(names)
    out["names_not_plain_A-Z0-9"] = _nonplain(names)
    out["distinct_names_plain_A-Z0-9"] = len(names) - len(out["names_not_plain_A-Z0-9"])
    chem = {(r[0], r[1]): int(r[3]) for r in rows if r[2] == "chemical"}
    bwm = {k: v for k, v in chem.items() if k[1].startswith("BWM-")}
    legacy = {k: v for k, v in chem.items() if k[1] == "LegacyBodyWallMuscles"}
    plain = {k: v for k, v in chem.items() if _PLAIN_NAME.fullmatch(k[0]) and _PLAIN_NAME.fullmatch(k[1])}
    out["chemical"] = {
        "rows": len(chem),
        "weight_sum": sum(chem.values()),
        "self_rows": sum(1 for k in chem if k[0] == k[1]),
        "distinct_pre_names": len({k[0] for k in chem}),
        "distinct_post_names": len({k[1] for k in chem}),
        "rows_post_BWM_prefixed": len(bwm),
        "weight_post_BWM_prefixed": sum(bwm.values()),
        "rows_post_LegacyBodyWallMuscles": len(legacy),
        "weight_post_LegacyBodyWallMuscles": sum(legacy.values()),
        "rows_both_names_plain": len(plain),
        "weight_both_names_plain": sum(plain.values()),
    }
    el = {(r[0], r[1]): int(r[3]) for r in rows if r[2] == "electrical"}
    es = _electrical_stats(el)
    es["weight_if_mirrored_into_both_directions"] = 2 * es["weight_sum_over_rows"] - es["self_weight"]
    es["rows_with_pre_lt_post_as_strings"] = sum(1 for a, b in el if a < b)
    es["rows_with_pre_gt_post_as_strings"] = sum(1 for a, b in el if a > b)
    out["electrical"] = es
    return out


# --- NemaNode source JSON -----------------------------------------------------

def _nemanode_export(records: list, cell_names: set) -> dict:
    """Re-derive NemaNode's CSV download from its source records.

    Rules from NemaNode's own code: populate-connections.js (type chemical if
    typ == 0 else electrical; weight = len(syn); an electrical record is
    skipped if its reverse key was already seen; weights of repeated keys are
    added) and db/download-data.js (keep only rows whose pre and post are both
    in the neurons table).
    """
    conn: dict = {}
    for r in records:
        t = "chemical" if r["typ"] == 0 else "electrical"
        if t == "electrical" and (r["post"], r["pre"], t) in conn:
            continue
        key = (r["pre"], r["post"], t)
        conn[key] = conn.get(key, 0) + len(r["syn"])
    kept = {k: v for k, v in conn.items() if k[0] in cell_names and k[1] in cell_names}
    dropped = sorted({n for k in conn for n in k[:2] if n not in cell_names})
    return {"kept": kept, "all": conn, "dropped_names": dropped}


def _nemanode_json_counts(path: Path, cell_names: set) -> tuple[dict, dict]:
    """Counts for a NemaNode connection JSON (a list of records).

    ``records_*`` count raw records. ``syn_entries`` is the number of entries in
    all ``syn`` lists (NemaNode's weight); ``syn_value_sum`` sums their values,
    reported because the two could differ. ``export_*`` describe the CSV that
    NemaNode would serve (``_nemanode_export``).
    """
    records = json.loads(path.read_text(encoding="utf-8"))
    out: dict = {"records": len(records)}
    out["records_by_typ"] = {str(k): v for k, v in sorted(Counter(r["typ"] for r in records).items())}
    out["record_keys"] = sorted({k for r in records for k in r})
    out["syn_entries"] = sum(len(r["syn"]) for r in records)
    out["syn_value_sum"] = sum(sum(r["syn"]) for r in records)
    out["records_with_empty_syn"] = sum(1 for r in records if not r["syn"])
    el = defaultdict(int)
    for r in records:
        if r["typ"] != 0:
            el[(r["pre"], r["post"])] += len(r["syn"])
    out["electrical_records_as_listed"] = _electrical_stats(dict(el))
    names = {r["pre"] for r in records} | {r["post"] for r in records}
    out["distinct_names"] = len(names)
    exp = _nemanode_export(records, cell_names)
    out["export_rows"] = len(exp["kept"])
    out["export_names_dropped_by_neurons_table"] = exp["dropped_names"]
    dropped_rows = {k: v for k, v in exp["all"].items() if k not in exp["kept"]}
    out["export_rows_dropped"] = len(dropped_rows)
    out["export_weight_dropped"] = sum(dropped_rows.values())
    return out, exp["kept"]


# --- Durbin neurodata.txt -----------------------------------------------------

_DURBIN_SEND = ("Send", "Send_joint")
_DURBIN_RECV = ("Receive", "Receive_joint")


def _durbin_counts(path: Path) -> dict:
    """Counts for Durbin's neurodata format: ``name1 name2 type series count``.

    Text after ``#`` is a comment (only neurodata_updated.txt has comments).
    Fields are split on whitespace. A record with 4 fields lacks its series
    (reported under series ``(missing)``).

    Per series:
    - ``chemical_send_side``: ordered pairs name1->name2 summed over Send and
      Send_joint records; ``_excluding_nonplain_names`` drops pairs where
      either name is not plain A-Z0-9 (mu_bod, hyp, CEPsh*; lexical only).
    - ``chemical_receive_side_mirrored``: Receive/Receive_joint records read as
      name2->name1. Durbin recorded each synapse from both partners' notes, so
      send- and receive-side totals are alternatives, not additive.
    - ``to_mu_bod``: Send/Send_joint records whose second name is ``mu_bod``
      (anonymous body-wall muscle, i.e. neuromuscular).
    - ``gap_junction``: see ``_electrical_stats``; Durbin lists both directions.
    """
    raw = path.read_bytes()
    out = _line_info(raw)
    lines = raw.decode("ascii").split("\n")
    if lines and lines[-1] == "":
        lines = lines[:-1]
    out["lines"] = len(lines)
    out["lines_with_comment"] = sum(1 for line in lines if "#" in line)
    out["blank_lines_after_comment_removal"] = sum(1 for line in lines if not line.split("#")[0].strip())
    recs = []
    bad = []
    for line in lines:
        body = line.split("#")[0]
        if not body.strip():
            continue
        f = body.split()
        if len(f) == 5:
            recs.append((f[0], f[1], f[2], f[3], int(f[4])))
        elif len(f) == 4:
            recs.append((f[0], f[1], f[2], "(missing)", int(f[3])))
            bad.append(" ".join(f))
        else:
            bad.append(" ".join(f))
    out["records"] = len(recs)
    out["records_without_5_fields"] = sorted(bad)
    out["record_types"] = sorted({r[2] for r in recs})
    keys = Counter(r[:4] for r in recs)
    out["duplicate_records"] = sum(1 for v in keys.values() if v > 1)
    by_series: dict = {}
    for series in sorted({r[3] for r in recs}):
        rr = [r for r in recs if r[3] == series]
        s: dict = {
            "records_by_type": dict(sorted(Counter(r[2] for r in rr).items())),
            "weight_by_type": dict(sorted((t, sum(r[4] for r in rr if r[2] == t)) for t in {r[2] for r in rr})),
        }
        names = {r[0] for r in rr} | {r[1] for r in rr}
        s["distinct_names"] = len(names)
        s["names_not_plain_A-Z0-9"] = _nonplain(names)
        send = defaultdict(int)
        recv = defaultdict(int)
        gj = defaultdict(int)
        for a, b, t, _, w in rr:
            if t in _DURBIN_SEND:
                send[(a, b)] += w
            elif t in _DURBIN_RECV:
                recv[(b, a)] += w
            elif t == "Gap_junction":
                gj[(a, b)] += w
        for label, m in (("chemical_send_side", send), ("chemical_receive_side_mirrored", recv)):
            plain = {k: v for k, v in m.items() if _PLAIN_NAME.fullmatch(k[0]) and _PLAIN_NAME.fullmatch(k[1])}
            s[label] = {
                "ordered_pairs": len(m),
                "weight": sum(m.values()),
                "ordered_pairs_excluding_nonplain_names": len(plain),
                "weight_excluding_nonplain_names": sum(plain.values()),
            }
        mub = {k: v for k, v in send.items() if k[1] == "mu_bod"}
        s["to_mu_bod"] = {"ordered_pairs": len(mub), "weight": sum(mub.values())}
        s["gap_junction"] = _electrical_stats(dict(gj))
        by_series[series] = s
    out["by_series"] = by_series
    return out


# --- Varshney NeuronConnect.xls -----------------------------------------------

def _varshney_counts(path: Path) -> dict:
    """Counts for Varshney et al. 2011 NeuronConnect.xls (one sheet, 4 columns).

    - ``chemical_S_plus_Sp``: ordered pairs Neuron1->Neuron2 with S+Sp > 0, and
      their summed Nbr. ``chemical_R_plus_Rp_mirrored``: R/Rp rows read as
      Neuron2->Neuron1; the same synapses seen from the receiving side.
    - ``EJ``: see ``_electrical_stats``; listed in both directions.
    - ``NMJ``: rows of type NMJ (Neuron 2 is the pseudo-name ``NMJ``).
    - ``names_in_nonzero_non_NMJ_rows``: distinct names in rows of type
      S/Sp/R/Rp/EJ with Nbr > 0 (lexical, no renaming of ``avfl``/``avfr``);
      ``_plain_A-Z0-9`` drops the lower-case tokens from that count.
    """
    import xlrd

    wb = xlrd.open_workbook(str(path))
    sh = wb.sheet_by_index(0)
    out: dict = {"sheets": wb.sheet_names(), "header": [str(sh.cell(0, c).value) for c in range(sh.ncols)]}
    rows = []
    nonnum = 0
    for r in range(1, sh.nrows):
        a, b, t, w = (sh.cell(r, c).value for c in range(4))
        if sh.cell(r, 3).ctype != xlrd.XL_CELL_NUMBER or float(w) != int(w):
            nonnum += 1
        rows.append((str(a), str(b), str(t), int(w)))
    out["data_rows"] = len(rows)
    out["rows_with_non_integer_Nbr"] = nonnum
    out["rows_by_type"] = dict(sorted(Counter(r[2] for r in rows).items()))
    out["weight_by_type"] = dict(sorted((t, sum(r[3] for r in rows if r[2] == t)) for t in {r[2] for r in rows}))
    out["rows_with_Nbr_0"] = sorted("|".join(map(str, r)) for r in rows if r[3] == 0)
    keys = Counter(r[:3] for r in rows)
    out["duplicate_neuron1_neuron2_type_keys"] = sorted("|".join(k) for k, v in keys.items() if v > 1)
    names = {r[0] for r in rows} | {r[1] for r in rows}
    out["distinct_name_tokens"] = len(names)
    out["name_tokens_not_plain_A-Z0-9"] = _nonplain(names)
    nz = {n for r in rows if r[3] > 0 and r[2] in ("S", "Sp", "R", "Rp", "EJ") for n in r[:2]}
    out["names_in_nonzero_non_NMJ_rows"] = len(nz)
    out["names_in_nonzero_non_NMJ_rows_plain_A-Z0-9"] = len(nz) - len(_nonplain(nz))
    out["name_tokens_absent_from_nonzero_non_NMJ_rows"] = sorted(names - nz)
    s = defaultdict(int)
    rcv = defaultdict(int)
    ej = defaultdict(int)
    nmj = defaultdict(int)
    for a, b, t, w in rows:
        if t in ("S", "Sp"):
            s[(a, b)] += w
        elif t in ("R", "Rp"):
            rcv[(b, a)] += w
        elif t == "EJ":
            ej[(a, b)] += w
        elif t == "NMJ":
            nmj[a] += w
    s = {k: v for k, v in s.items() if v > 0}
    rcv = {k: v for k, v in rcv.items() if v > 0}
    out["chemical_S_plus_Sp"] = {"ordered_pairs": len(s), "weight": sum(s.values()),
                                 "distinct_pre": len({k[0] for k in s}), "distinct_post": len({k[1] for k in s})}
    out["chemical_R_plus_Rp_mirrored"] = {"ordered_pairs": len(rcv), "weight": sum(rcv.values())}
    out["chemical_pairs_where_send_and_mirrored_receive_differ"] = sorted(
        f"{a}|{b}|S+Sp={s.get((a, b))}|R+Rp={rcv.get((a, b))}" for (a, b) in set(s) | set(rcv) if s.get((a, b)) != rcv.get((a, b))
    )
    out["EJ"] = _electrical_stats(dict(ej))
    out["NMJ"] = {"rows": sum(1 for r in rows if r[2] == "NMJ"), "distinct_neurons": len(nmj), "weight": sum(nmj.values())}
    return out


# --- Cook et al. 2019 SI 5 ------------------------------------------------------

def _read_cook_sheet(ws) -> dict:
    """Matrix of one SI 5 sheet: labels in row 3 (from column D) and column C (from row 4)."""
    rows = list(ws.iter_rows(values_only=True))
    col = {j: v for j, v in enumerate(rows[2]) if j >= 3 and v is not None}
    row = {i: r[2] for i, r in enumerate(rows) if i >= 3 and len(r) > 2 and r[2] is not None}
    vals = {}
    non_int = 0
    for i, rl in row.items():
        r = rows[i]
        for j, cl in col.items():
            v = r[j] if j < len(r) else None
            if v is None:
                continue
            if not isinstance(v, int) or isinstance(v, bool):
                non_int += 1
                continue
            vals[(rl, cl)] = vals.get((rl, cl), 0) + v
    groups_a = [(i, r[0]) for i, r in enumerate(rows) if r and r[0] is not None]

    def group_of(i):
        g = None
        for k, v in groups_a:
            if k <= i:
                g = v
        return g

    # The right-most column and bottom row repeat the labels; count disagreements.
    lastc, lastr = max(col) + 1, max(row) + 1
    right_mismatch = sum(1 for i, rl in row.items() if (rows[i][lastc] if lastc < len(rows[i]) else None) != rl)
    bottom = rows[lastr] if lastr < len(rows) else ()
    bottom_mismatch = sum(1 for j, cl in col.items() if (bottom[j] if j < len(bottom) else None) != cl)
    return {
        "row_labels": [row[i] for i in sorted(row)],
        "col_labels": [col[j] for j in sorted(col)],
        "vals": vals,
        "non_int_cells": non_int,
        "row_groups_colA": dict(sorted(Counter(str(group_of(i)) for i in row).items())),
        "right_echo_label_mismatches": right_mismatch,
        "bottom_echo_label_mismatches": bottom_mismatch,
    }


def _cook_counts(path: Path) -> tuple[dict, dict]:
    """Counts per sheet of a Cook et al. 2019 SI 5 workbook.

    - ``nonzero_cells`` / ``weight_sum``: cells with a value > 0 inside the
      labelled matrix and their sum (weights are EM serial-section counts).
    - ``diagonal_nonzero``: cells whose row and column labels are equal.
    - ``row_groups_colA``: row counts per group label written in column A.
    - Chemical sheets: ``nonzero_cells_post_label_also_a_row_label`` restricts
      to columns that are also presynaptic rows (the sheet's own 300-row set).
    - Gap sheets: ``cells_without_equal_mirror`` counts nonzero (i,j) with
      (j,i) absent or different; ``cells_with_nonzero_mirror`` counts nonzero
      off-diagonal cells whose mirror is also nonzero.
      ``nonzero_cells_among_chemical_row_labels`` restricts both labels to the
      same workbook's hermaphrodite/male chemical row labels.
    Duplicate labels are reported; values under a duplicated label pair are
    added together. ``<sex>_labels_union_all_sheets`` is the union of row and
    column labels over that sex's three sheets; ``_with_any_nonzero_cell``
    keeps labels that occur in at least one nonzero cell.
    """
    import openpyxl

    wb = openpyxl.load_workbook(path, read_only=True)
    sheets = {}
    out: dict = {"sheets": wb.sheetnames}
    for ws in wb.worksheets:
        if "LEGEND" in ws.title.upper():
            continue
        sheets[ws.title] = _read_cook_sheet(ws)
    wb.close()
    chem_rows = {
        "herm": set(sheets.get("hermaphrodite chemical", {}).get("row_labels", [])),
        "male": set(sheets.get("male chemical", {}).get("row_labels", [])),
    }
    per: dict = {}
    for title, s in sorted(sheets.items()):
        vals = {k: v for k, v in s["vals"].items() if v}
        rl, cl = s["row_labels"], s["col_labels"]
        d: dict = {
            "row_labels": len(rl),
            "col_labels": len(cl),
            "duplicate_row_labels": sorted(n for n, c in Counter(rl).items() if c > 1),
            "duplicate_col_labels": sorted(n for n, c in Counter(cl).items() if c > 1),
            "union_of_labels": len(set(rl) | set(cl)),
            "non_int_cells_in_matrix": s["non_int_cells"],
            "nonzero_cells": len(vals),
            "weight_sum": sum(vals.values()),
            "diagonal_nonzero": sum(1 for k in vals if k[0] == k[1]),
            "diagonal_weight": sum(v for k, v in vals.items() if k[0] == k[1]),
            "row_groups_colA": s["row_groups_colA"],
            "right_echo_label_mismatches": s["right_echo_label_mismatches"],
            "bottom_echo_label_mismatches": s["bottom_echo_label_mismatches"],
        }
        sex = "herm" if title.startswith("herm") else "male"
        if "chemical" in title:
            rows_set = set(rl)
            sub = {k: v for k, v in vals.items() if k[1] in rows_set}
            d["col_labels_not_row_labels"] = len(set(cl) - rows_set)
            d["nonzero_cells_post_label_also_a_row_label"] = len(sub)
            d["weight_post_label_also_a_row_label"] = sum(sub.values())
        else:
            d["cells_without_equal_mirror"] = sum(1 for (a, b), v in vals.items() if vals.get((b, a)) != v)
            d["cells_with_nonzero_mirror"] = sum(1 for (a, b) in vals if a != b and (b, a) in vals)
            sub = {k: v for k, v in vals.items() if k[0] in chem_rows[sex] and k[1] in chem_rows[sex]}
            d["nonzero_cells_among_chemical_row_labels"] = len(sub)
            d["weight_among_chemical_row_labels"] = sum(sub.values())
        per[title] = d
    out["per_sheet"] = per
    for sex, prefix in (("hermaphrodite", "herm"), ("male", "male")):
        labels, touched = set(), set()
        for title, s in sheets.items():
            if title.startswith(prefix):
                labels |= set(s["row_labels"]) | set(s["col_labels"])
                touched |= {n for k, v in s["vals"].items() if v for n in k}
        out[f"{sex}_labels_union_all_sheets"] = len(labels)
        out[f"{sex}_labels_with_any_nonzero_cell"] = len(touched)
    return out, sheets


def _cook_diff(a: dict, b: dict) -> dict:
    """Cell-level differences between two Cook workbooks, matching sheets by name.

    Sheet names in the corrected file use 'hermaphrodite gap jn ...' where the
    others use 'herm gap jn ...'; those are paired. Cells are matched by their
    exact (row label, column label); counts are of label pairs whose value
    differs (absent counts as 0).
    """
    alias = {"herm gap jn symmetric": "hermaphrodite gap jn symmetric",
             "herm gap jn asymmetric": "hermaphrodite gap jn asymmetric"}

    def norm_title(t):
        return alias.get(t, t)

    a2 = {norm_title(t): s for t, s in a.items()}
    b2 = {norm_title(t): s for t, s in b.items()}
    out = {}
    for t in sorted(set(a2) | set(b2)):
        if t not in a2 or t not in b2:
            out[t] = "sheet missing in one file"
            continue
        va = {k: v for k, v in a2[t]["vals"].items() if v}
        vb = {k: v for k, v in b2[t]["vals"].items() if v}
        diff = [k for k in set(va) | set(vb) if va.get(k) != vb.get(k)]
        out[t] = {
            "label_pairs_with_different_value": len(diff),
            "row_labels_only_in_first": sorted(set(a2[t]["row_labels"]) - set(b2[t]["row_labels"])),
            "row_labels_only_in_second": sorted(set(b2[t]["row_labels"]) - set(a2[t]["row_labels"])),
            "col_labels_only_in_first": sorted(set(a2[t]["col_labels"]) - set(b2[t]["col_labels"])),
            "col_labels_only_in_second": sorted(set(b2[t]["col_labels"]) - set(a2[t]["col_labels"])),
        }
    return out


# --- aconnectome.json -----------------------------------------------------------

def _aconnectome_json_counts(json_path: Path, ids_path: Path) -> dict:
    """Counts for aconnectome.json, indexed by pumpprobe's aconnectome_ids.txt.

    ``chemical[i][j]`` is read as ids[i] -> ids[j] (pumpprobe Anatlas
    transposes it to [to, from]). ``chemical_sign`` is a per-neuron vector.
    """
    d = json.loads(json_path.read_text(encoding="utf-8"))
    ids = [line.split("\t")[1] for line in ids_path.read_text(encoding="utf-8").splitlines() if line.strip()]
    out: dict = {"keys": sorted(d), "ids_lines": len(ids), "ids_distinct": len(set(ids))}
    ch, el, sg = d["chemical"], d["electrical"], d["chemical_sign"]
    out["chemical_shape"] = [len(ch), len(ch[0])]
    out["electrical_shape"] = [len(el), len(el[0])]
    out["chemical_sign_values"] = {str(k): v for k, v in sorted(Counter(sg).items())}
    out["chemical_sign_negative_ids"] = sorted(ids[i] for i, v in enumerate(sg) if v < 0)
    n = len(ids)
    c = {(i, j): ch[i][j] for i in range(n) for j in range(n) if ch[i][j]}
    e = {(ids[i], ids[j]): el[i][j] for i in range(n) for j in range(n) if el[i][j]}
    out["chemical_nonzero"] = len(c)
    out["chemical_sum"] = sum(c.values())
    out["chemical_non_integer_values"] = sum(1 for v in c.values() if v != int(v))
    out["chemical_diagonal_nonzero"] = sum(1 for (i, j) in c if i == j)
    es = _electrical_stats(e)
    es["pairs_listed_both_ways_with_unequal_weight"] = len(es["pairs_listed_both_ways_with_unequal_weight"])
    out["electrical"] = es
    names = set(ids)
    out["ids_not_plain_A-Z0-9"] = _nonplain(names)
    return out


# --- byte-level relationships --------------------------------------------------

def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def record_counts() -> dict:
    """Counts computed only from data/raw/white1986/, with no renaming or filtering.

    Every definition is in the docstring of the helper that computes it.
    Where a definition choice matters (send vs receive side, gap junctions
    single- vs double-counted, muscle pseudo-nodes in or out) the alternatives
    are reported side by side. "Plain" names means names made only of A-Z and
    0-9: a lexical test that separates the files' muscle/glia pseudo-names
    (BWM-*, CEPsh*, mu_bod, hyp, pm1, LegacyBodyWallMuscles) from the rest. It
    is NOT a neuron list; the neuron set is decided in Phase 2.
    """
    raw = RAW_ROOT / SOURCE_ID
    out: dict = {}

    tsvs = [
        "wna__aconnectome_white_1986_whole.csv",
        "wna__aconnectome_white_1986_A.csv",
        "wna__aconnectome_white_1986_L4.csv",
        "cect__aconnectome_white_1986_whole.csv",
        "cect__aconnectome_white_1986_A.csv",
        "cect__aconnectome_white_1986_L4.csv",
        "white_1986_jsh.csv",
        "white_1986_n2u.csv",
    ]
    for name in tsvs:
        out[name] = _nemanode_tsv_counts(raw / name)

    cell_table = json.loads((raw / f"nemanode_{NEMANODE_COMMIT[:7]}__neurons.json").read_text(encoding="utf-8"))
    cell_names = {c["name"] for c in cell_table}
    out[f"nemanode_{NEMANODE_COMMIT[:7]}__neurons.json"] = {"cells": len(cell_table), "distinct_names": len(cell_names)}
    reproduced = {}
    for ds in ("n2u", "jsh", "whole"):
        name = f"nemanode_{NEMANODE_COMMIT[:7]}__white_1986_{ds}.json"
        out[name], reproduced[ds] = _nemanode_json_counts(raw / name, cell_names)

    for name in ("neurodata.txt", "neurodata_updated.txt"):
        out[name] = _durbin_counts(raw / name)
    out["NeuronConnect.xls"] = _varshney_counts(raw / "NeuronConnect.xls")
    out["aconnectome.json"] = _aconnectome_json_counts(raw / "aconnectome.json", raw / "aconnectome_ids.txt")

    cook_names = [
        "41586_2019_1352_MOESM9_ESM.xlsx",
        "SI 5 Connectome adjacency matrices.xlsx",
        "SI 5 Connectome adjacency matrices, corrected July 2020.xlsx",
    ]
    cook_sheets = {}
    for name in cook_names:
        out[name], cook_sheets[name] = _cook_counts(raw / name)

    # Relationships between files, computed from bytes and parsed content.
    rel: dict = {}
    by_sha = defaultdict(list)
    for f in FILES:
        by_sha[_sha256(raw / f.filename)].append(f.filename)
    rel["groups_of_byte_identical_files"] = sorted(sorted(v) for v in by_sha.values() if len(v) > 1)
    crlf = {}
    for kind in ("whole", "A", "L4"):
        a = (raw / f"cect__aconnectome_white_1986_{kind}.csv").read_bytes()
        b = (raw / f"wna__aconnectome_white_1986_{kind}.csv").read_bytes()
        a_lf = a.replace(b"\r\n", b"\n")
        la, lb = a_lf.split(b"\n"), b.split(b"\n")
        if la and la[-1] == b"":
            la = la[:-1]
        if lb and lb[-1] == b"":
            lb = lb[:-1]
        crlf[kind] = {
            "identical_after_CRLF_to_LF": a_lf == b,
            "line_counts_cect_wna": [len(la), len(lb)],
            "differing_line_numbers_1based": [i + 1 for i, (x, y) in enumerate(zip(la, lb)) if x != y],
            "final_newline_cect_wna": [a.endswith(b"\n"), b.endswith(b"\n")],
        }
    rel["cect_vs_wna_aconnectome_csv"] = crlf

    def tsv_dict(name):
        _, _, rows = _read_nemanode_tsv(raw / name)
        return {(r[0], r[1], r[2]): int(r[3]) for r in rows}

    rel["nemanode_json_export_equals_csv"] = {
        f"white_1986_{ds} -> {csv}": reproduced[ds] == tsv_dict(csv)
        for ds, csv in (("n2u", "wna__aconnectome_white_1986_A.csv"),
                        ("jsh", "wna__aconnectome_white_1986_L4.csv"),
                        ("whole", "wna__aconnectome_white_1986_whole.csv"))
    }

    def durbin_records(name):
        recs = {}
        for line in (raw / name).read_text(encoding="ascii").split("\n"):
            f = line.split("#")[0].split()
            if len(f) == 5:
                recs[tuple(f[:4])] = int(f[4])
            elif len(f) == 4:
                recs[(f[0], f[1], f[2], "(missing)")] = int(f[3])
        return recs

    d0, d1 = durbin_records("neurodata.txt"), durbin_records("neurodata_updated.txt")
    rel["neurodata_original_vs_updated"] = {
        "records_only_in_original": sorted("|".join(k) for k in set(d0) - set(d1)),
        "records_only_in_updated": sorted("|".join(k) for k in set(d1) - set(d0)),
        "records_with_changed_count": sorted(f"{'|'.join(k)}: {d0[k]} -> {d1[k]}" for k in set(d0) & set(d1) if d0[k] != d1[k]),
    }
    rel["cook_nature_vs_wormwiring_original"] = _cook_diff(cook_sheets[cook_names[0]], cook_sheets[cook_names[1]])
    rel["cook_wormwiring_original_vs_corrected_2020"] = _cook_diff(cook_sheets[cook_names[1]], cook_sheets[cook_names[2]])
    out["_relationships"] = rel
    return out
