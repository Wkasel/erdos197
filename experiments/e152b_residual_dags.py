#!/usr/bin/env python3
"""e152b: provenance-tracked closure derivations for MC-residual pairs.
Extract minimal derivation DAGs for representative (q,p) outside the
mirror-cycle schema, to identify the missing uniform families.
"""
import sys
from collections import deque

def derive(M, p, q):
    """Closure with provenance; returns (contradiction_pair, proofs dict)."""
    N = 2*M + 15
    proof = {}   # fact -> ('unit', r, a) | ('RL', src) | ('RT', src) | ('T', f1, f2)
    dq = deque()
    def add(u, v, why):
        if u == v or (u, v) in proof:
            return None
        proof[(u, v)] = why
        dq.append((u, v))
        if (v, u) in proof:
            return (u, v)
        return None
    for r in (p, q):
        a = 1
        while 2*a + r <= N:
            c = add(2*a + r, a, ('unit', r, a))
            if c: return c, proof
            a += 1
    while dq:
        u, v = dq.popleft()
        w = 2*u - v
        if 1 <= w <= N:
            c = add(u, w, ('RL', (u, v)))
            if c: return c, proof
        w = 2*v - u
        if 1 <= w <= N:
            c = add(w, v, ('RT', (u, v)))
            if c: return c, proof
        for (x, y) in list(proof.keys()):
            if y == u:
                c = add(x, v, ('T', (x, u), (u, v)))
                if c: return c, proof
            if x == v:
                c = add(u, y, ('T', (u, v), (v, y)))
                if c: return c, proof
    return None, proof

def support(fact, proof, seen=None):
    if seen is None: seen = {}
    if fact in seen: return seen
    why = proof[fact]
    seen[fact] = why
    if why[0] in ('RL', 'RT'):
        support(why[1], proof, seen)
    elif why[0] == 'T':
        support(why[1], proof, seen); support(why[2], proof, seen)
    return seen

def show(M, p, q):
    c, proof = derive(M, p, q)
    if not c:
        print(f'(q={q},p={p}) M={M}: NO refutation (alive)'); return
    u, v = c
    sup = support((u, v), proof)
    sup2 = support((v, u), proof, dict(sup))
    print(f'(q={q},p={p}) M={M}: 2-cycle on ({u},{v}); DAG size {len(sup2)}')
    def fmt(f):
        w = sup2[f]
        if w[0] == 'unit':
            return f'{f[0]}<{f[1]}  [unit r={w[1]} at a={w[2]}]'
        if w[0] in ('RL','RT'):
            return f'{f[0]}<{f[1]}  [{w[0]} from {w[1][0]}<{w[1][1]}]'
        return f'{f[0]}<{f[1]}  [T: {w[1][0]}<{w[1][1]}, {w[2][0]}<{w[2][1]}]'
    # topological-ish print: by insertion is fine (proof dict preserves order)
    order = [f for f in proof if f in sup2]
    for f in order:
        print('   ', fmt(f))
    print()

if __name__ == '__main__':
    M = 48
    for (q, p) in [(1,2),(2,3),(4,5),(16,17),(30,31),(48,49),
                   (0,23),(0,24),(1,24),(2,25),(5,29),(20,53),(53,62)]:
        show(M, p, q)
