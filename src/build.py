"""Rebuild every derived artifact from data/raw and config/.

    python -m src.build

Steps: namespace (Phase 2), merged table (Phase 4), summary document. Raw
data must already be acquired (``python -m src.acquire``). The output is
deterministic.
"""

from __future__ import annotations

import json

from src.merge import build_table, summary
from src.namespace import mapping


def main() -> dict:
    ns = mapping.build()
    tbl = build_table.build()
    summary.write()
    return {"namespace": ns, "table": tbl}


if __name__ == "__main__":
    print(json.dumps(main(), indent=2, sort_keys=True))
