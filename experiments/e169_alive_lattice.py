"""e169: the H-LAT lattice route to bounding alpha_max  (notes/66).

Part H (HALVE-PURE machine check): the class-c PURE fan subsystem at
  full scale M — window P2 cap c, attackers P1 cap c, units z = 2y - x
  with y, z in the class, APs inside the class — is claimed isomorphic
  (affine relabeling, notes/66 Lemma HALVE-PURE) to the e155 halved
  double-fan system W2c(m), m = M/2:
      odd  c: 4M+s |-> 4m + (s+1)/2,  4M-p |-> 4m - (p-1)/2,
              window [4m+1, 6m+8]  (2m+8 values)
      even c: 4M+s |-> 4m + s/2,      4M-p |-> 4m - p/2,
              window [4m+1, 6m+7]  (2m+7 values)
      attackers |-> W1 = [3m-7, 4m] both cases; gap g |-> g/2.
  Check: for EVERY same-parity attacker pair at scale M, the direct
  pure closure at full scale agrees with close_window on the halved
  image; on closure-alive pairs, the direct pure SAT at full scale
  agrees with fan_sat_unsat on the halved image.

Part L (lattice scan at half scale m): for each window W2e/W2o with
  attackers W1 = [3m-7, 4m]: closure-prefilter every attacker pair,
  SAT-adjudicate the closure-alive ones (ONE incremental solver per
  window, units as assumptions), report:
    * SAT-alive pairs, their gaps, the H-LAT check (gaps == 0 mod 8),
    * max clique of the SAT-alive graph, full window AND restricted
      to the shallow zone [3m+1, 4m] (the exact image of alpha's
      vertex set at M = 2m) — the latter is an UPPER BOUND for the
      pure-SAT alpha-hat_c(M = 2m) by Lemma HALVE-PURE.

Run: python3 experiments/e169_alive_lattice.py --iso M [M ...]
     python3 experiments/e169_alive_lattice.py --scan m [m ...] [--workers N]
Log:  data/e169_alive_lattice.log (+ JSON data/e169_alive_lattice.json)
"""
import json
import os
import sys
import time
from collections import deque
from itertools import combinations
from multiprocessing import Pool

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from e155_parm_hypotheses import close_window, fan_sat_unsat

from pysat.solvers import Cadical195

DATA = os.path.join(HERE, '..', 'data')
LOG = os.path.join(DATA, 'e169_alive_lattice.log')
OUT = os.path.join(DATA, 'e169_alive_lattice.json')


def log(msg):
    print(msg, flush=True)
    with open(LOG, 'a') as f:
        f.write(msg + '\n')


# ----------------------------------------------------------------------
# generic closure (R1-R4 + transitivity) on an arbitrary value set
# ----------------------------------------------------------------------

def generic_close(V, units):
    """V: sorted list of values; units: iterable of (u, v) = 'u before
    v' seeds.  APs are all 3-term APs inside V.  True iff refuted."""
    Vs = set(V)
    aps = []
    for a, c in combinations(V, 2):
        if (a + c) % 2 == 0 and (a + c) // 2 in Vs and (a + c) // 2 != a:
            b = (a + c) // 2
            if b != a and b != c:
                aps.append((a, b, c))
    fact = set()
    q = deque()

    def add(u, v):
        if (u, v) in fact:
            return False
        fact.add((u, v))
        q.append((u, v))
        return (v, u) in fact

    for (u, v) in units:
        if add(u, v):
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
                conc = (c3, b)
            elif (u, v) == (b, c3):
                conc = (b, a)
            elif (u, v) == (c3, b):
                conc = (a, b)
            elif (u, v) == (b, a):
                conc = (b, c3)
            if conc and add(*conc):
                return True
    return False


def pure_units(V, X):
    Vs = set(V)
    units = []
    for x in X:
        for y in V:
            z = 2 * y - x
            if z != y and z in Vs:
                units.append((z, y))
    return units


