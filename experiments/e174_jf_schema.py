"""Erdős #197 — e174: FRONT J/F-SCHEMA machine companion (notes/71).

Instruments:
  fmass    — f(M): min over balanced colorings of (M/2, 8M] with
             μ_dn = 0 (no mono H_dn triple, either team) and
             LOW-IMPURE (some team's (Bm1 ∪ B0) has both parities)
             of max_T (μ_up(T) + μ_skip(T)).  Pure counting layer —
             NO order variables.  The J-schema's engine: L-PREFIX
             charges this mass unit-for-unit in s2, so
             (v, 0) UNSAT for v < f(M) on the low-impure branch.
             Scan m upward; dump the extremal witness at first SAT.
  ftot     — f_F(M): same but minimizing max_T (μ_dn + μ_up +
             μ_skip) with μ_dn free (≥ 0) — the F-cell variant
             (factor-2 charging: F(M; v) UNSAT for 2v < f_F(M) on
             the impure branch).
  interval — K(n, k; v): the budgeted Lemma K.  Interval [1..n],
             low [1..k] wholesale before the rest, ≤ v inverted
             (low, high) pairs, monotone-3AP-free order.
  lowprobe — zero-sumset structure probes at scale M (are the two
             parity low-schedules forced? enumerate).

Records: data/e174_jf.jsonl (+ stdout).
"""
import argparse
import json
import os
import time

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
DATA = os.path.join(REPO, 'data')
JSONL = os.path.join(DATA, 'e174_jf.jsonl')

from pysat.solvers import Cadical195
from pysat.card import CardEnc, EncType


def stream(row):
    os.makedirs(DATA, exist_ok=True)
    with open(JSONL, 'a') as f:
        f.write(json.dumps(row) + '\n')


def blkf(M):
    def blk(v):
        if v <= M:
            return -1
        if v <= 2 * M:
            return 0
        if v <= 4 * M:
            return 1
        return 2
    return blk


