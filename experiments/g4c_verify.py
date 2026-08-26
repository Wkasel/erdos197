"""Erdős #197 — G4c: adversarial re-verification of the G4b death certificates.

Independence from g4b_seam_law.py / s2_growing_death.py:
  * membership oracle for the stage-alternating variants REWRITTEN from the
    notes/42 definitions (no code shared with g4b's Variant class);
  * channel classifier REWRITTEN from the notes/42 SS2 table;
  * SAT instances (windows + unit lists) rebuilt from the mathematical
    definitions, then solved with a COMPLETE encoding (full 2*C(n,3)
    transitivity, no CEGAR) under Glucose42 — a different solver than the
    campaign's Cadical195 — for n <= 300; larger instances use a freshly
    written lazy loop (UNSAT-sound: only valid clauses are ever added),
    also under Glucose42;
  * every SAT verdict is checked on an explicit witness by an independent
    O(n^2) scanner; exact big-int walks confirm the seam-law geometry
    (X2 closed, C0 unconditional, FAN arithmetic) at scales far beyond
    enumeration (seam k <= 300, values ~2^45000).

Parts (run with --part):
  A     seam-law re-check: fresh oracle + fresh classifier vs the recorded
        channel counts in data/g4b_results.json (all 24 CHECK-A rows),
        + exact walks.
  B     small complete-encoding battery (M = 64/128 single-block, C3
        puncture, OG5, STG M=64 incl. Q1/Q3 punctures, chain M=128,
        3-block M=32, M=68 SAT control).
  C     heavy complete-encoding battery (n = 254..256: C3 puncture M=256,
        OG5 M=256, 1-block M=256, chain M=256 x3).
  D     fresh-CEGAR battery (n = 382..768: STG M=128 pairs intact/punct,
        Q1/Q3 M=128, STG M=256 pairs) + the gm/B RUNG-X t=9 seam rung
        (n = 1280) rebuilt from the Geneson-matched schedule definition.

Artifacts: data/g4c_verify_{A,B,C,D}.json + stdout logs.
"""
import argparse
import json
import os
import sys
import time
from fractions import Fraction

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
DATA = os.path.join(REPO, 'data')


# ======================================================================
# Fresh SAT machinery (complete encoding + witness check + lazy loop)
# ======================================================================

def _mk_vars(n):
    """var id for pair (i, j), i < j: row-major upper triangle."""
    off = {}
    nxt = 1
    for i in range(n):
        for j in range(i + 1, n):
            off[(i, j)] = nxt
            nxt += 1
    return off, nxt - 1


def solve_complete(V, units, expect=None, budget=3600.0, tag=''):
    """Complete encoding: AP clauses + units + full transitivity.
    Returns (verdict, seconds, extra)."""
    from pysat.solvers import Glucose42
    V = sorted(V)
    n = len(V)
    idx = {v: i for i, v in enumerate(V)}
    off, _nv = _mk_vars(n)

    def lit(u, w):
        """literal asserting u precedes w."""
        i, j = idx[u], idx[w]
        return off[(i, j)] if i < j else -off[(j, i)]

    t0 = time.time()
    Vs = set(V)

    def clauses():
        # monotone-3-AP prohibitions (both directions)
        for b in V:
            dmax = min(b - V[0], V[-1] - b)
            for d in range(1, dmax + 1):
                a, c = b - d, b + d
                if a in Vs and c in Vs:
                    yield [-lit(a, b), -lit(b, c)]
                    yield [lit(a, b), lit(b, c)]
        for (z, y) in units:
            yield [lit(z, y)]
        # transitivity: forbid both directed triangles on every i<j<k
        for i in range(n):
            oi = off
            for j in range(i + 1, n):
                xij = oi[(i, j)]
                for k in range(j + 1, n):
                    xjk = oi[(j, k)]
                    xik = oi[(i, k)]
                    yield [-xij, -xjk, xik]
                    yield [xij, xjk, -xik]

    with Glucose42(bootstrap_with=clauses()) as s:
        ok = s.solve()
        el = round(time.time() - t0, 1)
        if not ok:
            return 'UNSAT', el, {}
        model = s.get_model()
    # decode witness and verify independently
    pos = set(l for l in model if l > 0)
    wins = [0] * n
    for i in range(n):
        for j in range(i + 1, n):
            if off[(i, j)] in pos:
                wins[i] += 1
            else:
                wins[j] += 1
    order = [V[i] for i in sorted(range(n), key=lambda i: -wins[i])]
    err = check_witness(order, units)
    return ('SAT' if err is None else 'WITNESS-FAIL'), el, {'werr': err}


