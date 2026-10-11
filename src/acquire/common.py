"""Acquisition primitives shared by every source module.

Rules enforced here, all derived from the project's hard rules:

- Every file is pinned by size and SHA-256 in the source module that declares
  it. Bytes that do not match their pin are rejected and never written into
  ``data/raw/``.
- Files in ``data/raw/`` are written once, atomically, and then made read-only.
  A file that is already present is re-verified against its pin, never
  re-downloaded or overwritten.
- Files extracted from a wheel are also checked against the wheel's own
  ``RECORD``, the hash list the distributor published inside the archive.
- Files fetched from GitHub at a pinned commit are also checked against the
  git blob id the repository records for that path at that commit.
- Each source writes ``data/raw/<source>/MANIFEST.json``. The retrieval date
  lives there and in ``docs/provenance/``, never in interim or processed data.
- There is no "skip on failure". Any integrity problem raises and stops the run.
"""

from __future__ import annotations

import base64
import csv
import datetime as _dt
import hashlib
import io
import json
import os
import stat
import tempfile
import urllib.request
import zipfile
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
RAW_ROOT = REPO_ROOT / "data" / "raw"
DIST_DIR = RAW_ROOT / "_distributions"
MANIFEST_NAME = "MANIFEST.json"
_CHUNK = 1 << 20
_TIMEOUT_S = 300


class IntegrityError(RuntimeError):
    """Raised when bytes do not match their pin or their distributor's record."""


@dataclass(frozen=True)
class RemoteFile:
    """A file fetched byte-for-byte from a URL and stored unchanged.

    ``origin`` is "primary" when the URL is the publisher's own copy (journal
    supplement, the authors' official data portal). It is "secondary" when the
    copy comes from a redistributor, such as a PyPI package or another
    project's repository. ``primary_reference`` says where the primary copy
    lives, so it can be checked once the host is reachable.
    """

    url: str
    filename: str
    sha256: str
    size: int
    distributor: str
    origin: str
    primary_reference: str
    git_blob_sha1: str | None = None
    note: str = ""

    def __post_init__(self) -> None:
        if self.origin not in ("primary", "secondary"):
            raise ValueError(f"origin must be 'primary' or 'secondary', got {self.origin!r}")
        _check_hex(self.sha256, 64, "sha256")
        if self.git_blob_sha1 is not None:
            _check_hex(self.git_blob_sha1, 40, "git_blob_sha1")


@dataclass(frozen=True)
class ArchiveMember:
    """A file extracted unchanged from a downloaded zip archive, such as a wheel.

    The archive itself is kept, untouched, under ``data/raw/_distributions/``.
    """

    archive: RemoteFile
    member: str
    filename: str
    sha256: str
    size: int
    primary_reference: str
    note: str = ""

    def __post_init__(self) -> None:
        _check_hex(self.sha256, 64, "sha256")


def _check_hex(value: str, length: int, what: str) -> None:
    if len(value) != length or any(c not in "0123456789abcdef" for c in value):
        raise ValueError(f"{what} must be {length} lowercase hex characters, got {value!r}")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        while chunk := fh.read(_CHUNK):
            h.update(chunk)
    return h.hexdigest()


def git_blob_sha1_file(path: Path) -> str:
    """The id git assigns to this file's content: sha1(b"blob <size>\\0" + content)."""
    h = hashlib.sha1()
    h.update(b"blob %d\x00" % path.stat().st_size)
    with open(path, "rb") as fh:
        while chunk := fh.read(_CHUNK):
            h.update(chunk)
    return h.hexdigest()


def _make_read_only(path: Path) -> None:
    os.chmod(path, stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH)


