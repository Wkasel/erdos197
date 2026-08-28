#!/usr/bin/env python3
"""e154b: split-certificate status for every pair in D(48) (the 75
UNSAT closure-stalls = non-resonant E1xE1 attacker pairs).

Levels:
  L1: d=1 zigzag phase dichotomy (2 branches; Lemma D')
  L2: d=1 x d=2(even) x d=2(odd) phase fiats (8 branches)
  L3: adaptive single totality split on a candidate list (2 branches)
  L4: adaptive double totality split, candidates near the window
      bottom (4 branches)
Each branch must die by T/RL/RT closure.
"""
import json, time
from collections import deque

def closure_seeded(M, p, q, extra):
    N = 2*M + 15
    proof = set()
    dq = deque()
    def add(u, v):
        if u == v or (u, v) in proof:
            return False
        if (v, u) in proof:
            proof.add((u, v))
            return True
        proof.add((u, v)); dq.append((u, v))
        return False
    for r in (p, q):
        a = 1
        while 2*a + r <= N:
            if add(2*a + r, a): return True
            a += 1
    for (u, v) in extra:
        if add(u, v): return True
    while dq:
        u, v = dq.popleft()
        w = 2*u - v
        if 1 <= w <= N and add(u, w): return True
        w = 2*v - u
        if 1 <= w <= N and add(w, v): return True
        for (x, y) in list(proof):
            if y == u and add(x, v): return True
            if x == v and add(u, y): return True
    return False

def zig_edges(lo, hi, first, d, leader_first):
    """Alternating zigzag phase on the d-ladder starting at `first`:
    rung pairs (x, x+d); orientation alternates along the ladder."""
    edges = []
    x = first
    k = 0
    while x + d <= hi:
        asc = (k % 2 == 0) == leader_first
        edges.append((x, x + d) if asc else ((x + d), x))
        x += d
        k += 1
    return edges

def main():
    M = 48
    N = 2*M + 15
    D = json.load(open('data/e154_deep_classify.json'))['D']
    log = []
    def p_(*a):
        s = ' '.join(str(x) for x in a); print(s, flush=True); log.append(s)
    p_(f'== e154b: split certificates for |D(48)| = {len(D)} ==')
    t0 = time.time()
    status = {}
    lo, hi = 1, N
    for (q, p) in [tuple(x) for x in D]:
        # L1
        if all(closure_seeded(M, p, q, zig_edges(lo, hi, lo, 1, lf))
               for lf in (True, False)):
            status[(q, p)] = 'L1'
            continue
        # L2
        ok = all(closure_seeded(M, p, q,
                                zig_edges(lo, hi, lo, 1, a)
                                + zig_edges(lo, hi, lo, 2, b)
                                + zig_edges(lo, hi, lo + 1, 2, c))
                 for a in (0, 1) for b in (0, 1) for c in (0, 1))
        if ok:
            status[(q, p)] = 'L2'
            continue
        # L3: adaptive single totality split, candidate pairs
        cands = [(x, y) for x in range(1, 9) for y in range(x + 1, 17)]
        done = False
        for (x, y) in cands:
            if closure_seeded(M, p, q, [(x, y)]) and \
               closure_seeded(M, p, q, [(y, x)]):
                status[(q, p)] = f'L3({x},{y})'
                done = True
                break
        if done:
            continue
        status[(q, p)] = 'OPEN'
    from collections import Counter
    hist = Counter(v.split('(')[0] for v in status.values())
    p_('certificate levels:', dict(hist))
    open_pairs = sorted(k for k, v in status.items() if v == 'OPEN')
    p_(f'OPEN (no certificate found): {len(open_pairs)}')
    p_('open pairs:', open_pairs)
    p_('per-pair:', {str(k): v for k, v in sorted(status.items())})
    p_(f'total {time.time()-t0:.1f}s')
    with open('data/e154b_deep_splits.json', 'w') as f:
        json.dump({'status': {str(k): v for k, v in status.items()},
                   'open': open_pairs}, f)
    with open('data/e154b_deep_splits.log', 'w') as f:
        f.write('\n'.join(log) + '\n')

if __name__ == '__main__':
    main()
