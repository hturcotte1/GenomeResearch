"""Behaviour of the acquisition primitives.

These tests use arbitrary byte strings, not biological data. They check only
that hashing, pin enforcement and atomic writes behave as specified.
"""

import hashlib
import zipfile

import pytest

from src.acquire import common
from src.acquire.common import ArchiveMember, IntegrityError, RemoteFile


def test_git_blob_sha1_matches_git_definition(tmp_path):
    p = tmp_path / "f"
    p.write_bytes(b"hello\n")
    # `printf 'hello\n' | git hash-object --stdin`
    assert common.git_blob_sha1_file(p) == "ce013625030ba8dba906f756967f9e9ca394464a"


def test_write_atomically_rejects_wrong_pin_and_leaves_nothing(tmp_path):
    dest = tmp_path / "out.bin"
    with pytest.raises(IntegrityError):
        common._write_atomically(dest, [b"abc"], 3, "0" * 64, "test")
    assert not dest.exists()
    assert list(tmp_path.iterdir()) == []


def test_write_atomically_accepts_correct_pin_and_makes_read_only(tmp_path):
    dest = tmp_path / "out.bin"
    data = b"abc"
    common._write_atomically(dest, [data], len(data), hashlib.sha256(data).hexdigest(), "test")
    assert dest.read_bytes() == data
    assert not (dest.stat().st_mode & 0o222), "file should be read-only"


def test_existing_file_with_wrong_bytes_is_never_overwritten(tmp_path):
    dest = tmp_path / "f"
    dest.write_bytes(b"tampered")
    rf = RemoteFile(
        url="https://example.invalid/f",
        filename="f",
        sha256=hashlib.sha256(b"original").hexdigest(),
        size=8,
        distributor="test",
        origin="secondary",
        primary_reference="test",
    )
    with pytest.raises(IntegrityError):
        common.ensure_remote(rf, tmp_path)
    assert dest.read_bytes() == b"tampered"


def test_member_pin_must_agree_with_wheel_record(tmp_path, monkeypatch):
    payload = b"payload"
    good = hashlib.sha256(payload).digest()
    import base64

    record_digest = base64.urlsafe_b64encode(good).rstrip(b"=").decode()
    wheel = tmp_path / "pkg-0-py3-none-any.whl"
    with zipfile.ZipFile(wheel, "w") as zf:
        zf.writestr("pkg/data/x.bin", payload)
        zf.writestr("pkg-0.dist-info/RECORD", f"pkg/data/x.bin,sha256={record_digest},{len(payload)}\n")
    wheel_bytes = wheel.read_bytes()
    dist = tmp_path / "dist"
    dist.mkdir()
    (dist / wheel.name).write_bytes(wheel_bytes)
    monkeypatch.setattr(common, "DIST_DIR", dist)
    archive = RemoteFile(
        url="https://example.invalid/w",
        filename=wheel.name,
        sha256=hashlib.sha256(wheel_bytes).hexdigest(),
        size=len(wheel_bytes),
        distributor="test",
        origin="secondary",
        primary_reference="test",
    )
    wrong_pin = ArchiveMember(archive, "pkg/data/x.bin", "x.bin", "1" * 64, len(payload), "test")
    with pytest.raises(IntegrityError):
        common.ensure_member(wrong_pin, tmp_path / "src")
    right_pin = ArchiveMember(archive, "pkg/data/x.bin", "x.bin", good.hex(), len(payload), "test")
    path, extracted, checks = common.ensure_member(right_pin, tmp_path / "src")
    assert extracted and path.read_bytes() == payload
    assert any("RECORD" in c for c in checks)
