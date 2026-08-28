#!/usr/bin/env python3
"""e152c: affine certificate families beyond MC towers.

Gamma3 (2-D-unit cycles): D-unit D(a; r, r') = fact (2a+r) < b,
b = (3a+2r-r')/2, valid when b >= 1 integer and 3a+2r <= N
[derivation: unit (2a+r) < a, RL to 3a+2r, unit (3a+2r) = 2b+r' < b, T].
Cycle: D-units (u < v) and (u' < u) with u' = 2u-v; RL from u<v gives
u < u' — a 2-cycle.  Sign patterns (r1,r1',r2,r2') in {p,q}^4 give
   a  = -2r1 + 3r1' + 2r2 - 4r2'
   a' = (4a + 2r1 + r2' - 2r2)/3
with node/window constraints.  Soundness is by construction; this
script measures which (q,p) at M=48 admit a Gamma3 instance, combined
coverage with MC (e152), and runs the soundness cross-check (no alive
pair may admit an instance).
"""
import json
from e152_mc_schema import closure_verdict, mc_instances

def gamma3_instances(M, p, q, first_only=True):
    N = 2*M + 15
    out = []
    for r1 in (p, q):
        for r1p in (p, q):
            for r2 in (p, q):
                for r2p in (p, q):
                    a = -2*r1 + 3*r1p + 2*r2 - 4*r2p
                    if a < 1:
                        continue
                    num = 4*a + 2*r1 + r2p - 2*r2
                    if num % 3 or num <= 0:
                        continue
                    ap = num // 3
                    # D-unit 1: u = 2a+r1 < v = (3a+2r1-r1p)/2
                    if (3*a + 2*r1 - r1p) % 2:
                        continue
                    u = 2*a + r1
                    v = (3*a + 2*r1 - r1p) // 2
                    if v < 1 or 3*a + 2*r1 > N:
                        continue
                    # D-unit 2: u' = 2a'+r2 < v' = (3a'+2r2-r2p)/2 = u
                    if (3*ap + 2*r2 - r2p) % 2:
                        continue
                    up = 2*ap + r2
                    vp = (3*ap + 2*r2 - r2p) // 2
                    if vp != u or 3*ap + 2*r2 > N:
                        continue
                    if up != 2*u - v:      # cycle closing
                        continue
                    if up > N:
                        continue
                    out.append((a, ap, (r1, r1p, r2, r2p), u, v, up))
                    if first_only:
                        return out
    return out

def main():
    M = 48
    log = []
    def p_(*a):
        s = ' '.join(str(x) for x in a); print(s); log.append(s)
    p_(f'== e152c Gamma3 affine families, M={M} ==')
    dead, alive = [], []
    for q in range(0, M + 15):
        for p in range(q + 1, M + 16):
            ref, _ = closure_verdict(M, p, q)
            (dead if ref else alive).append((q, p))
    g3 = [(q, p) for (q, p) in dead if gamma3_instances(M, p, q)]
    mc = [(q, p) for (q, p) in dead if mc_instances(M, p, q)]
    union = sorted(set(g3) | set(mc))
    p_(f'dead {len(dead)}; MC {len(mc)}; Gamma3 {len(g3)}; union {len(union)}')
    p_(f'Gamma3-only (not MC): {len(set(g3)-set(mc))}')
    resid = sorted(set(dead) - set(union))
    p_(f'residual after MC+Gamma3: {len(resid)}')
    # residual anatomy: gap histogram
    from collections import Counter
    gh = Counter(p - q for (q, p) in resid)
    p_('residual gap histogram (p-q -> count):', dict(sorted(gh.items())))
    # which sign patterns fire
    pats = Counter()
    for (q, p) in g3:
        inst = gamma3_instances(M, p, q)[0]
        r1, r1p, r2, r2p = inst[2]
        lab = ''.join('p' if r == p else 'q' for r in (r1, r1p, r2, r2p))
        pats[lab] += 1
    p_('Gamma3 sign-pattern histogram:', dict(pats))
    # soundness: alive pairs must admit nothing
    badg = [(q, p) for (q, p) in alive if gamma3_instances(M, p, q)]
    p_(f'soundness (alive with Gamma3, must be 0): {len(badg)}', badg or '')
    with open('data/e152c_affine.json', 'w') as f:
        json.dump({'M': M, 'mc': len(mc), 'g3': len(g3),
                   'union': len(union), 'residual': resid,
                   'patterns': dict(pats)}, f)
    with open('data/e152c_affine.log', 'w') as f:
        f.write('\n'.join(log) + '\n')

if __name__ == '__main__':
    main()
