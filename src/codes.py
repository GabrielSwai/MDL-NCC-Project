# src/codes.py
from __future__ import annotations
import math


def elias_gamma_len(x: int) -> int:
    """
    Elias gamma code length in bits for x >= 1.
    L(x) = 2*floor(log2(x)) + 1

    This is a simple universal code starter for MDL baselines.
    """
    if x < 1:
        raise ValueError("elias_gamma_len expects x >= 1")
    return 2 * int(math.floor(math.log2(x))) + 1


def nat_len(x: int) -> int:
    """
    Universal-ish length for a natural number (>=0), using gamma on x+1.
    """
    if x < 0:
        raise ValueError("nat_len expects x >= 0")
    return elias_gamma_len(x + 1)