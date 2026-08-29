"""Erdős #197 — e159: FRONT SEAM-SPLIT — decomposing the budget demand
per seam.

e127 (notes/47/54) prices the TOTAL adjacent-seam inversion count of
each team on the 3-block window (M, 8M].  Its near-critical decision
queries are hopeless (bal@16 v=8: 17000 s TIMEOUT; bal@24 v=16: >22 h),
so v* growth cannot be measured head-on.  The witness anatomy says the
demand CONCENTRATES per seam (the bal@16 v=160 witness pays 85/105
entirely on seam-1; the v=80 witness's team A pays (1, 77) — almost
entirely seam-2), so this experiment splits the budget:

    seam-1 pairs (u, w), u in B0 = (M, 2M],  w in B1 = (2M, 4M]
    seam-2 pairs (y, z), y in B1,            z in B2 = (4M, 8M]

with SEPARATE per-team budgets a1 (seam-1) and a2 (seam-2); 'none'
leaves a seam unpriced (no indicators).  A cell (a1, a2) is the query
"is there an escape with <= a1 seam-1 AND <= a2 seam-2 inversions per
team?".

**Lemma T-FORCE-SPLIT [restriction — verbatim notes/54 Lemma T-FORCE,
which never uses the shape of the priced pair family].**  A valid pair
(A, B) meeting the block bounds at anchor M with per-seam counts
Inv1_T(M) <= a1 and Inv2_T(M) <= a2 for both teams induces a model.
Hence UNSAT(M; a1, a2) => every valid pair meeting the bounds has some
team T with Inv1_T(M) > a1 OR Inv2_T(M) > a2.  Unpriced seams impose
nothing, so UNSAT(M; a1, none) is the unconditional per-seam floor
    max_T Inv1_T(M) > a1        (regardless of seam-2 spending),
and dually for (none, a2).

Relation to the joint budget: a model at (a1, a2) is a model at joint
v = a1 + a2, and a joint-v model with per-seam split (s1, s2) is a
model at (s1, s2).  So UNSAT_joint(v) transfers to every cell with
a1 + a2 <= v, and the SAT region is upward closed per coordinate
(Lemma M(a) verbatim).  The object mapped here is the STAIRCASE
frontier in the (a1, a2) plane; cells with a1 + a2 >> v* that are
easily UNSAT are per-seam demand certificates the joint instrument
cannot see (and their UNSATs are expected FAR from the joint
criticality wall — the point of the front).

Soundness: complete encoding exactly as e127 (full transitivity per
team; AP clauses guarded by color, both monotone directions; inversion
indicators implied one-way by (color, color, order); seqcounter cards).
Every SAT verdict re-audited independently (bounds, per-team
monotone-AP freedom, PER-SEAM inversion recounts, mono-H-triple /
inversion-edge cross-audit).

Usage:
  e159_seam_split.py bal   --M 16 --cells "n:0,0:n,4:n,2:8" [--budget 600]
  e159_seam_split.py const --M 24 --bounds 3,6,12 --cells "0:n,n:0"
Cell syntax: "a1:a2" symmetric over teams ('n'/'none' = unpriced), or
"a1A:a2A:a1B:a2B" for per-team asymmetric budgets.
Artifacts: data/e159_seam_split.jsonl (streaming), data/e159_{tag}.json.
"""
import argparse
import json
import math
import os
import time

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
DATA = os.path.join(REPO, 'data')
JSONL = os.path.join(DATA, 'e159_seam_split.jsonl')

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


