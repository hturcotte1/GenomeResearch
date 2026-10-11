"""Command line entry point.

    python -m src.acquire                 # acquire every registered source
    python -m src.acquire randi2023       # acquire selected sources
    python -m src.acquire --verify        # re-hash all raw files, no network
    python -m src.acquire --counts randi2023   # print record counts as JSON
"""

from __future__ import annotations

import argparse
import importlib
import json
import sys

from . import SOURCE_MODULES
from .common import verify_source_offline


def _load(name: str):
    if name not in SOURCE_MODULES:
        raise SystemExit(f"unknown source {name!r}; registered: {', '.join(SOURCE_MODULES)}")
    return importlib.import_module(f"src.acquire.{name}")


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="python -m src.acquire")
    p.add_argument("sources", nargs="*", help="sources to process (default: all)")
    mode = p.add_mutually_exclusive_group()
    mode.add_argument("--verify", action="store_true", help="re-hash raw files against pins, no network")
    mode.add_argument("--counts", action="store_true", help="print record counts computed from raw files")
    args = p.parse_args(argv)
    names = args.sources or list(SOURCE_MODULES)

    if args.verify:
        problems = []
        for name in names:
            mod = _load(name)
            problems += verify_source_offline(mod.SOURCE_ID, mod.FILES)
        for line in problems:
            print("FAIL", line)
        print(f"verified {len(names)} source(s): {'OK' if not problems else f'{len(problems)} problem(s)'}")
        return 1 if problems else 0

    if args.counts:
        out = {name: _load(name).record_counts() for name in names}
        print(json.dumps(out, indent=2, sort_keys=True))
        return 0

    for name in names:
        mod = _load(name)
        entries = mod.acquire()
        print(f"[{mod.SOURCE_ID}] {len(entries)} file(s) present and verified")
        for e in entries:
            print(f"    {e['filename']}  {e['sha256']}  ({e['origin']})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