def check_witness(seq, units):
    """Independent witness check: seq is a permutation avoiding monotone
    3-APs, honouring every unit (z before y)."""
    p = {v: i for i, v in enumerate(seq)}
    vals = sorted(seq)
    vs = set(vals)
    for b in vals:
        for d in range(1, min(b - vals[0], vals[-1] - b) + 1):
            a, c = b - d, b + d
            if a in vs and c in vs:
                if p[a] < p[b] < p[c] or p[c] < p[b] < p[a]:
                    return f'monotone AP {(a, b, c)}'
    for (z, y) in units:
        if p[z] > p[y]:
            return f'unit {(z, y)} violated'
    return None


LAZY_SOLVER = os.environ.get('G4C_SOLVER', 'Glucose42')


def solve_lazy(V, units, budget=3600.0, tag=''):
    """Fresh lazy-transitivity loop (default Glucose42; override with
    G4C_SOLVER=Cadical195 — the loop, encoding, and instance builders
    stay independent of the campaign code either way).  UNSAT is sound
    (every added clause is a consequence of order axioms); SAT verified
    on an explicit witness."""
    import pysat.solvers as _ps
    Glucose42 = getattr(_ps, LAZY_SOLVER)
    V = sorted(V)
    n = len(V)
    idx = {v: i for i, v in enumerate(V)}
    off, top = _mk_vars(n)

    def lit(u, w):
        i, j = idx[u], idx[w]
        return off[(i, j)] if i < j else -off[(j, i)]

    Vs = set(V)
    base = []
    for b in V:
        for d in range(1, min(b - V[0], V[-1] - b) + 1):
            a, c = b - d, b + d
            if a in Vs and c in Vs:
                base.append([-lit(a, b), -lit(b, c)])
                base.append([lit(a, b), lit(b, c)])
    for (z, y) in units:
        base.append([lit(z, y)])
    s = Glucose42(bootstrap_with=base)
    t0 = time.time()
    rounds = 0
    iu = np.triu_indices(n, 1)
    while True:
        rounds += 1
        if time.time() - t0 > budget:
            s.delete()
            return 'TIMEOUT', round(time.time() - t0, 1), {'rounds': rounds}
        if not s.solve():
            s.delete()
            return 'UNSAT', round(time.time() - t0, 1), {'rounds': rounds}
        model = s.get_model()
        posv = np.zeros(top + 1, dtype=bool)
        for l in model:
            if 0 < l <= top:
                posv[l] = True
        B = np.zeros((n, n), dtype=bool)
        for i in range(n - 1):
            first = off[(i, i + 1)]
            row = posv[first: first + (n - 1 - i)]
            B[i, i + 1:] = row
            B[i + 1:, i] = ~row
        P = B.astype(np.uint8)
        M2 = (P @ P) > 0
        cyc = M2 & B.T          # (i, j): path i->k->j exists and j<i
        ii, jj = np.nonzero(cyc)
        if len(ii) == 0:
            wins = B.sum(axis=1)
            order = [V[int(i)] for i in np.argsort(-wins, kind='stable')]
            err = check_witness(order, units)
            s.delete()
            return ('SAT' if err is None else 'WITNESS-FAIL',
                    round(time.time() - t0, 1),
                    {'rounds': rounds, 'werr': err})
        lim = 20000
        for t in range(min(len(ii), lim)):
            i, j = int(ii[t]), int(jj[t])
            ks = np.nonzero(B[i] & B[:, j])[0]
            k = int(ks[0])
            s.add_clause([-lit(V[i], V[k]), -lit(V[k], V[j]),
                          lit(V[i], V[j])])


