# src/io.py
from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple
import json

Link = Tuple[int, int]


@dataclass(frozen=True)
class Chart:
    """
    A two-tier association chart.

    - n: number of positions on tier 1 (1..n)
    - m: number of positions on tier 2 (1..m)
    - links: list of (i, j) pairs with 1-based indices
    """
    id: str
    n: int
    m: int
    links: List[Link]


def validate_chart(chart: Chart) -> None:
    if chart.n < 1 or chart.m < 1:
        raise ValueError(f"{chart.id}: n and m must be >= 1")

    for (i, j) in chart.links:
        if not (1 <= i <= chart.n):
            raise ValueError(f"{chart.id}: link i={i} out of range 1..{chart.n}")
        if not (1 <= j <= chart.m):
            raise ValueError(f"{chart.id}: link j={j} out of range 1..{chart.m}")


def load_charts_jsonl(path: str | Path) -> List[Chart]:
    """
    Load charts from a JSONL file. Each line:
      {"id": "...", "n": int, "m": int, "links": [[i,j], ...]}

    Lines starting with '#' or empty lines are ignored.
    """
    p = Path(path)
    charts: List[Chart] = []

    with p.open("r", encoding="utf-8") as f:
        for line_no, raw in enumerate(f, start=1):
            s = raw.strip()
            if not s or s.startswith("#"):
                continue

            try:
                obj = json.loads(s)
            except json.JSONDecodeError as e:
                raise ValueError(f"{p}:{line_no}: invalid JSON: {e}") from e

            try:
                cid = str(obj["id"])
                n = int(obj["n"])
                m = int(obj["m"])
                links_raw = obj.get("links", [])
                links: List[Link] = [(int(a), int(b)) for (a, b) in links_raw]
            except Exception as e:
                raise ValueError(f"{p}:{line_no}: malformed chart fields: {e}") from e

            chart = Chart(id=cid, n=n, m=m, links=links)
            validate_chart(chart)
            charts.append(chart)

    if not charts:
        raise ValueError(f"{p}: no charts loaded (file empty or all commented?)")

    return charts