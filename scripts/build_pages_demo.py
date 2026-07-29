#!/usr/bin/env python3
"""Build the existing CampusWeave frontend as a static, fixture-backed demo."""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from campusweave.service import reference_response  # noqa: E402

RUNTIME_MARKER = '<meta name="campusweave-runtime" content="loopback">'
DEMO_MARKER = '<meta name="campusweave-runtime" content="static-demo">'


def build(output: Path) -> None:
    if output.exists():
        raise FileExistsError(f"output path already exists: {output}")

    shutil.copytree(ROOT / "web", output)
    index_path = output / "index.html"
    index = index_path.read_text(encoding="utf-8")
    if index.count(RUNTIME_MARKER) != 1:
        raise ValueError("web/index.html must contain one loopback runtime marker")
    index_path.write_text(index.replace(RUNTIME_MARKER, DEMO_MARKER), encoding="utf-8")

    fixture = json.dumps(reference_response(), indent=2, sort_keys=True) + "\n"
    (output / "demo-fixture.json").write_text(fixture, encoding="utf-8")
    (output / ".nojekyll").write_text("", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    build(args.output.resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
