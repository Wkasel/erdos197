#!/usr/bin/env python3
"""e153: GAP-J-pencil — hand-checkable derivations for the 36 minimal
forbidden sets of Lemma J (notes/55 SS3.4).

Coordinates: k = 0..15, v_k := w_{15-k} = the value 4M-k (k = offset
from the TOP of the run).  T(J) = AP-freeness on the 16 consecutive
values + units  v_t < v_{j+2t}  (j in J, t >= 0, j+2t <= 15)
["<" = placed before].  APs in offset coordinates are the integer APs
of [0,15]; the closure calculus T/RL/RT of e152 (Lemma CC) applies
verbatim on the window [0,15].

For each minimal forbidden set: run provenance closure; if refuted,
extract the 2-cycle support DAG and greedily minimize it (drop any
fact not needed — here we just report the support, which is already
small); print a compact pencil derivation.  If closure stalls, try
the 2-branch phase splits (Lemma D on a d-ladder orientation).
"""
import json
from collections import deque

def closure(units, lo=0, hi=15):
    """units: list of (u,v) facts. Returns (cycle_pair_or_None, proof)."""
    proof = {}
    dq = deque()
    def add(u, v, why):
        if u == v or (u, v) in proof:
            return None
        proof[(u, v)] = why
        dq.append((u, v))
        if (v, u) in proof:
            return (u, v)
        return None
    for (u, v) in units:
        c = add(u, v, ('unit',))
        if c: return c, proof
    while dq:
        u, v = dq.popleft()
        w = 2*u - v
        if lo <= w <= hi:
            c = add(u, w, ('RL', (u, v)))
            if c: return c, proof
        w = 2*v - u
        if lo <= w <= hi:
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

def units_for(J):
    out = []
    for j in J:
        t = 0
        while j + 2*t <= 15:
            out.append((t, j + 2*t))
            t += 1
    return out

def support(fact, proof, seen=None):
    if seen is None: seen = {}
    if fact in seen: return seen
    why = proof[fact]; seen[fact] = why
    for f in why[1:]:
        support(f, proof, seen)
    return seen

def fmt_deriv(cyc, proof):
    u, v = cyc
    sup = support((u, v), proof)
    sup = support((v, u), proof, sup)
    lines = [f'2-cycle on ({u},{v}); {len(sup)} facts']
    for f in proof:            # insertion order = derivation order
        if f not in sup: continue
        w = sup[f]
        if w[0] == 'unit':
            lines.append(f'  {f[0]}<{f[1]}  [unit]')
        elif w[0] in ('RL', 'RT'):
            lines.append(f'  {f[0]}<{f[1]}  [{w[0]} {w[1][0]}<{w[1][1]}]')
        else:
            lines.append(f'  {f[0]}<{f[1]}  [T {w[1][0]}<{w[1][1]}, {w[2][0]}<{w[2][1]}]')
    return len(sup), lines

def split_refute(J, log_fn):
    """Try a single totality split: find (x,y) with both branches
    closure-refuted.  Returns True and logs both branch derivations."""
    units = units_for(J)
    for x in range(0, 16):
        for y in range(x + 1, 16):
            ok = True
            branches = []
            for br in [(x, y), (y, x)]:
                cyc, proof = closure(units + [br])
                if cyc is None:
                    ok = False
                    break
                branches.append((br, cyc, proof))
            if ok:
                log_fn(f'J={J}: SPLIT on ({x},{y}) — both branches refute')
                for br, cyc, proof in branches:
                    n, lines = fmt_deriv(cyc, proof)
                    log_fn(f'  branch {br[0]}<{br[1]}: ' + lines[0])
                    for ln in lines[1:]:
                        log_fn('  ' + ln)
                return True
    # two-level splits (4 branches) — first level fixed to the best pair
    for x in range(0, 16):
        for y in range(x + 1, 16):
            for x2 in range(0, 16):
                for y2 in range(x2 + 1, 16):
                    if (x2, y2) <= (x, y):
                        continue
                    ok = True
                    for b1 in [(x, y), (y, x)]:
                        for b2 in [(x2, y2), (y2, x2)]:
                            cyc, _ = closure(units + [b1, b2])
                            if cyc is None:
                                ok = False; break
                        if not ok: break
                    if ok:
                        log_fn(f'J={J}: DOUBLE SPLIT on ({x},{y}) x ({x2},{y2}) — all 4 branches refute (derivations suppressed)')
                        return True
    return False

def main():
    mf = json.load(open('data/e138_transfer.json'))['partB']['minimal_forbidden']
    mf = sorted([tuple(s) for s in mf], key=lambda s: (len(s), s))
    log = []
    def p_(*a):
        s = ' '.join(str(x) for x in a); print(s); log.append(s)
    p_('== e153 J-pencil: closure derivations for the 36 minimal forbidden sets ==')
    stalled = []
    sizes = {}
    for J in mf:
        cyc, proof = closure(units_for(J))
        if cyc is None:
            stalled.append(J)
            p_(f'J={J}: CLOSURE STALLS ({len(proof)} facts)')
            continue
        n, lines = fmt_deriv(cyc, proof)
        sizes[J] = n
        p_(f'J={J}: ' + lines[0])
        for ln in lines[1:]:
            p_(ln)
    p_(f'-- summary: {len(mf)-len(stalled)}/{len(mf)} closure-refuted; stalled: {stalled}')
    unsplit = []
    for J in stalled:
        if not split_refute(J, p_):
            unsplit.append(J)
            p_(f'J={J}: NO single/double split closes it')
    p_(f'-- split summary: {len(stalled)-len(unsplit)}/{len(stalled)} closed by splits; open: {unsplit}')
    p_('sizes:', {str(k): v for k, v in sizes.items()})
    with open('data/e153_j_pencil.log', 'w') as f:
        f.write('\n'.join(log) + '\n')

if __name__ == '__main__':
    main()
