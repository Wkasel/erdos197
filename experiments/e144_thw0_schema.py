"""e144: branch-closure schema search for ThW0 (GAP-H1, notes/55 SS5.4c).

ThW0(m) = AP-freeness on the block [m+1, 2m] + the 16 halved crown
units {2m-k < m+j : k <= 3, j <= 7-2k}.  Machine-UNSAT on the
needed line m = 0 mod 8; plain closure stalls.  Search the e124g/h
recipe: Lemma-D phase fiats on ladder sets + R1-R4/transitivity
closure, all branches must refute.

Ladder sets (block coordinates):
  O  = odd d=2 ladder (m+1, m+3, ...)
  E  = even d=2 ladder (m+2, m+4, ...)
  A4 = d=4 ladder on values = 1 mod 4
  B4 = d=4 ladder on values = 3 mod 4
Levels: [O] (2 branches), [O,E] (4), [O,A4,B4] (8), [O,E,A4,B4] (16).

Run: .venv/bin/python experiments/e144_thw0_schema.py
Log: data/e144_thw0_schema.log
"""
import os
import sys
from collections import deque
from itertools import product

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)


def generic_close(V, seed_facts):
    V = sorted(V)
    Vs = set(V)
    lo, hi = V[0], V[-1]
    fact = set()
    q = deque()

    def add(u, v):
        if (u, v) in fact:
            return False
        fact.add((u, v))
        q.append((u, v))
        return (v, u) in fact

    for (u, v) in seed_facts:
        if add(u, v):
            return True
    by_pair = {}
    for b in V:
        for d in range(1, min(b - lo, hi - b) + 1):
            a, c = b - d, b + d
            if a in Vs and c in Vs:
                ap = (a, b, c)
                for pr in ((a, b), (b, a), (b, c), (c, b)):
                    by_pair.setdefault(pr, []).append(ap)
    succ, pred = {}, {}
    while q:
        (u, v) = q.popleft()
        succ.setdefault(u, set()).add(v)
        pred.setdefault(v, set()).add(u)
        for w in list(pred.get(u, ())):
            if add(w, v):
                return True
        for w2 in list(succ.get(v, ())):
            if add(u, w2):
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
            if conc and add(*conc):
                return True
    return False


def zig(V, first, d, leader_first):
    lad = [v for v in range(first, max(V) + 1, d) if v >= min(V)]
    e0 = 0 if leader_first else 1
    out = []
    for i in range(e0, len(lad), 2):
        if i > 0:
            out.append((lad[i], lad[i - 1]))
        if i + 1 < len(lad):
            out.append((lad[i], lad[i + 1]))
    return out


def crown_units(m):
    out = []
    for k in range(0, 4):
        for j in range(1, 8 - 2 * k):
            out.append((2 * m - k, m + j))
    assert len(out) == 16
    return out


def ladders(m):
    V = list(range(m + 1, 2 * m + 1))
    return {
        'O': (m + 1, 2),
        'E': (m + 2, 2),
        'A4': (m + 1 if (m + 1) % 4 == 1 else m + 3, 4),
        'B4': (m + 1 if (m + 1) % 4 == 3 else m + 3, 4),
    }


def try_level(m, names):
    V = list(range(m + 1, 2 * m + 1))
    lads = ladders(m)
    units = crown_units(m)
    for phases in product((True, False), repeat=len(names)):
        seeds = list(units)
        for nm, ph in zip(names, phases):
            first, d = lads[nm]
            seeds += zig(V, first, d, ph)
        if not generic_close(V, seeds):
            return False, phases
    return True, None


def try_level_split(m, names, split_val):
    """names-phases x orientation of (m0, split_val): 2^(len+1) br."""
    V = list(range(m + 1, 2 * m + 1))
    lads = ladders(m)
    units = crown_units(m)
    m0 = 3 * m // 2
    for phases in product((True, False), repeat=len(names)):
        for ori in (True, False):
            seeds = list(units)
            for nm, ph in zip(names, phases):
                first, d = lads[nm]
                seeds += zig(V, first, d, ph)
            seeds.append((m0, split_val) if ori else (split_val, m0))
            if not generic_close(V, seeds):
                return False, (phases, ori)
    return True, None


def main():
    levels = [('O',), ('O', 'E'), ('O', 'A4', 'B4'),
              ('O', 'E', 'A4', 'B4')]
    for m in (16, 24, 32, 40, 48, 56, 64):
        res = None
        for names in levels:
            ok, bad = try_level(m, names)
            if ok:
                res = names
                break
        if res:
            print(f'  m={m}: ALL branches close at level {res} '
                  f'({2 ** len(res)} branches)', flush=True)
            continue
        # escalate: interleave split (m0, x)
        m0 = 3 * m // 2
        done = False
        for sv, svname in ((2 * m - 1, 't1'), (m + 1, 'b1'),
                           (2 * m, 't0'), (m + 2, 'b2')):
            ok, bad = try_level_split(m, ('O', 'E', 'A4', 'B4'), sv)
            if ok:
                print(f'  m={m}: closes at OEAB x split(m0,{svname}) '
                      f'(32 branches)', flush=True)
                done = True
                break
        if not done:
            print(f'  m={m}: STILL OPEN after all 32-branch splits '
                  f'(last fail {bad})', flush=True)
    print('e144: DONE', flush=True)


if __name__ == '__main__':
    main()