def _write_atomically(dest: Path, data_iter, expected_size: int, expected_sha256: str, label: str) -> None:
    """Write chunks to a temp file beside ``dest``, verify, then rename into place."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(dir=dest.parent, prefix=".partial-")
    tmp = Path(tmp_name)
    try:
        h = hashlib.sha256()
        n = 0
        with os.fdopen(fd, "wb") as out:
            for chunk in data_iter:
                h.update(chunk)
                n += len(chunk)
                out.write(chunk)
        got = h.hexdigest()
        if n != expected_size or got != expected_sha256:
            raise IntegrityError(
                f"{label}: got size={n} sha256={got}, "
                f"pinned size={expected_size} sha256={expected_sha256}. Nothing was written."
            )
        os.replace(tmp, dest)
        _make_read_only(dest)
    finally:
        if tmp.exists():
            tmp.unlink()


def _verify_existing(path: Path, size: int, sha256: str) -> None:
    actual_size = path.stat().st_size
    actual_sha = sha256_file(path)
    if actual_size != size or actual_sha != sha256:
        raise IntegrityError(
            f"{path} already exists but does not match its pin "
            f"(size {actual_size} vs {size}, sha256 {actual_sha} vs {sha256}). "
            "Raw files are never overwritten; investigate before deleting it."
        )


def _url_chunks(url: str):
    req = urllib.request.Request(url, headers={"User-Agent": "GenomeResearch-acquire/1"})
    with urllib.request.urlopen(req, timeout=_TIMEOUT_S) as resp:
        while chunk := resp.read(_CHUNK):
            yield chunk


def ensure_remote(rf: RemoteFile, dest_dir: Path) -> tuple[Path, bool, list[str]]:
    """Make sure ``rf`` is present in ``dest_dir`` and matches its pin.

    Returns (path, downloaded_now, checks_passed).
    """
    dest = dest_dir / rf.filename
    downloaded = False
    if dest.exists():
        _verify_existing(dest, rf.size, rf.sha256)
    else:
        _write_atomically(dest, _url_chunks(rf.url), rf.size, rf.sha256, rf.url)
        downloaded = True
    checks = ["size and SHA-256 match the pin in the source module"]
    if rf.git_blob_sha1 is not None:
        blob = git_blob_sha1_file(dest)
        if blob != rf.git_blob_sha1:
            raise IntegrityError(
                f"{dest}: git blob id {blob} does not match pinned {rf.git_blob_sha1}"
            )
        checks.append("git blob SHA-1 matches the blob id recorded in the repository at the pinned commit")
    return dest, downloaded, checks


def _wheel_record(zf: zipfile.ZipFile) -> dict[str, tuple[str, int]]:
    """Parse a wheel's RECORD into {path: (sha256_hex, size)}."""
    names = [n for n in zf.namelist() if n.endswith(".dist-info/RECORD")]
    if len(names) != 1:
        raise IntegrityError(f"expected exactly one .dist-info/RECORD, found {names}")
    out: dict[str, tuple[str, int]] = {}
    with zf.open(names[0]) as fh:
        for row in csv.reader(io.TextIOWrapper(fh, "utf-8")):
            if len(row) != 3 or not row[1]:
                continue
            algo, b64 = row[1].split("=", 1)
            if algo != "sha256":
                continue
            digest = base64.urlsafe_b64decode(b64 + "=" * (-len(b64) % 4)).hex()
            out[row[0]] = (digest, int(row[2]))
    return out


def ensure_member(m: ArchiveMember, dest_dir: Path) -> tuple[Path, bool, list[str]]:
    """Make sure archive member ``m`` is extracted to ``dest_dir`` and verified.

    Returns (path, extracted_now, checks_passed). It downloads the archive
    first if needed.
    """
    dest = dest_dir / m.filename
    archive_path, _, archive_checks = ensure_remote(m.archive, DIST_DIR)
    checks = [f"archive {m.archive.filename}: {c}" for c in archive_checks]
    is_wheel = m.archive.filename.endswith(".whl")
    with zipfile.ZipFile(archive_path) as zf:
        record = _wheel_record(zf) if is_wheel else {}
        if is_wheel:
            if m.member not in record:
                raise IntegrityError(f"{m.member} has no sha256 entry in the wheel RECORD")
            rec_sha, rec_size = record[m.member]
            if rec_sha != m.sha256 or rec_size != m.size:
                raise IntegrityError(
                    f"pin for {m.member} (size {m.size}, sha256 {m.sha256}) disagrees with "
                    f"wheel RECORD (size {rec_size}, sha256 {rec_sha})"
                )
        extracted = False
        if dest.exists():
            _verify_existing(dest, m.size, m.sha256)
        else:
            data = zf.read(m.member)
            _write_atomically(dest, [data], m.size, m.sha256, f"{m.archive.filename}!{m.member}")
            extracted = True
    checks.append("size and SHA-256 match the pin in the source module")
    if is_wheel:
        checks.append("SHA-256 and size match the wheel's own RECORD entry")
    return dest, extracted, checks


