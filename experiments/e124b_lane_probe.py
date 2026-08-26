"""e124b_lane_probe: FRONT N2-OFF step 2 -- direct solver probes of the
candidate off-diagonal lanes surfaced by the e124 miner.

The e122/e124 laws were fitted on MINIMAL-core appearance lists, which
undercount (a core also fires at scales where a subset or different core
preempts minimality).  Here each lane instance is probed DIRECTLY:
AP-freeness on (M, 2M] + the lane's units assumed, exact SAT/UNSAT at
every M in the sweep, and the residue law fitted on the true firing set.

Lanes (units in (i, j) coords, t_i = 2M - i, b_j = M + j, attacker
a = i + 2j must be in {x, x+1}; instance defined for odd x >= 11):

  A4a(x) = {(x-11,6),(x-10,5),(x-9,5),(x-8,4)}   x=11: the 0-mod-8
           size-4 core {t0<b6,t1<b5,t2<b5,t3<b4} of the {11,12} lane
  A4b(x) = {(x-11,6),(x-9,5),(x-8,4),(x-4,2)}    x=11: {t0<b6,t2<b5,t3<b4,t7<b2}
  A4c(x) = {(x-11,6),(x-9,5),(x-4,2),(x-2,1)}    x=11: {t0<b6,t2<b5,t7<b2,t9<b1}
  A4d(x) = {(x-10,5),(x-9,5),(x-8,4),(x-5,3)}    x=11: {t1<b5,t2<b5,t3<b4,t6<b3}
  B2(x)  = {(x-9,5),(x-6,3),(x-4,2)}             x=11: {t2<b5,t5<b3,t7<b2}, M=2 mod 8
  B6(x)  = {(x-8,4),(x-6,3),(x-1,1)}             x=11: {t3<b4,t5<b3,t10<b1}, M=6 mod 8
  C(x)   = {(x-11,6),(x-9,5),(x-6,3)}            x=11: {t0<b6,t2<b5,t5<b3}, odd lane,
           miner law M = x+2 mod 8 for x = 11..17
  D3(p)  = diagonal control C3(p) at x = 3p (p = 5, 7): known flip law

Run: .venv/bin/python experiments/e124b_lane_probe.py [Mmax]
Output: data/e124b_lane_probe.json
"""
import json
import sys
import time

from pysat.solvers import Cadical195

BASE = "/Users/will/Dev/personal/tasks/math/erdos197/data"
XS = [11, 13, 15, 17, 19, 21]