def solve_split(M, abs_bounds, budA, budB, budget=600.0, solver=Cadical195):
    """Coupled 3-block window (M, 8M], per-team block lower bounds
    abs_bounds = (c0, c1, c2) (None => exact balance ceil(|blk|/2)),
    budT = (a1, a2): per-seam inversion budgets for team T (None
    entries = that seam unpriced for that team).
    Returns (verdict, secs, info)."""
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
    seam1 = [(u, w) for u in B0 for w in B1]
    seam2 = [(u, w) for u in B1 for w in B2]
    cls = []
    xvar = {}          # (team, seam_idx, u, w) -> indicator var
    for team, lit, g, bud in (('A', litA, lambda v: -ai[v], budA),
                              ('B', litB, lambda v: ai[v], budB)):
        # guarded AP clauses (both monotone directions), full window
        for b in V:
            for d in range(1, min(b - V[0], V[-1] - b) + 1):
                a, c = b - d, b + d
                if a in Vs and c in Vs:
                    gg = [g(a), g(b), g(c)]
                    cls.append(gg + [-lit(a, b), -lit(b, c)])
                    cls.append(gg + [lit(a, b), lit(b, c)])
        # inversion indicators on the PRICED seams only
        for si, pairs in ((1, seam1), (2, seam2)):
            if bud[si - 1] is None:
                continue
            for (u, w) in pairs:
                top += 1
                xvar[(team, si, u, w)] = top
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
    # cardinality: block bounds per team, per-seam budgets per team
    cards = []
    tid = top
    bounds = {}
    for bi, (bn, blk) in enumerate((('B0', B0), ('B1', B1), ('B2', B2))):
        base = (math.ceil(len(blk) / 2) if abs_bounds is None
                else abs_bounds[bi])
        bounds[bn] = {'A': base, 'B': base}
        for sign, bnd in ((1, base), (-1, base)):
            if bnd <= 0:
                continue
            enc = CardEnc.atleast(lits=[sign * ai[v] for v in blk],
                                  bound=bnd, top_id=tid,
                                  encoding=EncType.seqcounter)
            tid = max(tid, enc.nv)
            cards += enc.clauses
    for team, bud in (('A', budA), ('B', budB)):
        for si, pairs in ((1, seam1), (2, seam2)):
            aT = bud[si - 1]
            if aT is None:
                continue
            lits = [xvar[(team, si, u, w)] for (u, w) in pairs]
            if aT <= 0:
                cards += [[-l] for l in lits]
            else:
                enc = CardEnc.atmost(lits=lits, bound=aT, top_id=tid,
                                     encoding=EncType.seqcounter)
                tid = max(tid, enc.nv)
                cards += enc.clauses
    t0 = time.time()
    with solver(bootstrap_with=cls) as s:
        for c in cards:
            s.add_clause(c)
        ok = s.solve()
        el = round(time.time() - t0, 1)
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


def _worker(kw, outq):
    outq.put(solve_split(**kw))


def solve_split_sub(kw, budget):
    """Subprocess wrapper with hard wall-clock kill (pysat holds the
    GIL during solve)."""
    import multiprocessing as mp
    import queue as _q
    ctx = mp.get_context('fork')
    outq = ctx.Queue()
    p = ctx.Process(target=_worker, args=(kw, outq))
    t0 = time.time()
    p.start()
    try:
        verdict, el, info = outq.get(timeout=budget)
        p.join()
        return verdict, el, info
    except _q.Empty:
        p.terminate()
        p.join()
        return 'TIMEOUT', round(time.time() - t0, 1), {'bounds': None}


def audit(M, bounds, budA, budB, info):
    """Independent check of a SAT witness.  Returns (errs, anatomy)."""
    errs, anatomy = [], {}
    for team, bud in (('A', budA), ('B', budB)):
        col = info[team]
        order = info[f'order{team}']
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
        inv1 = [(u, w) for u in b0 for w in b1 if p[w] < p[u]]
        inv2 = [(u, w) for u in b1 for w in b2 if p[w] < p[u]]
        for si, inv in ((1, inv1), (2, inv2)):
            aT = bud[si - 1]
            if aT is not None and len(inv) > aT:
                errs.append(f'{team}: seam-{si} {len(inv)} inversions '
                            f'> budget {aT}')
        mono = [(u, y, 2 * y - u) for u in b0 for y in b1
                if 2 * y - u in vs and 2 * y - u > 4 * M]
        invset = set(inv1) | set(inv2)
        unbroken = [t for t in mono
                    if (t[0], t[1]) not in invset
                    and (t[1], t[2]) not in invset]
        if unbroken:
            errs.append(f'{team}: mono cross-triples w/o inversion edge '
                        f'{unbroken[:4]} (theory violation!)')
        skip = [(u, w) for u in b0 for w in b2 if p[w] < p[u]]
        anatomy[team] = {
            'sizes': [len(b0), len(b1), len(b2)],
            'n_inv_seam1': len(inv1), 'n_inv_seam2': len(inv2),
            'n_inv': len(inv1) + len(inv2),
            'inversions': inv1 + inv2,
            'n_skip_inv': len(skip),
            'mono_triples': mono, 'n_mono': len(mono)}
    return errs, anatomy


