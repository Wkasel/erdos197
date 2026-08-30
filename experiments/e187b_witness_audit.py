"""e187b_witness_audit: independent audit + descent miner for a
SPLIT-residue witness (notes/83 SS0b SAT branch).  No CP-SAT: pure
python re-verification of every axiom, then anatomy + the gap-g
descent scan (recurring one-team class sections mod g — the Lemma
Q-g targets).

Run: .venv/bin/python experiments/e187b_witness_audit.py WITNESS.json
Artifacts: data/e187b_audit_<stem>.json + terse stream to stdout.
"""
import json
import os
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.join(os.path.dirname(HERE), "data")


def blocks(hor, t_lo=5):
    t_hi = hor.bit_length() - 2
    for t in range(t_lo, t_hi + 1):
        yield t, list(range((1 << t) + 1, (1 << (t + 1)) + 1))


def audit(path):
    d = json.load(open(path))
    hor, D, F, A = d["hor"], d["D"], d["F"], set(d["A"])
    u0 = d.get("u0", 32)
    res = {"path": os.path.basename(path), "hor": hor, "F": F,
           "D": D, "u0": u0, "nA": len(A)}
    team = {v: (v in A) for v in range(1, hor + 1)}
    fails = []

    # -- axiom (a): split floor
    for t, blk in blocks(hor):
        f = max(2, t - 5)
        cA = sum(1 for v in blk if v in A)
        if not (f <= cA <= len(blk) - f):
            fails.append(("split", t, cA))

    # -- axiom (c): minority pair-sparse gap >= 3 (strict minority;
    #    at a tie the encoding lets either side be designated)
    gap_census = {}
    for t, blk in blocks(hor):
        cA = sum(1 for v in blk if v in A)
        half = len(blk) / 2
        cand = []
        if cA < half:
            cand = [True]
        elif cA > half:
            cand = [False]
        else:
            cand = [True, False]

        def sparse_ok(min_team):
            vals = [v for v in blk if team[v] == min_team]
            return all(b - a >= 3 for a, b in zip(vals, vals[1:])), vals
        oks = []
        for mt in cand:
            ok, vals = sparse_ok(mt)
            oks.append(ok)
            if ok or len(cand) == 1:
                gaps = [b - a for a, b in zip(vals, vals[1:])]
                gap_census[t] = {"team": "A" if mt else "B",
                                 "size": len(vals),
                                 "gaps": dict(Counter(gaps))}
        if not any(oks):
            fails.append(("sparse", t))

    # -- axiom (d): HSPLIT mods 4+8 bichromatic, t >= 6; measure more
    purity = {}
    for md in (3, 4, 5, 6, 7, 8, 9, 12, 16, 32):
        mono = []
        for t, blk in blocks(hor, t_lo=6):
            for c in range(md):
                sec = [v for v in blk if v % md == c]
                if len(sec) >= 2:
                    s = sum(1 for v in sec if v in A)
                    if s == 0 or s == len(sec):
                        mono.append((t, c, "A" if s else "B"))
        purity[md] = mono
        if md in (4, 8) and mono:
            fails.append(("hsplit", md, mono[:4]))
    res["purity_mono_sections"] = {m: len(v) for m, v in purity.items()}
    res["purity_detail_odd"] = {m: purity[m][:40]
                                for m in (3, 5, 6, 7, 9, 12) if purity[m]}

    # -- axiom (b): window floor
    for a in range(32, hor // 2 + 1):
        g = a // 4
        cA = sum(1 for v in range(a + 1, 2 * a + 1) if v in A)
        if not (g <= cA <= a - g):
            fails.append(("window", a, cA))

    # -- axiom (e): censor — no in-team doubling chain depth D,
    #    reflectors <= F, seed > u0, strictly increasing
    chains = 0
    for v in range(u0 + 1, hor + 1):
        for f1 in range(1, F + 1):
            w1 = 2 * v - f1
            if w1 <= v or w1 > hor:
                continue
            if not (team[v] == team.get(f1) == team.get(w1)):
                continue
            for f2 in range(1, F + 1):
                w2 = 2 * w1 - f2
                if w2 <= w1 or w2 > hor:
                    continue
                if team.get(f2) == team[w1] == team.get(w2):
                    chains += 1
                    if chains <= 5:
                        fails.append(("censor", v, f1, w1, f2, w2))
    res["depth2_chains_leF"] = chains

    # -- H-census at F' = 64 (what the censor did NOT ban)
    h64 = Counter()
    for v in range(u0 + 1, hor + 1):
        for f1 in range(1, 65):
            w1 = 2 * v - f1
            if w1 <= v or w1 > hor:
                continue
            if team[v] == team.get(f1) == team.get(w1):
                h64["d1_A" if team[v] else "d1_B"] += 1
    res["h_census_F64_depth1"] = dict(h64)

    # -- window minority profile at dyadic anchors
    prof = {}
    a = 32
    while a <= hor // 2:
        cA = sum(1 for v in range(a + 1, 2 * a + 1) if v in A)
        prof[a] = min(cA, a - cA)
        a *= 2
    res["nu_profile"] = prof
    res["gap_census"] = gap_census

    # -- DESCENT MINER: one-team full class sections mod g, g=2..12,
    #    t >= 6 (Lemma Q-g targets: any (g, c, team) recurring at
    #    many t charts onto dead territory)
    miner = {}
    for g in range(2, 13):
        hits = []
        for t, blk in blocks(hor, t_lo=6):
            for c in range(g):
                sec = [v for v in blk if v % g == c]
                if len(sec) >= 2:
                    s = sum(1 for v in sec if v in A)
                    if s == 0 or s == len(sec):
                        hits.append({"t": t, "c": c,
                                     "team": "A" if s else "B"})
        miner[g] = hits
    res["descent_sections"] = {g: v for g, v in miner.items() if v}

    # -- longest fixed-gap AP run inside each block's minority
    runs = {}
    for t, blk in blocks(hor, t_lo=6):
        info = gap_census.get(t)
        if not info:
            continue
        mt = info["team"] == "A"
        vals = [v for v in blk if team[v] == mt]
        best = (0, None)
        for i in range(len(vals) - 1):
            g = vals[i + 1] - vals[i]
            L = 2
            j = i + 1
            while j + 1 < len(vals) and vals[j + 1] - vals[j] == g:
                L += 1
                j += 1
            if L > best[0]:
                best = (L, g)
        runs[t] = {"len": best[0], "gap": best[1],
                   "minority_size": len(vals)}
    res["max_ap_runs"] = runs

    res["fails"] = fails[:50]
    res["n_fails"] = len(fails)
    stem = os.path.splitext(os.path.basename(path))[0]
    out = os.path.join(BASE, f"e187b_audit_{stem}.json")
    json.dump(res, open(out, "w"), indent=1)
    print(json.dumps({k: res[k] for k in
                      ("nA", "n_fails", "depth2_chains_leF",
                       "purity_mono_sections", "nu_profile")},
                     indent=1))
    print("[audit] ->", out, "FAILS" if fails else "ALL-PASS")
    return res


if __name__ == "__main__":
    audit(sys.argv[1])
