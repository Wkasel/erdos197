"""Erdős #197 — S2: death-mechanism theory for growing reflector sets.

Machine companion to notes/39-growing-death.md.  Context: all fixed-depth
sliver swaps die by lem:orbit (finite reflector set F) or portable crowns
(fixed attackers); the growing-sliver swap survives because its reflectors
and attackers must GROW with scale, voiding both hypotheses.  This file
machine-checks the candidate lemmas that map exactly what death machinery
survives growth:

  CHECK 1 (T-SHARP).  lem:orbit's finite-F hypothesis is SHARP: a greedy
    sparse permutable set containing an infinite doubling orbit
    u_{k+1} = 2 u_k - f_k with DISTINCT, slowly growing reflectors
    (f_k = Theta(k) = Theta(log u_k), the slowest growth beyond
    finiteness).  Finite certificates at 3 sizes: (a) the only 3-APs
    wholly inside S are the K orbit APs (exhaustive), (b) the interleaved
    order u_0 u_1 f_0 u_2 f_1 ... has no monotone 3-AP (exhaustive),
    (c) step-lemma sign audit on every orbit AP (late reflector <->
    ascent).  Consequence: NO theorem of the form "f_k = o(u_k) (or any
    size/growth condition on reflectors alone) => not permutable" exists.

  CHECK 2 (L-STEP / L-DESC finite shadow, SAT).  On explicit orbit
    prefixes of the S1 growing-sliver teams: the constraint set
    {f_k early (f_k < u_k in position) for all k} FORCES position descent
    pos(u_L) < ... < pos(u_0): asserting u_0 before u_L on top is UNSAT,
    asserting u_L before u_0 is SAT.  (Subset windows: UNSAT is sound for
    the full team; SAT side is a consistency demo.)  3 chains at 3 scales.

  CHECK 3 (SLIVER-ORBIT).  Exact existence condition for slow orbits
    (f_k <= C * s(scale)) in the growing-sliver partitions: the sliver
    route kept(t) -> received(t+1) -> kept(t+2) exists iff
        s_{t+2} <= 2 s_{t+1} - 2   (t of owner parity)
    plus in-team reflector availability.  Verified: predicate over
    t <= 200 per schedule/team; certified greedy walks to ~block 200
    (exact big ints, every step asserted); exhaustive blockage
    certificates where the predicate fails (geo / team A).

  CHECK 4 (SG rungs for T-REGRESS).  The scale-adapted crown gadget:
    arrange the kept interval (2^{t-1} + s_t, 2^t] free of monotone 3-APs
    with the attacker x = 2 s_t + c assumed placed before the whole
    window (units: 2y - x before y for every in-window pair).  UNSAT at a
    scale = rung: NO in-team value x of that size can precede its window,
    i.e. some window element w (exponentially larger than x) must precede
    x.  T-REGRESS (notes/39): if rungs hold at all large owner-parity
    scales for an offset window C covering all residues, every in-team
    value is preceded by an exponentially larger in-team value, giving an
    infinite strictly-descending position chain — death.  This REPLACES
    thm:ogred's fixed-attacker pigeonhole (which needed 15, 16 at
    finitely many positions).  Controls: s=0 reproduces OG(M) (known
    UNSAT); tiny attacker c=3 must be SAT (encoder sanity).

Usage:
  .venv/bin/python experiments/s2_growing_death.py sharp|shadow|orbit|sg|all
      [--json data/s2_<part>.json]  [--sg-scales ...] [--budget SECONDS]
"""
import argparse
import json
import os
import sys
import time

import numpy as np

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from g2_diagnose import geneson_blocks  # gm schedule source


# ----------------------------------------------------------------------
# Growing-sliver partitions (S1 family).  Blocks (2^{t-1}, 2^t]; owner
# A for even t, B for odd t; 1 -> B; owner donates the bottom
# min(s_t, |block|) offsets of each of its blocks to the partner.
# ----------------------------------------------------------------------

def octave(v):
    return (v - 1).bit_length()


def sched_lin(t):
    return t


