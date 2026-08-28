"""e155: the two finite hypotheses of Theorem P-ARM' (notes/58 SS3).

Part A (H-RW0): ThW0(m) = AP-free order theory on [m+1, 2m] + the 16
  halved crown units {2m-k < m+j : k <= 3, 1 <= j <= 7-2k}, unit
  (k, j) belonging to completion i = 2k+j in 1..7.  Check UNSAT of
  the full theory, of each of the 7 one-completion-dropped variants,
  and of all 21 two-completion-dropped variants (robustness margin).

Part B (H-FG6): on the HALVED windows W2e = [4m+1, 6m+7] and
  W2o = [4m+1, 6m+8] with attacker window W1 = [3m-7, 4m]: for every
  attacker pair, run plain R1-R4 + transitivity closure of the double
  fan; record dead/alive.  Verdict line: are ALL pairs at distance
  <= 6 closure-dead?  Also reports the full alive map (half-scale
  resonance data, feeds GAP-FG-schema).  Dead pairs at distance <= 6
  are SAT-cross-validated (direct solve of the fan order theory) —
  all of them for m <= 40, a 40-pair random sample for m > 40.

Run: .venv/bin/python experiments/e155_parm_hypotheses.py m [m ...]
Log: data/e155_parm_hyp.log ; data/e155_parm_hyp.json
"""
import json
import os
import random
import sys
import time
from collections import deque

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from pysat.solvers import Cadical195

LOG = os.path.join(HERE, '..', 'data', 'e155_parm_hyp.log')
OUT = os.path.join(HERE, '..', 'data', 'e155_parm_hyp.json')


def log(msg):
    print(msg, flush=True)
    with open(LOG, 'a') as f:
        f.write(msg + '\n')


# ----------------------------------------------------------------------
# generic order-theory SAT check
# ----------------------------------------------------------------------

def order_unsat(points, units):
    """Order theory on points: transitivity + AP midpoint constraints
    (for all integer 3-APs inside points) + units (u before v).
    Returns True iff UNSAT."""
    pts = sorted(points)
    ps = set(pts)
    idx = {v: i for i, v in enumerate(pts)}
    n = len(pts)
    off = {}
    top = 0
    for i in range(n):
        for j in range(i + 1, n):
            top += 1
            off[(i, j)] = top

    def lit(u, w):
        i, j = idx[u], idx[w]
        return off[(i, j)] if i < j else -off[(j, i)]

    cls = []
    for i in range(n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):
                x, y, z = off[(i, j)], off[(j, k)], off[(i, k)]
                cls.append([-x, -y, z])
                cls.append([x, y, -z])
    for b in pts:
        d = 1
        while b - d in ps or b + d in ps:
            a, c = b - d, b + d
            if a in ps and c in ps:
                cls.append([-lit(a, b), -lit(b, c)])
                cls.append([lit(a, b), lit(b, c)])
            d += 1
            if d > pts[-1] - pts[0]:
                break
    for (u, v) in units:
        cls.append([lit(u, v)])
    with Cadical195(bootstrap_with=cls) as s:
        return not s.solve()


# ----------------------------------------------------------------------
# Part A: punctured ThW0
# ----------------------------------------------------------------------

def crown_units_by_completion(m):
    by_i = {}
    for k in range(0, 4):
        for j in range(1, 8 - 2 * k):
            i = 2 * k + j
            by_i.setdefault(i, []).append((2 * m - k, m + j))
    assert sum(len(v) for v in by_i.values()) == 16
    assert sorted(by_i) == list(range(1, 8))
    return by_i


def part_A(m):
    pts = list(range(m + 1, 2 * m + 1))
    by_i = crown_units_by_completion(m)
    res = {}
    full = [u for us in by_i.values() for u in us]
    res['full'] = order_unsat(pts, full)
    ok1 = True
    for i in range(1, 8):
        units = [u for i2, us in by_i.items() if i2 != i for u in us]
        v = order_unsat(pts, units)
        res[f'drop{i}'] = v
        ok1 = ok1 and v
    ok2 = True
    worst2 = []
    for i in range(1, 8):
        for i2 in range(i + 1, 8):
            units = [u for i3, us in by_i.items()
                     if i3 not in (i, i2) for u in us]
            v = order_unsat(pts, units)
            ok2 = ok2 and v
            if not v:
                worst2.append((i, i2))
    log(f'  A m={m}: ThW0 full={"UNSAT" if res["full"] else "SAT"}; '
        f'1-drop all UNSAT: {ok1}; 2-drop all UNSAT: {ok2}'
        + (f' (SAT at {worst2})' if worst2 else ''))
    return {'full_unsat': res['full'], 'drop1_all_unsat': ok1,
            'drop1': {i: res[f"drop{i}"] for i in range(1, 8)},
            'drop2_all_unsat': ok2, 'drop2_sat_at': worst2}


