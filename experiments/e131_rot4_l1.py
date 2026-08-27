"""e131_rot4_l1: GAP-L1' machine layer.

ROT4 (the rotating-quarters partition): value v in octave
O_m = (2^m, 2^{m+1}], relative position p = (v - 2^m - 1) / 2^m in [0,1),
quarter q = floor(4p).  Team A owns quarters {m mod 4, (m+1) mod 4},
team B the other two -- i.e. A's half-octave interval rotates by one
quarter per octave.  Claimed (hand, notes/53): ROT4 is everywhere-split,
window-diffuse (no C-clean ratio-2 windows for any C, both teams), and
doubling-subcritical in BOTH teams for EVERY finite reflector set --
refuting L1' as stated in notes/46 SS5.

Parts:
  split    per-octave team counts (expect exactly half each).
  diffuse  max ratio-2 window density per team over all anchors
           a <= 2^17, horizon 2^18 (expect -> 3/4, never -> 1).
  subcrit  censored doubling closure (e121-style): seeds T n [2^10,2^11),
           reflectors T n [1,64], horizon 2^20 -- for ROT4 both teams
           (expect: closure dies within a few octaves), for an iid
           balanced control (expect: explosion), and for the GATE
           synthetic (B = pair-sparse random gaps {2,3}; expect: A's
           closure explodes -- the GATE lemma's prediction).
  bands    band-vacation statistics: for random (y, R): fraction of
           levels k <= 20 with band (2^k y, 2^k y + R] entirely
           A-free / B-free (ROT4: both happen at ~1/2 of levels;
           iid: never for R >= 24).
  columns  max monochrome run of owner(ceil(2^k y) + r) over k <= 60,
           random y, r in {0,1,2} (ROT4: expect <= 4).
  coupled  the C3 two-seam coupled gadget of e120 with the coloring
           FIXED to ROT4 on W = (M, 8M], M = 16, 32, 64: both teams'
           own orders, in-team AP clauses, block-order units at both
           seams for both teams (the G2 hypothesis).  UNSAT ==> ROT4's
           window pattern cannot recur under double block-order ==>
           ROT4 dies modulo GAP-G2, like every other Case-2 shape.

Run: .venv/bin/python experiments/e131_rot4_l1.py [part ...]
Artifacts: data/e131_rot4.json
"""
import json
import random
import sys
import time

from pysat.solvers import Cadical195

BASE = "/Users/will/Dev/personal/tasks/math/erdos197/data"
OUT = {}


def octave(v):
    m = v.bit_length() - 1
    if v == 1 << m:          # v = 2^m sits at the TOP of octave m-1
        m -= 1
    return m


def rot4_isA(v):
    if v <= 1:
        return True          # convention; irrelevant asymptotically
    m = octave(v)
    p = v - (1 << m) - 1     # 0 .. 2^m - 1
    q = (p * 4) >> m         # quarter 0..3
    return (q - m) % 4 in (0, 1)


def iid_isA(v, seed=7):
    rng = random.Random((v << 16) ^ seed)
    return rng.random() < 0.5


def make_gate_partner(n, seed=3):
    """B = pair-sparse random set (gaps 2 or 3); returns isA callable."""
    rng = random.Random(seed)
    B = set()
    v = 2
    while v <= n:
        B.add(v)
        v += rng.choice((2, 3))
    return lambda u: u not in B


def part_split():
    rows = {}
    for m in range(4, 21):
        lo, hi = (1 << m), (1 << (m + 1))
        nA = sum(1 for v in range(lo + 1, hi + 1) if rot4_isA(v))
        rows[m] = {"nA": nA, "nB": (hi - lo) - nA}
    OUT["split"] = rows
    print("split:", {m: r for m, r in rows.items() if m in (4, 10, 20)},
          flush=True)


def part_diffuse():
    N = 1 << 18
    isA = [False] * (N + 1)
    for v in range(1, N + 1):
        isA[v] = rot4_isA(v)
    pref = [0] * (N + 1)
    for v in range(1, N + 1):
        pref[v] = pref[v - 1] + (1 if isA[v] else 0)
    best = {}
    for m in range(5, 18):
        bA = bB = 0.0
        argA = argB = None
        for a in range(1 << m, 1 << (m + 1)):
            if 2 * a > N:
                break
            cA = pref[2 * a] - pref[a]
            dA = cA / a
            if dA > bA:
                bA, argA = dA, a
            dB = 1 - dA
            if dB > bB:
                bB, argB = dB, a
        best[m] = {"maxdensA": round(bA, 4), "argA": argA,
                   "maxdensB": round(bB, 4), "argB": argB}
    OUT["diffuse"] = best
    print("diffuse (max ratio-2 window density by anchor octave):",
          flush=True)
    for m, r in best.items():
        print("  ", m, r, flush=True)


