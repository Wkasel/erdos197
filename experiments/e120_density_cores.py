"""Erdős #197 — e120: FRONT N5, dense-subset cores (the Case-2 bridge).

Question (N5, notes/43 §3): does a pair rung fire on ANY in-team subset
of density >= 1/2 + eps of a block?  Here the subset is ADVERSARIAL:
selection variables s_v alongside the order variables, cardinality
|S| >= k, AP clauses and attack units guarded by selection.  The
combined formula is SAT  <=>  the adversary can pick a subset of size
>= k (and an order on it) that escapes the rung; UNSAT  <=>  the rung
fires on EVERY subset of size >= k.  Escape is monotone downward in k
(subsets of an escaping set escape), so there is a critical
    k_crit(M, F) = max k with an escape,   rho* = k_crit / M:
the rung is subset-robust exactly above density rho*.

Parts:
  A  fixed low pair F = {15,16} / {11,12}, window (M, 2M], M = 64/96/128.
     Expectation to test: the attack surface of a FIXED pair is O(x)
     (midpoints (M, M+x/2], or one parity class of receivers kills one
     attacker and singles are SAT), so d* = M - k_crit should be O(1)
     in M and rho* -> 1: fixed-pair rungs are NOT density-robust.
     Quantify d* exactly and extract the minimal escape's structure.
  B  chain-geometry pair F = {M/2+1, M/2+2} (the pair INSIDE the
     previous block), window (M, 2M]: Theta(M) units, receiver set
     (2M-x, 2M] of size ~M/2, midpoint set of size ~M/4.  If
     d* = Theta(M) here, rho* is bounded away from 1 — a genuine
     dense-subset core (the N5 bridge).  Also: singles x and x+1 alone
     (are chain singles SAT like low singles?).
  C  coupled complementary coloring (N6 probe): blocks B0 = (M, 2M],
     B1 = (2M, 4M]; every value colored A or B (one selection var);
     each team gets its own linear order on its values with the
     block-order hypothesis (its B0 values precede its B1 values —
     the non-procrastination assumption, flagged in notes/45), AP
     clauses guarded per team; balance dial: each team owns >= kb
     values of EACH block.  SAT <=> some coloring lets BOTH teams
     escape.  Scan kb from M/2 (balanced everywhere-split) downward.

Soundness: complete encoding (full transitivity on the window's order
variables, unguarded — restricting a total order to S stays total, so
UNSAT-for-all-subsets is sound); every SAT verdict re-checked by an
independent scanner on the decoded subset + order.

Usage: e120_density_cores.py --part A|B|C [--only TAG]
Artifacts: data/e120_results.jsonl (streaming), data/e120_{A,B,C}.json.
"""
import argparse
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
DATA = os.path.join(REPO, 'data')
JSONL = os.path.join(DATA, 'e120_results.jsonl')

from pysat.solvers import Cadical195
from pysat.card import CardEnc, EncType


def stream(row):
    with open(JSONL, 'a') as f:
        f.write(json.dumps(row) + '\n')


# ----------------------------------------------------------------------
# shared: order-variable table
# ----------------------------------------------------------------------

def _mk_vars(n, start=1):
    off = {}
    nxt = start
    for i in range(n):
        for j in range(i + 1, n):
            off[(i, j)] = nxt
            nxt += 1
    return off, nxt - 1


def attacks_into(W, F):
    """Units (z, y): x in F, y in W, z = 2y - x in W, z != y.
    Semantics: x placed before the window => the AP (x, y, z) must not
    be position-increasing => z precedes y."""
    Ws = set(W)
    out = []
    for x in F:
        for y in W:
            z = 2 * y - x
            if z != y and z in Ws:
                out.append((z, y))
    return sorted(set(out))


# ----------------------------------------------------------------------
# Parts A/B: single window, fixed attackers, adversarial subset
# ----------------------------------------------------------------------

