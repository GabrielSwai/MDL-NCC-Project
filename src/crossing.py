# src/crossing.py
from __future__ import annotations
from typing import Iterable, List, Tuple
from data_io import Link


def has_crossing(links: Iterable[Link]) -> bool:
    """
    Crossing definition (standard for two ordered tiers):
    Two links (i1,j1) and (i2,j2) cross iff i1 < i2 but j1 > j2.
    """
    L: List[Link] = sorted((int(i), int(j)) for (i, j) in links)
    for a in range(len(L)):
        i1, j1 = L[a]
        for b in range(a + 1, len(L)):
            i2, j2 = L[b]
            if i1 < i2 and j1 > j2:
                return True
    return False


def crossing_pairs(links: Iterable[Link]) -> List[Tuple[Link, Link]]:
    """Return the list of crossing link-pairs (useful for debugging)."""
    L: List[Link] = sorted((int(i), int(j)) for (i, j) in links)
    out: List[Tuple[Link, Link]] = []
    for a in range(len(L)):
        i1, j1 = L[a]
        for b in range(a + 1, len(L)):
            i2, j2 = L[b]
            if i1 < i2 and j1 > j2:
                out.append(((i1, j1), (i2, j2)))
    return out