def pure_sat_unsat(V, X):
    """Direct SAT of the pure subsystem: order theory on V with the
    double fans of X restricted to V."""
    idx = {v: i for i, v in enumerate(V)}
    n = len(V)
    var = {}
    top = 0
    for i in range(n):
        for j in range(i + 1, n):
            top += 1
            var[(i, j)] = top

    def lit(u, w):
        i, j = idx[u], idx[w]
        return var[(i, j)] if i < j else -var[(j, i)]

    cls = []
    Vs = set(V)
    for a, c in combinations(V, 2):
        if (a + c) % 2 == 0:
            b = (a + c) // 2
            if b in Vs and b != a and b != c:
                cls.append([-lit(a, b), -lit(b, c)])
                cls.append([lit(a, b), lit(b, c)])
    for (u, w) in pure_units(V, X):
        cls.append([lit(u, w)])
    for i in range(n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):
                x, y, z = var[(i, j)], var[(j, k)], var[(i, k)]
                cls.append([-x, -y, z])
                cls.append([x, y, -z])
    with Cadical195(bootstrap_with=cls) as s:
        return not s.solve()


# ----------------------------------------------------------------------
# Part H: the iso check at full scale M
# ----------------------------------------------------------------------

_H = {}


def _h_init(M):
    _H['M'] = M