def sched_geo(t):
    return 1 << (t // 2)


def sched_frac(t):
    return (1 << t) // t


_GM_STAGES = None


def _gm_stages():
    """(stage start, M_{k-1}) list from the Geneson construction:
    stage k starts at L_k + M_{k-1} (L_k = 4 M_{k-1}), sliver width
    M_{k-1}, M_k = 2 L_k 4^k.  Cross-checked against g2's
    geneson_blocks first block per stage."""
    global _GM_STAGES
    if _GM_STAGES is None:
        out = [(1, 1)]
        M_prev, k = 1, 0
        while True:
            k += 1
            L = 4 * M_prev
            start = L + M_prev
            if start > (1 << 400):
                break
            out.append((start, M_prev))
            M_prev = 2 * L * 4 ** k
        ref = {}
        for kk, lo, hi in geneson_blocks(1 << 60):
            ref.setdefault(kk, lo)
        for kk, lo in ref.items():
            assert out[kk][0] == lo, "gm stage table disagrees with g2"
        _GM_STAGES = out
    return _GM_STAGES


def sched_gm(t):
    """Geneson-matched: sliver width M_{k-1} of the stage active at 2^t,
    capped at a quarter block (so it stays a sliver)."""
    if t <= 2:
        return 1
    lo = 1 << (t - 1)
    s = 1
    for start, w in _gm_stages():
        if start <= lo:
            s = w
        else:
            break
    return max(1, min(s, 1 << (t - 2)))


SCHEDULES = {'lin': sched_lin, 'geo': sched_geo, 'frac': sched_frac,
             'gm': sched_gm}


def team_of(v, sched):
    """'A' or 'B' for value v under schedule sched (callable t -> s_t)."""
    if v == 1:
        return 'B'
    t = octave(v)
    owner = 'A' if t % 2 == 0 else 'B'
    partner = 'B' if owner == 'A' else 'A'
    o = v - (1 << (t - 1))
    s = min(sched(t), 1 << (t - 1))
    return partner if o <= s else owner


def team_set(name, sched, N):
    return [v for v in range(1, N + 1) if team_of(v, sched) == name]


# ----------------------------------------------------------------------
# Shared SAT core: monotone-3-AP-free linear order of a finite set V
# with optional unit precedences, lazy transitivity (UNSAT-sound: the
# lazy loop only ever ADDS clauses, so UNSAT of the partial system
# implies UNSAT of the full one; SAT is verified on an explicit witness
# including the units).
# ----------------------------------------------------------------------

def ap_order_sat(V, units=(), budget=1800.0, verbose=False):
    """V: sorted values.  units: (a, b) meaning a must precede b.
    Returns dict(result='SAT'|'UNSAT'|'TIMEOUT', ...)."""
    from pysat.solvers import Cadical195
    V = sorted(V)
    n = len(V)
    idx = {v: i for i, v in enumerate(V)}
    off = [0] * n
    for i in range(1, n):
        off[i] = off[i - 1] + (n - i)
    top = n * (n - 1) // 2

    def var(i, j):
        return 1 + off[i] + (j - i - 1)

    def before(u, w):
        i, j = idx[u], idx[w]
        return var(i, j) if i < j else -var(j, i)

    Vs = set(V)
    hi = V[-1]
    cl = []
    nap = 0
    for y in V:
        for d in range(1, min(y - V[0], hi - y) + 1):
            x, z = y - d, y + d
            if x in Vs and z in Vs:
                nap += 1
                cl.append([-before(x, y), -before(y, z)])
                cl.append([-before(z, y), -before(y, x)])
    for a, b in units:
        cl.append([before(a, b)])
    info = {'n': n, 'aps': nap, 'units': len(units)}
    if verbose:
        print(f"    n={n} vars={top} ap_triples={nap} units={len(units)}",
              flush=True)
    s = Cadical195(bootstrap_with=cl)
    t0 = time.time()
    rounds = 0
    while True:
        rounds += 1
        if time.time() - t0 > budget:
            info.update(result='TIMEOUT', rounds=rounds,
                        time=round(time.time() - t0, 1))
            return info
        if not s.solve():
            info.update(result='UNSAT', rounds=rounds,
                        time=round(time.time() - t0, 1))
            return info
        model = s.get_model()
        pos = np.zeros(top + 1, dtype=bool)
        for l in model:
            if 0 < l <= top:
                pos[l] = True
        B = np.zeros((n, n), dtype=bool)
        for i in range(n - 1):
            row = pos[var(i, i + 1): var(i, n - 1) + 1]
            B[i, i + 1:] = row
            B[i + 1:, i] = ~row
        wins = B.sum(axis=1)
        order = np.argsort(-wins, kind='stable')
        R = B[np.ix_(order, order)]
        iu = np.triu_indices(n, 1)
        bad = np.nonzero(~R[iu])[0]
        if len(bad) == 0:
            seq = [V[int(i)] for i in order]
            err = verify_order(seq, units)
            info.update(result='SAT' if err is None else 'WITNESS-FAIL',
                        rounds=rounds, time=round(time.time() - t0, 1),
                        witness_verified=err is None)
            if err is not None:
                info['witness_error'] = err
            return info
        for bi in bad[:30000]:
            a_, b_ = int(iu[0][bi]), int(iu[1][bi])
            i, j = int(order[a_]), int(order[b_])
            ks = np.nonzero(B[i] & B[:, j])[0]
            if len(ks):
                k = int(ks[0])
                s.add_clause([-before(V[i], V[k]), -before(V[k], V[j]),
                              before(V[i], V[j])])
        if verbose and rounds % 20 == 0:
            print(f"    round {rounds} ({time.time()-t0:.0f}s, "
                  f"{len(bad)} viol)", flush=True)


def verify_order(seq, units=()):
    """None if seq has no monotone in-set 3-AP and satisfies units."""
    pos = {v: i for i, v in enumerate(seq)}
    vals = set(seq)
    hi = max(seq)
    lo = min(seq)
    for y in seq:
        for d in range(1, min(y - lo, hi - y) + 1):
            x, z = y - d, y + d
            if x in vals and z in vals:
                if pos[x] < pos[y] < pos[z] or pos[x] > pos[y] > pos[z]:
                    return f"monotone AP {(x, y, z)}"
    for a, b in units:
        if pos[a] > pos[b]:
            return f"unit violated {(a, b)}"
    return None


# ----------------------------------------------------------------------
# CHECK 1 — T-SHARP greedy counterexample
# ----------------------------------------------------------------------

def all_aps(S):
    """All 3-APs (a, b, c), a < b < c, wholly inside the set S."""
    Ss = set(S)
    out = []
    L = sorted(S)
    for i, a in enumerate(L):
        for b in L[i + 1:]:
            c = 2 * b - a
            if c in Ss:
                out.append((a, b, c))
    return out


def build_sharp(K, u0=101, f_start=3):
    """Greedy orbit u_{k+1} = 2 u_k - f_k with strictly increasing
    reflectors, keeping the invariant that the ONLY 3-APs inside
    S = {u_k} u {f_k} are the orbit APs.  Exact big ints."""
    us = [u0]
    fs = []
    S = {u0}
    for k in range(K):
        u = us[-1]
        f = (fs[-1] + 1) if fs else f_start
        while True:
            nxt = 2 * u - f
            trial = S | {f, nxt}
            aps = all_aps(trial)
            allowed = {(fs[i], us[i], us[i + 1]) for i in range(len(fs))}
            allowed.add((f, u, nxt))
            if f not in S and nxt not in S and set(aps) == allowed:
                break
            f += 1
            if f >= u:
                raise RuntimeError("greedy stuck")
        fs.append(f)
        us.append(nxt)
        S = trial
    return us, fs


def check_sharp(sizes=(20, 40, 60)):
    out = {'lemma': 'T-SHARP: permutable set with infinite orbit, distinct '
                    'slowly growing reflectors (finite certificates)',
           'sizes': []}
    for K in sizes:
        t0 = time.time()
        us, fs = build_sharp(K)
        S = sorted(set(us) | set(fs))
        aps = all_aps(S)
        orbit_aps = [(fs[k], us[k], us[k + 1]) for k in range(K)]
        only_orbit = set(aps) == set(orbit_aps)
        # interleaved order u_0 u_1 f_0 u_2 f_1 ... u_K f_{K-1}
        seq = [us[0], us[1]]
        for k in range(1, K):
            seq += [fs[k - 1], us[k + 1]]
        seq.append(fs[K - 1])
        pos = {v: i for i, v in enumerate(seq)}
        mono = None
        for (a, b, c) in aps:
            if pos[a] < pos[b] < pos[c] or pos[a] > pos[b] > pos[c]:
                mono = (a, b, c)
                break
        # step-lemma sign audit: reflector late <-> ascent
        sign_ok = all((pos[fs[k]] > pos[us[k]]) ==
                      (pos[us[k + 1]] > pos[us[k]]) for k in range(K))
        growth = max(fs[k] / us[k] for k in range(K))
        entry = {'K': K, 'u0': us[0], 'f_first': fs[0], 'f_last': fs[-1],
                 'u_last_bits': us[-1].bit_length(),
                 'aps_in_S': len(aps), 'only_orbit_aps': bool(only_orbit),
                 'order_monotone_ap': mono,
                 'order_valid': mono is None,
                 'step_sign_rule_holds': bool(sign_ok),
                 'max_f_over_u': growth,
                 'reflectors_distinct': len(set(fs)) == K,
                 'time': round(time.time() - t0, 2)}
        entry['pass'] = bool(only_orbit and mono is None and sign_ok
                             and len(set(fs)) == K)
        out['sizes'].append(entry)
        print(f"  T-SHARP K={K}: only_orbit={only_orbit} "
              f"order_valid={mono is None} sign_rule={sign_ok} "
              f"f: {fs[0]}..{fs[-1]} (distinct), u_K ~ 2^"
              f"{us[-1].bit_length()}  max f/u={growth:.2e}  "
              f"-> {'PASS' if entry['pass'] else 'FAIL'}", flush=True)
    out['pass'] = all(e['pass'] for e in out['sizes'])
    return out


# ----------------------------------------------------------------------
# CHECK 3 — slow-orbit existence in the S1 partitions
# ----------------------------------------------------------------------

def team_values_in(lo, hi, team, sched, limit=8, prefer='high'):
    """Up to `limit` values of `team` in [lo, hi], taken from the ends of
    the team's segments (donated slivers / kept bodies) intersecting the
    interval.  O(#octaves) — works for astronomically large intervals.
    prefer='high' returns large values first, 'low' small values first."""
    out = []
    if lo > hi or hi < 1:
        return out
    lo = max(lo, 1)
    r_hi, r_lo = octave(hi), octave(max(lo, 2))
    octs = range(r_hi, r_lo - 1, -1) if prefer == 'high' \
        else range(r_lo, r_hi + 1)
    if prefer == 'low' and lo <= 1 <= hi and team == 'B':
        out.append(1)
    for r in octs:
        if r < 1:
            continue
        blo = 1 << (r - 1)
        s = min(sched(r), blo)
        owner = 'A' if r % 2 == 0 else 'B'
        partner = 'B' if owner == 'A' else 'A'
        segs = []
        if partner == team:
            segs.append((blo + 1, blo + s))          # donated sliver
        if owner == team:
            segs.append((blo + s + 1, 2 * blo))      # kept body
        if prefer == 'high':
            segs = segs[::-1]
        for a, b in segs:
            a2, b2 = max(a, lo), min(b, hi)
            if a2 <= b2:
                ends = (b2, a2) if prefer == 'high' else (a2, b2)
                out.append(ends[0])
                if a2 != b2:
                    out.append(ends[1])
                if b2 - a2 > 1:
                    out.append((a2 + b2) // 2)
        if len(out) >= 4 * limit:
            break
    if prefer == 'high' and lo <= 1 <= hi and team == 'B':
        out.append(1)
    # dedupe, keep order (high octaves / segment tops first)
    seen, res = set(), []
    for v in out:
        if v not in seen:
            seen.add(v)
            res.append(v)
        if len(res) >= limit:
            break
    return res


def slow_orbit_walk(sched_name, team, t0, n_blocks, cap_mult=6,
                    o_span=None, branch=8, node_budget=200000):
    """Bounded-branching DFS for a sliver-route orbit
    kept(t) -> received(t+1) -> kept(t+2) with all reflectors
    f <= cap_mult * max(s at the step), everything in-team, exact big
    ints.  Candidate reflectors are drawn from team-segment ends inside
    the feasible interval (no offset enumeration, so huge schedules like
    s_t = 2^t/t are fine).  Returns (chain [(t, offset, kind)],
    reflectors) or None."""
    sched = SCHEDULES[sched_name]
    sys.setrecursionlimit(20000)
    target_t = t0 + 2 * n_blocks
    nodes = [0]

    def dfs(t, o, kind, chain, refl):
        if t >= target_t:
            return chain, refl
        if nodes[0] > node_budget:
            return None
        nodes[0] += 1
        s_next = min(sched(t + 1), 1 << t)   # block t+1 donated depth
        cap = cap_mult * max(sched(t), sched(t + 1), sched(t + 2))
        if kind == 'kept':
            # -> received sliver of t+1: o2 = 2o - f in [1, s_next]
            f_lo, f_hi = max(1, 2 * o - s_next), 2 * o - 1
        else:
            # -> kept body of t+1: o2 = 2o - f in (s_next, s_next + cap]
            f_lo, f_hi = max(1, 2 * o - s_next - cap), 2 * o - s_next - 1
        f_hi = min(f_hi, cap)            # slow-reflector cap
        nkind = 'recv' if kind == 'kept' else 'kept'
        pref = 'low' if kind == 'kept' else 'high'
        for f in team_values_in(f_lo, f_hi, team, sched, limit=branch,
                                prefer=pref):
            o2 = 2 * o - f
            r = dfs(t + 1, o2, nkind,
                    chain + [(t + 1, o2, nkind)], refl + [f])
            if r:
                return r
        return None

    s0 = min(sched(t0), 1 << (t0 - 1))
    span = o_span or min(cap_mult * max(1, sched(t0)), 1 << (t0 - 2))
    for o in range(s0 + 1, min(s0 + span, 1 << (t0 - 1)) + 1):
        v = (1 << (t0 - 1)) + o
        if team_of(v, sched) == team:
            r = dfs(t0, o, 'kept', [(t0, o, 'kept')], [])
            if r:
                return r
    return None


def verify_chain(sched_name, team, chain, refl, cap_mult):
    """Assert the walk is a genuine in-team orbit with slow reflectors."""
    sched = SCHEDULES[sched_name]
    vals = [(1 << (t - 1)) + o for (t, o, _) in chain]
    assert all(team_of(v, sched) == team for v in vals), "chain not in-team"
    assert all(team_of(f, sched) == team for f in refl), "refl not in-team"
    for i, f in enumerate(refl):
        assert vals[i + 1] == 2 * vals[i] - f, "orbit relation broken"
        assert vals[i + 1] > vals[i], "not increasing"
        t = chain[i][0]
        cap = cap_mult * max(sched(t), sched(t + 1), sched(t + 2))
        assert f <= cap, f"reflector {f} above slow cap {cap} at t={t}"
    return True


def sliver_orbit_condition(sched, parity, tmax=200):
    """t of owner parity with s_{t+2} > 2 s_{t+1} - 2 (route blocked)."""
    bad = []
    for t in range(4, tmax):
        if t % 2 == parity:
            if min(sched(t + 2), 1 << (t + 1)) > \
               2 * min(sched(t + 1), 1 << t) - 2:
                bad.append(t)
    return bad


def blockage_certificate(sched_name, team, scales, cap_mult=6):
    """At each scale t (owner parity): certify no continuation
    received(t+1) -> kept(t+2) exists.  The continuation needs an
    o2 <= s_{t+1} with 2 o2 - 1 >= s_{t+2} + 1, i.e. it is IMPOSSIBLE
    for every o2 (regardless of reflectors or team membership) iff
    s_{t+2} > 2 s_{t+1} - 2 — a pure inequality certificate.  When the
    inequality fails we fall back to bounded enumeration."""
    sched = SCHEDULES[sched_name]
    rows = []
    for t in scales:
        s1 = min(sched(t + 1), 1 << t)
        s2 = min(sched(t + 2), 1 << (t + 1))
        cap = cap_mult * max(sched(t + 1), sched(t + 2))
        if s2 > 2 * s1 - 2:
            rows.append({'t': t, 's_t1': s1, 's_t2': s2,
                         'certificate': 'inequality s_{t+2} > 2 s_{t+1} - 2'
                                        ' (independent of reflectors)',
                         'blocked': True})
            continue
        found = None
        for o2 in range(1, min(s1, 1 << 20) + 1):
            hi_o = min(2 * o2 - 1, s2 + cap)
            for o3 in range(s2 + 1, hi_o + 1):
                f = 2 * o2 - o3
                if 1 <= f and team_of(f, sched) == team:
                    found = (o2, o3, f)
                    break
            if found:
                break
        rows.append({'t': t, 's_t1': s1, 's_t2': s2, 'cap': cap,
                     'continuation': found, 'blocked': found is None,
                     'certificate': 'bounded enumeration'})
    return rows


def check_orbit():
    out = {'lemma': 'SLIVER-ORBIT: slow route exists iff '
                    's_{t+2} <= 2 s_{t+1} - 2 at owner parity '
                    '(+ in-team reflector availability)',
           'results': []}
    cases = [('lin', 'A', 0), ('lin', 'B', 1),
             ('geo', 'A', 0), ('geo', 'B', 1),
             ('frac', 'A', 0), ('frac', 'B', 1),
             ('gm', 'A', 0), ('gm', 'B', 1)]
    for sched_name, team, parity in cases:
        sched = SCHEDULES[sched_name]
        bad = sliver_orbit_condition(sched, parity)
        # one blocked scale kills the route THERE; the route dies iff
        # blocked scales recur unboundedly (else start above them).
        big_bad = [t for t in bad if t >= 10]
        predicted = 'BLOCKED' if big_bad else 'EXISTS'
        entry = {'schedule': sched_name, 'team': team,
                 'condition_violations_t<=200': len(bad),
                 'violations_t>=10': big_bad[:12],
                 'last_violation': (bad[-1] if bad else None),
                 'predicted': predicted}
        if predicted == 'EXISTS':
            t0 = 12 if parity == 0 else 13
            got = None
            for tries in (200, 100, 50):
                got = slow_orbit_walk(sched_name, team, t0, tries)
                if got:
                    break
            if got:
                chain, refl = got
                verify_chain(sched_name, team, chain, refl, cap_mult=6)
                smax = max(min(sched(t), 1 << (t - 1))
                           for (t, _, _) in chain)
                entry.update(
                    walk_blocks=len(chain) - 1,
                    walk_top_octave=chain[-1][0],
                    walk_verified=True,
                    max_reflector=max(refl),
                    max_s_along_walk=smax,
                    chain_head=[(t, o, k) for (t, o, k) in chain[:8]],
                    reflectors_head=refl[:8],
                    reflectors_distinct=len(set(refl)),
                    outcome='EXISTS (certified walk, exact ints)')
            else:
                entry.update(outcome='NOT FOUND (predicted exists!)',
                             walk_verified=False)
        else:
            scales = big_bad[:3] if len(big_bad) >= 3 else big_bad
            rows = blockage_certificate(sched_name, team, scales)
            entry.update(blockage=rows,
                         outcome='BLOCKED (exhaustive at 3 scales)'
                         if all(r['blocked'] for r in rows)
                         else 'LEAK (predicted blocked!)')
        ok = (('EXISTS' in entry['outcome']) == (predicted == 'EXISTS'))
        entry['prediction_confirmed'] = bool(ok)
        out['results'].append(entry)
        print(f"  SLIVER-ORBIT {sched_name}/{team}: predicted {predicted} "
              f"-> {entry['outcome']}", flush=True)
    out['pass'] = all(e['prediction_confirmed'] for e in out['results'])
    return out


# ----------------------------------------------------------------------
# CHECK 2 — descent finite shadow on real S1 chains
# ----------------------------------------------------------------------

def check_shadow():
    out = {'lemma': 'L-STEP/L-DESC shadow: reflectors-early forces '
                    'pos(u_L) < ... < pos(u_0) on S1 orbit prefixes',
           'cases': []}
    specs = [('lin', 'A', 12, 3), ('lin', 'A', 14, 4), ('lin', 'B', 13, 5)]
    for sched_name, team, t0, blocks in specs:
        got = slow_orbit_walk(sched_name, team, t0, blocks)
        if not got:
            out['cases'].append({'spec': (sched_name, team, t0, blocks),
                                 'result': 'NO-CHAIN'})
            continue
        chain, refl = got
        verify_chain(sched_name, team, chain, refl, cap_mult=6)
        us = [(1 << (t - 1)) + o for (t, o, _) in chain]
        V = sorted(set(us) | set(refl))
        early = [(refl[k], us[k]) for k in range(len(refl))]
        r_bad = ap_order_sat(V, units=early + [(us[0], us[-1])], budget=120)
        r_ok = ap_order_sat(V, units=early + [(us[-1], us[0])], budget=120)
        entry = {'spec': [sched_name, team, t0, blocks],
                 'chain_len': len(us), 'u0': us[0], 'uL': us[-1],
                 'reflectors': refl,
                 'early+u0_before_uL': r_bad['result'],
                 'early+uL_before_u0': r_ok['result'],
                 'pass': r_bad['result'] == 'UNSAT'
                 and r_ok['result'] == 'SAT'}
        out['cases'].append(entry)
        print(f"  SHADOW {sched_name}/{team} t0={t0} L={len(us)-1}: "
              f"early+u0<uL={r_bad['result']} (want UNSAT), "
              f"early+uL<u0={r_ok['result']} (want SAT) -> "
              f"{'PASS' if entry['pass'] else 'FAIL'}", flush=True)
    out['pass'] = all(c.get('pass') for c in out['cases'])
    return out


# ----------------------------------------------------------------------
# CHECK 4 — SG(t, c) rungs
# ----------------------------------------------------------------------

def sg_gadget(sched_name, t, cs, ext_sliver=False, budget=1800,
              s_override=None):
    """Kept interval of block t + attacker(s) x = 2 s_t + c assumed early.
    cs: tuple of attacker offsets used jointly."""
    sched = SCHEDULES[sched_name] if sched_name else (lambda _t: 0)
    M = 1 << (t - 1)
    s = s_override if s_override is not None \
        else min(sched(t), 1 << (t - 1))    # same convention as team_of
    V = list(range(M + s + 1, 2 * M + 1))
    if len(V) < 8:
        return {'result': 'TRIVIAL', 'n': len(V), 't': t, 's': s}
    if ext_sliver:
        s_next = min(sched(t + 1), 1 << (t - 1))
        V += list(range(2 * M + 1, 2 * M + s_next + 1))
    Vs = set(V)
    units = []
    attackers = []
    for c in cs:
        x = 2 * s + c
        attackers.append(x)
        for y in V:
            z = 2 * y - x
            if z in Vs:
                units.append((z, y))
    r = ap_order_sat(V, units=units, budget=budget)
    r.update(schedule=sched_name or 'none', t=t, M=M, s=s, cs=list(cs),
             attackers=attackers, ext_sliver=ext_sliver)
    return r


def sg_c3(sched_name, t, budget=1800, s_override=None):
    """C3-shifted 3-precedence core on the truncated window: units
    {t5 < b'5, t3 < b'6, t10 < b'3} with b'_j = M + s + j, t_i = 2M - i
    (the completions are s-independent).  These are exactly the forced
    precedences of attackers x1 = 2s+15 (j=5,6) and x2 = 2s+16 (j=3),
    so UNSAT here implies UNSAT of the pair SG gadget a fortiori — and
    it is the direct test of whether thm:c3core survives truncation."""
    sched = SCHEDULES[sched_name] if sched_name else (lambda _t: 0)
    M = 1 << (t - 1)
    s = s_override if s_override is not None \
        else min(sched(t), 1 << (t - 1))
    V = list(range(M + s + 1, 2 * M + 1))
    units = [(2 * M - 5, M + s + 5), (2 * M - 3, M + s + 6),
             (2 * M - 10, M + s + 3)]
    r = ap_order_sat(V, units=units, budget=budget)
    r.update(schedule=sched_name or 'none', t=t, M=M, s=s,
             core='C3-shifted', units_used=units)
    return r


def check_c3(scales=(9, 10, 11, 12), budget=3000, jsonl=None):
    out = {'lemma': 'C3-shifted core on truncated windows '
                    '(thm:c3core truncation survival)', 'cases': []}
    # control: s=0 is the original C3 (known UNSAT at M = 0 mod 8)
    r = sg_c3(None, 10, budget=budget, s_override=0)
    r['want'] = 'UNSAT (original C3, M=512)'
    out['cases'].append(r)
    print(f"  C3 control s=0 t=10: {r['result']} [{r['time']}s]",
          flush=True)
    if jsonl:
        with open(jsonl, 'a') as fh:
            fh.write(json.dumps({'kind': 'c3', **r}, default=str) + '\n')
    for sched_name in ('lin', 'geo', 'frac', 'gm'):
        for t in scales:
            r = sg_c3(sched_name, t, budget=budget)
            out['cases'].append(r)
            print(f"  C3-shifted {sched_name} t={t} s={r['s']}: "
                  f"{r['result']} [{r.get('time')}s, n={r['n']}]",
                  flush=True)
            if jsonl:
                with open(jsonl, 'a') as fh:
                    fh.write(json.dumps({'kind': 'c3', **r},
                                        default=str) + '\n')
    return out


def sg_sacrifice(sched_name, t, c1=15, c2=16, k=0, budget=900,
                 s_override=None):
    """Quantitative sacrifice rung.  x1 = 2s+c1 assumed early (units);
    x2 = 2s+c2 is an ORDER ELEMENT whose attacks are conditional (the
    generic AP clauses on V = W u {x2} express them), plus a cardinality
    constraint: at most k window elements precede x2.  k=0 is the pair
    rung.  The minimal SAT k is the forced sacrifice depth: at least
    that many window elements must precede the sacrificed attacker."""
    from pysat.solvers import Cadical195
    from pysat.card import CardEnc, EncType
    sched = SCHEDULES[sched_name] if sched_name else (lambda _t: 0)
    M = 1 << (t - 1)
    s = s_override if s_override is not None \
        else min(sched(t), 1 << (t - 1))
    x1, x2 = 2 * s + c1, 2 * s + c2
    W = list(range(M + s + 1, 2 * M + 1))
    V = sorted(W + [x2])
    n = len(V)
    idx = {v: i for i, v in enumerate(V)}
    off = [0] * n
    for i in range(1, n):
        off[i] = off[i - 1] + (n - i)
    top = n * (n - 1) // 2

    def var(i, j):
        return 1 + off[i] + (j - i - 1)

    def before(u, w):
        i, j = idx[u], idx[w]
        return var(i, j) if i < j else -var(j, i)

    Vs = set(V)
    hi = V[-1]
    cl = []
    for y in V:
        for d in range(1, min(y - V[0], hi - y) + 1):
            a, z = y - d, y + d
            if a in Vs and z in Vs:
                cl.append([-before(a, y), -before(y, z)])
                cl.append([-before(z, y), -before(y, a)])
    Ws = set(W)
    for y in W:                      # x1 unconditional attacks
        z = 2 * y - x1
        if z in Ws:
            cl.append([before(z, y)])
    lits = [before(w, x2) for w in W]
    card = CardEnc.atmost(lits=lits, bound=k, top_id=top,
                          encoding=EncType.seqcounter)
    cl.extend(card.clauses)
    sol = Cadical195(bootstrap_with=cl)
    t0 = time.time()
    rounds = 0
    while True:
        rounds += 1
        if time.time() - t0 > budget:
            return {'result': 'TIMEOUT', 'k': k, 't': t, 's': s,
                    'time': round(time.time() - t0, 1)}
        if not sol.solve():
            return {'result': 'UNSAT', 'k': k, 't': t, 's': s,
                    'x1': x1, 'x2': x2, 'n': n,
                    'time': round(time.time() - t0, 1)}
        model = sol.get_model()
        pos = np.zeros(top + 1, dtype=bool)
        for l in model:
            if 0 < l <= top:
                pos[l] = True
        B = np.zeros((n, n), dtype=bool)
        for i in range(n - 1):
            row = pos[var(i, i + 1): var(i, n - 1) + 1]
            B[i, i + 1:] = row
            B[i + 1:, i] = ~row
        wins = B.sum(axis=1)
        order = np.argsort(-wins, kind='stable')
        R = B[np.ix_(order, order)]
        iu = np.triu_indices(n, 1)
        bad = np.nonzero(~R[iu])[0]
        if len(bad) == 0:
            seq = [V[int(i)] for i in order]
            err = verify_order(seq)
            pre = [w for w in seq[:seq.index(x2)] if w != x2]
            entry = {'result': 'SAT', 'k': k, 't': t, 's': s,
                     'x1': x1, 'x2': x2, 'n': n,
                     'witness_verified': err is None,
                     'window_before_x2': pre,
                     'time': round(time.time() - t0, 1)}
            if err is not None:
                entry['result'] = 'WITNESS-FAIL'
                entry['err'] = err
            # verify x1 attacks + cardinality on the witness
            p = {v: i for i, v in enumerate(seq)}
            for y in W:
                z = 2 * y - x1
                if z in Ws and p[z] > p[y]:
                    entry['result'] = 'WITNESS-FAIL'
                    entry['err'] = f'x1 attack ({z},{y})'
            if len(pre) > k:
                entry['result'] = 'WITNESS-FAIL'
                entry['err'] = f'cardinality {len(pre)} > {k}'
            return entry
        for bi in bad[:30000]:
            a_, b_ = int(iu[0][bi]), int(iu[1][bi])
            i, j = int(order[a_]), int(order[b_])
            ks = np.nonzero(B[i] & B[:, j])[0]
            if len(ks):
                kk = int(ks[0])
                sol.add_clause([-before(V[i], V[kk]),
                                -before(V[kk], V[j]),
                                before(V[i], V[j])])


def check_sg(scale_sets=None, budget=1800, jsonl=None,
             skip_controls=False):
    out = {'lemma': 'SG(t, c) rungs: kept interval (2^{t-1}+s_t, 2^t] '
                    'UNSAT with attacker 2 s_t + c early '
                    '(T-REGRESS per-scale rungs)',
           'controls': [], 'rungs': []}

    def emit(kind, r):
        if jsonl:
            with open(jsonl, 'a') as fh:
                fh.write(json.dumps({'kind': kind, **r},
                                    default=str) + '\n')

    if not skip_controls:
        # controls: s=0 == OG(M) (known UNSAT); c=3 sanity SAT
        for t, cs, want in [(9, (15, 16), 'UNSAT'),
                            (10, (15, 16), 'UNSAT'),
                            (9, (3,), 'SAT')]:
            r = sg_gadget(None, t, cs, budget=budget, s_override=0)
            r['want'] = want
            r['ok'] = r['result'] == want
            out['controls'].append(r)
            emit('control', r)
            print(f"  SG control s=0 t={t} cs={cs}: {r['result']} "
                  f"(want {want}) [{r['time']}s]", flush=True)
    if scale_sets is None:
        scale_sets = {'lin': [9, 10, 11, 12],
                      'geo': [9, 10, 11, 12],
                      'frac': [9, 10, 11, 12],
                      'gm': [9, 10, 11, 12]}
    for sched_name, scales in scale_sets.items():
        for t in scales:
            team = 'A' if t % 2 == 0 else 'B'      # owner parity
            configs = [(15, 16)]
            if t <= 10:
                configs += [(15,), (16,), (17,), (18,)]
                if sched_name in ('geo', 'gm'):
                    configs += [(63,), (64,)]      # wide-offset probes
            for cs in configs:
                r = sg_gadget(sched_name, t, cs, budget=budget)
                r['team'] = team
                x_in = [team_of(x, SCHEDULES[sched_name]) == team
                        for x in r.get('attackers', [])]
                r['attacker_in_team'] = x_in
                out['rungs'].append(r)
                emit('rung', r)
                print(f"  SG {sched_name}/{team} t={t} s={r['s']} "
                      f"cs={cs} x={r.get('attackers')} in-team={x_in}: "
                      f"{r['result']} [{r.get('time')}s, n={r['n']}]",
                      flush=True)
    return out


# ----------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('part', choices=['sharp', 'shadow', 'orbit', 'sg',
                                     'c3', 'all'])
    ap.add_argument('--json', default=None)
    ap.add_argument('--budget', type=float, default=1800)
    ap.add_argument('--sg-sched', default=None,
                    help='restrict sg to one schedule')
    ap.add_argument('--sg-scales', default=None,
                    help='comma list of t values for sg')
    args = ap.parse_args()

    results = {}
    if args.part in ('sharp', 'all'):
        print("== CHECK 1: T-SHARP ==", flush=True)
        results['sharp'] = check_sharp()
    if args.part in ('orbit', 'all'):
        print("== CHECK 3: SLIVER-ORBIT ==", flush=True)
        results['orbit'] = check_orbit()
    if args.part in ('shadow', 'all'):
        print("== CHECK 2: descent shadow ==", flush=True)
        results['shadow'] = check_shadow()
    if args.part in ('c3', 'all'):
        print("== CHECK 4b: C3-shifted cores ==", flush=True)
        scales = tuple(int(x) for x in
                       (args.sg_scales or '9,10,11,12').split(','))
        jsonl = os.path.join(REPO, 'data', 's2_sg_rungs.jsonl')
        results['c3'] = check_c3(scales=scales, budget=args.budget,
                                 jsonl=jsonl)
    if args.part in ('sg', 'all'):
        print("== CHECK 4: SG rungs ==", flush=True)
        ss = None
        if args.sg_sched:
            scales = [int(x) for x in
                      (args.sg_scales or '9,10,11,12').split(',')]
            ss = {args.sg_sched: scales}
        jsonl = os.path.join(REPO, 'data', 's2_sg_rungs.jsonl')
        results['sg'] = check_sg(scale_sets=ss, budget=args.budget,
                                 jsonl=jsonl,
                                 skip_controls=bool(args.sg_sched)
                                 and args.sg_sched != 'lin')

    path = args.json or os.path.join(REPO, 'data', f's2_{args.part}.json')
    with open(path, 'w') as fh:
        json.dump(results, fh, indent=1, default=str)
    print(f"saved {path}", flush=True)


if __name__ == '__main__':
    main()
