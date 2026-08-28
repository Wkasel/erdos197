"""e147: the ADV(M) CEGAR loop for COV(M)  (notes/56 SS2).

ADV(M): coloring-only SAT on CORE'(M) — one Boolean per value (true =
team A) — with
  (i)   straddle-freeness for both teams,
  (ii)  per-team per-block lower bounds (default (2,2,2)),
  (iii) for every death pattern S in the catalogue and both teams:
        "S is not monochromatic".
While ADV is SAT: take the witness coloring chi, evaluate all six
block theories Th_i(T) (Lemma U); at least one is UNSAT (the e135
lock + Lemma U guarantee this for every straddle-free bounded
coloring); extract an assumption-core, deletion-minimize it, validate
its value support as a death pattern (e146 restricted-theory
checkers), and add it to the catalogue.  UNSAT = COV(M) holds with
the final catalogue.

WLOG chi(M+1) = A (team-swap symmetry; all constraints are
swap-invariant).

Run: .venv/bin/python experiments/e147_adv_cegar.py M [maxiter] [b0 b1 b2]
Out: data/e147_cegar_M{M}.json (discovered patterns + witness anatomy)
Log: data/e147_cegar_M{M}.log
"""
import json
import os
import sys
import time
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from e146_dp_catalogue import (th1_restricted_unsat, th2_restricted_unsat,
                               _order_theory_unsat)

from pysat.solvers import Cadical195
from pysat.card import CardEnc, EncType


def core_support(M):
    P0 = list(range(M + 1, 2 * M + 1))
    P1 = list(range(3 * M - 15, 4 * M + 1))
    P2 = list(range(4 * M + 1, 6 * M + 16))
    return P0, P1, P2


def th0_restricted_unsat(M, S):
    """Th_0[S]: APs inside S cap P0 + (0,0,1)-units with completion
    in S cap P1."""
    S = set(S)
    U = sorted(v for v in S if v <= 2 * M)
    Us = set(U)
    aps = []
    for b in U:
        for d in range(1, min(b - (M + 1), 2 * M - b) + 1):
            if b - d in Us and b + d in Us:
                aps.append((b - d, b, b + d))
    units = []
    for a in U:
        for b in U:
            if b <= a:
                continue
            c = 2 * b - a
            if c > 2 * M and c in S:
                units.append((b, a))          # b before a
    return _order_theory_unsat(U, aps, units)


RESTRICTED = {0: th0_restricted_unsat, 1: th1_restricted_unsat,
              2: th2_restricted_unsat}


# ----------------------------------------------------------------------
# guarded block theories under a coloring (constraint lists)
# ----------------------------------------------------------------------

def block_theory_constraints(M, i, T, Tset):
    """Constraints of Th_i(T) under the coloring (T = sorted team
    values, Tset = set(T)).  Returns (points, constraints) with each
    constraint ('ap'|'unit', a, b, c) meaning: 'ap' = midpoint rule on
    (a,b,c); 'unit' on pattern-specific pair, stored with its full AP
    (a,b,c) and the forced pair derived per block table."""
    P0hi, P1lo, P1hi, P2lo, P2hi = (2 * M, 3 * M - 15, 4 * M,
                                    4 * M + 1, 6 * M + 15)
    if i == 0:
        pts = [v for v in T if v <= P0hi]
    elif i == 1:
        pts = [v for v in T if P1lo <= v <= P1hi]
    else:
        pts = [v for v in T if v >= P2lo]
    ps = set(pts)
    cons = []
    lo, hi = (pts[0], pts[-1]) if pts else (0, -1)
    for b in pts:
        for d in range(1, max(b - lo, hi - b) + 1):
            a, c = b - d, b + d
            if a in ps and c in ps:
                cons.append(('ap', a, b, c))
    if i == 0:
        for a in pts:
            for b in pts:
                if b <= a:
                    continue
                c = 2 * b - a
                if c > P0hi and c in Tset:
                    cons.append(('unit', a, b, c))     # b < a
    elif i == 1:
        for b in pts:                                  # alpha: c < b
            for c in pts:
                if c <= b:
                    continue
                a = 2 * b - c
                if a <= P0hi and a in Tset:
                    cons.append(('unit', a, b, c))
        for a in pts:                                  # beta: b < a
            for b in pts:
                if b <= a:
                    continue
                c = 2 * b - a
                if c >= P2lo and c in Tset:
                    cons.append(('unit', a, b, c))
    else:
        for b in pts:                                  # c < b
            for c in pts:
                if c <= b:
                    continue
                a = 2 * b - c
                if a < P2lo and a in Tset:
                    cons.append(('unit', a, b, c))
    return pts, cons


