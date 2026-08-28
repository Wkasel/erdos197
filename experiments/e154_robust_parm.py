"""e154: RP-ARM(M, d0) — the ROBUST parity arm  (notes/58 SS4).

Instance (orientation 1 WLOG; team-swap covers the other):
  * U pinned:  odds of P0 -> A, evens -> B;
  * P2 coloring FREE, with at most d0 defectors from the alignment
    (aligned: evens -> A, odds -> B; defector = even in B or odd in A);
  * band coloring FREE with >= 2 per team;
  * straddle-freeness for both teams (NOT vacuous once d0 > 0);
  * all six guarded block theories:
      Th0(T): order on the pinned P0 half; in-block APs; (0,0,1)
              units guarded by the completion's band membership;
      Th1(T): order on P1; guarded in-band APs; alpha units (attacker
              parity pins its team); beta units guarded by the
              completion's P2 membership (variable now);
      Th2(T): order on ALL of P2 (Z_T is variable); in-P2 APs guarded
              by 3x membership; (1,2,2) units guarded by attacker in
              Y_T + pair in Z_T; (0,2,2) units (attacker parity pins
              team) guarded by pair in Z_T  — the A5 family, EMPTY at
              d0 = 0 but live for defectors.
  * optional --minY K: add min|Y| >= K both teams (the P-arm scope).

RP-ARM(M, d0) UNSAT  =  "the parity hatch survives d0 Z-defectors":
with the quantitative Lemma PH (notes/58 SS4, Phi < M+7 forces
U-purity and Phi = (M/2) x #defectors), this replaces P-ARM in the
COV-W assembly and absorbs the narrowing L/P overlap.

d0 = 0 must reproduce e150 part_A blocks (0,1,2) UNSAT — the audit
mode --audit additionally solves with block 2 DROPPED and demands
SAT (mirroring e150's blocks {0,1} SAT), so a trivially-UNSAT
encoding bug cannot pass silently.

Run: .venv/bin/python experiments/e154_robust_parm.py M d0
        [--minY K] [--audit] [--blocks 012]
Log: data/e154_rparm.log (+ .json)
"""
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from e147_adv_cegar import core_support
from e150_wholesale import Vars, order_block

from pysat.solvers import Cadical195
from pysat.card import CardEnc, EncType

LOG = os.path.join(HERE, '..', 'data', 'e154_rparm.log')
OUT = os.path.join(HERE, '..', 'data', 'e154_rparm.json')


def log(msg):
    print(msg, flush=True)
    with open(LOG, 'a') as f:
        f.write(msg + '\n')


