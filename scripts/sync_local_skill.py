#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "skills" / "agent" / "leveraged-etp-risk-lab" / "SKILL.md"


def main() -> int:
    parser = argparse.ArgumentParser(description="Sync the repo skill into a local Codex skills directory.")
    parser.add_argument("--source", default=str(SOURCE), help="source SKILL.md path")
    parser.add_argument(
        "--target-dir",
        default=str(_default_target_dir()),
        help="target skill directory; defaults to CODEX_HOME/skills/leveraged-etp-risk-lab or ~/.codex/skills/leveraged-etp-risk-lab",
    )
    args = parser.parse_args()
    source = Path(args.source)
    target_dir = Path(args.target_dir)
    if not source.exists():
        raise FileNotFoundError(source)
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / "SKILL.md"
    shutil.copyfile(source, target)
    print(f"synced {source} -> {target}")
    return 0


def _default_target_dir() -> Path:
    codex_home = os.environ.get("CODEX_HOME")
    base = Path(codex_home) if codex_home else Path.home() / ".codex"
    return base / "skills" / "leveraged-etp-risk-lab"


if __name__ == "__main__":
    raise SystemExit(main())