def closure(isA, team_sign, horizon, seed_lo=1 << 10, seed_hi=1 << 11,
            refl_hi=64, cap=200_000):
    """Censored doubling closure of team T (T = A if team_sign else B)."""
    def inT(v):
        return isA(v) == team_sign
    refl = [f for f in range(1, refl_hi + 1) if inT(f)]
    seeds = [v for v in range(seed_lo, seed_hi) if inT(v)]
    seen = set(seeds)
    frontier = list(seeds)
    top = 0
    while frontier:
        nxt = []
        for u in frontier:
            for f in refl:
                w = 2 * u - f
                if w <= u or w > horizon:
                    continue
                if w not in seen and inT(w):
                    seen.add(w)
                    nxt.append(w)
                    if w > top:
                        top = w
            if len(seen) > cap:
                return {"nodes": len(seen), "top": top,
                        "verdict": "EXPLODES(cap)"}
        frontier = nxt
    return {"nodes": len(seen), "top": top,
            "verdict": ("EXPLODES" if top > horizon // 4 else "DIES"),
            "top_octave": octave(top) if top else None}


def part_subcrit():
    H = 1 << 18
    rows = {}
    t0 = time.time()
    rows["rot4_A"] = closure(rot4_isA, True, H)
    rows["rot4_B"] = closure(rot4_isA, False, H)
    rows["iid_A"] = closure(iid_isA, True, H)
    gate = make_gate_partner(H)
    rows["gate_majorityA"] = closure(gate, True, H)
    rows["gate_sparseB"] = closure(gate, False, H)
    OUT["subcrit"] = rows
    for k, r in rows.items():
        print(f"subcrit {k}: {r}", flush=True)
    print(f"  ({time.time()-t0:.0f}s)", flush=True)


def part_bands():
    rng = random.Random(41)
    rows = []
    for trial in range(24):
        y = 1 + rng.random()          # y in (1, 2)
        R = 32
        vacA = vacB = lvl = 0
        for k in range(8, 20):
            base = int(y * (1 << k))
            band = range(base + 1, base + R + 1)
            a = sum(1 for v in band if rot4_isA(v))
            lvl += 1
            if a == 0:
                vacA += 1
            if a == R:
                vacB += 1
        rows.append({"y": round(y, 5), "levels": lvl,
                     "A_vacated": vacA, "B_vacated": vacB})
    iid_vac = 0
    for trial in range(24):
        y = 1 + rng.random()
        for k in range(8, 20):
            base = int(y * (1 << k))
            a = sum(1 for v in range(base + 1, base + 33) if iid_isA(v))
            if a in (0, 32):
                iid_vac += 1
    OUT["bands"] = {"rot4": rows, "iid_vacations_total": iid_vac}
    agg = sum(r["A_vacated"] + r["B_vacated"] for r in rows)
    print(f"bands: rot4 total vacations {agg}/{24*12*2} slots; "
          f"iid {iid_vac} (expect 0)", flush=True)


def part_columns():
    rng = random.Random(17)
    D = 61                       # y = num / 2^D, exact integer arithmetic
    worst = 0
    for trial in range(200):
        num = (1 << D) + rng.getrandbits(D)      # y in (1, 2)
        for r in (0, 1, 2):
            run = best = 0
            last = None
            for k in range(4, 60):
                v = ((num << k) + (1 << D) - 1) >> D   # ceil(2^k y)
                own = rot4_isA(v + r)
                if own == last:
                    run += 1
                else:
                    run, last = 1, own
                best = max(best, run)
            worst = max(worst, best)
    OUT["columns"] = {"max_monochrome_run": worst}
    print(f"columns: max monochrome run over 200 y x 3 shifts = {worst}",
          flush=True)


def part_coupled():
    for M in [16, 32, 64]:
        t0 = time.time()
        W = list(range(M + 1, 8 * M + 1))
        colA = {v: rot4_isA(v) for v in W}
        res = {}
        for team, isT in (("A", True), ("B", False)):
            vals = [v for v in W if colA[v] == isT]
            idx = {v: i for i, v in enumerate(vals)}
            n = len(vals)
            var = {}
            c = 0
            for p in range(n):
                for q in range(p + 1, n):
                    c += 1
                    var[(p, q)] = c

            def o(u, w):
                p, q = idx[u], idx[w]
                return var[(p, q)] if p < q else -var[(q, p)]

            cl = []
            vset = set(vals)
            for y in vals:
                d = 1
                while y + d <= 8 * M and y - d > M:
                    a, b = y - d, y + d
                    if a in vset and b in vset:
                        cl.append([-o(a, y), -o(y, b)])
                        cl.append([-o(b, y), -o(y, a)])
                    d += 1
            for p in range(n):
                for q in range(p + 1, n):
                    vpq = var[(p, q)]
                    for r in range(q + 1, n):
                        cl.append([-vpq, -var[(q, r)], var[(p, r)]])
                        cl.append([vpq, var[(q, r)], -var[(p, r)]])
            # block-order units at both seams (G2 hypothesis)
            B0 = [v for v in vals if v <= 2 * M]
            B1 = [v for v in vals if 2 * M < v <= 4 * M]
            B2 = [v for v in vals if v > 4 * M]
            for u in B0:
                for w in B1:
                    cl.append([o(u, w)])
            for u in B1:
                for w in B2:
                    cl.append([o(u, w)])
            sol = Cadical195(bootstrap_with=cl)
            sat = sol.solve()
            sol.delete()
            res[team] = "SAT" if sat else "UNSAT"
        row = {"M": M, "verdicts": res,
               "sizes": {t: sum(1 for v in W if colA[v] == (t == 'A'))
                         for t in "AB"},
               "secs": round(time.time() - t0, 1)}
        OUT.setdefault("coupled", {})[str(M)] = row
        print(f"coupled M={M}: {res} ({row['secs']}s)", flush=True)
        dump()


def dump():
    json.dump(OUT, open(f"{BASE}/e131_rot4.json", "w"), indent=1)


def main():
    parts = sys.argv[1:] or ["split", "diffuse", "subcrit", "bands",
                             "columns", "coupled"]
    for p in parts:
        globals()[f"part_{p}"]()
        dump()
    print(f"-> {BASE}/e131_rot4.json", flush=True)


if __name__ == "__main__":
    main()
