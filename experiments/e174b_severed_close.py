"""e174b_severed_close: close the surviving branches of the severed-ladder
derivation (e130c part2) with EXTRA battleground splits.

e130c part2 left surviving branches for the {11,12} K4 core at
punctures even_mid (12/64), b1 (2/32), and for m0-punctured
battlegrounds m0_c+2 (4-8/64), m0_c-2 (8-10/64) at M = 48/80/112.
Each surviving branch is a consistent-looking polarity assignment the
single split (t1 vs c) plus per-run Lemma-D fiats cannot refute.

Extension tried here (sound: order trichotomy is exhaustive case
analysis): for every surviving branch, add a SECOND (and if needed
THIRD) split literal from EXTRA = [(t1, m0-2), (t1, m0+2), (t3, m0),
(t3, m0-2), (t3, m0+2)] (skipping any pair touching the puncture),
i.e. branch on both orders of each extra pair, recursively, depth <= 3.
A branch is CLOSED if some depth's full sub-branch set all reach
contradiction.  ALL branches closing at all 3 scales + both control
scales still leaving survivors ==> the severed-ladder hand schema
extends to every tested single-puncture position with bounded extra
case analysis.

Run: .venv/bin/python experiments/e174b_severed_close.py
Artifacts: data/e174b_severed.json
"""
import itertools
import json
import sys
import time

sys.path.insert(0, "/Users/will/Dev/personal/tasks/math/erdos197/experiments")
from e130c_punctured_schema import closure, runs_of, fiat_edges  # noqa: E402

BASE = "/Users/will/Dev/personal/tasks/math/erdos197/data"
OUT = {}


def close_branch(M, seeds, pset, extra_pairs, depth):
    """True iff seeds close, possibly after splitting on extra pairs."""
    if closure(M, set(seeds), pset) == "contradiction":
        return 0  # closed with no extra split
    if depth == 0 or not extra_pairs:
        return None
    (u, v), rest = extra_pairs[0], extra_pairs[1:]
    if u in pset or v in pset:
        return close_branch(M, seeds, pset, rest, depth)
    best = None
    for lit in ((u, v), (v, u)):
        r = close_branch(M, set(seeds) | {lit}, pset, rest, depth - 1)
        if r is None:
            return None
        best = max(best or 0, r + 1)
    return best


def k4_branches_ext(M, punct, battleground, maxdepth=4):
    t0v, t1v, t2v, t3v = 2 * M, 2 * M - 1, 2 * M - 2, 2 * M - 3
    b4, b5, b6 = M + 4, M + 5, M + 6
    m0 = 3 * M // 2
    core = {(t0v, b6), (t1v, b5), (t2v, b5), (t3v, b4)}
    pset = frozenset(punct)
    for v in core:
        assert v[0] not in pset and v[1] not in pset, "core hit"
    ladders = [(M + 1, 2, 2 * M - 1), (M + 2, 4, 2 * M - 2),
               (M + 3, 4, 2 * M - 1), (M + 4, 4, 2 * M)]
    all_runs = []
    for (f, d, l) in ladders:
        all_runs += runs_of(f, d, l, pset)
    extra = [(t1v, m0 - 2), (t1v, m0 + 2), (t3v, m0),
             (t3v, m0 - 2), (t3v, m0 + 2)]
    if punct:
        pv = min(punct)
        if pv % 2 == 0:
            # severed even ladder: cross-run phase literals first
            extra = ([(pv - 4, pv + 4), (pv - 8, pv + 8),
                      (battleground, pv - 4), (battleground, pv + 4),
                      (t2v, pv - 4), (t2v, pv + 4), (t0v, pv - 4)]
                     + extra)
        elif pv == m0:
            extra = ([(m0 - 2, m0 + 2), (m0 - 4, m0 + 4),
                      (t1v, m0 - 4), (t1v, m0 + 4)] + extra)
    c = battleground
    nsurv = nclosed_extra = tot = 0
    worst_depth = 0
    for split in ((t1v, c), (c, t1v)):
        for pol in itertools.product((True, False), repeat=len(all_runs)):
            tot += 1
            seeds = set(core) | {split}
            for run, lf in zip(all_runs, pol):
                seeds |= fiat_edges(run, lf)
            if closure(M, set(seeds), pset) == "contradiction":
                continue
            r = close_branch(M, seeds, pset, extra, maxdepth)
            if r is None:
                nsurv += 1
            else:
                nclosed_extra += 1
                worst_depth = max(worst_depth, r)
    return {"branches": tot, "closed_by_extra_splits": nclosed_extra,
            "still_surviving": nsurv, "max_extra_depth": worst_depth}


def main():
    for M in (48, 80, 112):
        m0 = 3 * M // 2
        cases = {
            "even_mid": ([m0 + 2], m0),
            "b1": ([M + 1], m0),
            "m0_c+2": ([m0], m0 + 2),
            "m0_c-2": ([m0], m0 - 2),
        }
        for name, (punct, c) in cases.items():
            t0 = time.time()
            row = k4_branches_ext(M, punct, c)
            row["secs"] = round(time.time() - t0, 1)
            OUT.setdefault(str(M), {})[name] = row
            print(f"[ext] M={M} {name}: {row}", flush=True)
            json.dump(OUT, open(f"{BASE}/e174b_severed.json", "w"),
                      indent=1)
    # controls at 4 mod 8: extra splits must NOT close everything
    for M in (52, 84):
        row = k4_branches_ext(M, [], 3 * M // 2)
        OUT.setdefault(str(M), {})["control_intact"] = row
        print(f"[ext] control M={M}: {row}", flush=True)
    json.dump(OUT, open(f"{BASE}/e174b_severed.json", "w"), indent=1)
    print(f"-> {BASE}/e174b_severed.json", flush=True)


if __name__ == "__main__":
    main()
