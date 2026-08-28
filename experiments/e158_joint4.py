"""Erdős #197 — e158: GAP-JOINT — the 4-block DOWNWARD gadget.

Extends the e127 budget instance one block DOWN: values (M/2, 8M],
blocks Bm1 = (M/2, M], B0 = (M, 2M], B1 = (2M, 4M], B2 = (4M, 8M].
Two overlapping 3-block windows share the material:

    upper window W(M)   = (M, 8M]    seams: s1 = B0->B1, s2 = B1->B2
    lower window W(M/2) = (M/2, 4M]  seams: s0 = Bm1->B0, s1 = B0->B1

Per-team budgets: vup on Inv(anchor M) = #inverted s1+s2 pairs,
vdn on Inv(anchor M/2) = #inverted s0+s1 pairs (s1 counts in BOTH).
Either budget may be absent (None): the corresponding anchor is
unpriced, its seam indicators are not created.

Soundness (T-FORCE-4, restriction — same proof as notes/54 Lemma
T-FORCE): a valid pair whose teams meet the four block lower bounds
at anchor M with Inv_T(M) <= vup and Inv_T(M/2) <= vdn for both T
induces a model.  Hence UNSAT  ==>  every valid pair meeting the
bounds has some team exceeding a budget at one of the two anchors.

Cells this instrument distinguishes (notes/62):
  C0 (vup=None, vdn=None): encoding sanity — finite theory is SAT.
  C1 (vup=v,   vdn=None): does the mere presence of the dense block
      BELOW the window raise the anchor-M price past the 3-block
      v*(M)?  (e130 check 3: escapes park ~2x exposure mass below.)
  C2 (vup=None, vdn=w): the anchor-M/2 price with the material of B2
      present but the upper anchor unpriced (baseline for C3).
  C3 (vup=v*,  vdn=w): THE PUMP — does paying the anchor-M price
      force strictly more at anchor M/2 than C2's baseline?

Encoding: complete (full transitivity per team; guarded APs both
monotone directions over the whole 4-block range; indicators one-way;
seqcounter cardinality).  Every SAT verdict independently re-audited
(bounds, per-team monotone-AP freedom, per-seam inversion recounts at
both anchors, mono cross-triple/inversion-edge cross-audit for BOTH
windows' H-families).

Usage:
  e158_joint4.py bal   --M 16 --vup 6 --vdn none [--budget S] [--tag T]
  e158_joint4.py const --M 24 --bounds 2,3,6,12 --vup 4 --vdn 2
Artifacts: data/e158_joint4.jsonl (streaming), data/e158_{tag}.json.
"""
import argparse
import json
import math
import os
import time

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
DATA = os.path.join(REPO, 'data')
JSONL = os.path.join(DATA, 'e158_joint4.jsonl')

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


