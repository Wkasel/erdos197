"""e140b: sharpening the SS5 frontier.

Part B2  Is the pure band-pair hypothesis enough?  Decomposed CI(48)
         at bounds (0,2,0), (1,2,0), (0,2,1) — if (0,2,0) is UNSAT,
         Theorem N6a reduces to: no 2-coloring of CORE'(M) in which
         BOTH teams own >= 2 band values is feasible (B0/P2 bounds
         irrelevant).  Also the mirror question (2,0,0) and (0,0,2):
         are the other single-block-pair hypotheses enough?

Part F2  Fan placement scan at M=48: FG (AP-free P2-core + unguarded
         double fans) for pairs across the band — does the kill
         depend on where the two band values sit?

Part F3  Fan robustness: adversarial subset S of P2-core (|S| >= k),
         AP clauses and fan units guarded by membership in S; find
         k_crit = max k with an escape for X = (192, 191) and
         X = (192, 190).  Quantifies how many P2 punctures a double
         fan survives (the supply side of the assembly).

Run: .venv/bin/python experiments/e140b_frontier2.py
Log: data/e140b_frontier2.log
"""
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from e136_u_decomp_check import solve_decomposed
from e140_bounds_probes import order_theory, fan_units

from pysat.solvers import Cadical195
from pysat.card import CardEnc, EncType


def partB2():
    print('== part B2: single-block-pair hypotheses, M=48 ==', flush=True)
    for bounds in ((0, 2, 0), (1, 2, 0), (0, 2, 1),
                   (2, 0, 0), (0, 0, 2)):
        v, el, info = solve_decomposed(48, bounds)
        line = f'  bounds {bounds}: {v} [{el}s]'
        if v == 'SAT':
            profs = {}
            for team in 'AB':
                col = info[team]
                profs[team] = [len([x for x in col if x <= 96]),
                               len([x for x in col if 96 < x <= 192]),
                               len([x for x in col if x > 192])]
            line += f'  profiles A{profs["A"]} B{profs["B"]}'
        print(line, flush=True)


def partF2():
    print('== part F2: fan placement scan, M=48 ==', flush=True)
    M = 48
    core = list(range(4 * M + 1, 6 * M + 16))
    pairs = [(129, 130), (129, 131), (129, 192), (150, 151),
             (168, 169), (168, 170), (168, 172), (180, 181),
             (129, 160), (140, 170)]
    for X in pairs:
        units = []
        for x in X:
            units += fan_units(M, x)
        v, el = order_theory(core, units)
        print(f'  FG(48; X={X}) units={len(units)}: {v} [{el}s]',
              flush=True)


def solve_fan_subset(M, X, k):
    """Adversary keeps S subset of P2-core with |S| >= k; AP clauses
    and fan units guarded by S-membership; SAT <=> escape exists."""
    V = list(range(4 * M + 1, 6 * M + 16))
    n = len(V)
    idx = {v: i for i, v in enumerate(V)}
    off = {}
    top = 0
    for i in range(n):
        for j in range(i + 1, n):
            top += 1
            off[(i, j)] = top
    sel = {}
    for v in V:
        top += 1
        sel[v] = top

    def lit(u, w):
        i, j = idx[u], idx[w]
        return off[(i, j)] if i < j else -off[(j, i)]

    Vs = set(V)
    cls = []
    for b in V:
        for d in range(1, min(b - V[0], V[-1] - b) + 1):
            a, c = b - d, b + d
            if a in Vs and c in Vs:
                g = [-sel[a], -sel[b], -sel[c]]
                cls.append(g + [-lit(a, b), -lit(b, c)])
                cls.append(g + [lit(a, b), lit(b, c)])
    for x in X:
        for (z, y) in fan_units(M, x):
            cls.append([-sel[y], -sel[z], lit(z, y)])
    for i in range(n):
        for j in range(i + 1, n):
            xij = off[(i, j)]
            for kk in range(j + 1, n):
                cls.append([-xij, -off[(j, kk)], off[(i, kk)]])
                cls.append([xij, off[(j, kk)], -off[(i, kk)]])
    card = CardEnc.atleast(lits=[sel[v] for v in V], bound=k,
                           top_id=top, encoding=EncType.seqcounter)
    t0 = time.time()
    with Cadical195(bootstrap_with=cls) as s:
        for c in card.clauses:
            s.add_clause(c)
        ok = s.solve()
        el = round(time.time() - t0, 1)
        if not ok:
            return 'UNSAT', el, None
        model = set(l for l in s.get_model() if l > 0)
    S = [v for v in V if sel[v] in model]
    return 'SAT', el, sorted(set(V) - set(S))


def partF3():
    print('== part F3: double-fan subset robustness, M=48 ==', flush=True)
    M = 48
    n = 2 * M + 15
    for X in ((192, 191), (192, 190)):
        lo, hi = 1, n            # SAT at lo?, UNSAT at hi (from F)
        v, el, _ = solve_fan_subset(M, X, n)
        print(f'  X={X} k={n}: {v} [{el}s]', flush=True)
        assert v == 'UNSAT'
        # find largest k with escape
        a, b = 1, n              # assume SAT at some small k
        v, el, _ = solve_fan_subset(M, X, a)
        print(f'  X={X} k={a}: {v} [{el}s]', flush=True)
        if v != 'SAT':
            print(f'  X={X}: no escape even at k=1 ?!', flush=True)
            continue
        while b - a > 1:
            mid = (a + b) // 2
            v, el, dropped = solve_fan_subset(M, X, mid)
            print(f'  X={X} k={mid}: {v} [{el}s]'
                  + (f' dropped({len(dropped)})={dropped[:20]}'
                     if v == 'SAT' and dropped is not None else ''),
                  flush=True)
            if v == 'SAT':
                a = mid
            else:
                b = mid
        print(f'  >> X={X}: k_crit={a} of {n} (d*={n - a} punctures '
              f'needed to escape)', flush=True)


def main():
    partB2()
    partF2()
    partF3()
    print('e140b: DONE', flush=True)


if __name__ == '__main__':
    main()