def theory_mus(M, i, T, cap_min=150, n_mus=4):
    """Solve Th_i(T); if UNSAT return a list of (support, constraints)
    pairs — up to n_mus distinct deletion-minimized cores (shuffled
    orders) — else None."""
    Tset = set(T)
    pts, cons = block_theory_constraints(M, i, T, Tset)
    if len(pts) < 3:
        return None
    idx = {v: k for k, v in enumerate(pts)}
    n = len(pts)
    off = {}
    top = 0
    for a in range(n):
        for b in range(a + 1, n):
            top += 1
            off[(a, b)] = top

    def lit(u, w):
        x, y = idx[u], idx[w]
        return off[(x, y)] if x < y else -off[(y, x)]

    cls = []
    for a in range(n):
        for b in range(a + 1, n):
            for c in range(b + 1, n):
                x, y, z = off[(a, b)], off[(b, c)], off[(a, c)]
                cls.append([-x, -y, z])
                cls.append([x, y, -z])
    sel = {}
    P1lo = 3 * M - 15
    for k, con in enumerate(cons):
        top += 1
        s = top
        sel[s] = con
        kind, a, b, c = con
        if kind == 'ap':
            cls.append([-s, -lit(a, b), -lit(b, c)])
            cls.append([-s, lit(a, b), lit(b, c)])
        else:
            if i == 0:
                u, w = b, a
            elif i == 2:
                u, w = c, b
            else:
                # block 1: attacker in P0 -> alpha (c < b);
                #          completion in P2 -> beta (b < a)
                if a < P1lo:
                    u, w = c, b
                else:
                    u, w = b, a
            cls.append([-s, lit(u, w)])
    def shrink(slv, start):
        core = set(start)
        for s in sorted(core, reverse=True):
            if s not in core:
                continue
            trial = sorted(core - {s})
            if not slv.solve(assumptions=trial):
                nc = set(slv.get_core() or trial)
                core = nc & set(trial)
        return core

    results = []
    seen_supports = set()

    def emit(core):
        used = [sel[s] for s in sorted(core)]
        supp = set()
        for (_, a, b, c) in used:
            supp.update((a, b, c))
        key = tuple(sorted(supp))
        if key not in seen_supports:
            seen_supports.add(key)
            results.append((sorted(supp), used))

    with Cadical195(bootstrap_with=cls) as slv:
        asel = sorted(sel)
        if slv.solve(assumptions=asel):
            return None
        core0 = set(slv.get_core() or asel) & set(asel)
        if len(core0) > cap_min:
            emit(core0)
            return results
        mus1 = shrink(slv, core0)
        emit(mus1)
        # diversify: ban one constraint of mus1 at a time (CAMUS step)
        banned_tries = sorted(mus1)[:: max(1, len(mus1) // max(1, n_mus - 1))]
        for c in banned_tries:
            if len(results) >= n_mus:
                break
            rest = sorted(set(asel) - {c})
            if not slv.solve(assumptions=rest):
                core = set(slv.get_core() or rest) & set(rest)
                if len(core) <= cap_min:
                    emit(shrink(slv, core))
    return results


# ----------------------------------------------------------------------
# witness anatomy
# ----------------------------------------------------------------------

def anatomy(M, colA, colB):
    out = {}
    for name, col in (('A', colA), ('B', colB)):
        U = [v for v in col if v <= 2 * M]
        Y = [v for v in col if 2 * M < v <= 4 * M]
        Z = [v for v in col if v > 4 * M]
        out[name] = {
            'sizes': [len(U), len(Y), len(Z)],
            'mod2': [dict(Counter(v % 2 for v in part))
                     for part in (U, Y, Z)],
            'mod4': [dict(Counter(v % 4 for v in part))
                     for part in (U, Y, Z)],
            'U_off': [v - M for v in U],
            'Y_off': [v - 4 * M for v in Y],
            'Z_off': [v - 4 * M for v in Z],
        }
    return out


# ----------------------------------------------------------------------
# main loop
# ----------------------------------------------------------------------

def main():
    M = int(sys.argv[1]) if len(sys.argv) > 1 else 48
    maxiter = int(sys.argv[2]) if len(sys.argv) > 2 else 500
    bounds = (tuple(int(x) for x in sys.argv[3:6]) if len(sys.argv) > 5
              else (2, 2, 2))
    P0, P1, P2 = core_support(M)
    blocks = (P0, P1, P2)
    V = P0 + P1 + P2
    ai = {v: k + 1 for k, v in enumerate(V)}
    top = len(V)

    cat_path = os.path.join(HERE, '..', 'data', f'e146_catalogue_M{M}.json')
    with open(cat_path) as f:
        seed = json.load(f)
    # resume: reload a previous run's discoveries (kept in `found` so
    # the output JSON stays cumulative)
    prev_found = []
    prev_path = os.path.join(HERE, '..', 'data', f'e147_cegar_M{M}.json')
    if os.path.exists(prev_path):
        with open(prev_path) as f:
            prev = json.load(f)
        prev_found = [{k: p[k] for k in ('blk', 'S', 'src')}
                      for p in prev.get('discovered', [])]
        print(f'resume: +{len(prev_found)} patterns from previous run',
              flush=True)

    slv = Cadical195()
    # straddles
    n_str = 0
    for y in P1:
        for u in P0:
            z = 2 * y - u
            if 4 * M + 1 <= z <= 6 * M + 15:
                slv.add_clause([-ai[u], -ai[y], -ai[z]])
                slv.add_clause([ai[u], ai[y], ai[z]])
                n_str += 1
    # bounds
    for bi, B in enumerate(blocks):
        if bounds[bi] <= 0:
            continue
        for sign in (1, -1):
            enc = CardEnc.atleast(lits=[sign * ai[v] for v in B],
                                  bound=bounds[bi], top_id=top,
                                  encoding=EncType.seqcounter)
            top = max(top, enc.nv)
            for c in enc.clauses:
                slv.add_clause(c)
    # seed patterns

    def add_pattern(S):
        slv.add_clause([-ai[v] for v in S])
        slv.add_clause([ai[v] for v in S])

    for e in seed:
        add_pattern(e['S'])
    for e in prev_found:
        add_pattern(e['S'])
    # symmetry: WLOG M+1 is team A
    slv.add_clause([ai[M + 1]])

    print(f'ADV({M}) bounds={bounds}: straddle={n_str} '
          f'seed patterns={len(seed)}+{len(prev_found)}', flush=True)

    found = list(prev_found)
    witnesses = []
    t_start = time.time()
    verdict = 'MAXITER'
    for it in range(1, maxiter + 1):
        t0 = time.time()
        if not slv.solve():
            verdict = 'UNSAT'
            print(f'[{it}] ADV UNSAT after {len(found)} discovered '
                  f'patterns [{time.time()-t0:.1f}s solve, '
                  f'{time.time()-t_start:.0f}s total] — COV({M}) holds '
                  f'with |catalogue| = {len(seed) + len(found)}',
                  flush=True)
            break
        model = set(l for l in slv.get_model() if l > 0)
        colA = [v for v in V if ai[v] in model]
        colB = [v for v in V if ai[v] not in model]
        ana = anatomy(M, colA, colB)
        szs = {t: ana[t]['sizes'] for t in 'AB'}
        it_patterns = []
        theories = []
        # cheap blocks (0, 1) for both teams first; Th2 only if needed
        for stage in ((0, 1), (2,)):
            for name, col in (('A', colA), ('B', colB)):
                for i in stage:
                    r = theory_mus(M, i, col)
                    if r is None:
                        continue
                    for supp, used in r:
                        assert RESTRICTED[i](M, supp), (it, name, i, supp)
                        theories.append((name, i, len(supp), len(used)))
                        it_patterns.append({'blk': i, 'S': supp,
                                            'src': f'cegar(it={it},'
                                                   f'team={name})',
                                            'n_cons': len(used)})
            if it_patterns:
                break
        assert it_patterns, (it, 'no UNSAT block theory — violates '
                             'e135+LemmaU', szs)
        for pat in it_patterns:
            add_pattern(pat['S'])
            found.append(pat)
        witnesses.append({'it': it, 'sizes': szs,
                          'kills': theories, 'anatomy': ana})
        print(f'[{it}] sizes A={szs["A"]} B={szs["B"]} '
              f'kills={[(n, i, ls) for (n, i, ls, _) in theories]} '
              f'[{time.time()-t0:.1f}s]', flush=True)
        for p in it_patterns:
            anchor = {0: M, 1: 4 * M, 2: 4 * M}[p['blk']]
            print(f'      blk{p["blk"]} |S|={len(p["S"])} '
                  f'offs={[v - anchor for v in p["S"]]}', flush=True)
    out = {'M': M, 'bounds': bounds, 'verdict': verdict,
           'seed': len(seed), 'discovered': found,
           'witnesses': witnesses,
           'total_s': round(time.time() - t_start, 1)}
    path = os.path.join(HERE, '..', 'data', f'e147_cegar_M{M}.json')
    with open(path, 'w') as f:
        json.dump(out, f)
    print(f'e147: {verdict} at M={M}; +{len(found)} patterns; -> {path}',
          flush=True)


if __name__ == '__main__':
    main()