def blocks_of(M):
    assert M % 2 == 0
    V = list(range(M // 2 + 1, 8 * M + 1))
    Bm1 = [v for v in V if v <= M]
    B0 = [v for v in V if M < v <= 2 * M]
    B1 = [v for v in V if 2 * M < v <= 4 * M]
    B2 = [v for v in V if v > 4 * M]
    return V, (Bm1, B0, B1, B2)


def solve_joint(M, abs_bounds, vup, vdn, budget=3600.0,
                solver=Cadical195):
    """abs_bounds = (c_m1, c0, c1, c2) lower bounds per team per block,
    or None => exact balance (ceil(|blk|/2) both teams; block sizes are
    even for M % 4 == 0).  vup / vdn: int or None (anchor unpriced).
    Returns (verdict, secs, info)."""
    V, (Bm1, B0, B1, B2) = blocks_of(M)
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
    s0 = [(u, w) for u in Bm1 for w in B0]
    s1 = [(u, w) for u in B0 for w in B1]
    s2 = [(u, w) for u in B1 for w in B2]
    need = set()
    if vup is not None:
        need |= {'s1', 's2'}
    if vdn is not None:
        need |= {'s0', 's1'}
    seams = {'s0': s0, 's1': s1, 's2': s2}
    cls = []
    xvar = {}          # (team, seam, u, w) -> indicator var
    for team, lit, g in (('A', litA, lambda v: -ai[v]),
                         ('B', litB, lambda v: ai[v])):
        # guarded AP clauses (both monotone directions), full range
        for b in V:
            for d in range(1, min(b - V[0], V[-1] - b) + 1):
                a, c = b - d, b + d
                if a in Vs and c in Vs:
                    gg = [g(a), g(b), g(c)]
                    cls.append(gg + [-lit(a, b), -lit(b, c)])
                    cls.append(gg + [lit(a, b), lit(b, c)])
        # inversion indicators on the needed seams
        for sn in sorted(need):
            for (u, w) in seams[sn]:
                top += 1
                xvar[(team, sn, u, w)] = top
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
    # cardinality: block bounds per team, two anchor budgets per team
    cards = []
    tid = top
    bounds = {}
    blks = (('Bm1', Bm1), ('B0', B0), ('B1', B1), ('B2', B2))
    for bi, (bn, blk) in enumerate(blks):
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
            cards += enc.clauses
    for team in ('A', 'B'):
        for vT, sns in ((vup, ('s1', 's2')), (vdn, ('s0', 's1'))):
            if vT is None:
                continue
            lits = [xvar[(team, sn, u, w)] for sn in sns
                    for (u, w) in seams[sn]]
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
    outq.put(solve_joint(**kw))


def solve_joint_sub(kw, budget):
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


def audit(M, bounds, vup, vdn, info):
    """Independent check of a SAT witness.  Returns (errs, anatomy)."""
    V, (Bm1, B0, B1, B2) = blocks_of(M)
    errs, anatomy = [], {}
    for team in ('A', 'B'):
        col = info[team]
        order = info[f'order{team}']
        cset = set(col)
        bm1 = [v for v in col if v in set(Bm1)]
        b0 = [v for v in col if v in set(B0)]
        b1 = [v for v in col if v in set(B1)]
        b2 = [v for v in col if v in set(B2)]
        for bn, blk in (('Bm1', bm1), ('B0', b0), ('B1', b1),
                        ('B2', b2)):
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
        inv = {}
        for sn, lo, hi in (('s0', bm1, b0), ('s1', b0, b1),
                           ('s2', b1, b2)):
            inv[sn] = [(u, w) for u in lo for w in hi if p[w] < p[u]]
        n_up = len(inv['s1']) + len(inv['s2'])
        n_dn = len(inv['s0']) + len(inv['s1'])
        if vup is not None and n_up > vup:
            errs.append(f'{team}: up-inversions {n_up} > {vup}')
        if vdn is not None and n_dn > vdn:
            errs.append(f'{team}: dn-inversions {n_dn} > {vdn}')
        # mono cross-triples of both windows must carry an inverted edge
        for wn, (lo, mid, hicap) in (
                ('H_up', (b0, b1, 8 * M)),
                ('H_dn', (bm1, b0, 4 * M))):
            mono = [(u, y, 2 * y - u) for u in lo for y in mid
                    if 2 * y - u in vs and 2 * y - u <= hicap
                    and 2 * y - u > (2 * M if wn == 'H_up' else M)]
            # keep only triples whose top lands one block up
            mono = [t for t in mono
                    if (t[2] > 4 * M if wn == 'H_up' else
                        2 * M < t[2] <= 4 * M)]
            unbroken = [t for t in mono
                        if not (p[t[1]] < p[t[0]] or p[t[2]] < p[t[1]])]
            if unbroken:
                errs.append(f'{team}: {wn} mono triple w/o inversion '
                            f'edge {unbroken[:4]} (theory violation!)')
            anatomy.setdefault(team, {})[f'n_{wn}'] = len(mono)
        skip_up = [(u, w) for u in b0 for w in b2 if p[w] < p[u]]
        skip_dn = [(u, w) for u in bm1 for w in b1 if p[w] < p[u]]
        anatomy[team].update({
            'sizes': [len(bm1), len(b0), len(b1), len(b2)],
            'n_s0': len(inv['s0']), 'n_s1': len(inv['s1']),
            'n_s2': len(inv['s2']),
            'n_up': n_up, 'n_dn': n_dn,
            'n_skip_up': len(skip_up), 'n_skip_dn': len(skip_dn),
            'inv_s0': inv['s0'], 'inv_s1': inv['s1'],
            'inv_s2': inv['s2']})
    return errs, anatomy


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('mode', choices=['const', 'bal'])
    ap.add_argument('--M', type=int, required=True)
    ap.add_argument('--bounds', type=str, default='2,3,6,12')
    ap.add_argument('--vup', type=str, default='none')
    ap.add_argument('--vdn', type=str, default='none')
    ap.add_argument('--budget', type=float, default=3600.0)
    ap.add_argument('--tag', type=str, default=None)
    args = ap.parse_args()
    os.makedirs(DATA, exist_ok=True)
    vup = None if args.vup.lower() == 'none' else int(args.vup)
    vdn = None if args.vdn.lower() == 'none' else int(args.vdn)
    abs_bounds = (None if args.mode == 'bal'
                  else tuple(int(x) for x in args.bounds.split(',')))
    tag = args.tag or (f'{args.mode}_M{args.M}_up{args.vup}_'
                       f'dn{args.vdn}')
    verdict, el, info = solve_joint_sub(
        dict(M=args.M, abs_bounds=abs_bounds, vup=vup, vdn=vdn),
        args.budget)
    row = {'tag': tag, 'M': args.M, 'mode': args.mode,
           'bounds': abs_bounds, 'vup': vup, 'vdn': vdn,
           'verdict': verdict, 'time': el}
    if verdict == 'SAT':
        errs, anat = audit(args.M, info['bounds'], vup, vdn, info)
        if errs:
            row['verdict'] = 'WITNESS-FAIL'
            row['errs'] = errs[:8]
        row['anatomy'] = anat
        row['colorA'] = info['A']
        row['orderA'] = info['orderA']
        row['orderB'] = info['orderB']
    stream(row)
    slim = {t: {k: a[k] for k in ('sizes', 'n_s0', 'n_s1', 'n_s2',
                                  'n_up', 'n_dn', 'n_H_up', 'n_H_dn')}
            for t, a in row.get('anatomy', {}).items()}
    print(f'{tag}: {row["verdict"]} [{el}s] '
          + (json.dumps(slim) if slim else ''), flush=True)
    with open(os.path.join(DATA, f'e158_{tag}.json'), 'w') as f:
        json.dump(row, f, indent=1)


if __name__ == '__main__':
    main()
