# src/mdl.py
from __future__ import annotations
from dataclasses import dataclass
from typing import Iterable, List
from codes import nat_len
from data_io import Link


@dataclass(frozen=True)
class ModelBits:
    """
    Fixed model description lengths (in bits).
    """
    general: int = 0
    ncc: int = 100  # tweak: 0, 50, 100, 500...


def dl_general(n: int, m: int, links: Iterable[Link]) -> int:
    """
    General (crossings-allowed) encoding:
      - encode n, m, k
      - encode each endpoint i, j as naturals
    """
    L: List[Link] = [(int(i), int(j)) for (i, j) in links]
    k = len(L)
    bits = nat_len(n) + nat_len(m) + nat_len(k)
    for i, j in L:
        bits += nat_len(i) + nat_len(j)
    return bits


def dl_ncc_monotone(n: int, m: int, links: Iterable[Link]) -> int:
    """
    NCC-friendly encoding for v0:
    Assumes links are most naturally described as *order-preserving* w.r.t. tier order,
    so we encode in sorted i order and compress using deltas.

    This does NOT forbid crossings; crossings just tend to cost more bits because the
    j-deltas jump around.
    """
    L: List[Link] = sorted((int(i), int(j)) for (i, j) in links)
    k = len(L)

    bits = nat_len(n) + nat_len(m) + nat_len(k)

    prev_i = 0
    prev_j = 0
    for i, j in L:
        # gaps in i positions (>=1 because i is 1-based and sorted)
        di = i - prev_i
        # "delta-ish" for j that is cheap when j is nondecreasing.
        # Using nat_len on (j - prev_j) with +something is one way; here we use nat_len(max(0, dj))
        dj = j - prev_j
        bits += nat_len(di) + nat_len(max(0, dj))
        prev_i, prev_j = i, j

    return bits


def total_dl_for_dataset(
    charts: Iterable[tuple[int, int, List[Link]]],
    model_bits: int,
    dl_chart_fn,
) -> int:
    total = model_bits
    for (n, m, links) in charts:
        total += int(dl_chart_fn(n, m, links))
    return total