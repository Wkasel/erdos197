"""e124_family_miner: FRONT N2 step 2b -- mine the e122 catalogue for
uniform (affine-in-x) core families.

A FAMILY is: a lane (arithmetic progression of pair-indices x with step
s in {2, 4, 6, 12}), one core per lane member, and a bijection between
consecutive cores' units such that every unit moves by the SAME (di, dj)
per lane step, with di and dj EVEN (offset parities are what the hand
proofs consume, so a uniform schema needs them constant along the lane).
For each family report how the residue law varies along the lane.

Also: the dyadic sub-catalogue -- for every pair, which cores fire at
M = 0 mod 8 (the class of dyadic block scales, the only class T-PIN
needs) -- and whether every pair has one.

Run: .venv/bin/python experiments/e124_family_miner.py
Output: data/e124_families.json

2026-08-26 session note: the final e122_n2_residue.json was lost with
the e122 session (killed at M=135); input is now the reconstruction
data/e122_n2_residue_recon.json (built by e124_prep_catalogue.py from
the complete-sweep partial checkpoint, M = 16..128).  Also fixed: the
constant-delta requirement is now enforced DURING chain extension (the
committed version had dead code there and only filtered afterwards,
which both blows up and keeps subset-chains alive).
"""
import itertools
import json
import os

BASE = "/Users/will/Dev/personal/tasks/math/erdos197/data"


def match_step(c1, c2, s):
    """All unit-bijections c1 -> c2 with constant even (di, dj) per unit.
    Returns list of tuples (delta-vector) where delta-vector is the
    sorted multiset of (di, dj) used -- but we require ONE (di,dj) per
    UNIT-SLOT, so return the assignment as a tuple of (di,dj) aligned to
    sorted(c1)."""
    out = []
    if len(c1) != len(c2):      # zip would silently truncate
        return out
    c1s = sorted(c1)
    for perm in itertools.permutations(sorted(c2)):
        ds = []
        ok = True
        for (i1, j1), (i2, j2) in zip(c1s, perm):
            di, dj = i2 - i1, j2 - j1
            if di % 2 or dj % 2 or di + 2 * dj != s or abs(di) > 14:
                ok = False
                break
            ds.append((di, dj))
        if ok:
            out.append((tuple(ds), perm))
    return out


def main():
    src = f"{BASE}/e122_n2_residue.json"
    if not os.path.exists(src):
        src = f"{BASE}/e122_n2_residue_recon.json"
    print(f"catalogue: {src}")
    d = json.load(open(src))
    cores = {}      # x -> list of (coretuple, law)
    for e in d["cores"]:
        x = e["x"]
        cr = tuple(sorted(map(tuple, e["core"])))
        cores.setdefault(x, []).append((cr, e["law"], e["ms"]))
    xs = sorted(cores)
    print(f"pairs: {xs}; catalogue sizes "
          f"{[len(cores[x]) for x in xs]}")

    # ---- dyadic (0 mod 8) sub-catalogue ----
    dyadic = {}
    for x in xs:
        dy = []
        for cr, law, ms in cores[x]:
            hits = [m for m in ms if m % 8 == 0]
            if len(hits) >= 5:
                dy.append((cr, law, hits))
        dyadic[x] = dy
        print(f"x={x}: {len(dy)} cores fire on >= 5 scales M = 0 mod 8")

    # ---- affine families ----
    fams = []
    for s in (2, 4, 6, 12):
        lanes = {}
        for x in xs:
            lanes.setdefault(x % s if s > 2 else 0, []).append(x)
        for lane in lanes.values():
            lane = sorted(lane)
            if len(lane) < 3:
                continue
            # extend chains core-by-core along the lane
            chains = [[(lane[0], cr, None)] for cr, _, _ in cores[lane[0]]]
            for x2 in lane[1:]:
                nxt = []
                for ch in chains:
                    x1, cr1, _ = ch[-1]
                    if x2 - x1 != s:
                        continue
                    prev_delta = ch[-1][2] if len(ch) >= 2 else None
                    for cr2, _, _ in cores[x2]:
                        for ds, perm in match_step(cr1, cr2, s):
                            # delta must equal the chain's existing delta
                            if prev_delta is not None and ds != prev_delta:
                                continue
                            nxt.append(ch + [(x2, cr2, ds)])
                chains = [c for c in chains] + nxt
            # keep chains of length >= 3 with CONSTANT delta
            for ch in chains:
                if len(ch) < 3:
                    continue
                deltas = {c[2] for c in ch[1:] if len(c) > 2}
                if len(deltas) != 1:
                    continue
                fams.append({
                    "step": s,
                    "members": [{"x": c[0],
                                 "core": [list(u) for u in c[1]]}
                                for c in ch],
                    "delta": [list(t) for t in list(deltas)[0]]})
    # dedupe subset-families (keep maximal)
    fams.sort(key=lambda f: -len(f["members"]))
    kept = []
    seen = set()
    for f in fams:
        key = tuple((m["x"], tuple(map(tuple, m["core"])))
                    for m in f["members"])
        if any(set(key) < set(k2) for k2 in seen):
            continue
        if key in seen:
            continue
        seen.add(key)
        kept.append(f)
    print(f"\n{len(kept)} maximal affine families (len >= 3):")
    law_by = {}
    for e in d["cores"]:
        law_by[(e["x"], tuple(sorted(map(tuple, e["core"]))))] = \
            e["law"].get("law", "?")
    for f in kept:
        desc = []
        for m in f["members"]:
            cr = tuple(sorted(map(tuple, m["core"])))
            pretty = ",".join(f"t{i}<b{j}" for i, j in cr)
            desc.append(f"x={m['x']}: {{{pretty}}} "
                        f"[{law_by.get((m['x'], cr), '?')}]")
        print(f"  step {f['step']}, delta {f['delta']}:")
        for line in desc:
            print(f"    {line}")
    json.dump({"families": kept,
               "dyadic_counts": {x: len(dyadic[x]) for x in xs}},
              open(f"{BASE}/e124_families.json", "w"), indent=1)
    print(f"-> {BASE}/e124_families.json")


if __name__ == "__main__":
    main()
