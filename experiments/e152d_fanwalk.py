#!/usr/bin/env python3
"""e152d: the fan-walk schema FW — coverage of the closure-dead grid.

For a head h in [1,N] define the descent set D(h) (values x with the
derived fact h < x), the least set with:
  seed: h = 2a+r (r in {p,q}, a>=1)          =>  a in D(h)      [unit]
  (i)   x in D(h), 2h-x = 2y+r, y>=1          =>  y in D(h)
        [RL: h < 2h-x; unit: 2h-x < y; T]     (needs 2h-x <= N)
  (ii)  x in D(h), x = 2b+r, b>=1,
        2x-b <= N                             =>  2x-b in D(h)
        [unit: x < b; RL on (b,x,2x-b): x < 2x-b; T]
  (iii) x in D(h), x = 2b+r, b>=1             =>  b in D(h)
        [unit: x < b; T]
Fact graph E: h -> x for x in D(h), and h -> 2h-x (RL) for x in D(h)
with 1 <= 2h-x <= N, 2h-x != h.  Every edge is a sound derivation of
"h placed before target"; a directed cycle in E is a refutation of the
double fan + AP-freeness (an element before itself).

Coverage at M=48 over the 2016-pair grid; soundness check: the 165
closure-alive pairs must have acyclic E (else the schema would be
unsound — their theories are SAT).
"""
import json
from collections import Counter
from e152_mc_schema import closure_verdict

def descent(h, p, q, N):
    D = set()
    stack = []
    for r in (p, q):
        if (h - r) % 2 == 0 and (h - r) // 2 >= 1:
            a = (h - r) // 2
            D.add(a); stack.append(a)
    while stack:
        x = stack.pop()
        w = 2*h - x
        if 1 <= w <= N:
            for r in (p, q):
                if (w - r) % 2 == 0 and (w - r) // 2 >= 1:
                    y = (w - r) // 2
                    if y not in D:
                        D.add(y); stack.append(y)
        for r in (p, q):
            if (x - r) % 2 == 0 and (x - r) // 2 >= 1:
                b = (x - r) // 2
                if b not in D:
                    D.add(b); stack.append(b)
                z = 2*x - b
                if z <= N and z not in D:
                    D.add(z); stack.append(z)
    D.discard(h)
    return D

def fw_refutes(M, p, q):
    N = 2*M + 15
    adj = {}
    for h in range(1, N + 1):
        Dh = descent(h, p, q, N)
        out = set(Dh)
        for x in Dh:
            w = 2*h - x
            if 1 <= w <= N and w != h:
                out.add(w)
        out.discard(h)
        adj[h] = out
    # cycle detection (iterative DFS, colors)
    color = {v: 0 for v in adj}
    for s in adj:
        if color[s]:
            continue
        stack = [(s, iter(adj[s]))]
        color[s] = 1
        while stack:
            v, it = stack[-1]
            adv = False
            for w in it:
                if color[w] == 1:
                    return True
                if color[w] == 0:
                    color[w] = 1
                    stack.append((w, iter(adj[w])))
                    adv = True
                    break
            if not adv:
                color[v] = 2
                stack.pop()
    return False

def main():
    M = 48
    log = []
    def p_(*a):
        s = ' '.join(str(x) for x in a); print(s); log.append(s)
    p_(f'== e152d fan-walk schema coverage, M={M} ==')
    dead, alive = [], []
    for q in range(0, M + 15):
        for p in range(q + 1, M + 16):
            ref, _ = closure_verdict(M, p, q)
            (dead if ref else alive).append((q, p))
    fw = [(q, p) for (q, p) in dead if fw_refutes(M, p, q)]
    resid = sorted(set(dead) - set(fw))
    p_(f'dead {len(dead)}; FW-covered {len(fw)}; residual {len(resid)}')
    gh = Counter(pp - qq for (qq, pp) in resid)
    p_('residual gap histogram:', dict(sorted(gh.items())))
    p_('residual pairs:', resid)
    bad = [(q, p) for (q, p) in alive if fw_refutes(M, p, q)]
    p_(f'soundness (alive with FW cycle, MUST be 0): {len(bad)}', bad or '')
    with open('data/e152d_fanwalk.json', 'w') as f:
        json.dump({'M': M, 'n_dead': len(dead), 'n_fw': len(fw),
                   'residual': resid, 'alive_bad': bad}, f)
    with open('data/e152d_fanwalk.log', 'w') as f:
        f.write('\n'.join(log) + '\n')

if __name__ == '__main__':
    main()