# ======================================================================
# Fresh instance builders
# ======================================================================

def attacks_into(W, F):
    """Units (z, y): for x in F, y in W, z = 2y - x in W, z != y."""
    Ws = set(W)
    out = []
    for x in F:
        for y in W:
            z = 2 * y - x
            if z != y and z in Ws:
                out.append((z, y))
    return out


def c3_units(M):
    """The C3 core of thm:c3core: t5<b5, t3<b6, t10<b3."""
    return [(2 * M - 5, M + 5), (2 * M - 3, M + 6), (2 * M - 10, M + 3)]


# ---- Geneson-matched schedule (rebuilt from the construction) --------

def gm_stage_table(limit_log2=400):
    """[(stage_start, sliver_width M_{k-1})]: L_k = 4 M_{k-1},
    start_k = L_k + M_{k-1} = 5 M_{k-1}, M_k = 2 L_k 4^k."""
    out = [(1, 1)]
    M_prev, k = 1, 0
    while True:
        k += 1
        L = 4 * M_prev
        start = L + M_prev
        if start > (1 << limit_log2):
            break
        out.append((start, M_prev))
        M_prev = 2 * L * 4 ** k
    return out


def sched_gm(t, _tbl=gm_stage_table()):
    if t <= 2:
        return 1
    lo = 1 << (t - 1)
    s = 1
    for start, w in _tbl:
        if start <= lo:
            s = w
        else:
            break
    return max(1, min(s, 1 << (t - 2)))


def s1_team_of(v, sched):
    """S1 octave-alternating family: block (2^{t-1}, 2^t] owned by A for
    even t; owner donates bottom min(s_t, half-block) to partner; 1->B."""
    if v == 1:
        return 'B'
    t = (v - 1).bit_length()
    owner = 'A' if t % 2 == 0 else 'B'
    partner = 'B' if owner == 'A' else 'A'
    return partner if v - (1 << (t - 1)) <= min(sched(t), 1 << (t - 1)) \
        else owner


def build_gm_rungx_t9():
    """Rebuild RUNG-X gm/B t=9 from the notes/39 SS4 definitions:
    V = I_9 u I_11, I_r = (2^{r-1}+s_r, 2^r+s_{r+1}]; attackers = in-team
    x < n_10 = 2 s_10 - s_11 with at least one in-window attack."""
    def I(r):
        lo = (1 << (r - 1)) + min(sched_gm(r), 1 << (r - 1))
        hi = (1 << r) + min(sched_gm(r + 1), 1 << r)
        return lo, hi
    lo1, hi1 = I(9)
    lo2, hi2 = I(11)
    V = list(range(lo1 + 1, hi1 + 1)) + list(range(lo2 + 1, hi2 + 1))
    assert all(s1_team_of(v, sched_gm) == 'B' for v in V)
    n10 = 2 * min(sched_gm(10), 1 << 9) - min(sched_gm(11), 1 << 10)
    Vset = set(V)
    units, used = [], []
    for x in range(1, max(2, n10)):
        if s1_team_of(x, sched_gm) != 'B' or x > lo1:
            continue
        mine = [(2 * y - x, y) for y in V if 2 * y - x in Vset and
                2 * y - x != y]
        if mine:
            used.append(x)
            units.extend(mine)
    return V, units, used, (lo1 + 1, hi1), (lo2 + 1, hi2), n10


# ======================================================================
# Part A: fresh oracle + fresh classifier vs recorded channel counts
# ======================================================================

SPLIT_FROM = 3


