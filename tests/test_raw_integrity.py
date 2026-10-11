"""Every raw file is exactly the bytes its source module pins.

These tests need the raw data to be present. Run ``python -m src.acquire``
first. Missing files are reported as failures, never skipped, so that a
missing source cannot pass unnoticed.
"""

import importlib
import json

import pytest

from src.acquire import SOURCE_MODULES
from src.acquire.common import MANIFEST_NAME, RAW_ROOT, sha256_file


def _modules():
    return [importlib.import_module(f"src.acquire.{name}") for name in SOURCE_MODULES]


@pytest.mark.parametrize("name", SOURCE_MODULES)
def test_module_contract(name):
    mod = importlib.import_module(f"src.acquire.{name}")
    assert mod.SOURCE_ID == name
    assert isinstance(mod.CITATION, str) and mod.CITATION
    assert mod.FILES, f"{name} declares no files"
    filenames = [f.filename for f in mod.FILES]
    assert len(filenames) == len(set(filenames)), f"{name}: duplicate filenames"
    assert callable(mod.acquire) and callable(mod.record_counts)


@pytest.mark.parametrize("name", SOURCE_MODULES)
def test_raw_files_match_pins(name):
    mod = importlib.import_module(f"src.acquire.{name}")
    for f in mod.FILES:
        path = RAW_ROOT / mod.SOURCE_ID / f.filename
        assert path.exists(), f"missing {path}; run: python -m src.acquire {name}"
        assert path.stat().st_size == f.size, f"{path}: size differs from pin"
        assert sha256_file(path) == f.sha256, f"{path}: SHA-256 differs from pin"


@pytest.mark.parametrize("name", SOURCE_MODULES)
def test_manifest_agrees_with_pins(name):
    mod = importlib.import_module(f"src.acquire.{name}")
    manifest_path = RAW_ROOT / mod.SOURCE_ID / MANIFEST_NAME
    assert manifest_path.exists(), f"missing {manifest_path}; run: python -m src.acquire {name}"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert manifest["source"] == mod.SOURCE_ID
    by_name = {e["filename"]: e for e in manifest["files"]}
    assert set(by_name) == {f.filename for f in mod.FILES}, "manifest and module list different files"
    for f in mod.FILES:
        entry = by_name[f.filename]
        assert entry["sha256"] == f.sha256
        assert entry["size"] == f.size
        assert entry["origin"] in ("primary", "secondary")
        assert entry["primary_reference"], f"{f.filename}: no primary_reference recorded"
        assert entry["retrieved_utc_date"] != "UNKNOWN", f"{f.filename}: retrieval date unknown"
        assert entry["checks"], f"{f.filename}: no integrity checks recorded"


def test_shared_distribution_archives_match_pins():
    from src.acquire.common import ArchiveMember, DIST_DIR

    archives = {}
    for mod in _modules():
        for f in mod.FILES:
            if isinstance(f, ArchiveMember):
                archives[f.archive.filename] = f.archive
    for name, rf in sorted(archives.items()):
        path = DIST_DIR / name
        assert path.exists(), f"missing {path}"
        assert sha256_file(path) == rf.sha256


def test_manifests_are_byte_stable():
    """Manifests are written with sorted keys and a trailing newline, so re-serialising them is a no-op."""
    for mod in _modules():
        path = RAW_ROOT / mod.SOURCE_ID / MANIFEST_NAME
        text = path.read_text(encoding="utf-8")
        assert text == json.dumps(json.loads(text), indent=2, sort_keys=True) + "\n"