def lanes_for(x):
    d = x - 11
    out = {
        "A4a": [(x - 11, 6), (x - 10, 5), (x - 9, 5), (x - 8, 4)],
        "A4b": [(x - 11, 6), (x - 9, 5), (x - 8, 4), (x - 4, 2)],
        "A4c": [(x - 11, 6), (x - 9, 5), (x - 4, 2), (x - 2, 1)],
        "A4d": [(x - 10, 5), (x - 9, 5), (x - 8, 4), (x - 5, 3)],
        "B2": [(x - 9, 5), (x - 6, 3), (x - 4, 2)],
        "B6": [(x - 8, 4), (x - 6, 3), (x - 1, 1)],
        "C": [(x - 11, 6), (x - 9, 5), (x - 6, 3)],
    }
    if x % 3 == 0 and (x // 3) % 2 == 1:
        p = x // 3
        out["D3"] = [(p, p), (p - 2, p + 1), (p + 5, p - 2)]
    # attacker sanity: every unit's attacker must be x or x+1
    for name, us in out.items():
        for (i, j) in us:
            assert i + 2 * j in (x, x + 1), (x, name, i, j)
    return out


def build_base(M, all_units):
    n = M
    var = {}
    c = 0
    for p in range(n):
        for q in range(p + 1, n):
            c += 1
            var[(p, q)] = c

    def o(u, w):
        p, q = u - M - 1, w - M - 1
        return var[(p, q)] if p < q else -var[(q, p)]

    cl = []
    for y in range(M + 2, 2 * M):
        d = 1
        while y + d <= 2 * M and y - d > M:
            a, b = y - d, y + d
            cl.append([-o(a, y), -o(y, b)])
            cl.append([-o(b, y), -o(y, a)])
            d += 1
    for p in range(n):
        for q in range(p + 1, n):
            vpq = var[(p, q)]
            for r in range(q + 1, n):
                vqr, vpr = var[(q, r)], var[(p, r)]
                cl.append([-vpq, -vqr, vpr])
                cl.append([vpq, vqr, -vpr])
    sel = {}
    nv = c
    for (i, j) in sorted(all_units):
        z, y = 2 * M - i, M + j
        if not (M < z <= 2 * M and M < y <= 2 * M and z != y):
            continue
        nv += 1
        sel[(i, j)] = nv
        cl.append([o(z, y), -nv])
    return Cadical195(bootstrap_with=cl), sel


def infer_law(unsat_ms, sweep):
    if not unsat_ms:
        return "never"
    uset = set(unsat_ms)
    for r in (1, 2, 3, 4, 5):
        mod = 2 ** r
        S = sorted({m % mod for m in unsat_ms})
        cand = [m for m in sweep if m % mod in S]
        misses = [m for m in cand if m not in uset]
        if not misses:
            return f"M mod {mod} in {S} (from {min(unsat_ms)})"
        m0 = max(misses) + 1
        cand_above = [m for m in cand if m >= m0]
        if cand_above and all(m in uset for m in cand_above) \
                and len(cand_above) >= 5:
            spor = sorted(m for m in unsat_ms if m < m0)
            return (f"M mod {mod} in {S}, M >= {m0}"
                    f" (+{len(spor)} sporadic {spor})")
    return f"irregular ({len(unsat_ms)} scales: {unsat_ms})"


def main():
    mmax = int(sys.argv[1]) if len(sys.argv) > 1 else 160
    sweep = list(range(16, mmax + 1))
    inst = {}          # (x, lane) -> units
    all_units = set()
    for x in XS:
        for name, us in lanes_for(x).items():
            inst[(x, name)] = us
            all_units |= set(us)
    fires = {k: [] for k in inst}
    t00 = time.time()
    for M in sweep:
        t0 = time.time()
        sol, sel = build_base(M, all_units)
        row = []
        for (x, name), us in sorted(inst.items()):
            if any(u not in sel for u in us):
                continue        # unit degenerate at this M
            if not sol.solve(assumptions=[sel[u] for u in us]):
                fires[(x, name)].append(M)
                row.append(f"{name}({x})")
        sol.delete()
        print(f"M={M}: {' '.join(row)}  ({time.time()-t0:.1f}s, "
              f"total {time.time()-t00:.0f}s)", flush=True)
        if M % 16 == 0:
            json.dump(
                {"sweep_done_to": M,
                 "fires": {f"{x}:{n}": ms
                           for (x, n), ms in sorted(fires.items())}},
                open(f"{BASE}/e124b_lane_probe.json", "w"), indent=1)
    print("\n=== fitted laws (true firing sets) ===")
    out = {"sweep": [sweep[0], sweep[-1]], "lanes": []}
    for (x, name), ms in sorted(fires.items(), key=lambda kv: (kv[0][1],
                                                               kv[0][0])):
        law = infer_law(ms, sweep)
        us = inst[(x, name)]
        pretty = ",".join(f"t{i}<b{j}" for i, j in sorted(us))
        print(f"{name}(x={x}) {{{pretty}}}: {law}", flush=True)
        out["lanes"].append({"lane": name, "x": x,
                             "units": [list(u) for u in sorted(us)],
                             "fires": ms, "law": law})
    json.dump(out, open(f"{BASE}/e124b_lane_probe.json", "w"), indent=1)
    print(f"-> {BASE}/e124b_lane_probe.json")


if __name__ == "__main__":
    main()