def _h_work(job):
    (eps, p, q) = job                    # p > q, both == eps (mod 2)
    M = _H['M']
    m = M // 2
    X = (4 * M - p, 4 * M - q)
    # attacker 4M-p has parity of p; its pure class = P2 values 4M+s
    # with s == eps (mod 2)
    V = [v for v in range(4 * M + 1, 6 * M + 16)
         if (v - 4 * M) % 2 == eps]
    dead_full = generic_close(V, pure_units(V, X))
    if eps == 1:
        Xh = (4 * m - (p - 1) // 2, 4 * m - (q - 1) // 2)
        lo, hi = 4 * m + 1, 6 * m + 8
    else:
        Xh = (4 * m - p // 2, 4 * m - q // 2)
        lo, hi = 4 * m + 1, 6 * m + 7
    dead_half = close_window(lo, hi, (min(Xh), max(Xh)))
    sat_agree = None
    if not dead_full:                    # closure-alive: SAT both levels
        su_full = pure_sat_unsat(V, X)
        su_half = fan_sat_unsat(lo, hi, (min(Xh), max(Xh)))
        sat_agree = (su_full == su_half)
    return (eps, p, q, dead_full, dead_half, sat_agree)


def part_H(M, workers):
    t0 = time.time()
    jobs = []
    for eps in (1, 0):
        offs = [p for p in range(0, M + 16) if p % 2 == eps]
        for q, p in combinations(offs, 2):
            jobs.append((eps, max(p, q), min(p, q)))
    mism_clo, mism_sat, n_alive, n_dead = [], [], 0, 0
    with Pool(workers, initializer=_h_init, initargs=(M,)) as pool:
        for (eps, p, q, df, dh, sa) in pool.imap_unordered(
                _h_work, jobs, chunksize=8):
            if df != dh:
                mism_clo.append((eps, q, p, df, dh))
            if df:
                n_dead += 1
            else:
                n_alive += 1
                if sa is False:
                    mism_sat.append((eps, q, p))
    el = time.time() - t0
    log(f'H : M={M}: {len(jobs)} same-parity pairs; pure-closure dead '
        f'{n_dead} / alive {n_alive}; closure mismatches vs halved: '
        f'{len(mism_clo)}; SAT mismatches on alive: {len(mism_sat)} '
        f'[{el:.0f}s]')
    if mism_clo:
        log(f'    CLO MISM: {mism_clo[:10]}')
    if mism_sat:
        log(f'    SAT MISM: {mism_sat[:10]}')
    return {'M': M, 'pairs': len(jobs), 'dead': n_dead,
            'alive': n_alive, 'mism_clo': mism_clo,
            'mism_sat': mism_sat}


# ----------------------------------------------------------------------
# Part L: half-scale scan
# ----------------------------------------------------------------------

_L = {}


def _l_init(lo, hi):
    _L['lo'], _L['hi'] = lo, hi


def _l_work(pair):
    return (pair, close_window(_L['lo'], _L['hi'], pair))


def max_clique(verts, dead_pairs):
    verts = sorted(verts)
    dead = set(frozenset(p) for p in dead_pairs)
    best = [0, []]

    def grow(cur, cand):
        if len(cur) > best[0]:
            best[0], best[1] = len(cur), list(cur)
        for i, v in enumerate(cand):
            if len(cur) + len(cand) - i <= best[0]:
                break
            if all(frozenset((v, w)) not in dead for w in cur):
                grow(cur + [v], cand[i + 1:])

    grow([], verts)
    return best[0], sorted(best[1])


def sat_adjudicate(lo, hi, pairs):
    """One incremental solver per window: static clauses = APs +
    transitivity on [lo, hi]; per-pair fan units passed as assumptions.
    Returns dict pair -> True iff UNSAT (dead)."""
    pts = list(range(lo, hi + 1))
    idx = {v: i for i, v in enumerate(pts)}
    n = len(pts)
    var = {}
    top = 0
    for i in range(n):
        for j in range(i + 1, n):
            top += 1
            var[(i, j)] = top

    def lit(u, w):
        i, j = idx[u], idx[w]
        return var[(i, j)] if i < j else -var[(j, i)]

    cls = []
    for b in pts:
        for d in range(1, min(b - lo, hi - b) + 1):
            a, c = b - d, b + d
            cls.append([-lit(a, b), -lit(b, c)])
            cls.append([lit(a, b), lit(b, c)])
    for i in range(n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):
                x, y, z = var[(i, j)], var[(j, k)], var[(i, k)]
                cls.append([-x, -y, z])
                cls.append([x, y, -z])
    out = {}
    with Cadical195(bootstrap_with=cls) as s:
        for X in pairs:
            assume = []
            for x in X:
                for y in pts:
                    z = 2 * y - x
                    if z != y and lo <= z <= hi:
                        assume.append(lit(z, y))
            out[X] = not s.solve(assumptions=assume)
    return out


def part_L(m, workers):
    res = {}
    for name, hi in (('W2e', 6 * m + 7), ('W2o', 6 * m + 8)):
        lo = 4 * m + 1
        t0 = time.time()
        attackers = list(range(3 * m - 7, 4 * m + 1))
        pairs = list(combinations(attackers, 2))
        alive = []
        with Pool(workers, initializer=_l_init,
                  initargs=(lo, hi)) as pool:
            for (pr, dead) in pool.imap_unordered(_l_work, pairs,
                                                  chunksize=8):
                if not dead:
                    alive.append(pr)
        alive.sort()
        t1 = time.time()
        verdicts = sat_adjudicate(lo, hi, alive)
        sat_alive = sorted(pr for pr, dead in verdicts.items()
                           if not dead)
        t2 = time.time()
        gaps = sorted(set(b - a for (a, b) in sat_alive))
        hlat = [g for g in gaps if g % 8 != 0]
        # cliques of the SAT-alive graph: dead edges = every pair NOT
        # SAT-alive (closure-dead or SAT-dead)
        sat_alive_set = set(sat_alive)
        verts_full = attackers
        verts_shal = [x for x in attackers if x >= 3 * m + 1]

        def dead_edges(verts):
            return [(a, b) for a, b in combinations(sorted(verts), 2)
                    if (a, b) not in sat_alive_set]

        wf, witf = max_clique(verts_full, dead_edges(verts_full))
        ws, wits = max_clique(verts_shal, dead_edges(verts_shal))
        log(f'L : m={m} {name}: {len(pairs)} pairs -> closure-alive '
            f'{len(alive)} -> SAT-alive {len(sat_alive)} '
            f'[clo {t1-t0:.0f}s, sat {t2-t1:.0f}s]')
        log(f'    gaps {gaps}; H-LAT(mod 8) '
            f'{"HOLDS" if not hlat else f"VIOLATED at {hlat}"}')
        log(f'    max clique FULL = {wf} {witf}; SHALLOW '
            f'[3m+1,4m] = {ws} {wits}  => alpha-hat bound {ws} '
            f'for M={2*m}')
        res[name] = {'n_pairs': len(pairs), 'n_clo_alive': len(alive),
                     'sat_alive': sat_alive, 'gaps': gaps,
                     'hlat_ok': not hlat, 'clique_full': [wf, witf],
                     'clique_shallow': [ws, wits]}
    return res


def main():
    args = sys.argv[1:]
    workers = 40
    if '--workers' in args:
        i = args.index('--workers')
        workers = int(args[i + 1])
        del args[i:i + 2]
    mode = args[0]
    vals = [int(a) for a in args[1:]]
    store = {}
    if os.path.exists(OUT):
        with open(OUT) as f:
            store = json.load(f)
    if mode == '--iso':
        for M in vals:
            r = part_H(M, workers)
            store.setdefault('iso', {})[str(M)] = r
            with open(OUT, 'w') as f:
                json.dump(store, f)
    elif mode == '--scan':
        for m in vals:
            r = part_L(m, workers)
            store.setdefault('scan', {})[str(m)] = r
            with open(OUT, 'w') as f:
                json.dump(store, f)
    log('e169: DONE')


if __name__ == '__main__':
    main()