def solve_subset(W, F, k, budget=3600.0):
    """SAT <=> exists S subset of W, |S| >= k, and an order of S with no
    monotone 3-AP inside S and honouring every attack unit of F into S.
    Returns (verdict, secs, info); SAT info carries the escape subset."""
    V = sorted(W)
    n = len(V)
    idx = {v: i for i, v in enumerate(V)}
    off, top = _mk_vars(n, start=1)
    sel = {}                                   # selection vars
    for v in V:
        top += 1
        sel[v] = top

    def lit(u, w):
        i, j = idx[u], idx[w]
        return off[(i, j)] if i < j else -off[(j, i)]

    Vs = set(V)
    cls = []
    # AP prohibitions inside the selected set (guarded, both directions)
    for b in V:
        for d in range(1, min(b - V[0], V[-1] - b) + 1):
            a, c = b - d, b + d
            if a in Vs and c in Vs:
                g = [-sel[a], -sel[b], -sel[c]]
                cls.append(g + [-lit(a, b), -lit(b, c)])
                cls.append(g + [lit(a, b), lit(b, c)])
    # attack units, guarded by both endpoints selected
    units = attacks_into(V, F)
    for (z, y) in units:
        cls.append([-sel[y], -sel[z], lit(z, y)])
    # full transitivity (unguarded, sound)
    for i in range(n):
        for j in range(i + 1, n):
            xij = off[(i, j)]
            for kk in range(j + 1, n):
                xjk = off[(j, kk)]
                xik = off[(i, kk)]
                cls.append([-xij, -xjk, xik])
                cls.append([xij, xjk, -xik])
    # cardinality: at least k selected
    card = CardEnc.atleast(lits=[sel[v] for v in V], bound=k,
                           top_id=top, encoding=EncType.seqcounter)
    t0 = time.time()
    with Cadical195(bootstrap_with=cls) as s:
        for c in card.clauses:
            s.add_clause(c)
        ok = s.solve()
        el = round(time.time() - t0, 1)
        if not ok:
            return 'UNSAT', el, {'units': len(units)}
        model = set(l for l in s.get_model() if l > 0)
    S = [v for v in V if sel[v] in model]
    # decode order restricted to S
    posneg = lambda l: (l in model) if l > 0 else (abs(l) not in model)
    wins = {v: 0 for v in S}
    for i, u in enumerate(S):
        for w in S[i + 1:]:
            if posneg(lit(u, w)):
                wins[u] += 1
            else:
                wins[w] += 1
    order = sorted(S, key=lambda v: -wins[v])
    err = check_escape(order, S, F, k)
    verdict = 'SAT' if err is None else 'WITNESS-FAIL'
    dropped = sorted(set(V) - set(S))
    return verdict, el, {'units': len(units), 'S_size': len(S),
                         'dropped': dropped, 'werr': err}


def check_escape(order, S, F, k):
    """Independent check: |S| >= k; order is a permutation of S with no
    monotone 3-AP inside S; and no AP (x, y, z), x in F, y, z in S is
    position-increasing when x is placed first (i.e. unit z before y)."""
    if len(S) < k:
        return f'size {len(S)} < {k}'
    if sorted(order) != sorted(S):
        return 'order is not a permutation of S'
    p = {v: i for i, v in enumerate(order)}
    vals = sorted(S)
    vs = set(vals)
    for b in vals:
        for d in range(1, min(b - vals[0], vals[-1] - b) + 1):
            a, c = b - d, b + d
            if a in vs and c in vs:
                if p[a] < p[b] < p[c] or p[c] < p[b] < p[a]:
                    return f'monotone AP {(a, b, c)}'
    for x in F:
        for y in vals:
            z = 2 * y - x
            if z != y and z in vs and p[y] < p[z]:
                return f'attack AP ({x}, {y}, {z}) increasing'
    return None