def mass_base(M, hard_mu_dn_zero):
    """Common coloring-layer CNF: balance + low-impurity + triple
    indicators.  Returns (cls, tA, tB, nxt, ai, V) where tA/tB are
    the per-team mono-triple indicator lists (charged families)."""
    V = list(range(M // 2 + 1, 8 * M + 1))
    blk = blkf(M)
    ai = {v: i + 1 for i, v in enumerate(V)}
    nxt = len(V)
    cls = []
    tA, tB = [], []
    for u in V:
        for y in V:
            if y <= u:
                continue
            z = 2 * y - u
            if z > 8 * M:
                continue
            p = (blk(u), blk(y), blk(z))
            if p == (-1, 0, 1):
                if hard_mu_dn_zero:
                    cls.append([-ai[u], -ai[y], -ai[z]])
                    cls.append([ai[u], ai[y], ai[z]])
                else:
                    nxt += 1
                    tA.append(nxt)
                    cls.append([-ai[u], -ai[y], -ai[z], nxt])
                    nxt += 1
                    tB.append(nxt)
                    cls.append([ai[u], ai[y], ai[z], nxt])
            elif p in ((0, 1, 2), (-1, 1, 2)):
                nxt += 1
                tA.append(nxt)
                cls.append([-ai[u], -ai[y], -ai[z], nxt])
                nxt += 1
                tB.append(nxt)
                cls.append([ai[u], ai[y], ai[z], nxt])
    blocks = {}
    for v in V:
        blocks.setdefault(blk(v), []).append(v)
    for b, vs in blocks.items():
        half = len(vs) // 2
        for sign in (1, -1):
            enc = CardEnc.atleast(lits=[sign * ai[v] for v in vs],
                                  bound=half, top_id=nxt,
                                  encoding=EncType.seqcounter)
            nxt = max(nxt, enc.nv)
            cls += enc.clauses
    low = [v for v in V if blk(v) < 1]
    pO, pE = nxt + 1, nxt + 2
    nxt += 2
    cls.append([-pO] + [ai[v] for v in low if v % 2 == 1])
    cls.append([-pE] + [ai[v] for v in low if v % 2 == 0])
    cls.append([pO])
    cls.append([pE])
    return cls, tA, tB, nxt, ai, V


def run_mass(M, mode, mmax, mstart=0):
    tag = f'{mode}_M{M}'
    cls, tA, tB, nxt, ai, V = mass_base(M, mode == 'fmass')
    blk = blkf(M)
    for m in range(mstart, mmax + 1):
        c2 = list(cls)
        tid = nxt
        for lits in (tA, tB):
            if m == 0:
                c2 += [[-l] for l in lits]
            else:
                enc = CardEnc.atmost(lits=lits, bound=m, top_id=tid,
                                     encoding=EncType.seqcounter)
                tid = max(tid, enc.nv)
                c2 += enc.clauses
        t0 = time.time()
        with Cadical195(bootstrap_with=c2) as s:
            ok = s.solve()
            model = set(l for l in s.get_model() if l > 0) if ok else None
        el = round(time.time() - t0, 1)
        print(f'{tag} m={m}: {"SAT" if ok else "UNSAT"} [{el}s]',
              flush=True)
        stream({'tag': tag, 'm': m,
                'verdict': 'SAT' if ok else 'UNSAT', 'time': el})
        if ok:
            colA = sorted(v for v in V if ai[v] in model)
            anat = {}
            for nm, b in (('Bm1', -1), ('B0', 0), ('B1', 1), ('B2', 2)):
                anat[nm] = [v for v in colA if blk(v) == b]
            stream({'tag': tag, 'witness_at': m, 'colorA': colA,
                    'blocksA': anat})
            print(f'  witness A: ' + json.dumps(anat), flush=True)
            return m
    return None


def run_interval(n, k, vlist):
    off = {}
    nxt = 1
    for i in range(1, n + 1):
        for j in range(i + 1, n + 1):
            off[(i, j)] = nxt
            nxt += 1

    def lit(u, w):
        return off[(u, w)] if u < w else -off[(w, u)]
    base = []
    for b in range(1, n + 1):
        for d in range(1, n):
            a, c = b - d, b + d
            if a >= 1 and c <= n:
                base.append([-lit(a, b), -lit(b, c)])
                base.append([lit(a, b), lit(b, c)])
    for i in range(1, n + 1):
        for j in range(i + 1, n + 1):
            for kk in range(j + 1, n + 1):
                base.append([-off[(i, j)], -off[(j, kk)], off[(i, kk)]])
                base.append([off[(i, j)], off[(j, kk)], -off[(i, kk)]])
    top = nxt - 1
    xl = []
    pre = []
    for u in range(1, k + 1):
        for w in range(k + 1, n + 1):
            top += 1
            pre.append([lit(u, w), top])
            xl.append(top)
    for v in vlist:
        cls = base + pre
        if v <= 0:
            cls = cls + [[-l] for l in xl]
        else:
            enc = CardEnc.atmost(lits=xl, bound=v, top_id=top,
                                 encoding=EncType.seqcounter)
            cls = cls + enc.clauses
        t0 = time.time()
        with Cadical195(bootstrap_with=cls) as s:
            ok = s.solve()
        el = round(time.time() - t0, 1)
        print(f'K({n},{k}) v={v}: {"SAT" if ok else "UNSAT"} [{el}s]',
              flush=True)
        stream({'tag': f'interval_{n}_{k}', 'v': v,
                'verdict': 'SAT' if ok else 'UNSAT', 'time': el})


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('cmd', choices=['fmass', 'ftot', 'interval'])
    ap.add_argument('--M', type=str, default='8')
    ap.add_argument('--mmax', type=int, default=60)
    ap.add_argument('--mstart', type=int, default=0)
    ap.add_argument('--n', type=int, default=24)
    ap.add_argument('--k', type=int, default=8)
    ap.add_argument('--v', type=str, default='0')
    args = ap.parse_args()
    if args.cmd in ('fmass', 'ftot'):
        for Ms in args.M.split(','):
            r = run_mass(int(Ms), args.cmd, args.mmax, args.mstart)
            print(f'==> {args.cmd}({Ms}) = {r}', flush=True)
    else:
        run_interval(args.n, args.k,
                     [int(x) for x in args.v.split(',')])


if __name__ == '__main__':
    main()
