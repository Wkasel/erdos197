"""Erdős #197 — e172: FRONT MAXSAT — core-guided lower bounds on the
inversion SUM of the budget instance (notes/54 GAP-V*; notes/67-maxsat).

The budget instance U(M; c; vA, vB) (e127_seam_budget.solve_budget) is a
min-violations problem: v*_c(M) = least symmetric v with U(M; c; v, v)
SAT.  Near-critical DECISION queries are hopeless (bal@24: v=4 UNSAT in
5.9 h, v=16 TIMEOUT at 22 h).  Reformulate as MaxSAT:

    hard = guarded APs (both directions, full window) + complete
           per-team transitivity + per-team block balance cards +
           one-way inversion-indicator semantics       (exactly e127's)
    soft = { (¬x) : x inversion indicator, either team }, weight 1.

MaxSAT optimum  s*(M) = min over valid colorings + per-team orders of
(inv_A + inv_B) — the minimum TOTAL seam-inversion count.  (In any
model #x-true >= actual inversions, and the honest setting achieves
equality, so the min over models equals the min over colorings/orders.)
RC2 (core-guided) certifies monotonically growing lower bounds on s*
long before the optimum: after each processed core, rc2.cost is a valid
LB — every bump is streamed here with a timestamp and core certificate.

RELATION TO v* (the symmetric max-budget price, notes/54 §1) — exact:
  (i)  every valid coloring/orders has inv_A + inv_B >= s*, hence
       max(inv_A, inv_B) >= ceil(s*/2); so U(M; c; v, v) is UNSAT for
       all v < ceil(s*/2):   v*_c(M) >= ceil(s*(M)/2),
       and every INTERMEDIATE lower bound s <= s* gives
       v*_c(M) >= ceil(s/2) the same way.  This feeds Theorem LT
       verbatim (notes/54 Cor. D1: max_T Inv_T(N) >= v*_c(N) >=
       ceil(s/2) at every qualifying Case-2 anchor).
  (ii) conversely a min-max model pays <= v* per team, so
       s* <= 2 v*_c(M):  s* ∈ [v*, 2v*].  The sum route loses at most
       a factor 2 and CALIBRATION at M = 16 (v* ∈ {5,6}, e127/e132)
       must land s*(16) in [5, 12].
  (iii) an OPT model also gives an UPPER bound: v* <= max(inv_A, inv_B)
       of the optimal-sum witness (any model's max bounds v* above).

Certificates: each cost bump logs elapsed time, raw core size, and the
seam pairs of the core's original soft literals (when few) — an
auditable "at least one of these inversions is unavoidable given the
previously relaxed structure" chain.  OPT models are independently
re-audited by e127's audit() (bounds, AP-freedom, inversion recount).

Usage:
  e172_maxsat_lb.py bal   --M 16 [--wall 86400] [--solver g3]
  e172_maxsat_lb.py const --M 24 --bounds 3,6,12 [--wall 86400]
Artifacts: data/e172_maxsat_lb.jsonl (streaming), data/e172_{tag}.json.
Run under `timeout` for a hard wall (the final near-critical SAT call
cannot be interrupted in-process; the jsonl LB record survives a kill).
"""
import argparse
import json
import math
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
DATA = os.path.join(REPO, 'data')
JSONL = os.path.join(DATA, 'e172_maxsat_lb.jsonl')

sys.path.insert(0, HERE)
from pysat.formula import WCNF
from pysat.card import CardEnc, EncType
from pysat.examples.rc2 import RC2

import e127_seam_budget as e127


def stream(row):
    with open(JSONL, 'a') as f:
        f.write(json.dumps(row) + '\n')


