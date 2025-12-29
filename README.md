# NCC-MDL-Project

MDL experiments for an *emergent* No-Crossing-Constraint–like bias in autosegmental association.

The goal is to test whether a Minimum Description Length (MDL) objective prefers **order-preserving (noncrossing)** association patterns because they are cheaper to encode, compared to more general association structures where crossings occur.

This repo is **research code** and currently **experimental**.

## What this is (and is not)

**This is:**
- A small MDL framework for comparing description lengths of autosegmental-style association charts under different encodings/model families.
- A reproducible harness for running those comparisons on toy data now, and curated datasets later.

**This is not:**
- A full phonology learner (yet).
- A claim that the No-Crossing Constraint is “real” as a standalone universal constraint (the point is to test whether it *emerges* under MDL).

## Core idea

We compare total description length:

\[
L(\text{model}) + \sum_i L(\text{chart}_i \mid \text{model})
\]

between (at minimum) two model families:

- **General**: crossings allowed; encode links as a general edge list (or equivalent).
- **NCC-friendly**: assume order-preserving structure; encode associations as a monotone mapping / compressed sequence (cheap when noncrossing).

If the NCC-friendly family wins *after* accounting for the model cost, that’s evidence that an NCC-like bias can be justified as a compression preference rather than a stipulation.

## Data format (JSONL)

Each line is one chart:

~~~json
{"id":"toy1","n":4,"m":5,"links":[[1,1],[2,2],[3,4]]}
{"id":"toy2","n":4,"m":5,"links":[[1,3],[2,1],[3,4]]}
~~~

Conventions:
- `n`: number of positions on tier 1 (e.g., TBUs)
- `m`: number of positions on tier 2 (e.g., tones)
- `links`: list of `(i, j)` pairs using **1-based indices**
- A crossing occurs when there exist `(i1, j1)` and `(i2, j2)` with `i1 < i2` but `j1 > j2`.

## Quickstart

### 1) Create a virtual environment

~~~bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
~~~

### 2) Install

If/when this repo becomes a package, do:

~~~bash
pip install -e .
~~~

(For now, you can just run scripts from `src/` directly.)

### 3) Run the comparison

Example (placeholder; adjust to match the CLI you implement):

~~~bash
python -m ncc_mdl.compare data/charts.jsonl
~~~

Expected output: total DL under each model family + which one wins + summary stats (e.g., how many charts contain crossings).

## Repo structure

~~~text
NCC-MDL-Project/
  data/
    charts.jsonl
  src/
    __init__.py
    io.py
    crossing.py
    codes.py
    mdl.py
    compare.py
  tests/
  README.md
  LICENSE
  CITATION.cff
~~~

## Roadmap

- v0: fixed association charts, compare encodings (General vs NCC-friendly).
- v1: richer link types (many-to-one, one-to-many / spreading).
- v2: latent structure (infer associations/tiers), with tractable search.
- v3: typology-style evaluation across multiple phenomena/languages.

## Notes & caveats

- This repo does **not** include copyrighted PDFs or proprietary datasets.
- Results in early versions may be sensitive to the chosen universal code / encoding scheme; that’s a feature, not a bug—this work is partly about making those commitments explicit.

## License

MIT — see `LICENSE`.

## Contact

Maintained by **Gabriel Swai**.  
If you open an issue, include:
- a minimal repro example
- your environment (`python --version`, OS)
- expected vs observed behavior