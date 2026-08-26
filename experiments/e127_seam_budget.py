"""Erdős #197 — e127: FRONT G2 — quantifying the procrastination cost.

The two-seam coupled core (e120 Part C3, notes/45) assumes DOUBLE
NON-PROCRASTINATION: both teams block-ordered at both seams of the window
B0 u B1 u B2 = (M, 8M].  G2 (STATUS post-merge gap 2) is whether that
hypothesis can be earned.  This experiment replaces the hard seam units by
a BUDGET: each team may carry at most v cross-seam INVERSION PAIRS — a
pair (u, w) with u in B_i, w in B_{i+1}, both in the team, and w placed
before u in the team's order.  v = 0 is the original core.

    SAT at budget v   <=>  some coloring + per-team orders escape with
                           <= v adjacent-seam inversions per team;
    v*(M, bounds)     :=   least v that is SAT.

UNSAT at budgets v' < v* means: every window coloring obeying the bounds
FORCES some team to procrastinate — more than v' seam inversions — i.e.
the hypothesis CANNOT simply fail cheaply; a valid Case-2 partition must
re-descend with volume >= v*(M) at EVERY window (the finite shadow).

Structural fact (proved in notes/47): a monochromatic cross-triple
(u, y, 2y-u), u in B0, y in B1, 2y-u in B2, whose team is intact at both
seams is position-forced increasing; avoiding death requires y before u or
(2y-u) before y — an inverted ADJACENT seam edge — and every seam edge
(u, y) resp. (y, z) lies in EXACTLY ONE cross-triple (z = 2y-u resp.
u = 2y-z determined).  Hence

    v*  >=  min #monochromatic cross-triples over colorings meeting the
            bounds (the sumset relaxation);

the SAT instance additionally charges the in-block/other-AP order theory.
Skip inversions (B0-value after a B2-value) are not counted: one skip
inversion forces an adjacent inversion for EVERY y in B1 ∩ T (transitivity
case split), so at budget v < c1 they cannot occur anyway.

Soundness: complete encoding (full transitivity per team, unguarded; AP
clauses guarded by color; inversion indicators implied one-way by
(color, color, order); CardEnc.atmost over indicators).  A true escape
with <= v inversions sets its indicators honestly, so SAT is complete;
UNSAT needs no extra argument.  Every SAT verdict is re-checked by an
independent scanner (bounds, per-team monotone-AP freedom, recount of
inversions, mono-triple/inversion-edge cross-audit).

Usage:
  e127_seam_budget.py const --M 24 --bounds 3,6,12 [--vmax 24] [--budget S]
  e127_seam_budget.py bal   --M 16 [--vmax 4096] [--budget S]
Artifacts: data/e127_seam_budget.jsonl (streaming), data/e127_{tag}.json.
"""
import argparse
import json
import os
import time

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
DATA = os.path.join(REPO, 'data')
JSONL = os.path.join(DATA, 'e127_seam_budget.jsonl')

from pysat.solvers import Cadical195
from pysat.card import CardEnc, EncType


def stream(row):
    with open(JSONL, 'a') as f:
        f.write(json.dumps(row) + '\n')


def _mk_vars(n, start=1):
    off = {}
    nxt = start
    for i in range(n):
        for j in range(i + 1, n):
            off[(i, j)] = nxt
            nxt += 1
    return off, nxt - 1