class FreshStagePartition:
    """Stage-alternating partition, rebuilt from notes/42 SS1."""

    def __init__(self, bounds, sigma=lambda k: 0, tau=lambda k: 0,
                 orient='top', split='all'):
        self.a = bounds
        self.sigma = sigma
        self.tau = tau
        self.orient = orient
        self.split = split

    def octave(self, v):
        return (v - 1).bit_length()

    def stage(self, j):
        """stage k such that a_k < j <= a_{k+1} (octaves <= a_1: stage 0)."""
        a = self.a
        if j <= a[1]:
            return 0
        for k in range(1, len(a) - 1):
            if a[k] < j <= a[k + 1]:
                return k
        raise ValueError(j)

    def owner(self, k):
        return 'A' if k % 2 == 0 else 'B'

    def beta(self, j):
        if self.orient == 'top':
            return 'T'
        if self.orient == 'bot':
            return 'B'
        if self.orient == 'mixTB':
            return 'T' if j % 2 == 0 else 'B'
        if self.orient == 'halfBT':
            k = self.stage(j)
            return 'B' if 2 * j <= self.a[k] + self.a[k + 1] else 'T'
        raise ValueError(self.orient)

    def splittable(self, j):
        if self.split == 'none' or j < SPLIT_FROM:
            return False
        if self.split == 'interior' and j in self.a[1:]:
            return False
        return True

    def plant(self, j):
        if not self.splittable(j):
            return None
        return (1 << j) if self.beta(j) == 'T' else (1 << j) - 1

    def zone(self, v):
        """(kind, aux, team); kinds plant/kpair/bsliv/tsliv/kept."""
        j = self.octave(v)
        k = self.stage(j)
        own, par = self.owner(k), self.owner(k + 1)
        if v in ((1 << j) - 1, 1 << j) and self.splittable(j):
            return ('plant', j, par) if v == self.plant(j) \
                else ('kpair', j, own)
        if j in self.a[1:]:                      # top octave of stage k
            ks = self.a.index(j)
            t = self.tau(ks)
            if t and v > (1 << j) - t:
                return ('tsliv', ks, self.owner(ks))
        if k >= 1 and j == self.a[k] + 1:        # first octave of stage k
            s = self.sigma(k)
            if s and v <= (1 << self.a[k]) + s:
                return ('bsliv', k, self.owner(k - 1))
        return ('kept', k, own)

    def team(self, v):
        return self.zone(v)[2]