def parse_cell(spec):
    """'a1:a2' (symmetric) or 'a1A:a2A:a1B:a2B'; 'n'/'none' = None."""
    def tok(x):
        return None if x in ('n', 'none') else int(x)
    parts = [tok(x) for x in spec.strip().split(':')]
    if len(parts) == 2:
        return (parts[0], parts[1]), (parts[0], parts[1])
    if len(parts) == 4:
        return (parts[0], parts[1]), (parts[2], parts[3])
    raise ValueError(f'bad cell spec {spec!r}')


def fmt_bud(bud):
    return ':'.join('n' if x is None else str(x) for x in bud)


def run_cells(M, abs_bounds, cells, budget, tag):
    out = {'tag': tag, 'M': M, 'bounds': abs_bounds, 'rows': []}
    path = os.path.join(DATA, f'e159_{tag}.json')
    for spec in cells:
        budA, budB = parse_cell(spec)
        cell = (fmt_bud(budA) if budA == budB
                else fmt_bud(budA) + '/' + fmt_bud(budB))
        verdict, el, info = solve_split_sub(
            dict(M=M, abs_bounds=abs_bounds, budA=budA, budB=budB),
            budget)
        row = {'tag': tag, 'M': M, 'bounds': abs_bounds, 'cell': cell,
               'a1': budA[0], 'a2': budA[1], 'verdict': verdict,
               'time': el}
        if verdict == 'SAT':
            errs, anat = audit(M, info['bounds'], budA, budB, info)
            if errs:
                row['verdict'] = 'WITNESS-FAIL'
                row['errs'] = errs[:8]
            row['anatomy'] = anat
            row['colorA'] = info['A']
            row['orderA'] = info['orderA']
            row['orderB'] = info['orderB']
        out['rows'].append(row)
        stream(row)
        print(f'  {tag} ({cell}): {row["verdict"]} [{el}s] '
              + (json.dumps({t: {kk: a[kk] for kk in
                                 ('sizes', 'n_inv_seam1', 'n_inv_seam2',
                                  'n_mono')}
                             for t, a in row['anatomy'].items()})
                 if 'anatomy' in row else ''), flush=True)
        with open(path, 'w') as f:
            json.dump(out, f, indent=1)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('mode', choices=['const', 'bal'])
    ap.add_argument('--M', type=int, required=True)
    ap.add_argument('--bounds', type=str, default='3,6,12')
    ap.add_argument('--cells', type=str, required=True,
                    help='comma-list of cells a1:a2 (n = unpriced)')
    ap.add_argument('--budget', type=float, default=600.0)
    ap.add_argument('--tag', type=str, default=None)
    args = ap.parse_args()
    os.makedirs(DATA, exist_ok=True)
    cells = args.cells.split(',')
    if args.mode == 'const':
        bounds = tuple(int(x) for x in args.bounds.split(','))
        tag = args.tag or f'const{"_".join(map(str, bounds))}_M{args.M}'
        run_cells(args.M, bounds, cells, args.budget, tag)
    else:
        tag = args.tag or f'bal_M{args.M}'
        run_cells(args.M, None, cells, args.budget, tag)


if __name__ == '__main__':
    main()
