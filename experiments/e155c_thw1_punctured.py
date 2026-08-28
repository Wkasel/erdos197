"""e155c: punctured-ThW1' checks for the P-ARM S2 corner
(notes/58 SS3.5/SS3.7).

Under the hatch, Th1(A)[A_o] is the odd-class alpha system: the
image under h_O of [AP-freeness on the odd band values + the A2
alpha-units of the odd class (attacker auto-in-U_A)], restricted to
A_o = odds \ B_o.  In Case S2 the fan-safe B_o is contained in some
MAXIMAL clique Q of the e155b SAT-alive graph, so if the theory
minus h(Q) is UNSAT then the theory minus any subset is UNSAT
(a-fortiori: fewer punctures = more constraints).  Mirror statement
for Th1(B)[B_e] with the even class.

Checks per m and per class c in {odd, even}:
  full      : the class alpha system on the full class   — UNSAT?
  minus {v} : for every single class value v             — UNSAT?
  minus Q   : for every maximal clique Q of the matching alive
              graph (odd class punctures come from W2o cliques,
              even from W2e)                              — UNSAT?

The theories are generated at FULL scale (M = 2m) by direct A2/AP
enumeration inside the class, then halved — no hand-transcribed
unit family, so boundary parity effects are impossible.

Run: .venv/bin/python experiments/e155c_thw1_punctured.py m [m ...]
Log: data/e155_parm_hyp.log (+ JSON key 'C')
"""
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from e155_parm_hypotheses import order_unsat, log, OUT


def class_alpha_system(M, parity, removed_full=()):
    """Full-scale: points = band values of `parity` minus removed;
    units z < y for A2 APs (x, y, z) inside the class with x in
    [2M-30, 2M] (attacker parity matches automatically), y, z in
    the point set.  Halved coordinates via (v + (parity odd)) / 2."""
    pts_full = [v for v in range(3 * M - 15, 4 * M + 1)
                if v % 2 == parity and v not in removed_full]
    s = set(pts_full)
    units = []
    for y in pts_full:
        for z in pts_full:
            if z <= y:
                continue
            x = 2 * y - z
            if 2 * M - 30 <= x <= 2 * M:
                units.append((z, y))
    # halve (h preserves APs and order structure)
    off = 1 if parity == 1 else 0
    h = {v: (v + off) // 2 for v in pts_full}
    return [h[v] for v in pts_full], [(h[a], h[b]) for (a, b) in units]


def maximal_cliques(edges):
    verts = sorted(set(x for p in edges for x in p))
    adj = {v: set() for v in verts}
    for (a, b) in edges:
        adj[a].add(b)
        adj[b].add(a)
    out = []

    def bk(r, p, x):
        if not p and not x:
            out.append(sorted(r))
            return
        pivot = max(p | x, key=lambda u: len(adj[u]), default=None)
        for v in list(p - (adj[pivot] if pivot else set())):
            bk(r | {v}, p & adj[v], x & adj[v])
            p.discard(v)
            x.add(v)
    bk(set(), set(verts), set())
    return out


def main():
    with open(OUT) as f:
        res = json.load(f)
    for marg in sys.argv[1:]:
        m = int(marg)
        M = 2 * m
        summary = {}
        for parity, wname in ((1, 'W2o'), (0, 'W2e')):
            t0 = time.time()
            pts, units = class_alpha_system(M, parity)
            full_unsat = order_unsat(pts, units)
            # single punctures
            allv = [v for v in range(3 * M - 15, 4 * M + 1)
                    if v % 2 == parity]
            sat_singles = []
            for v in allv:
                p2, u2 = class_alpha_system(M, parity, (v,))
                if not order_unsat(p2, u2):
                    off = 1 if parity == 1 else 0
                    sat_singles.append((v + off) // 2)
            # maximal-clique punctures (cliques are in halved coords)
            sat_alive = res[str(m)]['B'][wname].get('sat_alive', [])
            cliqs = maximal_cliques([tuple(p) for p in sat_alive])
            off = 1 if parity == 1 else 0
            sat_cliques = []
            for Q in cliqs:
                rem = tuple(2 * q - off for q in Q)
                p2, u2 = class_alpha_system(M, parity, rem)
                if not order_unsat(p2, u2):
                    sat_cliques.append(Q)
            log(f'  e155c m={m} {"odd" if parity else "even"} class '
                f'({wname} cliques): full '
                f'{"UNSAT" if full_unsat else "SAT"}; single-drop SAT '
                f'at {len(sat_singles)}/{len(allv)} values '
                f'{sat_singles[:12]}; {len(cliqs)} maximal cliques, '
                f'SAT after removal: {len(sat_cliques)} '
                f'{sat_cliques[:6]} [{time.time()-t0:.0f}s]')
            summary['odd' if parity else 'even'] = {
                'full_unsat': full_unsat,
                'sat_singles': sat_singles,
                'n_cliques': len(cliqs),
                'sat_cliques': sat_cliques}
        res[str(m)]['C'] = summary
        with open(OUT, 'w') as f:
            json.dump(res, f, indent=0)
    log('e155c: done')


if __name__ == '__main__':
    main()