def build(M, d0, blocks=(0, 1, 2), minY=None):
    P0, P1, P2 = core_support(M)
    U = {'A': [v for v in P0 if v % 2 == 1],
        'B': [v for v in P0 if v % 2 == 0]}
    vp = Vars()
    cA = {v: vp.new() for v in P1 + P2}     # True = team A

    def mem(t, v):
        """Literal: v is in team t (v in P1 u P2)."""
        return cA[v] if t == 'A' else -cA[v]

    def pteam(u):
        """Pinned team of u in P0."""
        return 'A' if u % 2 == 1 else 'B'

    cls = []
    # band bounds >= 2 per team
    for sign in (1, -1):
        enc = CardEnc.atleast(lits=[sign * cA[v] for v in P1], bound=2,
                              top_id=vp.top, encoding=EncType.seqcounter)
        vp.top = max(vp.top, enc.nv)
        cls += enc.clauses
    # optional min|Y| >= K
    if minY:
        for sign in (1, -1):
            enc = CardEnc.atleast(lits=[sign * cA[v] for v in P1],
                                  bound=minY, top_id=vp.top,
                                  encoding=EncType.seqcounter)
            vp.top = max(vp.top, enc.nv)
            cls += enc.clauses
    # defector budget on P2
    dlits = []
    for z in P2:
        d = vp.new()
        dlits.append(d)
        aligned_A = (z % 2 == 0)
        # defect <-> z on the wrong team
        if aligned_A:
            cls.append([-d, -cA[z]])
            cls.append([d, cA[z]])
        else:
            cls.append([-d, cA[z]])
            cls.append([d, -cA[z]])
    if d0 == 0:
        for d in dlits:
            cls.append([-d])
    else:
        enc = CardEnc.atmost(lits=dlits, bound=d0, top_id=vp.top,
                             encoding=EncType.seqcounter)
        vp.top = max(vp.top, enc.nv)
        cls += enc.clauses
    # straddle-freeness (u, y, z = 2y - u), u's team pinned
    for y in P1:
        for u in P0:
            z = 2 * y - u
            if 4 * M + 1 <= z <= 6 * M + 15:
                t = pteam(u)
                cls.append([-mem(t, y), -mem(t, z)])
    n_units = 0
    for t in 'AB':
        if 0 in blocks:
            pts = U[t]
            Us = set(pts)
            lit0, tr = order_block(vp, pts)
            cls += tr
            for b in pts:
                for dd in range(1, min(b - (M + 1), 2 * M - b) + 1):
                    a, c = b - dd, b + dd
                    if a in Us and c in Us:
                        cls.append([-lit0(a, b), -lit0(b, c)])
                        cls.append([lit0(a, b), lit0(b, c)])
                for a in pts:
                    if a >= b:
                        continue
                    c = 2 * b - a
                    if 3 * M - 15 <= c <= 4 * M:   # (0,0,1) unit b < a
                        cls.append([-mem(t, c), lit0(b, a)])
                        n_units += 1
        if 1 in blocks:
            lit1, tr = order_block(vp, P1)
            cls += tr
            lo1, hi1 = 3 * M - 15, 4 * M
            for b in P1:
                for dd in range(1, min(b - lo1, hi1 - b) + 1):
                    a, c = b - dd, b + dd
                    g = [-mem(t, a), -mem(t, b), -mem(t, c)]
                    cls.append(g + [-lit1(a, b), -lit1(b, c)])
                    cls.append(g + [lit1(a, b), lit1(b, c)])
            for b in P1:                            # alpha: c < b
                for c in P1:
                    if c <= b:
                        continue
                    a = 2 * b - c
                    if M + 1 <= a <= 2 * M and pteam(a) == t:
                        cls.append([-mem(t, b), -mem(t, c), lit1(c, b)])
                        n_units += 1
            for a in P1:                            # beta: b < a
                for b in P1:
                    if b <= a:
                        continue
                    c = 2 * b - a
                    if 4 * M + 1 <= c <= 6 * M + 15:
                        cls.append([-mem(t, a), -mem(t, b),
                                    -mem(t, c), lit1(b, a)])
                        n_units += 1
        if 2 in blocks:
            lit2, tr = order_block(vp, P2)
            cls += tr
            lo2, hi2 = 4 * M + 1, 6 * M + 15
            for b in P2:
                for dd in range(1, min(b - lo2, hi2 - b) + 1):
                    a, c = b - dd, b + dd
                    g = [-mem(t, a), -mem(t, b), -mem(t, c)]
                    cls.append(g + [-lit2(a, b), -lit2(b, c)])
                    cls.append(g + [lit2(a, b), lit2(b, c)])
            for b in P2:
                for c in P2:
                    if c <= b:
                        continue
                    a = 2 * b - c
                    if 3 * M - 15 <= a <= 4 * M:    # (1,2,2): c < b
                        cls.append([-mem(t, a), -mem(t, b),
                                    -mem(t, c), lit2(c, b)])
                        n_units += 1
                    elif M + 1 <= a <= 2 * M:       # (0,2,2): c < b
                        if pteam(a) == t:
                            cls.append([-mem(t, b), -mem(t, c),
                                        lit2(c, b)])
                            n_units += 1
    return vp, cls, n_units


def run_one(M, d0, blocks, minY, tag):
    t0 = time.time()
    vp, cls, n_units = build(M, d0, blocks, minY)
    tb = time.time() - t0
    log(f'  RP-ARM({M}, d0={d0}) blocks={blocks} minY={minY}: '
        f'vars={vp.top} clauses={len(cls)} units={n_units} '
        f'[built {tb:.0f}s]')
    t0 = time.time()
    with Cadical195(bootstrap_with=cls) as s:
        ok = s.solve()
    el = time.time() - t0
    v = 'SAT' if ok else 'UNSAT'
    log(f'  RP-ARM({M}, d0={d0}) blocks={blocks} minY={minY}: {v} '
        f'[{el:.1f}s]')
    res = {}
    if os.path.exists(OUT):
        with open(OUT) as f:
            res = json.load(f)
    res[tag] = {'verdict': v, 'secs': round(el, 1),
                'clauses': len(cls)}
    with open(OUT, 'w') as f:
        json.dump(res, f, indent=0)
    return v


def main():
    M = int(sys.argv[1])
    d0 = int(sys.argv[2])
    args = sys.argv[3:]
    minY = None
    audit = '--audit' in args
    blocks = (0, 1, 2)
    if '--minY' in args:
        minY = int(args[args.index('--minY') + 1])
    if '--blocks' in args:
        blocks = tuple(int(c) for c in args[args.index('--blocks') + 1])
    if audit:
        v01 = run_one(M, d0, (0, 1), minY, f'M{M}_d{d0}_b01_audit')
        log(f'  audit blocks(0,1): {v01} '
            f'(expect SAT — else encoding suspicious)')
    tag = f'M{M}_d{d0}_b{"".join(map(str, blocks))}' + \
        (f'_minY{minY}' if minY else '')
    run_one(M, d0, blocks, minY, tag)


if __name__ == '__main__':
    main()