def build(M, abs_bounds):
    """Replicates e127_seam_budget.solve_budget's encoding verbatim,
    minus the budget cardinality; returns (wcnf, xmap, ai, litA, litB,
    V, bounds).  xmap: indicator var -> (team, u, w)."""
    V = list(range(M + 1, 8 * M + 1))
    n = len(V)
    idx = {v: i for i, v in enumerate(V)}
    offA, top = e127._mk_vars(n, start=1)
    offB, top = e127._mk_vars(n, start=top + 1)
    ai = {}
    for v in V:
        top += 1
        ai[v] = top

    def litT(off):
        def lit(u, w):
            i, j = idx[u], idx[w]
            return off[(i, j)] if i < j else -off[(j, i)]
        return lit

    litA, litB = litT(offA), litT(offB)
    Vs = set(V)
    B0 = [v for v in V if v <= 2 * M]
    B1 = [v for v in V if 2 * M < v <= 4 * M]
    B2 = [v for v in V if v > 4 * M]
    seampairs = [(u, w) for u in B0 for w in B1] + \
                [(u, w) for u in B1 for w in B2]
    cls = []
    xmap = {}
    for team, lit, g in (('A', litA, lambda v: -ai[v]),
                         ('B', litB, lambda v: ai[v])):
        for b in V:
            for d in range(1, min(b - V[0], V[-1] - b) + 1):
                a, c = b - d, b + d
                if a in Vs and c in Vs:
                    gg = [g(a), g(b), g(c)]
                    cls.append(gg + [-lit(a, b), -lit(b, c)])
                    cls.append(gg + [lit(a, b), lit(b, c)])
        for (u, w) in seampairs:
            top += 1
            xmap[top] = (team, u, w)
            cls.append([g(u), g(w), lit(u, w), top])
    for off in (offA, offB):
        for i in range(n):
            for j in range(i + 1, n):
                xij = off[(i, j)]
                for kk in range(j + 1, n):
                    cls.append([-xij, -off[(j, kk)], off[(i, kk)]])
                    cls.append([xij, off[(j, kk)], -off[(i, kk)]])
    tid = top
    bounds = {}
    for bi, (bn, blk) in enumerate((('B0', B0), ('B1', B1), ('B2', B2))):
        base = (math.ceil(len(blk) / 2) if abs_bounds is None
                else abs_bounds[bi])
        bounds[bn] = {'A': base, 'B': base}
        for sign in (1, -1):
            if base <= 0:
                continue
            enc = CardEnc.atleast(lits=[sign * ai[v] for v in blk],
                                  bound=base, top_id=tid,
                                  encoding=EncType.seqcounter)
            tid = max(tid, enc.nv)
            cls += enc.clauses
    wcnf = WCNF()
    for c in cls:
        wcnf.append(c)
    for x in xmap:
        wcnf.append([-x], weight=1)
    return wcnf, xmap, ai, V, bounds


class Deadline(Exception):
    pass


class RC2LB(RC2):
    """RC2 with per-core LB streaming.  Set .lb_meta / .lb_t0 /
    .lb_wall / .lb_xmap / .lb_rows after construction."""

    def process_core(self):
        pairs = None
        try:
            orig = [self.lb_xmap[abs(l)] for l in self.core
                    if abs(l) in self.lb_xmap]
            if len(orig) <= 16:
                pairs = orig
            n_orig = len(orig)
        except Exception:
            n_orig = -1
        csz = len(self.core)
        super().process_core()
        el = round(time.time() - self.lb_t0, 1)
        row = dict(self.lb_meta)
        row.update({'event': 'lb', 'lb_sum': self.cost,
                    'vstar_lb': (self.cost + 1) // 2, 't': el,
                    'core_sz': csz, 'core_orig': n_orig})
        if pairs is not None:
            row['core_pairs'] = pairs
        self.lb_rows.append(row)
        stream(row)
        print(f"  {row['tag']} LB sum>={self.cost} (v*>="
              f"{row['vstar_lb']}) t={el}s core={csz}/{n_orig}",
              flush=True)
        if self.lb_wall and el > self.lb_wall:
            raise Deadline()