# ----------------------------------------------------------------------
# Part B: closure on halved windows
# ----------------------------------------------------------------------

def close_window(lo, hi, X):
    """Plain R1-R4 + transitivity closure of the double fans of the
    attacker set X on the window [lo, hi].  Returns True iff a
    contradiction (some pair both ways) is derived."""
    V = range(lo, hi + 1)
    aps = []
    for b in V:
        for d in range(1, min(b - lo, hi - b) + 1):
            aps.append((b - d, b, b + d))
    fact = set()
    q = deque()

    def add(u, v):
        if (u, v) in fact:
            return False
        fact.add((u, v))
        q.append((u, v))
        return (v, u) in fact

    for x in X:
        for y in V:
            z = 2 * y - x
            if z != y and lo <= z <= hi:
                if add(z, y):
                    return True
    by_pair = {}
    for (a, b, c) in aps:
        for pr in ((a, b), (b, a), (b, c), (c, b)):
            by_pair.setdefault(pr, []).append((a, b, c))
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
                conc = (c3, b)              # R1
            elif (u, v) == (b, c3):
                conc = (b, a)               # R2
            elif (u, v) == (c3, b):
                conc = (a, b)               # R3
            elif (u, v) == (b, a):
                conc = (b, c3)              # R4
            if conc and add(*conc):
                return True
    return False


def fan_sat_unsat(lo, hi, X):
    """Direct SAT check: fan order theory on [lo, hi] with the double
    fans of X.  True iff UNSAT."""
    pts = list(range(lo, hi + 1))
    units = []
    for x in X:
        for y in pts:
            z = 2 * y - x
            if z != y and lo <= z <= hi:
                units.append((z, y))
    return order_unsat(pts, units)


def part_B(m):
    w1_lo, w1_hi = 3 * m - 7, 4 * m
    out = {}
    for name, hi in (('W2e', 6 * m + 7), ('W2o', 6 * m + 8)):
        lo = 4 * m + 1
        t0 = time.time()
        alive = []
        dead_small = []
        n_dead = 0
        attackers = list(range(w1_lo, w1_hi + 1))
        for ia, x1 in enumerate(attackers):
            for x2 in attackers[ia + 1:]:
                dead = close_window(lo, hi, (x1, x2))
                if dead:
                    n_dead += 1
                    if x2 - x1 <= 6:
                        dead_small.append((x1, x2))
                else:
                    alive.append((x1, x2))
        small_alive = [p for p in alive if p[1] - p[0] <= 6]
        gaps = sorted(set(p[1] - p[0] for p in alive))
        log(f'  B m={m} {name}: {n_dead} dead / {len(alive)} alive; '
            f'alive gaps {gaps[:8]}{"..." if len(gaps) > 8 else ""}; '
            f'H-FG6: {"HOLDS" if not small_alive else f"FAILS {small_alive}"}'
            f'  [{time.time()-t0:.0f}s]')
        # SAT cross-validation of the load-bearing dead pairs
        sample = dead_small if m <= 40 else random.sample(
            dead_small, min(40, len(dead_small)))
        t0 = time.time()
        bad = []
        for (x1, x2) in sample:
            if not fan_sat_unsat(lo, hi, (x1, x2)):
                bad.append((x1, x2))
        assert not bad, f'closure claims dead but SAT says SAT: {bad}'
        log(f'    SAT-validated {len(sample)} gap<=6 dead pairs '
            f'[{time.time()-t0:.0f}s]')
        out[name] = {'n_dead': n_dead, 'n_alive': len(alive),
                     'alive_gaps': gaps, 'hfg6': not small_alive,
                     'alive': alive[:400]}
    return out


def main():
    ms = [int(x) for x in sys.argv[1:]]
    res = {}
    if os.path.exists(OUT):
        with open(OUT) as f:
            res = json.load(f)
    for m in ms:
        log(f'e155 m={m}:')
        ra = part_A(m)
        rb = part_B(m)
        res[str(m)] = {'A': ra, 'B': rb}
        with open(OUT, 'w') as f:
            json.dump(res, f, indent=0)
    log(f'e155: done {ms}')


if __name__ == '__main__':
    main()
