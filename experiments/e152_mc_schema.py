#!/usr/bin/env python3
"""e152: GAP-FG-schema — the mirror-cycle (MC) uniform schema for the
double-fan closure kills, and its coverage of the closure-dead (q,p) grid.

Setting (offsets from 4M): window O = [1, N], N = 2M+15.  Attackers
x1 = 4M-p, x2 = 4M-q (0 <= q < p <= M+15).  Fan units: (2a+r) < a for
r in {p, q}, whenever 2a+r <= N (u < v means "u placed before v" in the
P2 order of the team owning everything = the death-pattern reading).

Part 1 (ground truth): full closure engine, rules
    T:  u<v, v<w  =>  u<w
    RL: u<v  =>  u < 2u-v          (midpoint-leads; AP (v,u,2u-v))
    RT: u<v  =>  2v-u < v          (midpoint-trails; AP (u,v,2v-u))
  (both guarded by the third point lying in O), contradiction = u<v & v<u.
This reproduces the e142/e142o verdicts independently.

Part 2 (schema): MC(k) towers.  Base a in O, tower m_i = 2^{i-1}(m1-a)+a
(i = 1..k), requiring
    m_1, ..., m_{k-1} in Chain(a)   [iterated fan units from a => m_i < a]
    m_k = 2*m_1 + r, r in {p,q}     [a direct fan unit m_k < m_1]
    all m_i and all chain intermediates in O.
Then m_i < m_{i+1} by RL from m_i < a, and m_k < m_1 closes the cycle.

Part 3: coverage report — which closure-dead pairs at M=48 admit an MC
certificate (and with which minimal (k, chain-depths)); the residual list.
Also: verify Gamma2' (p = 5a+6q) instances are closure-dead at several
scales, and q=0 resonance cross-check at M=48..96.
"""
import json, sys, time
from collections import deque

LOG = []
def log(*a):
    s = ' '.join(str(x) for x in a)
    print(s); LOG.append(s)

# ---------- Part 1: closure engine ----------

def closure_verdict(M, p, q, max_facts=200000):
    """Return (refuted: bool, n_facts)."""
    N = 2*M + 15
    facts = set()
    dq = deque()
    def add(u, v):
        if u == v:
            return True
        if (v, u) in facts:
            facts.add((u, v))
            return True
        if (u, v) not in facts:
            facts.add((u, v)); dq.append((u, v))
        return False
    # seed units
    for r in (p, q):
        a = 1
        while 2*a + r <= N:
            if add(2*a + r, a): return True, len(facts)
            a += 1
    # successors index for transitivity
    while dq:
        u, v = dq.popleft()
        # reflections
        w = 2*u - v
        if 1 <= w <= N:
            if add(u, w): return True, len(facts)
        w = 2*v - u
        if 1 <= w <= N:
            if add(w, v): return True, len(facts)
        # transitivity (scan; fact sets stay small enough)
        for (x, y) in list(facts):
            if y == u:
                if add(x, v): return True, len(facts)
            if x == v:
                if add(u, y): return True, len(facts)
        if len(facts) > max_facts:
            log(f'  WARN facts cap hit at (q={q},p={p})'); break
    return False, len(facts)

# ---------- Part 2: MC schema ----------

def chain_set(a, p, q, N, maxdepth=6):
    """Values reachable from a by iterated fan-unit steps v -> 2v+r <= N.
    Returns {value: depth} (min depth)."""
    out = {}
    frontier = [(a, 0)]
    while frontier:
        v, d = frontier.pop()
        if d >= maxdepth:
            continue
        for r in (p, q):
            w = 2*v + r
            if w <= N and (w not in out or out[w] > d + 1):
                out[w] = d + 1
                frontier.append((w, d + 1))
    return out

def mc_instances(M, p, q, kmax=5, maxdepth=6, first_only=True):
    """Enumerate MC(k) certificates; return list of (k, a, m1, r, depths)."""
    N = 2*M + 15
    found = []
    for a in range(1, N + 1):
        C = chain_set(a, p, q, N, maxdepth)
        if not C:
            continue
        for m1 in C:
            for k in range(3, kmax + 1):
                # m_i = 2^{i-1}(m1-a)+a
                ms = [(1 << i) * (m1 - a) + a for i in range(k)]
                if ms[-1] > N:
                    continue
                # closing unit
                r = ms[-1] - 2*m1
                if r not in (p, q):
                    continue
                # m_1..m_{k-1} must be chain values (m_k is NOT required:
                # its fact is the closing unit itself)
                if all(m in C for m in ms[:k-1]):
                    depths = [C[m] for m in ms[:k-1]]
                    found.append((k, a, m1, r, depths))
                    if first_only:
                        return found
    return found

# ---------- runs ----------

def main():
    t0 = time.time()
    M = 48
    N = 2*M + 15
    log(f'== e152 MC schema, M={M}, window [1,{N}] ==')

    # ground truth grid
    log('-- Part 1: closure grid (ground truth), 0 <= q < p <= M+15 --')
    dead, alive = [], []
    for q in range(0, M + 15):
        for p in range(q + 1, M + 16):
            ref, nf = closure_verdict(M, p, q)
            (dead if ref else alive).append((q, p))
    log(f'closure-dead pairs: {len(dead)}   alive: {len(alive)}  (e142o: 1851/165)')

    # MC coverage
    log('-- Part 2/3: MC coverage of the dead pairs --')
    covered, residual, byshape = [], [], {}
    for (q, p) in dead:
        inst = mc_instances(M, p, q)
        if inst:
            k, a, m1, r, depths = inst[0]
            covered.append((q, p))
            key = (k, tuple(depths))
            byshape[key] = byshape.get(key, 0) + 1
        else:
            residual.append((q, p))
    log(f'MC-covered: {len(covered)} / {len(dead)};  residual: {len(residual)}')
    log('shape histogram (k, chain-depths) -> count:')
    for key in sorted(byshape):
        log('   ', key, byshape[key])
    log('residual pairs (q,p):', residual)

    # sanity: no alive pair should admit an MC certificate (soundness check)
    bad = [(q, p) for (q, p) in alive if mc_instances(M, p, q)]
    log(f'soundness: MC instances on ALIVE pairs (must be 0): {len(bad)}', bad if bad else '')

    # Gamma2' spot checks at other scales: p = 5a+6q, q >= 1
    log('-- Gamma2\' (p = 5a+6q) closure spot checks --')
    g2 = []
    for (MM, q, a) in [(48, 1, 1), (48, 2, 3), (64, 3, 5), (80, 4, 7), (96, 5, 2)]:
        p = 5*a + 6*q
        if p > MM + 15 or 13*a + 12*q > 2*MM + 15:
            g2.append((MM, q, p, 'window-fail')); continue
        ref, nf = closure_verdict(MM, p, q)
        inst = mc_instances(MM, p, q)
        g2.append((MM, q, p, 'dead' if ref else 'ALIVE', 'mc' if inst else 'NO-MC'))
    for row in g2: log('   ', row)

    out = {'M': M, 'n_dead': len(dead), 'n_alive': len(alive),
           'n_mc_covered': len(covered), 'residual': residual,
           'shape_hist': {str(k): v for k, v in byshape.items()},
           'alive': alive, 'gamma2_checks': [list(map(str, r)) for r in g2]}
    with open('data/e152_mc_schema.json', 'w') as f:
        json.dump(out, f)
    log(f'total {time.time()-t0:.1f}s')
    with open('data/e152_mc_schema.log', 'w') as f:
        f.write('\n'.join(LOG) + '\n')

if __name__ == '__main__':
    main()
