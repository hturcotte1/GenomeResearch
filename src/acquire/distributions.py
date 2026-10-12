"""Redistribution channels that several sources are acquired through.

Each is declared once here so that every source module pins the same bytes.
All of them are SECONDARY copies. The project owner approved using them on
2026-10-11 because the primary hosts are blocked by this environment's network
policy; see docs/decisions.md D-003. Verifying against the primary copies is
still pending and blocks the Phase 4 freeze.
"""

from __future__ import annotations

from urllib.parse import quote, unquote

from .common import RemoteFile

# The `wormneuroatlas` Python package, by F. Randi (first author of Randi et al.
# 2023), version 0.0.7.3, uploaded to PyPI on 2023-06-29. Its data/ folder
# bundles the signal propagation atlas and copies of several other datasets.
# The sha256 equals the digest PyPI publishes for this file; acquisition
# re-checks that live.
WORMNEUROATLAS_PACKAGE = "wormneuroatlas"
WORMNEUROATLAS_VERSION = "0.0.7.3"
WORMNEUROATLAS_WHEEL = RemoteFile(
    url=(
        "https://files.pythonhosted.org/packages/b3/dc/"
        "634b2a009739f692bad83325e5c0f8fd5b1323ac1a9ce11df7d4c8ac40db/"
        "wormneuroatlas-0.0.7.3-py3-none-any.whl"
    ),
    filename="wormneuroatlas-0.0.7.3-py3-none-any.whl",
    sha256="166289031784c9565f6b9205e30dc718bafbc092db3b46f1aef73d93dc4d1325",
    size=37760635,
    distributor="PyPI package wormneuroatlas 0.0.7.3 (F. Randi / Leifer lab), uploaded 2023-06-29",
    origin="secondary",
    primary_reference="https://pypi.org/project/wormneuroatlas/0.0.7.3/ (redistribution archive; each member names its own primary)",
)

# The OpenWorm C. elegans Connectome Toolbox repository, pinned to one commit.
# Files are fetched individually from raw.githubusercontent.com at that commit,
# and each is checked against the git blob id the commit records for its path.
CONNECTOME_TOOLBOX_REPO = "openworm/ConnectomeToolbox"
CONNECTOME_TOOLBOX_COMMIT = "ffe570268b7cffb9329cd009a1bb37d60db2d465"  # 2026-09-29


def connectome_toolbox_file(
    path: str,
    *,
    sha256: str,
    size: int,
    git_blob_sha1: str,
    primary_reference: str,
    filename: str | None = None,
    note: str = "",
) -> RemoteFile:
    """Declare one file from the pinned ConnectomeToolbox commit.

    ``path`` is the path inside the repository, e.g. "cect/data/edgelist_MA.csv".
    It may be given raw ("witvliet_2020_7 adult.xlsx") or already
    percent-encoded ("witvliet_2020_7%20adult.xlsx"). Existing %XX escapes are
    kept, so both forms give the same URL. ``filename`` defaults to the decoded
    basename of ``path``.
    """
    encoded = quote(path, safe="/%")
    return RemoteFile(
        url=f"https://raw.githubusercontent.com/{CONNECTOME_TOOLBOX_REPO}/{CONNECTOME_TOOLBOX_COMMIT}/{encoded}",
        filename=filename or unquote(path.rsplit("/", 1)[-1]),
        sha256=sha256,
        size=size,
        distributor=f"GitHub {CONNECTOME_TOOLBOX_REPO} @ {CONNECTOME_TOOLBOX_COMMIT}",
        origin="secondary",
        primary_reference=primary_reference,
        git_blob_sha1=git_blob_sha1,
        note=note,
    )