def fresh_variants():
    tri = [0] + [2 + k * (k + 1) // 2 for k in range(1, 40)]
    quad = [0] + [2 + k * k for k in range(1, 40)]
    grow = lambda k: k + 2           # noqa: E731
    return {
        'tri_top': FreshStagePartition(tri, orient='top'),
        'tri_bot': FreshStagePartition(tri, orient='bot'),
        'tri_mixTB': FreshStagePartition(tri, orient='mixTB'),
        'tri_top_sliv': FreshStagePartition(tri, sigma=grow, orient='top'),
        'tri_tau4_int': FreshStagePartition(tri, tau=lambda k: 4,
                                            orient='top', split='interior'),
        'quad_top': FreshStagePartition(quad, orient='top'),
        'quad_bot_sliv6': FreshStagePartition(quad, sigma=lambda k: 6,
                                              orient='bot'),
        'tri_halfBT': FreshStagePartition(tri, orient='halfBT'),
        'tri_none': FreshStagePartition(tri, split='none'),
    }


def pairlvl(v):
    j = (v - 1).bit_length()
    return j if v in ((1 << j) - 1, 1 << j) else None


def classify_fresh(P, x, y, z):
    """Channel of in-team triple (x, y, z=2y-x) per the notes/42 table.
    Returns (label, seam_index_or_level_or_stage); (None, info) if the
    triple fits no channel (a catalogue violation)."""
    zy, zz = P.zone(y), P.zone(z)
    ky, ay = zy[0], zy[1]
    kz, az = zz[0], zz[1]
    py, pz = pairlvl(y), pairlvl(z)
    # DUST: adjacent pair values with at least one planted (forces x = 1)
    if py is not None and pz == py + 1 and 'plant' in (ky, kz):
        return ('DUST', py)
    if ky in ('kept', 'kpair') and kz in ('kept', 'kpair'):
        sy = ay if ky == 'kept' else P.stage(ay)
        sz = az if kz == 'kept' else P.stage(az)
        return ('C0', sy) if sy == sz else (None, ('X2', sy, sz))
    if kz == 'bsliv' and ky in ('kept', 'kpair'):
        return ('C1', az) if P.octave(y) == P.a[az] \
            else (None, 'C1-not-top-octave')
    if ky == 'bsliv' and kz == 'plant' and az == P.a[ay] + 1:
        return ('C2', ay)
    if ky == 'bsliv' and kz == 'bsliv' and ay == az:
        return ('SLIVIN', ay)
    if ky == 'tsliv' and kz == 'tsliv' and ay == az:
        return ('TSLIVIN', ay)
    if ky == 'tsliv' and kz in ('kept', 'kpair'):
        return ('C4', ay)
    if ky == 'plant' and kz == 'tsliv' and ay == P.a[az] - 1:
        return ('C5', az)
    if ky == 'plant' and (ay in P.a[1:]) and kz in ('kept', 'kpair'):
        return ('FAN', P.a.index(ay))
    return (None, (zy, zz))


def partA():
    print('== G4c PART A: fresh oracle + classifier vs g4b records ==')
    res = {'rows': [], 'ok': True}
    with open(os.path.join(DATA, 'g4b_results.json')) as f:
        rec = json.load(f)['checkA_rows']
    variants = fresh_variants()
    XMAX = 24
    for row in rec:
        P = variants[row['variant']]
        sk = None
        for k, aa in enumerate(P.a):
            if aa == row['seam_level']:
                sk = k
        m = 1 << row['seam_level']
        assert m == row['m']
        s_level = row['seam_level']
        ylo, yhi = 1 << (s_level - 2), 1 << (s_level + 2)
        counts = {}
        bad = []
        for x in range(1, XMAX + 1):
            tx = P.team(x)
            for y in range(max(ylo, x) + 1, yhi + 1):
                if P.team(y) != tx:
                    continue
                z = 2 * y - x
                if P.team(z) != tx:
                    continue
                lab, aux = classify_fresh(P, x, y, z)
                if lab is None:
                    bad.append((x, y, z, repr(aux)))
                    continue
                key = lab if (lab in ('C0', 'DUST') or aux == sk) \
                    else f'{lab}@{aux}'
                counts[key] = counts.get(key, 0) + 1
        want = dict(row['channel_counts'])
        ok = (counts == want) and not bad
        res['ok'] &= ok
        res['rows'].append({'variant': row['variant'], 'm': m,
                            'fresh': counts, 'recorded': want,
                            'unclassified': bad[:5], 'ok': ok})
        print(f"  {row['variant']:16s} m={m:5d} "
              f"{'OK' if ok else 'MISMATCH'}"
              + ('' if ok else f' fresh={counts} want={want} bad={bad[:3]}'))
    # ---- exact walks (big ints) ----
    print('  -- exact walks --')
    tri = [0] + [2 + k * (k + 1) // 2 for k in range(1, 302)]
    quad = [0] + [2 + k * k for k in range(1, 302)]
    walks_ok = True
    for name, a in (('tri', tri), ('quad', quad)):
        for k in range(1, 298):
            lo_k = 1 << a[k]              # super-block (2^{a_k}, 2^{a_{k+1}}]
            hi_k = 1 << a[k + 1]
            lo_k2 = 1 << a[k + 2]
            # X2 closed: 2*hi(stage k) < lo(stage k+2) once L_{k+1} >= 2
            if a[k + 2] - a[k + 1] >= 2:
                walks_ok &= 2 * hi_k < lo_k2
            # C0 unconditional: interval neck 2*lo - hi -> -infinity
            if k >= 3:
                walks_ok &= 2 * lo_k - hi_k < -(1 << a[k])
    # FAN arithmetic at a huge seam (tri k=200): planted member p of the
    # seam pair has completion 2p - x inside the new owner's first octave
    # for every fixed 1 <= x <= 10^6
    a = tri
    j = a[200]
    m = 1 << j
    for p in (m - 1, m):
        for x in (1, 2, 3, 5, 999983, 10 ** 6):
            z = 2 * p - x
            walks_ok &= (m < z <= 2 * m) == (x < m)  # z in octave j+1
    res['walks_ok'] = walks_ok
    res['ok'] &= walks_ok
    print(f'  exact walks (X2 closed + neck -> -inf, k <= 300; FAN at '
          f'seam 2^{j}): {"OK" if walks_ok else "FAIL"}')
    with open(os.path.join(DATA, 'g4c_verify_A.json'), 'w') as f:
        json.dump(res, f, indent=1)
    print(f'PART A: {"ALL OK" if res["ok"] else "FAILURES"}')
    return res['ok']


# ======================================================================
# SAT batteries
# ======================================================================

def run_row(rows, tag, V, units, mode, expect, budget=3600.0):
    fn = solve_complete if mode == 'complete' else solve_lazy
    verdict, secs, extra = fn(V, units, budget=budget, tag=tag)
    match = (verdict == expect)
    rows.append({'tag': tag, 'n': len(V), 'units': len(units),
                 'mode': mode, 'solver': 'Glucose42',
                 'verdict': verdict, 'expect': expect, 'match': match,
                 'time': secs, **{k: v for k, v in extra.items()
                                  if k != 'werr'}})
    print(f'  {tag:44s} {verdict:7s} (expect {expect}) n={len(V)} '
          f'units={len(units)} [{secs}s] '
          f'{"OK" if match else "*** MISMATCH ***"}', flush=True)
    return match


def partB():
    print('== G4c PART B: complete-encoding battery (small) ==')
    rows = []
    ok = True
    # B: C3 puncture robustness, M = 64, 128 (+ 4mod8 SAT control)
    for M in (64, 128):
        W = list(range(M + 1, 2 * M + 1))
        ok &= run_row(rows, f'B intact M={M}', W, c3_units(M),
                      'complete', 'UNSAT')
        ok &= run_row(rows, f'B minus2M M={M}',
                      [v for v in W if v != 2 * M], c3_units(M),
                      'complete', 'UNSAT')
        ok &= run_row(rows, f'B minus2M-1 M={M}',
                      [v for v in W if v != 2 * M - 1], c3_units(M),
                      'complete', 'UNSAT')
        ok &= run_row(rows, f'B minusboth M={M}',
                      [v for v in W if v < 2 * M - 1], c3_units(M),
                      'complete', 'UNSAT')
    Mc = 68
    ok &= run_row(rows, 'B minus2M M=68 (4mod8 ctrl)',
                  [v for v in range(Mc + 1, 2 * Mc + 1) if v != 2 * Mc],
                  c3_units(Mc), 'complete', 'SAT')
    # D: OG5
    for M in (64, 128):
        W = list(range(M + 1, 2 * M + 1))
        ok &= run_row(rows, f'D OG5 M={M} F=31,32', W,
                      attacks_into(W, (31, 32)), 'complete', 'UNSAT')
    # single-block pairs
    ONEB = {64: [((21, 22), 'UNSAT'), ((3, 4), 'SAT'), ((3, 5), 'SAT')],
            128: [((21, 22), 'UNSAT'), ((3, 4), 'SAT'), ((3, 5), 'SAT'),
                  ((7, 8), 'SAT'), ((9, 13), 'SAT'), ((11, 12), 'UNSAT'),
                  ((13, 14), 'UNSAT'), ((15, 17), 'UNSAT'),
                  ((17, 18), 'UNSAT'), ((41, 42), 'UNSAT')]}
    for M, cfgs in ONEB.items():
        W = list(range(M + 1, 2 * M + 1))
        for F, exp in cfgs:
            ok &= run_row(rows, f'1block M={M} F={F}', W,
                          attacks_into(W, F), 'complete', exp)
    # STG M=64 (2 consecutive blocks)
    M = 64
    intact = list(range(M + 1, 4 * M + 1))
    punct = [v for v in intact if v not in (2 * M, 4 * M)]
    for F, exp in (((3,), 'SAT'), ((15,), 'SAT'), ((15, 16), 'UNSAT'),
                   ((21, 22), 'UNSAT'), ((3, 4), 'UNSAT'),
                   ((3, 5), 'UNSAT'), ((5, 9), 'UNSAT'),
                   ((19, 27), 'UNSAT'), ((21, 25), 'UNSAT')):
        ok &= run_row(rows, f'STG intact M=64 F={F}', intact,
                      attacks_into(intact, F), 'complete', exp)
    for F in ((15, 16), (21, 22)):
        ok &= run_row(rows, f'STG punct M=64 F={F}', punct,
                      attacks_into(punct, F), 'complete', 'UNSAT')
    # Q3 puncture torture, M=64
    W0 = intact
    cfgs = [('punctB', [v for v in W0 if v not in (2*M - 1, 4*M - 1)]),
            ('punct_all4', [v for v in W0
                            if v not in (2*M - 1, 2*M, 4*M - 1, 4*M)]),
            ('punct8_arb', [v for v in W0
                            if v not in (M + 7, M + 30, 2*M - 11, 2*M,
                                         2*M + 13, 3*M + 1, 4*M - 5,
                                         4*M - 1)])]
    for tag, W in cfgs:
        for F in ((21, 22), (3, 5)):
            ok &= run_row(rows, f'STG {tag} M=64 F={F}', W,
                          attacks_into(W, F), 'complete', 'UNSAT')
    # chain M=128, attacker pair inside (64, 128]
    W = list(range(129, 257))
    ok &= run_row(rows, 'chain M=128 F=65,66', W,
                  attacks_into(W, (65, 66)), 'complete', 'UNSAT')
    # 3-block single attacker M=32 (SAT)
    W = list(range(33, 257))
    for F in ((3,), (15,)):
        ok &= run_row(rows, f'3block M=32 F={F}', W, attacks_into(W, F),
                      'complete', 'SAT')
    with open(os.path.join(DATA, 'g4c_verify_B.json'), 'w') as f:
        json.dump({'ok': ok, 'rows': rows}, f, indent=1)
    print(f'PART B: {"ALL OK" if ok else "FAILURES"}')
    return ok


def partC():
    print('== G4c PART C: complete-encoding battery (n ~ 256) ==')
    rows = []
    ok = True
    M = 256
    W = list(range(M + 1, 2 * M + 1))
    ok &= run_row(rows, 'B intact M=256', W, c3_units(M),
                  'complete', 'UNSAT', budget=7200)
    ok &= run_row(rows, 'B minusboth M=256',
                  [v for v in W if v < 2 * M - 1], c3_units(M),
                  'complete', 'UNSAT', budget=7200)
    ok &= run_row(rows, 'D OG5 M=256 F=31,32', W,
                  attacks_into(W, (31, 32)), 'complete', 'UNSAT',
                  budget=7200)
    ok &= run_row(rows, '1block M=256 F=21,22', W,
                  attacks_into(W, (21, 22)), 'complete', 'UNSAT',
                  budget=7200)
    for F in ((65, 66), (100, 101), (129, 130)):
        ok &= run_row(rows, f'chain M=256 F={F}', W,
                      attacks_into(W, F), 'complete', 'UNSAT', budget=7200)
    with open(os.path.join(DATA, 'g4c_verify_C.json'), 'w') as f:
        json.dump({'ok': ok, 'rows': rows}, f, indent=1)
    print(f'PART C: {"ALL OK" if ok else "FAILURES"}')
    return ok


def partD():
    print('== G4c PART D: fresh-CEGAR battery (big) ==')
    rows = []
    ok = True
    # STG M=128 pairs
    M = 128
    intact = list(range(M + 1, 4 * M + 1))
    punct = [v for v in intact if v not in (2 * M, 4 * M)]
    for F in ((15, 16), (21, 22)):
        ok &= run_row(rows, f'STG intact M=128 F={F}', intact,
                      attacks_into(intact, F), 'lazy', 'UNSAT',
                      budget=3600)
        ok &= run_row(rows, f'STG punct M=128 F={F}', punct,
                      attacks_into(punct, F), 'lazy', 'UNSAT',
                      budget=3600)
    for F in ((3, 4), (3, 5), (19, 27), (21, 25), (5, 9)):
        ok &= run_row(rows, f'STG intact M=128 F={F} (Q1)', intact,
                      attacks_into(intact, F), 'lazy', 'UNSAT',
                      budget=3600)
    cfgs = [('punctB', [v for v in intact
                        if v not in (2*M - 1, 4*M - 1)]),
            ('punct_all4', [v for v in intact
                            if v not in (2*M - 1, 2*M, 4*M - 1, 4*M)]),
            ('punct8_arb', [v for v in intact
                            if v not in (M + 7, M + 30, 2*M - 11, 2*M,
                                         2*M + 13, 3*M + 1, 4*M - 5,
                                         4*M - 1)])]
    for tag, W in cfgs:
        for F in ((21, 22), (3, 5)):
            ok &= run_row(rows, f'STG {tag} M=128 F={F} (Q3)', W,
                          attacks_into(W, F), 'lazy', 'UNSAT',
                          budget=3600)
    # STG M=256 pairs
    M = 256
    intact = list(range(M + 1, 4 * M + 1))
    punct = [v for v in intact if v not in (2 * M, 4 * M)]
    for F in ((15, 16), (21, 22)):
        ok &= run_row(rows, f'STG intact M=256 F={F}', intact,
                      attacks_into(intact, F), 'lazy', 'UNSAT',
                      budget=7200)
        ok &= run_row(rows, f'STG punct M=256 F={F}', punct,
                      attacks_into(punct, F), 'lazy', 'UNSAT',
                      budget=7200)
    # gm/B RUNG-X t=9 rebuilt from the schedule definition
    V, units, used, I1, I2, n10 = build_gm_rungx_t9()
    print(f'  gm rung rebuilt: n={len(V)} units={len(units)} I_9={I1} '
          f'I_11={I2} neck10={n10} attackers={used}')
    rec = json.load(open(os.path.join(DATA, 's2_rungx_gmB.json')))
    r0 = rec['rungx'][0]
    ident = (len(V) == r0['n'] and len(units) == r0['n_units'] and
             used == r0['attackers'] and list(I1) == r0['I_t'] and
             list(I2) == r0['I_t2'])
    print(f'  instance identity vs s2 record: '
          f'{"MATCH" if ident else "*** DIFFERS ***"}')
    ok &= ident
    ok &= run_row(rows, 'RUNG-X gm/B t=9 (rebuilt)', V, units, 'lazy',
                  'UNSAT', budget=7200)
    with open(os.path.join(DATA, 'g4c_verify_D.json'), 'w') as f:
        json.dump({'ok': ok, 'identity_match': ident, 'rows': rows},
                  f, indent=1)
    print(f'PART D: {"ALL OK" if ok else "FAILURES"}')
    return ok


def partE():
    """Scale escalation beyond the G4b horizon: generic-pair and chain
    rungs at M = 512 / 1024 (lazy, Glucose42)."""
    print('== G4c PART E: scale escalation M = 512 / 1024 ==')
    rows = []
    ok = True
    for M in (512, 1024):
        W = list(range(M + 1, 2 * M + 1))
        ok &= run_row(rows, f'1block M={M} F=21,22', W,
                      attacks_into(W, (21, 22)), 'lazy', 'UNSAT',
                      budget=7200)
    for M in (512, 1024):
        W = list(range(2 * M + 1, 4 * M + 1))     # block (2M, 4M]
        ok &= run_row(rows, f'chain M={2*M} F={M+1},{M+2}', W,
                      attacks_into(W, (M + 1, M + 2)), 'lazy', 'UNSAT',
                      budget=7200)
    M = 512
    intact = list(range(M + 1, 4 * M + 1))
    ok &= run_row(rows, 'STG intact M=512 F=(15, 16)', intact,
                  attacks_into(intact, (15, 16)), 'lazy', 'UNSAT',
                  budget=7200)
    with open(os.path.join(DATA, 'g4c_verify_E.json'), 'w') as f:
        json.dump({'ok': ok, 'rows': rows}, f, indent=1)
    print(f'PART E: {"ALL OK" if ok else "FAILURES"}')
    return ok


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--part', required=True, choices=list('ABCDE'))
    args = ap.parse_args()
    ok = {'A': partA, 'B': partB, 'C': partC, 'D': partD,
          'E': partE}[args.part]()
    sys.exit(0 if ok else 1)


if __name__ == '__main__':
    main()
