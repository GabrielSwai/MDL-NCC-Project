# src/compare.py
from __future__ import annotations
from dataclasses import dataclass
from typing import List
from data_io import load_charts_jsonl
from crossing import has_crossing
from mdl import ModelBits, dl_general, dl_ncc_monotone, total_dl_for_dataset
import argparse

@dataclass(frozen=True)
class Totals:
    general: int
    ncc: int


def compute_totals(path: str, model_bits: ModelBits) -> Totals:
    charts = load_charts_jsonl(path)
    triples = [(c.n, c.m, c.links) for c in charts]

    dl_g = total_dl_for_dataset(triples, model_bits.general, dl_general)
    dl_n = total_dl_for_dataset(triples, model_bits.ncc, dl_ncc_monotone)
    return Totals(general=dl_g, ncc=dl_n)


def main(argv: List[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Compare MDL totals: General vs NCC-friendly encoding.")
    p.add_argument("jsonl", help="Path to data/charts.jsonl (JSONL charts)")
    p.add_argument("--model-general", type=int, default=0, help="Fixed model bits for General")
    p.add_argument("--model-ncc", type=int, default=100, help="Fixed model bits for NCC-friendly")
    p.add_argument("--show-crossings", action="store_true", help="Print crossing stats")

    args = p.parse_args(argv)

    charts = load_charts_jsonl(args.jsonl)
    model_bits = ModelBits(general=args.model_general, ncc=args.model_ncc)
    totals = compute_totals(args.jsonl, model_bits)

    winner = "NCC-friendly" if totals.ncc < totals.general else "General"
    margin = abs(totals.ncc - totals.general)

    print("== NCC MDL Project ==")
    print(f"Charts: {len(charts)}")
    if args.show_crossings:
        num_cross = sum(1 for c in charts if has_crossing(c.links))
        print(f"Crossing charts: {num_cross} / {len(charts)}")

    print("")
    print(f"Model bits: General={model_bits.general} | NCC={model_bits.ncc}")
    print(f"Total DL:   General={totals.general} | NCC={totals.ncc}")
    print(f"Winner: {winner} (margin {margin} bits)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())