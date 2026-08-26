"""e124f_ap_core: FRONT N2-OFF step 3d -- which AP triples carry the two
half-flips of the {11,12} dyadic core?  Selector per in-block AP triple
(its two forbidden-monotone clauses), premises hard; get the solver's
unsat core and greedily minimize.  The surviving triples ARE the proof
skeleton (ladders + mirror APs) for the hand schema.

HALF-A: {t0<b6, t2<b5} + (t1 < m0)   [expect UNSAT at 0 mod 8]
HALF-B: {t1<b5, t3<b4} + (m0 < t1)   [expect UNSAT at 0 mod 8]

Run: .venv/bin/python experiments/e124f_ap_core.py [M ...]
"""
import sys
import time

from pysat.solvers import Cadical195


def build(M, premises):
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
    for p in range(n):
        for q in range(p + 1, n):
            vpq = var[(p, q)]
            for r in range(q + 1, n):
                vqr, vpr = var[(q, r)], var[(p, r)]
                cl.append([-vpq, -vqr, vpr])
                cl.append([vpq, vqr, -vpr])
    for (u, w) in premises:
        cl.append([o(u, w)])
    aps = []
    for y in range(M + 2, 2 * M):
        d = 1
        while y + d <= 2 * M and y - d > M:
            aps.append((y - d, y, y + d))
            d += 1
    nv = c
    sel = {}
    for (a, y, b) in aps:
        nv += 1
        sel[(a, y, b)] = nv
        cl.append([-o(a, y), -o(y, b), -nv])
        cl.append([-o(b, y), -o(y, a), -nv])
    return Cadical195(bootstrap_with=cl), sel


def minimize(sol, sel, core):
    core = list(core)
    changed = True
    while changed:
        changed = False
        for t in list(core):
            trial = [u for u in core if u != t]
            if not sol.solve(assumptions=[sel[u] for u in trial]):
                core = trial
                changed = True
    return core


def run(M, name, premises):
    t0 = time.time()
    sol, sel = build(M, premises)
    allsel = {v: k for k, v in sel.items()}
    if sol.solve(assumptions=list(sel.values())):
        print(f"M={M} {name}: SAT (no core)", flush=True)
        return
    core = [allsel[abs(l)] for l in sol.get_core()]
    core = minimize(sol, sel, core)
    m0 = 3 * M // 2

    def nm(v):
        if v == m0:
            return "m0"
        if abs(v - m0) <= 3:
            return f"m0{v - m0:+d}"
        return f"b{v - M}" if v < m0 else f"t{2 * M - v}"

    pretty = sorted((a, y, b) for (a, y, b) in core)
    print(f"M={M} {name}: minimized AP-core, {len(pretty)} triples "
          f"({time.time()-t0:.0f}s):", flush=True)
    for (a, y, b) in pretty:
        print(f"    ({nm(a)}, {nm(y)}, {nm(b)})  =  ({a}, {y}, {b})"
              f"   d={y - a}", flush=True)
    sol.delete()


def main():
    Ms = [int(a) for a in sys.argv[1:]] or [24, 32]
    for M in Ms:
        m0 = 3 * M // 2
        t0v, t1v, t2v, t3v = 2 * M, 2 * M - 1, 2 * M - 2, 2 * M - 3
        b4, b5, b6 = M + 4, M + 5, M + 6
        run(M, "HALF-A {t0<b6,t2<b5}+(t1<m0)",
            [(t0v, b6), (t2v, b5), (t1v, m0)])
        run(M, "HALF-B {t1<b5,t3<b4}+(m0<t1)",
            [(t1v, b5), (t3v, b4), (m0, t1v)])


if __name__ == "__main__":
    main()
