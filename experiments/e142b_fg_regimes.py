"""e142b: the FG regime map (GAP-FG).

Part G  Full (q, p) grid at M = 48 (attackers x1 = 4M-p, x2 = 4M-q,
        0 <= q < p <= M+15): plain-closure verdict for every pair.
        Hypothesis from the hand gadget: refutes when p > 2q (the
        attacker pair is itself high) with room 5p-6q <= 2M+15;
        stalls otherwise.  Report the exact stall set.

Part S  For every stalled pair: closure after a Lemma-D phase fiat
        on the d=1 ladder of the window (2 branches); if any branch
        survives, escalate to d=1 x d=2 phases (8 branches).
        Report the branch level that kills each.

Run: .venv/bin/python experiments/e142b_fg_regimes.py
Log: data/e142b_fg_regimes.log
"""
import sys
import os

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from e142_fg_closure import close as plain_close
from collections import deque


def close_with_fiat(M, X, fiat_edges):
    """Plain closure seeded with fans + fiat zigzag edges."""
    lo, hi = 4 * M + 1, 6 * M + 15
    V = range(lo, hi + 1)
    fact = {}
    q = deque()

    def add(u, v, why):
        if (u, v) in fact:
            return None
        fact[(u, v)] = why
        q.append((u, v))
        return (u, v) if (v, u) in fact else None

    for x in X:
        for y in V:
            z = 2 * y - x
            if z != y and lo <= z <= hi:
                c = add(z, y, 'unit')
                if c:
                    return True
    for (u, v) in fiat_edges:
        c = add(u, v, 'fiat')
        if c:
            return True
    by_pair = {}
    for b in V:
        for d in range(1, min(b - lo, hi - b) + 1):
            ap = (b - d, b, b + d)
            for pr in ((ap[0], ap[1]), (ap[1], ap[0]),
                       (ap[1], ap[2]), (ap[2], ap[1])):
                by_pair.setdefault(pr, []).append(ap)
    succ, pred = {}, {}
    while q:
        (u, v) = q.popleft()
        succ.setdefault(u, set()).add(v)
        pred.setdefault(v, set()).add(u)
        for w in list(pred.get(u, ())):
            if add(w, v, 't'):
                return True
        for w2 in list(succ.get(v, ())):
            if add(u, w2, 't'):
                return True
        for (a, b, c3) in by_pair.get((u, v), ()):
            conc = None
            if (u, v) == (a, b):
                conc = (c3, b)
            elif (u, v) == (c3, b):
                conc = (a, b)
            elif (u, v) == (b, c3):
                conc = (b, a)
            elif (u, v) == (b, a):
                conc = (b, c3)
            if conc and add(conc[0], conc[1], 'r'):
                return True
    return False


def zig_edges(lo, hi, first, d, leader_first):
    lad = list(range(first, hi + 1, d))
    e0 = 0 if leader_first else 1
    out = []
    for i in range(e0, len(lad), 2):
        if i > 0:
            out.append((lad[i], lad[i - 1]))
        if i + 1 < len(lad):
            out.append((lad[i], lad[i + 1]))
    return out


def partG(M=48):
    print(f'== part G: (q, p) grid at M={M} ==', flush=True)
    stalls = []
    n_ref = 0
    for p in range(1, M + 16):
        for qq in range(0, p):
            X = (4 * M - p, 4 * M - qq)
            cyc, fact = plain_close(M, X, verbose=False)
            if cyc:
                n_ref += 1
            else:
                stalls.append((qq, p))
    print(f'  refuted: {n_ref}; stalled: {len(stalls)}', flush=True)
    # regime check: does "p > 2q and 5p-6q <= 2M+15" predict refutation?
    mispredict = []
    for p in range(1, M + 16):
        for qq in range(0, p):
            pred_ref = (p > 2 * qq) and (5 * p - 6 * qq <= 2 * M + 15)
            actual_ref = (qq, p) not in set(stalls)
            if pred_ref and not actual_ref:
                mispredict.append(('pred-ref-but-stall', qq, p))
    print(f'  gadget-regime mispredictions (should be none): '
          f'{mispredict[:10]}', flush=True)
    print(f'  stalled pairs (q, p) [first 40]: {stalls[:40]}', flush=True)
    # characterize stalls
    if stalls:
        viol = [(qq, p) for (qq, p) in stalls if p > 2 * qq]
        print(f'  stalls with p > 2q (gadget regime but no room or '
              f'other): {viol[:20]}', flush=True)
    return stalls


def partS(M, stalls):
    print(f'== part S: phase-split closure on {len(stalls)} stalls, '
          f'M={M} ==', flush=True)
    lo, hi = 4 * M + 1, 6 * M + 15
    lev1 = lev2 = fail = 0
    failures = []
    for (qq, p) in stalls:
        X = (4 * M - p, 4 * M - qq)
        # level 1: d=1 phase (2 branches)
        ok = all(close_with_fiat(M, X, zig_edges(lo, hi, lo, 1, lf))
                 for lf in (True, False))
        if ok:
            lev1 += 1
            continue
        # level 2: d=1 x d=2(even start) x d=2(odd start) -> 8 branches
        ok = True
        for lf1 in (True, False):
            for lf2 in (True, False):
                for lf3 in (True, False):
                    edges = (zig_edges(lo, hi, lo, 1, lf1)
                             + zig_edges(lo, hi, lo, 2, lf2)
                             + zig_edges(lo, hi, lo + 1, 2, lf3))
                    if not close_with_fiat(M, X, edges):
                        ok = False
                        break
                if not ok:
                    break
            if not ok:
                break
        if ok:
            lev2 += 1
        else:
            fail += 1
            failures.append((qq, p))
    print(f'  killed by d=1 dichotomy: {lev1}; by d=1xd=2 (8 br): '
          f'{lev2}; unresolved: {fail}', flush=True)
    if failures:
        print(f'  unresolved pairs: {failures[:30]}', flush=True)
    return failures


def main():
    stalls = partG(48)
    failures = partS(48, stalls)
    # scale spot-check on the deep adjacent pair
    for M in (64,):
        deep = [(M + 14, M + 15)]
        partS(M, deep)
    print('e142b: DONE', flush=True)


if __name__ == '__main__':
    main()