def run(M, abs_bounds, tag, wall, solver='g3', adapt=True, exhaust=True,
        minz=True, trim=0):
    meta = {'tag': tag, 'M': M, 'bounds': abs_bounds, 'solver': solver}
    path = os.path.join(DATA, f'e172_{tag}.json')
    t0 = time.time()
    print(f'== {tag}: building (M={M}, bounds='
          f'{abs_bounds or "bal"})', flush=True)
    wcnf, xmap, ai, V, bounds = build(M, abs_bounds)
    print(f'   {len(wcnf.hard)} hard, {len(wcnf.soft)} soft '
          f'[{round(time.time() - t0, 1)}s]', flush=True)
    t0 = time.time()
    rc2 = RC2LB(wcnf, solver=solver, adapt=adapt, exhaust=exhaust,
                minz=minz, trim=trim, verbose=0)
    rc2.lb_meta, rc2.lb_t0, rc2.lb_wall = meta, t0, wall
    rc2.lb_xmap, rc2.lb_rows = xmap, []
    row0 = dict(meta)
    row0.update({'event': 'init', 'lb_sum': rc2.cost,
                 'vstar_lb': (rc2.cost + 1) // 2,
                 't': round(time.time() - t0, 1)})
    rc2.lb_rows.append(row0)
    stream(row0)
    print(f'  {tag} init cost={rc2.cost} (adapt) '
          f"t={row0['t']}s", flush=True)

    def snap(extra=None):
        out = dict(meta)
        out['rows'] = rc2.lb_rows
        if extra:
            out.update(extra)
        with open(path, 'w') as f:
            json.dump(out, f, indent=1)

    try:
        model = rc2.compute()
    except Deadline:
        row = dict(meta)
        row.update({'event': 'partial', 'lb_sum': rc2.cost,
                    'vstar_lb': (rc2.cost + 1) // 2,
                    't': round(time.time() - t0, 1)})
        stream(row)
        rc2.lb_rows.append(row)
        snap()
        print(f'== {tag}: WALL at LB sum>={rc2.cost} '
              f'(v*>={(rc2.cost + 1) // 2})', flush=True)
        return
    finally:
        try:
            snap()
        except Exception:
            pass
    if model is None:
        row = dict(meta)
        row.update({'event': 'hard-unsat', 't': round(time.time() - t0, 1)})
        stream(row)
        snap()
        print(f'== {tag}: HARD PART UNSAT (unexpected!)', flush=True)
        return
    # optimum: audit the model independently (e127 audit)
    mset = set(l for l in model if l > 0)
    colA = [v for v in V if ai[v] in mset]
    colB = [v for v in V if ai[v] not in mset]
    info = {'A': colA, 'B': colB, 'bounds': bounds}
    # positions: recover per-team order by win-count exactly as e127
    n = len(V)
    idx = {v: i for i, v in enumerate(V)}
    offA, top = e127._mk_vars(n, start=1)
    offB, top = e127._mk_vars(n, start=top + 1)

    def litT(off):
        def lit(u, w):
            i, j = idx[u], idx[w]
            return off[(i, j)] if i < j else -off[(j, i)]
        return lit

    posneg = lambda l: (l in mset) if l > 0 else (abs(l) not in mset)
    for team, off, col in (('A', offA, colA), ('B', offB, colB)):
        lit = litT(off)
        wins = {v: 0 for v in col}
        for i, u in enumerate(col):
            for w in col[i + 1:]:
                if posneg(lit(u, w)):
                    wins[u] += 1
                else:
                    wins[w] += 1
        info[f'order{team}'] = sorted(col, key=lambda v: -wins[v])
    errs, anat = e127.audit(M, bounds, 10 ** 9, 10 ** 9, info)
    nA, nB = anat['A']['n_inv'], anat['B']['n_inv']
    row = dict(meta)
    row.update({'event': 'opt', 'opt_sum': rc2.cost,
                'vstar_lb': (rc2.cost + 1) // 2,
                'witness_inv': [nA, nB],
                'vstar_ub': max(nA, nB),
                'audit_errs': errs[:8],
                'sum_matches': (nA + nB == rc2.cost),
                't': round(time.time() - t0, 1)})
    stream(row)
    rc2.lb_rows.append(row)
    snap(extra={'opt_model_anatomy': {t: {k: a[k] for k in
                ('sizes', 'n_inv', 'n_inv_seam1', 'n_inv_seam2',
                 'n_mono')} for t, a in anat.items()},
                'colorA': colA, 'orderA': info['orderA'],
                'orderB': info['orderB']})
    print(f'== {tag}: OPT sum = {rc2.cost} '
          f'(witness {nA}/{nB}; v* in [{(rc2.cost + 1) // 2}, '
          f'{max(nA, nB)}]) errs={len(errs)} '
          f'[{round(time.time() - t0, 1)}s]', flush=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('mode', choices=['bal', 'const'])
    ap.add_argument('--M', type=int, required=True)
    ap.add_argument('--bounds', type=str, default='3,6,12')
    ap.add_argument('--wall', type=float, default=None,
                    help='soft wall (checked between cores); pair with '
                         'an outer `timeout` for a hard kill')
    ap.add_argument('--solver', type=str, default='g3')
    ap.add_argument('--no-adapt', action='store_true')
    ap.add_argument('--no-exhaust', action='store_true')
    ap.add_argument('--no-minz', action='store_true')
    ap.add_argument('--trim', type=int, default=0)
    ap.add_argument('--tag', type=str, default=None)
    args = ap.parse_args()
    os.makedirs(DATA, exist_ok=True)
    if args.mode == 'const':
        bounds = tuple(int(x) for x in args.bounds.split(','))
        tag = args.tag or (f'const{"_".join(map(str, bounds))}'
                           f'_M{args.M}')
    else:
        bounds = None
        tag = args.tag or f'bal_M{args.M}'
    run(args.M, bounds, tag, args.wall, solver=args.solver,
        adapt=not args.no_adapt, exhaust=not args.no_exhaust,
        minz=not args.no_minz, trim=args.trim)


if __name__ == '__main__':
    main()