def solve_budget(M, abs_bounds, vA, vB, budget=3600.0, solver=Cadical195,
                 majority_B=False):
    """Coupled 3-block window (M, 8M], per-team block lower bounds
    abs_bounds = (c0, c1, c2) (None => exact balance ceil(|blk|/2)),
    NO hard seam units; instead each team T has inversion indicators on
    adjacent seam pairs with sum <= vT.  Returns (verdict, secs, info)."""
    V = list(range(M + 1, 8 * M + 1))
    n = len(V)
    idx = {v: i for i, v in enumerate(V)}
    offA, top = _mk_vars(n, start=1)
    offB, top = _mk_vars(n, start=top + 1)
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
    xvar = {}          # (team, u, w) -> indicator var
    for team, lit, g, vT in (('A', litA, lambda v: -ai[v], vA),
                             ('B', litB, lambda v: ai[v], vB)):
        # guarded AP clauses (both monotone directions), full window
        for b in V:
            for d in range(1, min(b - V[0], V[-1] - b) + 1):
                a, c = b - d, b + d
                if a in Vs and c in Vs:
                    gg = [g(a), g(b), g(c)]
                    cls.append(gg + [-lit(a, b), -lit(b, c)])
                    cls.append(gg + [lit(a, b), lit(b, c)])
        # inversion indicators on adjacent seam pairs
        for (u, w) in seampairs:
            top += 1
            xvar[(team, u, w)] = top
            # u,w both in team and w before u  =>  indicator
            cls.append([g(u), g(w), lit(u, w), top])
    # transitivity, complete, per team
    for off in (offA, offB):
        for i in range(n):
            for j in range(i + 1, n):
                xij = off[(i, j)]
                for kk in range(j + 1, n):
                    cls.append([-xij, -off[(j, kk)], off[(i, kk)]])
                    cls.append([xij, off[(j, kk)], -off[(i, kk)]])
    # cardinality: block bounds per team, inversion budgets per team
    import math
    cards = []
    tid = top
    bounds = {}
    for bi, (bn, blk) in enumerate((('B0', B0), ('B1', B1), ('B2', B2))):
        base = (math.ceil(len(blk) / 2) if abs_bounds is None
                else abs_bounds[bi])
        # sign +1 counts team A (ai true), -1 counts team B
        bndA = base
        bndB = math.ceil(len(blk) / 2) if majority_B else base
        bounds[bn] = {'A': bndA, 'B': bndB}
        for sign, bnd in ((1, bndA), (-1, bndB)):
            if bnd <= 0:
                continue
            enc = CardEnc.atleast(lits=[sign * ai[v] for v in blk],
                                  bound=bnd, top_id=tid,
                                  encoding=EncType.seqcounter)
            tid = max(tid, enc.nv)
            cards += enc.clauses
    for team, vT in (('A', vA), ('B', vB)):
        if vT is None:
            continue                    # unconstrained team
        lits = [xvar[(team, u, w)] for (u, w) in seampairs]
        if vT <= 0:
            cards += [[-l] for l in lits]
        else:
            enc = CardEnc.atmost(lits=lits, bound=vT, top_id=tid,
                                 encoding=EncType.seqcounter)
            tid = max(tid, enc.nv)
            cards += enc.clauses
    t0 = time.time()
    with solver(bootstrap_with=cls) as s:
        for c in cards:
            s.add_clause(c)
        if budget:
            import threading
            timer = threading.Timer(budget, s.interrupt)
            timer.start()
            ok = s.solve_limited(expect_interrupt=True)
            timer.cancel()
        else:
            ok = s.solve()
        el = round(time.time() - t0, 1)
        if ok is None:
            return 'TIMEOUT', el, {'bounds': bounds}
        if not ok:
            return 'UNSAT', el, {'bounds': bounds}
        model = set(l for l in s.get_model() if l > 0)
    colA = [v for v in V if ai[v] in model]
    colB = [v for v in V if ai[v] not in model]
    posneg = lambda l: (l in model) if l > 0 else (abs(l) not in model)
    info = {'A': colA, 'B': colB, 'bounds': bounds}
    for team, lit, col in (('A', litA, colA), ('B', litB, colB)):
        wins = {v: 0 for v in col}
        for i, u in enumerate(col):
            for w in col[i + 1:]:
                if posneg(lit(u, w)):
                    wins[u] += 1
                else:
                    wins[w] += 1
        info[f'order{team}'] = sorted(col, key=lambda v: -wins[v])
    return 'SAT', el, info


def audit(M, bounds, vA, vB, info):
    """Independent check of a SAT witness.  Returns (errs, anatomy)."""
    errs, anatomy = [], {}
    for team in ('A', 'B'):
        col = info[team]
        order = info[f'order{team}']
        vT = vA if team == 'A' else vB
        b0 = [v for v in col if v <= 2 * M]
        b1 = [v for v in col if 2 * M < v <= 4 * M]
        b2 = [v for v in col if v > 4 * M]
        for bn, blk in (('B0', b0), ('B1', b1), ('B2', b2)):
            if len(blk) < bounds[bn][team]:
                errs.append(f'{team}: |{bn}|={len(blk)} < '
                            f'{bounds[bn][team]}')
        p = {v: i for i, v in enumerate(order)}
        vals = sorted(col)
        vs = set(vals)
        for b in vals:                       # monotone APs
            for d in range(1, min(b - vals[0], vals[-1] - b) + 1):
                a, c = b - d, b + d
                if a in vs and c in vs:
                    if p[a] < p[b] < p[c] or p[c] < p[b] < p[a]:
                        errs.append(f'{team}: monotone AP {(a, b, c)}')
        inv = [(u, w) for lo, hi in ((b0, b1), (b1, b2))
               for u in lo for w in hi if p[w] < p[u]]
        if len(inv) > vT:
            errs.append(f'{team}: {len(inv)} inversions > budget {vT}')
        mono = [(u, y, 2 * y - u) for u in b0 for y in b1
                if 2 * y - u in vs and 2 * y - u > 4 * M]
        invset = set(inv)
        unbroken = [t for t in mono
                    if (t[0], t[1]) not in invset
                    and (t[1], t[2]) not in invset]
        if unbroken:
            errs.append(f'{team}: mono cross-triples w/o inversion edge '
                        f'{unbroken[:4]} (theory violation!)')
        skip = [(u, w) for u in b0 for w in b2 if p[w] < p[u]]
        anatomy[team] = {
            'sizes': [len(b0), len(b1), len(b2)],
            'inversions': inv, 'n_inv': len(inv),
            'n_inv_seam1': len([1 for u, w in inv if u <= 2 * M]),
            'n_inv_seam2': len([1 for u, w in inv if u > 2 * M]),
            'n_skip_inv': len(skip),
            'mono_triples': mono, 'n_mono': len(mono)}
    return errs, anatomy