def verify_pypi_digest(package: str, version: str, filename: str, sha256: str) -> str:
    """Check ``sha256`` against the digest PyPI publishes for this release file.

    Returns a description of the check. Raises IntegrityError on mismatch.
    """
    url = f"https://pypi.org/pypi/{package}/{version}/json"
    req = urllib.request.Request(url, headers={"User-Agent": "GenomeResearch-acquire/1"})
    with urllib.request.urlopen(req, timeout=_TIMEOUT_S) as resp:
        meta = json.load(resp)
    digests = {u["filename"]: u["digests"]["sha256"] for u in meta["urls"]}
    if filename not in digests:
        raise IntegrityError(f"PyPI lists no file {filename} for {package} {version}")
    if digests[filename] != sha256:
        raise IntegrityError(
            f"PyPI digest for {filename} is {digests[filename]}, pin is {sha256}"
        )
    return f"SHA-256 equals the digest PyPI publishes for {package} {version} ({filename})"


def _today_utc() -> str:
    return _dt.datetime.now(_dt.timezone.utc).date().isoformat()


def _load_manifest(source_id: str) -> dict:
    path = RAW_ROOT / source_id / MANIFEST_NAME
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def write_manifest(source_id: str, entries: list[dict]) -> Path:
    """Write ``data/raw/<source>/MANIFEST.json`` in a stable layout.

    A file's retrieval date is set when its bytes first arrive and carried
    forward on later runs. If a file is present but has no recorded date (the
    manifest was lost), the date is recorded as "UNKNOWN" rather than guessed.
    """
    previous = {e["filename"]: e for e in _load_manifest(source_id).get("files", [])}
    out_entries = []
    for e in sorted(entries, key=lambda x: x["filename"]):
        e = dict(e)
        prev = previous.get(e["filename"])
        if e.pop("_fetched_now"):
            e["retrieved_utc_date"] = _today_utc()
        elif prev is not None and prev.get("sha256") == e["sha256"]:
            e["retrieved_utc_date"] = prev["retrieved_utc_date"]
        else:
            e["retrieved_utc_date"] = "UNKNOWN"
        out_entries.append(e)
    manifest = {"source": source_id, "files": out_entries}
    path = RAW_ROOT / source_id / MANIFEST_NAME
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def acquire_source(source_id: str, files: tuple, extra_checks: dict[str, list[str]] | None = None) -> list[dict]:
    """Fetch and verify every declared file for one source, then write its manifest.

    ``extra_checks`` maps a filename to further check descriptions, for checks
    the source module performed itself (e.g. a PyPI digest lookup). Archive
    members share their archive's retrieval: if the archive was fetched in
    this run, so were they.
    """
    extra_checks = extra_checks or {}
    dest_dir = RAW_ROOT / source_id
    entries: list[dict] = []
    seen: set[str] = set()
    for f in files:
        if f.filename in seen:
            raise ValueError(f"{source_id}: duplicate filename {f.filename}")
        seen.add(f.filename)
        if isinstance(f, RemoteFile):
            path, fetched, checks = ensure_remote(f, dest_dir)
            entry = {
                "filename": f.filename,
                "sha256": f.sha256,
                "size": f.size,
                "url": f.url,
                "distributor": f.distributor,
                "origin": f.origin,
                "primary_reference": f.primary_reference,
                "git_blob_sha1": f.git_blob_sha1,
                "note": f.note,
            }
        elif isinstance(f, ArchiveMember):
            archive_existed = (DIST_DIR / f.archive.filename).exists()
            path, fetched, checks = ensure_member(f, dest_dir)
            fetched = fetched or not archive_existed
            entry = {
                "filename": f.filename,
                "sha256": f.sha256,
                "size": f.size,
                "url": f"{f.archive.url}#{f.member}",
                "archive_filename": f.archive.filename,
                "archive_sha256": f.archive.sha256,
                "archive_member": f.member,
                "distributor": f.archive.distributor,
                "origin": f.archive.origin,
                "primary_reference": f.primary_reference,
                "note": f.note,
            }
        else:
            raise TypeError(f"{source_id}: unsupported file declaration {f!r}")
        entry["checks"] = checks + list(extra_checks.get(f.filename, []))
        entry["_fetched_now"] = fetched
        entries.append(entry)
    write_manifest(source_id, entries)
    return [{k: v for k, v in e.items() if k != "_fetched_now"} for e in entries]


def verify_source_offline(source_id: str, files: tuple) -> list[str]:
    """Re-hash every declared file without network access. Returns a list of problems."""
    problems = []
    dest_dir = RAW_ROOT / source_id
    for f in files:
        path = dest_dir / f.filename
        if not path.exists():
            problems.append(f"{source_id}: missing {path}")
            continue
        size, sha = path.stat().st_size, sha256_file(path)
        if size != f.size or sha != f.sha256:
            problems.append(f"{source_id}: {f.filename} size/sha256 {size}/{sha} != pin {f.size}/{f.sha256}")
    return problems
