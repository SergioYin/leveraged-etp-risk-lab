from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any, Dict, List

from .models import ProductTerms, ScenarioDay


def load_product(path: str) -> ProductTerms:
    with Path(path).open("r", encoding="utf-8") as handle:
        data: Dict[str, Any] = json.load(handle)
    return ProductTerms.from_dict(data)


def load_path(path: str) -> List[ScenarioDay]:
    days: List[ScenarioDay] = []
    with Path(path).open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames:
            raise ValueError("path CSV is empty")
        required = {"day", "underlying_return"}
        missing = required.difference(reader.fieldnames)
        if missing:
            raise ValueError(f"path CSV is missing column(s): {', '.join(sorted(missing))}")
        for row in reader:
            day = int(row["day"])
            label = row.get("label") or f"Day {day}"
            days.append(ScenarioDay(day=day, label=label, underlying_return=float(row["underlying_return"])))
    if not days:
        raise ValueError("path CSV has no scenario rows")
    return days


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