def vstar_scan(M, abs_bounds, vmax, budget, tag, vlist=None, asym=False,
               majority_B=False):
    """UNSAT region is downward closed in v (larger budget = weaker
    constraint), so scan upward for `const`; for `bal` bracket by
    doubling then binary-search."""
    out = {'tag': tag, 'M': M, 'bounds': abs_bounds, 'rows': []}
    path = os.path.join(DATA, f'e127_{tag}.json')

    def q(v):
        vA = None if asym else v
        verdict, el, info = solve_budget(M, abs_bounds, vA, v, budget,
                                         majority_B=majority_B)
        row = {'tag': tag, 'M': M, 'bounds': abs_bounds, 'v': v,
               'verdict': verdict, 'time': el}
        if verdict == 'SAT':
            errs, anat = audit(M, info['bounds'],
                               10**9 if vA is None else vA, v, info)
            if errs:
                row['verdict'] = 'WITNESS-FAIL'
                row['errs'] = errs[:8]
            row['anatomy'] = anat
            row['colorA'] = info['A']
            row['orderA'] = info['orderA']
            row['orderB'] = info['orderB']
        out['rows'].append(row)
        stream(row)
        keep = {k: row[k] for k in row
                if k not in ('colorA', 'orderA', 'orderB')}
        print(f'  {tag} v={v}: {row["verdict"]} [{el}s] '
              + (json.dumps({t: {kk: a[kk] for kk in
                                 ('sizes', 'n_inv', 'n_inv_seam1',
                                  'n_inv_seam2', 'n_mono')}
                             for t, a in row['anatomy'].items()})
                 if 'anatomy' in row else ''), flush=True)
        with open(path, 'w') as f:
            json.dump(out, f, indent=1)
        return row['verdict']

    if vlist is not None:
        for v in vlist:
            q(v)
        sat_vs = [r['v'] for r in out['rows'] if r['verdict'] == 'SAT']
        uns_vs = [r['v'] for r in out['rows'] if r['verdict'] == 'UNSAT']
        out['vstar'] = (f'in ({max(uns_vs, default=-1)}, '
                        f'{min(sat_vs)}]' if sat_vs else
                        f'> {max(uns_vs, default=-1)} (UNSAT side only)')
    elif abs_bounds is not None:
        v = 0
        while v <= vmax:
            if q(v) == 'SAT':
                out['vstar'] = v
                break
            v += 1
        else:
            out['vstar'] = f'> {vmax}'
    else:
        # balance: bracket by doubling, then bisect (TIMEOUT = unknown,
        # keeps bracketing on confirmed verdicts only)
        lo, hi, v = -1, None, 1
        if q(0) == 'SAT':
            out['vstar'] = 0
        else:
            lo = 0
            while v <= vmax:
                r = q(v)
                if r == 'SAT':
                    hi = v
                    break
                if r == 'UNSAT':
                    lo = v
                v *= 2
            while hi is not None and hi - lo > 1:
                mid = (lo + hi) // 2
                r = q(mid)
                if r == 'SAT':
                    hi = mid
                elif r == 'UNSAT':
                    lo = mid
                else:
                    break        # timeout in the gap: report bracket
            out['vstar'] = (f'in ({lo}, {hi}]' if hi is not None
                            else f'> {lo}')
    print(f'== {tag}: v* = {out["vstar"]}', flush=True)
    with open(path, 'w') as f:
        json.dump(out, f, indent=1)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('mode', choices=['const', 'bal', 'asym', 'majb'])
    ap.add_argument('--M', type=int, required=True)
    ap.add_argument('--bounds', type=str, default='3,6,12')
    ap.add_argument('--vmax', type=int, default=None)
    ap.add_argument('--vs', type=str, default=None,
                    help='explicit comma-list of budgets to query')
    ap.add_argument('--budget', type=float, default=3600.0)
    ap.add_argument('--tag', type=str, default=None)
    args = ap.parse_args()
    os.makedirs(DATA, exist_ok=True)
    vlist = ([int(x) for x in args.vs.split(',')] if args.vs else None)
    if args.mode in ('const', 'asym', 'majb'):
        bounds = tuple(int(x) for x in args.bounds.split(','))
        vmax = args.vmax if args.vmax is not None else 24
        pre = args.mode
        tag = (args.tag
               or f'{pre}{"_".join(map(str, bounds))}_M{args.M}')
        vstar_scan(args.M, bounds, vmax, args.budget, tag, vlist,
                   asym=(args.mode in ('asym', 'majb')),
                   majority_B=(args.mode == 'majb'))
    else:
        vmax = args.vmax if args.vmax is not None else 4096
        tag = args.tag or f'bal_M{args.M}'
        vstar_scan(args.M, None, vmax, args.budget, tag, vlist)


if __name__ == '__main__':
    main()