def bsearch_kcrit(W, F, lo, hi, tag, budget=3600.0):
    """Largest k in [lo, hi] with an escape (SAT); requires SAT at lo,
    UNSAT at hi (verified first).  Returns k_crit and the escape at
    k_crit (dropped set)."""
    M = len(W)
    rows = []

    def q(k):
        v, el, info = solve_subset(W, F, k, budget)
        row = {'tag': tag, 'M': M, 'F': list(F), 'k': k, 'verdict': v,
               'time': el,
               'units': info.get('units'),
               'dropped': info.get('dropped'),
               'S_size': info.get('S_size')}
        rows.append(row)
        stream(row)
        d = info.get('dropped')
        print(f'  {tag} k={k}: {v} [{el}s]'
              + (f' dropped={d}' if v == 'SAT' else ''), flush=True)
        if v == 'WITNESS-FAIL':
            raise RuntimeError(f'witness fail at {tag} k={k}: '
                               f'{info.get("werr")}')
        return v

    if q(hi) != 'UNSAT':
        print(f'  {tag}: NOT UNSAT at k={hi} — no rung at all', flush=True)
        return hi, rows          # k_crit >= hi
    if q(lo) != 'SAT':
        # widen downward until SAT (escape must exist eventually)
        while lo > 1 and q(lo) != 'SAT':
            hi = lo
            lo = max(1, lo - max(4, M // 8))
    best = lo
    a, b = lo, hi                # SAT at a, UNSAT at b
    while b - a > 1:
        mid = (a + b) // 2
        if q(mid) == 'SAT':
            a = mid
        else:
            b = mid
    best = a
    return best, rows


def partA(only=None):
    print('== e120 PART A: fixed-pair density dial ==', flush=True)
    out = {'part': 'A', 'rows': [], 'summary': []}
    for F in ((15, 16), (11, 12)):
        for M in (64, 96, 128):
            tag = f'A F={F} M={M}'
            if only and only not in tag:
                continue
            W = list(range(M + 1, 2 * M + 1))
            # sanity: intact block (k = M)
            kc, rows = bsearch_kcrit(W, F, M - 12, M, tag)
            out['rows'] += rows
            dstar = M - kc
            escape = next((r['dropped'] for r in rows
                           if r['k'] == kc and r['verdict'] == 'SAT'), None)
            s = {'F': list(F), 'M': M, 'k_crit': kc, 'd_star': dstar,
                 'rho_star': round(kc / M, 4), 'escape_dropped': escape}
            out['summary'].append(s)
            stream({'tag': tag + ' SUMMARY', **s})
            print(f'  >> {tag}: k_crit={kc} d*={dstar} '
                  f'rho*={kc / M:.3f} escape drops {escape}', flush=True)
            with open(os.path.join(DATA, 'e120_A.json'), 'w') as f:
                json.dump(out, f, indent=1)
    return out


def partB(only=None):
    print('== e120 PART B: chain-geometry pair density dial ==', flush=True)
    out = {'part': 'B', 'rows': [], 'summary': []}
    for M in (64, 96, 128):
        x = M // 2 + 1
        F = (x, x + 1)
        tag = f'B F={F} M={M}'
        if only and only not in tag:
            continue
        W = list(range(M + 1, 2 * M + 1))
        # singles first: is the dense-channel SINGLE attacker SAT?
        for Fs in ((x,), (x + 1,)):
            v, el, info = solve_subset(W, Fs, M, budget=3600)
            row = {'tag': f'{tag} single F={Fs} intact', 'M': M,
                   'F': list(Fs), 'k': M, 'verdict': v, 'time': el,
                   'units': info.get('units')}
            out['rows'].append(row)
            stream(row)
            print(f'  {tag} single {Fs} intact: {v} [{el}s]', flush=True)
        kc, rows = bsearch_kcrit(W, F, M // 2, M, tag)
        out['rows'] += rows
        dstar = M - kc
        escape = next((r['dropped'] for r in rows
                       if r['k'] == kc and r['verdict'] == 'SAT'), None)
        s = {'F': list(F), 'M': M, 'k_crit': kc, 'd_star': dstar,
             'rho_star': round(kc / M, 4), 'escape_dropped': escape}
        out['summary'].append(s)
        stream({'tag': tag + ' SUMMARY', **s})
        print(f'  >> {tag}: k_crit={kc} d*={dstar} rho*={kc / M:.3f} '
              f'escape drops {escape}', flush=True)
        with open(os.path.join(DATA, 'e120_B.json'), 'w') as f:
            json.dump(out, f, indent=1)
    return out


# ----------------------------------------------------------------------
# Part D: existential-attacker two-scale gadget (the faithful N5 form)
# ----------------------------------------------------------------------

def solve_twoscale(M, k0, k1, budget=3600.0):
    """B0 = (M/2, M], B1 = (M, 2M].  Adversary keeps S0 (>= k0 of B0)
    and S1 (>= k1 of B1).  Hypothesis (T-PIN / non-procrastination):
    every kept B0 value precedes every kept B1 value in the team's
    order.  Constraints: guarded APs among ALL kept triples of B0 u B1
    (cross-block APs (u, y, 2y-u) become the chain attacks
    automatically), block-order units, cardinalities.  SAT <=> escape."""
    assert M % 2 == 0
    V = sorted(range(M // 2 + 1, 2 * M + 1))
    n = len(V)
    idx = {v: i for i, v in enumerate(V)}
    off, top = _mk_vars(n, start=1)
    sel = {}
    for v in V:
        top += 1
        sel[v] = top

    def lit(u, w):
        i, j = idx[u], idx[w]
        return off[(i, j)] if i < j else -off[(j, i)]

    Vs = set(V)
    B0 = [v for v in V if v <= M]
    B1 = [v for v in V if v > M]
    cls = []
    for b in V:
        for d in range(1, min(b - V[0], V[-1] - b) + 1):
            a, c = b - d, b + d
            if a in Vs and c in Vs:
                g = [-sel[a], -sel[b], -sel[c]]
                cls.append(g + [-lit(a, b), -lit(b, c)])
                cls.append(g + [lit(a, b), lit(b, c)])
    for u in B0:
        for w in B1:
            cls.append([-sel[u], -sel[w], lit(u, w)])
    for i in range(n):
        for j in range(i + 1, n):
            xij = off[(i, j)]
            for kk in range(j + 1, n):
                cls.append([-xij, -off[(j, kk)], off[(i, kk)]])
                cls.append([xij, off[(j, kk)], -off[(i, kk)]])
    cards = []
    tid = top
    for blk, bnd in ((B0, k0), (B1, k1)):
        enc = CardEnc.atleast(lits=[sel[v] for v in blk], bound=bnd,
                              top_id=tid, encoding=EncType.seqcounter)
        tid = max(tid, enc.nv)
        cards += enc.clauses
    t0 = time.time()
    with Cadical195(bootstrap_with=cls) as s:
        for c in cards:
            s.add_clause(c)
        ok = s.solve()
        el = round(time.time() - t0, 1)
        if not ok:
            return 'UNSAT', el, {}
        model = set(l for l in s.get_model() if l > 0)
    S = [v for v in V if sel[v] in model]
    posneg = lambda l: (l in model) if l > 0 else (abs(l) not in model)
    wins = {v: 0 for v in S}
    for i, u in enumerate(S):
        for w in S[i + 1:]:
            if posneg(lit(u, w)):
                wins[u] += 1
            else:
                wins[w] += 1
    order = sorted(S, key=lambda v: -wins[v])
    err = check_twoscale(order, S, M, k0, k1)
    S0 = [v for v in S if v <= M]
    S1 = [v for v in S if v > M]
    return ('SAT' if err is None else 'WITNESS-FAIL'), el, \
        {'S0': S0, 'S1': S1,
         'drop0': sorted(set(B0) - set(S0)),
         'drop1': sorted(set(B1) - set(S1)), 'werr': err}


def check_twoscale(order, S, M, k0, k1):
    S0 = [v for v in S if v <= M]
    S1 = [v for v in S if v > M]
    if len(S0) < k0 or len(S1) < k1:
        return f'sizes ({len(S0)}, {len(S1)}) < ({k0}, {k1})'
    p = {v: i for i, v in enumerate(order)}
    for u in S0:
        for w in S1:
            if p[u] > p[w]:
                return f'block order violated ({u}, {w})'
    vals = sorted(S)
    vs = set(vals)
    for b in vals:
        for d in range(1, min(b - vals[0], vals[-1] - b) + 1):
            a, c = b - d, b + d
            if a in vs and c in vs:
                if p[a] < p[b] < p[c] or p[c] < p[b] < p[a]:
                    return f'monotone AP {(a, b, c)}'
    return None


def partD(only=None):
    """Joint density dial: k0 = ceil(rho |B0|), k1 = ceil(rho |B1|);
    binary search rho on a 1/64 grid between 1/2 and 1."""
    print('== e120 PART D: existential-attacker two-scale dial ==',
          flush=True)
    out = {'part': 'D', 'rows': [], 'summary': []}
    import math
    for M in (64, 96, 128):
        tag = f'D M={M}'
        if only and only not in tag:
            continue
        n0, n1 = M // 2, M

        def q(num, den=64):
            k0 = math.ceil(num * n0 / den)
            k1 = math.ceil(num * n1 / den)
            v, el, info = solve_twoscale(M, k0, k1)
            row = {'tag': tag, 'M': M, 'rho': f'{num}/{den}',
                   'k0': k0, 'k1': k1, 'verdict': v, 'time': el,
                   'drop0': info.get('drop0'), 'drop1': info.get('drop1')}
            out['rows'].append(row)
            stream(row)
            print(f'  {tag} rho={num}/{den} (k0={k0}, k1={k1}): {v} '
                  f'[{el}s]' + (f" drop0={info.get('drop0')} "
                                f"drop1={info.get('drop1')}"
                                if v == 'SAT' else ''), flush=True)
            if v == 'WITNESS-FAIL':
                raise RuntimeError(f'{tag}: {info.get("werr")}')
            return v

        # intact control then binary search on the 1/64 grid
        if q(64) != 'UNSAT':
            print(f'  {tag}: intact SAT — no rung', flush=True)
            continue
        lo, hi = 32, 64          # rho = lo/64 .. hi/64
        if q(lo) != 'SAT':
            print(f'  {tag}: UNSAT already at rho=1/2 !', flush=True)
            out['summary'].append({'M': M, 'rho_star': '<=1/2'})
            stream({'tag': tag + ' SUMMARY', 'M': M, 'rho_star': '<=1/2'})
            with open(os.path.join(DATA, 'e120_D.json'), 'w') as f:
                json.dump(out, f, indent=1)
            continue
        while hi - lo > 1:
            mid = (lo + hi) // 2
            if q(mid) == 'SAT':
                lo = mid
            else:
                hi = mid
        s = {'M': M, 'rho_star_grid': f'{lo}/64',
             'rho_star': round(lo / 64, 4),
             'first_unsat': f'{hi}/64'}
        out['summary'].append(s)
        stream({'tag': tag + ' SUMMARY', **s})
        print(f'  >> {tag}: last escape at rho={lo}/64='
              f'{lo / 64:.3f}, UNSAT-for-all from rho={hi}/64', flush=True)
        with open(os.path.join(DATA, 'e120_D.json'), 'w') as f:
            json.dump(out, f, indent=1)
    return out


# ----------------------------------------------------------------------
# Part C: coupled complementary coloring of two consecutive blocks
# ----------------------------------------------------------------------

def solve_coupled(M, kb, budget=3600.0):
    """B0 = (M, 2M], B1 = (2M, 4M].  Coloring c_v in {A, B} (var a_v).
    Each team T: its own order on B0 u B1; guarded AP clauses (all three
    in T); block-order units (every T-value of B0 precedes every T-value
    of B1 — the non-procrastination hypothesis, which is what turns the
    cross-block APs into chain attacks); balance: each team owns >= kb
    of EACH block.  SAT <=> a coloring + two orders escape."""
    V = sorted(range(M + 1, 4 * M + 1))
    n = len(V)
    idx = {v: i for i, v in enumerate(V)}
    offA, top = _mk_vars(n, start=1)
    offB, top = _mk_vars(n, start=top + 1)
    ai = {}
    for v in V:
        top += 1
        ai[v] = top                            # true = team A

    def litT(off):
        def lit(u, w):
            i, j = idx[u], idx[w]
            return off[(i, j)] if i < j else -off[(j, i)]
        return lit

    litA, litB = litT(offA), litT(offB)
    Vs = set(V)
    B0 = [v for v in V if v <= 2 * M]
    B1 = [v for v in V if v > 2 * M]
    cls = []
    for team, lit, g in (('A', litA, lambda v: -ai[v]),
                         ('B', litB, lambda v: ai[v])):
        # g(v) is the guard literal meaning "v NOT in team" when added
        for b in V:
            for d in range(1, min(b - V[0], V[-1] - b) + 1):
                a, c = b - d, b + d
                if a in Vs and c in Vs:
                    gg = [g(a), g(b), g(c)]
                    cls.append(gg + [-lit(a, b), -lit(b, c)])
                    cls.append(gg + [lit(a, b), lit(b, c)])
        # block order: u in B0, w in B1, both in team => u precedes w
        for u in B0:
            for w in B1:
                cls.append([g(u), g(w), lit(u, w)])
        # full transitivity per team (unguarded)
    for off in (offA, offB):
        for i in range(n):
            for j in range(i + 1, n):
                xij = off[(i, j)]
                for kk in range(j + 1, n):
                    cls.append([-xij, -off[(j, kk)], off[(i, kk)]])
                    cls.append([xij, off[(j, kk)], -off[(i, kk)]])
    # balance per block per team
    cards = []
    tid = top
    for blk, bnd in ((B0, kb), (B1, 2 * kb)):   # same DENSITY kb/M per block
        for sign in (1, -1):
            lits = [sign * ai[v] for v in blk]
            enc = CardEnc.atleast(lits=lits, bound=bnd, top_id=tid,
                                  encoding=EncType.seqcounter)
            tid = enc.nv if enc.nv > tid else tid
            cards += enc.clauses
    t0 = time.time()
    with Cadical195(bootstrap_with=cls) as s:
        for c in cards:
            s.add_clause(c)
        ok = s.solve()
        el = round(time.time() - t0, 1)
        if not ok:
            return 'UNSAT', el, {}
        model = set(l for l in s.get_model() if l > 0)
    colA = [v for v in V if ai[v] in model]
    colB = [v for v in V if ai[v] not in model]
    posneg = lambda l: (l in model) if l > 0 else (abs(l) not in model)
    info = {'A': colA, 'B': colB}
    for team, lit, col in (('A', litA, colA), ('B', litB, colB)):
        wins = {v: 0 for v in col}
        for i, u in enumerate(col):
            for w in col[i + 1:]:
                if posneg(lit(u, w)):
                    wins[u] += 1
                else:
                    wins[w] += 1
        order = sorted(col, key=lambda v: -wins[v])
        err = check_coupled_team(order, col, M, kb)
        if err:
            return 'WITNESS-FAIL', el, {'team': team, 'werr': err}
        info[f'order{team}'] = order
    return 'SAT', el, info


def check_coupled_team(order, col, M, kb):
    """Independent: block balance, block order, no monotone AP."""
    b0 = [v for v in col if v <= 2 * M]
    b1 = [v for v in col if v > 2 * M]
    if len(b0) < kb or len(b1) < 2 * kb:
        return f'balance violated ({len(b0)}, {len(b1)}) < ({kb}, {2 * kb})'
    p = {v: i for i, v in enumerate(order)}
    for u in b0:
        for w in b1:
            if p[u] > p[w]:
                return f'block order violated ({u}, {w})'
    vals = sorted(col)
    vs = set(vals)
    for b in vals:
        for d in range(1, min(b - vals[0], vals[-1] - b) + 1):
            a, c = b - d, b + d
            if a in vs and c in vs:
                if p[a] < p[b] < p[c] or p[c] < p[b] < p[a]:
                    return f'monotone AP {(a, b, c)}'
    return None


def partC(only=None):
    print('== e120 PART C: coupled complementary coloring ==', flush=True)
    out = {'part': 'C', 'rows': []}
    for M in (32, 64):
        for kb in (M // 2, 3 * M // 8, M // 4, M // 8):
            tag = f'C M={M} kb={kb}'
            if only and only not in tag:
                continue
            v, el, info = solve_coupled(M, kb)
            row = {'tag': tag, 'M': M, 'kb': kb,
                   'rho_each': round(kb / M, 3), 'verdict': v,
                   'time': el}
            if v == 'SAT':
                row['A_B0'] = len([x for x in info['A'] if x <= 2 * M])
                row['A_B1'] = len([x for x in info['A'] if x > 2 * M])
                row['colorA'] = info['A']
            if v == 'WITNESS-FAIL':
                row['werr'] = info.get('werr')
            out['rows'].append(row)
            stream(row)
            print(f'  {tag}: {v} [{el}s]'
                  + (f" A owns {row.get('A_B0')}/{row.get('A_B1')} "
                     f'of B0/B1' if v == 'SAT' else ''), flush=True)
            with open(os.path.join(DATA, 'e120_C.json'), 'w') as f:
                json.dump(out, f, indent=1)
            if v == 'SAT':
                break            # escapes get easier as kb drops
    return out


# ----------------------------------------------------------------------
# Part C3: coupled complementary coloring over THREE consecutive blocks
# ----------------------------------------------------------------------

def solve_coupled3(M, kb_frac_num, kb_frac_den, budget=3600.0):
    """B0 = (M, 2M], B1 = (2M, 4M], B2 = (4M, 8M].  Same as Part C but
    with THREE blocks and TWO seams: coloring c_v in {A, B}; each team
    its own order; guarded APs (all three in team); block-order units
    at BOTH seams (B0 < B1 < B2 within each team — double
    non-procrastination); balance: each team owns >= (num/den) of EACH
    block.  SAT <=> a coloring + two orders escape the 2-seam coupling."""
    V = sorted(range(M + 1, 8 * M + 1))
    n = len(V)
    idx = {v: i for i, v in enumerate(V)}
    offA, top = _mk_vars(n, start=1)
    offB, top = _mk_vars(n, start=top + 1)
    ai = {}
    for v in V:
        top += 1
        ai[v] = top

    def litT(off):
        def lit(u, w):
            i, j = idx[u], idx[w]
            return off[(i, j)] if i < j else -off[(j, i)]
        return lit

    litA, litB = litT(offA), litT(offB)
    Vs = set(V)
    B0 = [v for v in V if v <= 2 * M]
    B1 = [v for v in V if 2 * M < v <= 4 * M]
    B2 = [v for v in V if v > 4 * M]
    cls = []
    for team, lit, g in (('A', litA, lambda v: -ai[v]),
                         ('B', litB, lambda v: ai[v])):
        for b in V:
            for d in range(1, min(b - V[0], V[-1] - b) + 1):
                a, c = b - d, b + d
                if a in Vs and c in Vs:
                    gg = [g(a), g(b), g(c)]
                    cls.append(gg + [-lit(a, b), -lit(b, c)])
                    cls.append(gg + [lit(a, b), lit(b, c)])
        for lowblk, highblk in ((B0, B1), (B1, B2), (B0, B2)):
            for u in lowblk:
                for w in highblk:
                    cls.append([g(u), g(w), lit(u, w)])
    for off in (offA, offB):
        for i in range(n):
            for j in range(i + 1, n):
                xij = off[(i, j)]
                for kk in range(j + 1, n):
                    cls.append([-xij, -off[(j, kk)], off[(i, kk)]])
                    cls.append([xij, off[(j, kk)], -off[(i, kk)]])
    import math
    cards = []
    tid = top
    bounds = {}
    for blkname, blk in (('B0', B0), ('B1', B1), ('B2', B2)):
        bnd = math.ceil(kb_frac_num * len(blk) / kb_frac_den)
        bounds[blkname] = bnd
        for sign in (1, -1):
            enc = CardEnc.atleast(lits=[sign * ai[v] for v in blk],
                                  bound=bnd, top_id=tid,
                                  encoding=EncType.seqcounter)
            tid = enc.nv if enc.nv > tid else tid
            cards += enc.clauses
    t0 = time.time()
    with Cadical195(bootstrap_with=cls) as s:
        for c in cards:
            s.add_clause(c)
        ok = s.solve()
        el = round(time.time() - t0, 1)
        if not ok:
            return 'UNSAT', el, {'bounds': bounds}
        model = set(l for l in s.get_model() if l > 0)
    colA = [v for v in V if ai[v] in model]
    colB = [v for v in V if ai[v] not in model]
    posneg = lambda l: (l in model) if l > 0 else (abs(l) not in model)
    info = {'A': colA, 'B': colB, 'bounds': bounds}
    for team, lit, col in (('A', litA, colA), ('B', litB, colB)):
        wins = {v: 0 for v in col}
        for i, u in enumerate(col):
            for w in col[i + 1:]:
                if posneg(lit(u, w)):
                    wins[u] += 1
                else:
                    wins[w] += 1
        order = sorted(col, key=lambda v: -wins[v])
        err = check_coupled3_team(order, col, M, bounds)
        if err:
            return 'WITNESS-FAIL', el, {'team': team, 'werr': err}
        info[f'order{team}'] = order
    return 'SAT', el, info


def check_coupled3_team(order, col, M, bounds):
    b0 = [v for v in col if v <= 2 * M]
    b1 = [v for v in col if 2 * M < v <= 4 * M]
    b2 = [v for v in col if v > 4 * M]
    if (len(b0) < bounds['B0'] or len(b1) < bounds['B1']
            or len(b2) < bounds['B2']):
        return (f'balance violated ({len(b0)}, {len(b1)}, {len(b2)})'
                f' < {bounds}')
    p = {v: i for i, v in enumerate(order)}
    for low, high in ((b0, b1), (b1, b2), (b0, b2)):
        for u in low:
            for w in high:
                if p[u] > p[w]:
                    return f'block order violated ({u}, {w})'
    vals = sorted(col)
    vs = set(vals)
    for b in vals:
        for d in range(1, min(b - vals[0], vals[-1] - b) + 1):
            a, c = b - d, b + d
            if a in vs and c in vs:
                if p[a] < p[b] < p[c] or p[c] < p[b] < p[a]:
                    return f'monotone AP {(a, b, c)}'
    return None


def partC3(only=None):
    print('== e120 PART C3: 3-block / 2-seam coupled coloring ==',
          flush=True)
    out = {'part': 'C3', 'rows': []}
    for M in (16, 24, 32):
        tag = f'C3 M={M}'
        if only and only not in tag:
            continue
        v, el, info = solve_coupled3(M, 1, 2)   # exact balance
        row = {'tag': tag, 'M': M, 'balance': '1/2', 'verdict': v,
               'time': el, 'bounds': info.get('bounds')}
        if v == 'SAT':
            row['A_sizes'] = [
                len([x for x in info['A'] if x <= 2 * M]),
                len([x for x in info['A'] if 2 * M < x <= 4 * M]),
                len([x for x in info['A'] if x > 4 * M])]
            row['colorA'] = info['A']
        if v == 'WITNESS-FAIL':
            row['werr'] = info.get('werr')
        out['rows'].append(row)
        stream(row)
        print(f'  {tag} balance=1/2: {v} [{el}s]'
              + (f" A sizes {row.get('A_sizes')}" if v == 'SAT' else ''),
              flush=True)
        with open(os.path.join(DATA, 'e120_C3.json'), 'w') as f:
            json.dump(out, f, indent=1)
    return out


# ----------------------------------------------------------------------
# Part E: fixed pair, TWO-block STG window, per-block density dial
# ----------------------------------------------------------------------

def solve_stg_subset(M, F, k1, k2, budget=3600.0):
    """Window (M, 4M] = block1 (M, 2M] u block2 (2M, 4M]; FIXED
    attacker pair F (low, placed early); adversary keeps >= k1 of
    block1 and >= k2 of block2.  Attack units = attacks_into over the
    kept union (x-attacks into block1, into block2, AND the dense
    channel: y in block1, z = 2y - x in block2); guarded APs on the
    union; full transitivity."""
    V = sorted(range(M + 1, 4 * M + 1))
    n = len(V)
    idx = {v: i for i, v in enumerate(V)}
    off, top = _mk_vars(n, start=1)
    sel = {}
    for v in V:
        top += 1
        sel[v] = top

    def lit(u, w):
        i, j = idx[u], idx[w]
        return off[(i, j)] if i < j else -off[(j, i)]

    Vs = set(V)
    cls = []
    for b in V:
        for d in range(1, min(b - V[0], V[-1] - b) + 1):
            a, c = b - d, b + d
            if a in Vs and c in Vs:
                g = [-sel[a], -sel[b], -sel[c]]
                cls.append(g + [-lit(a, b), -lit(b, c)])
                cls.append(g + [lit(a, b), lit(b, c)])
    for (z, y) in attacks_into(V, F):
        cls.append([-sel[y], -sel[z], lit(z, y)])
    for i in range(n):
        for j in range(i + 1, n):
            xij = off[(i, j)]
            for kk in range(j + 1, n):
                cls.append([-xij, -off[(j, kk)], off[(i, kk)]])
                cls.append([xij, off[(j, kk)], -off[(i, kk)]])
    B1 = [v for v in V if v <= 2 * M]
    B2 = [v for v in V if v > 2 * M]
    cards = []
    tid = top
    for blk, bnd in ((B1, k1), (B2, k2)):
        enc = CardEnc.atleast(lits=[sel[v] for v in blk], bound=bnd,
                              top_id=tid, encoding=EncType.seqcounter)
        tid = max(tid, enc.nv)
        cards += enc.clauses
    t0 = time.time()
    with Cadical195(bootstrap_with=cls) as s:
        for c in cards:
            s.add_clause(c)
        ok = s.solve()
        el = round(time.time() - t0, 1)
        if not ok:
            return 'UNSAT', el, {}
        model = set(l for l in s.get_model() if l > 0)
    S = [v for v in V if sel[v] in model]
    posneg = lambda l: (l in model) if l > 0 else (abs(l) not in model)
    wins = {v: 0 for v in S}
    for i, u in enumerate(S):
        for w in S[i + 1:]:
            if posneg(lit(u, w)):
                wins[u] += 1
            else:
                wins[w] += 1
    order = sorted(S, key=lambda v: -wins[v])
    err = check_escape(order, S, F, 0)
    s1 = [v for v in S if v <= 2 * M]
    s2 = [v for v in S if v > 2 * M]
    if err is None and (len(s1) < k1 or len(s2) < k2):
        err = f'block sizes ({len(s1)}, {len(s2)}) < ({k1}, {k2})'
    return ('SAT' if err is None else 'WITNESS-FAIL'), el, \
        {'drop1': sorted(set(B1) - set(s1)),
         'drop2': sorted(set(B2) - set(s2)), 'werr': err}


def partE(only=None):
    """Per-block density dial rho on the 1/32 grid for the STG
    two-block window with FIXED pair (no varying-attacker caveat)."""
    print('== e120 PART E: fixed pair, STG two-block density dial ==',
          flush=True)
    import math
    out = {'part': 'E', 'rows': [], 'summary': []}
    for M, F in ((32, (15, 16)), (64, (15, 16)), (64, (21, 22))):
        tag = f'E M={M} F={F}'
        if only and only not in tag:
            continue

        def q(num, den=32):
            k1 = math.ceil(num * M / den)
            k2 = math.ceil(num * 2 * M / den)
            v, el, info = solve_stg_subset(M, F, k1, k2)
            row = {'tag': tag, 'M': M, 'F': list(F), 'rho': f'{num}/{den}',
                   'k1': k1, 'k2': k2, 'verdict': v, 'time': el,
                   'drop1': info.get('drop1'), 'drop2': info.get('drop2')}
            out['rows'].append(row)
            stream(row)
            print(f'  {tag} rho={num}/{den} (k1={k1}, k2={k2}): {v} '
                  f'[{el}s]' + (f" drop1={info.get('drop1')} "
                                f"drop2={info.get('drop2')}"
                                if v == 'SAT' else ''), flush=True)
            if v == 'WITNESS-FAIL':
                raise RuntimeError(f'{tag}: {info.get("werr")}')
            return v

        if q(32) != 'UNSAT':
            print(f'  {tag}: intact SAT — rung absent at this scale',
                  flush=True)
            continue
        lo, hi = 16, 32
        if q(lo) != 'SAT':
            print(f'  {tag}: UNSAT already at rho=1/2 !!', flush=True)
            out['summary'].append({'M': M, 'F': list(F),
                                   'rho_star': '<=1/2'})
            stream({'tag': tag + ' SUMMARY', 'M': M, 'rho_star': '<=1/2'})
            with open(os.path.join(DATA, 'e120_E.json'), 'w') as f:
                json.dump(out, f, indent=1)
            continue
        while hi - lo > 1:
            mid = (lo + hi) // 2
            if q(mid) == 'SAT':
                lo = mid
            else:
                hi = mid
        s = {'M': M, 'F': list(F), 'rho_last_escape': f'{lo}/32',
             'rho_star': round(lo / 32, 4), 'first_unsat': f'{hi}/32'}
        out['summary'].append(s)
        stream({'tag': tag + ' SUMMARY', **s})
        print(f'  >> {tag}: last escape rho={lo}/32={lo / 32:.3f}, '
              f'UNSAT-for-all from {hi}/32', flush=True)
        with open(os.path.join(DATA, 'e120_E.json'), 'w') as f:
            json.dump(out, f, indent=1)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--part', required=True)
    ap.add_argument('--only', default=None)
    args = ap.parse_args()
    t0 = time.time()
    if args.part == 'A':
        partA(args.only)
    elif args.part == 'B':
        partB(args.only)
    elif args.part == 'C':
        partC(args.only)
    elif args.part == 'C3':
        partC3(args.only)
    elif args.part == 'D':
        partD(args.only)
    elif args.part == 'E':
        partE(args.only)
    else:
        sys.exit('unknown part')
    print(f'TOTAL {round(time.time() - t0, 1)}s', flush=True)


if __name__ == '__main__':
    main()
