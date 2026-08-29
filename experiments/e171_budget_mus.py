"""e171: FRONT BUDGET-MUS — resumable deletion-minimal SUPPORT of the
seam-BUDGET cores (notes/68; playbook of e126_case2_mus + e158b).

Target family: the e127 budget instance U(M; bal; v, v) — 3-block
window (M, 8M], balanced per-block lower bounds, per-team adjacent-seam
inversion budgets = v.  UNSAT at v means every valid balanced pair pays
> v inversions at the window (Lemma T-FORCE, notes/54 SS2).  Extracting
the deletion-minimal value support of the UNSAT is the anatomy
instrument: comparing supports across v (v = 2 vs 4 at M = 16) shows
WHAT GROWS as the budget rises — the v*-growth mechanism itself, and
the GAP-V*-schema seed.

Deletion semantics (restriction-monotone, verbatim e158b): deleting a
value from block i lowers that block's per-team lower bound by one,
    bound_i = max(0, |full B_i|/2 - #deleted_i),
so any model of the FULL instance restricts to a model of the support
instance (induced colors meet the lowered bounds; the induced order's
inversion pairs are a subset of the original's, so the budgets still
hold).  Support UNSAT therefore certifies the full-core UNSAT and every
intermediate step — a strengthening chain, exactly e158b's.

Color-swap pin (the pod3_pin16 variant, WLOG): with symmetric budgets
(v, v) and identical per-team bounds, the global color swap A <-> B is
an instance automorphism, so pinning the SMALLEST support value to team
A is sound: pinned UNSAT <=> unpinned UNSAT.  Measured speedup ~2x
(pod3: v=4 UNSAT 5535s pinned vs projected ~3h+ unpinned).

Crash-safe: the surviving support is snapshotted after every accepted
drop and every criticality step; a rerun resumes from the snapshot
(re-verifying UNSAT first).  TIMEOUT trials are treated as "cannot
drop" and recorded.

Usage:
  e171_budget_mus.py --M 16 --v 2 [--budget 1800] [--chunk 32]
                     [--no-pin] [--seed-json seeds.json]
  seeds.json = list of candidate starting supports (ascending size);
  the first that verifies UNSAT is the start; else the full window.

Artifacts: data/e171_mus_bal_M{M}_v{v}[_pin].json (+ .resume.json)
"""
import argparse
import json
import math
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
DATA = os.path.join(REPO, 'data')

from pysat.solvers import Cadical195, Glucose42
from pysat.card import CardEnc, EncType


def blocks_of(M):
    return (('B0', M, 2 * M), ('B1', 2 * M, 4 * M), ('B2', 4 * M, 8 * M))


def bounds_for(M, support):
    """Restriction-monotone balance bounds (e158b): full half minus
    deletions, floored at 0.  Identical for both teams (pin-sound)."""
    sset = set(support)
    out = []
    for _, lo, hi in blocks_of(M):
        full = hi - lo                       # even for all M
        deleted = full - len([v for v in sset if lo < v <= hi])
        out.append(max(0, full // 2 - deleted))
    return tuple(out)


def solve_budget_support(M, support, v, pin=True, solver=Cadical195):
    """e127.solve_budget restricted to a value support, explicit
    per-block bounds via bounds_for, symmetric budgets (v, v), optional
    min-value color pin.  Returns (verdict, secs)."""
    V = sorted(support)
    n = len(V)
    idx = {u: i for i, u in enumerate(V)}
    bounds = bounds_for(M, V)

    def _mk(start):
        off = {}
        nxt = start
        for i in range(n):
            for j in range(i + 1, n):
                off[(i, j)] = nxt
                nxt += 1
        return off, nxt - 1

    offA, top = _mk(1)
    offB, top = _mk(top + 1)
    ai = {}
    for u in V:
        top += 1
        ai[u] = top

    def litT(off):
        def lit(u, w):
            i, j = idx[u], idx[w]
            return off[(i, j)] if i < j else -off[(j, i)]
        return lit

    litA, litB = litT(offA), litT(offB)
    Vs = set(V)
    blks = [[u for u in V if lo < u <= hi] for _, lo, hi in blocks_of(M)]
    B0, B1, B2 = blks
    seampairs = [(u, w) for u in B0 for w in B1] + \
                [(u, w) for u in B1 for w in B2]
    cls = []
    xvar = {}
    for team, lit, g in (('A', litA, lambda u: -ai[u]),
                         ('B', litB, lambda u: ai[u])):
        for b in V:
            for d in range(1, min(b - V[0], V[-1] - b) + 1):
                a, c = b - d, b + d
                if a in Vs and c in Vs:
                    gg = [g(a), g(b), g(c)]
                    cls.append(gg + [-lit(a, b), -lit(b, c)])
                    cls.append(gg + [lit(a, b), lit(b, c)])
        for (u, w) in seampairs:
            top += 1
            xvar[(team, u, w)] = top
            cls.append([g(u), g(w), lit(u, w), top])
    for off in (offA, offB):
        for i in range(n):
            for j in range(i + 1, n):
                xij = off[(i, j)]
                for kk in range(j + 1, n):
                    cls.append([-xij, -off[(j, kk)], off[(i, kk)]])
                    cls.append([xij, off[(j, kk)], -off[(i, kk)]])
    if pin and V:
        cls.append([ai[V[0]]])               # WLOG: min value in team A
    cards = []
    tid = top
    for blk, bnd in zip(blks, bounds):
        if bnd <= 0:
            continue
        for sign in (1, -1):                 # A counts +ai, B counts -ai
            enc = CardEnc.atleast(lits=[sign * ai[u] for u in blk],
                                  bound=bnd, top_id=tid,
                                  encoding=EncType.seqcounter)
            tid = max(tid, enc.nv)
            cards += enc.clauses
    for team in ('A', 'B'):
        lits = [xvar[(team, u, w)] for (u, w) in seampairs]
        if v <= 0:
            cards += [[-l] for l in lits]
        else:
            enc = CardEnc.atmost(lits=lits, bound=v, top_id=tid,
                                 encoding=EncType.seqcounter)
            tid = max(tid, enc.nv)
            cards += enc.clauses
    t0 = time.time()
    with solver(bootstrap_with=cls) as s:
        for c in cards:
            s.add_clause(c)
        ok = s.solve()
    return ('SAT' if ok else 'UNSAT'), round(time.time() - t0, 1)


def _worker(kw, outq):
    outq.put(solve_budget_support(**kw))


def solve_sub(kw, budget):
    import multiprocessing as mp
    import queue as _q
    ctx = mp.get_context('fork')
    outq = ctx.Queue()
    p = ctx.Process(target=_worker, args=(kw, outq))
    t0 = time.time()
    p.start()
    try:
        verdict, el = outq.get(timeout=budget)
        p.join()
        return verdict, el
    except _q.Empty:
        p.terminate()
        p.join()
        return 'TIMEOUT', round(time.time() - t0, 1)


def anchor_anatomy(sup, M):
    out = {}
    for name, lo, hi in blocks_of(M):
        vals = sorted(u for u in sup if lo < u <= hi)
        mid = (lo + hi + 1) // 2
        out[name] = {
            'n': len(vals), 'vals': vals,
            'bound': None,                    # filled by caller
            'bot_offsets': [u - lo for u in vals],
            'top_offsets': [hi - u for u in vals],
            'mid_offsets': [u - mid for u in vals],
            'parities_mod4': sorted({u % 4 for u in vals}),
        }
    return out


def run(M, v, budget, chunk0, pin, seed_json):
    t00 = time.time()
    tag = f'bal_M{M}_v{v}' + ('_pin' if pin else '')
    rpath = os.path.join(DATA, f'e171_mus_{tag}.resume.json')
    fpath = os.path.join(DATA, f'e171_mus_{tag}.json')
    Vfull = list(range(M + 1, 8 * M + 1))
    n_timeouts = [0]
    total = [0]

    def unsat(sup):
        verdict, el = solve_sub(dict(M=M, support=sorted(sup), v=v,
                                     pin=pin), budget)
        total[0] += 1
        if verdict == 'TIMEOUT':
            n_timeouts[0] += 1
        return verdict == 'UNSAT', verdict, el

    def snapshot(sup, phase, extra=None):
        rec = {'M': M, 'v': v, 'pin': pin, 'phase': phase,
               'n': len(sup), 'support': sorted(sup),
               'bounds': list(bounds_for(M, sup)),
               'elapsed': round(time.time() - t00, 1),
               'solves': total[0], 'timeouts': n_timeouts[0]}
        if extra:
            rec.update(extra)
        with open(rpath, 'w') as f:
            json.dump(rec, f)

    if os.path.exists(rpath):
        with open(rpath) as f:
            saved = json.load(f)
        sup = list(saved['support'])
        ok, verdict, el = unsat(sup)
        print(f'RESUME n={len(sup)} phase={saved["phase"]}: {verdict} '
              f'[{el}s]', flush=True)
        assert ok, 'resumed support not UNSAT — snapshot corrupt'
    else:
        sup = None
        if seed_json:
            with open(seed_json) as f:
                seeds = json.load(f)
            for k, cand in enumerate(seeds):
                cand = sorted(set(cand) & set(Vfull))
                ok, verdict, el = unsat(cand)
                print(f'seed {k} n={len(cand)}: {verdict} [{el}s]',
                      flush=True)
                if ok:
                    sup = cand
                    break
        if sup is None:
            ok, verdict, el = unsat(Vfull)
            print(f'start FULL n={len(Vfull)}: {verdict} [{el}s]',
                  flush=True)
            assert ok, 'full budget instance not UNSAT at this v'
            sup = list(Vfull)
        snapshot(sup, 'start')

    chunk = chunk0
    while chunk >= 1:
        i = 0
        cand = sorted(sup, reverse=True)
        while i < len(cand):
            batch = [u for u in cand[i:i + chunk] if u in set(sup)]
            if not batch:
                i += chunk
                continue
            trial = [u for u in sup if u not in set(batch)]
            if not trial:
                i += chunk
                continue
            ok, verdict, el = unsat(trial)
            if ok:
                sup = trial
                print(f'  -{len(batch)} (chunk={chunk}) -> n={len(sup)}'
                      f' [{el}s]', flush=True)
                snapshot(sup, f'chunk{chunk}')
            else:
                if verdict == 'TIMEOUT':
                    print(f'  keep chunk={chunk}@{i} (TIMEOUT {el}s)',
                          flush=True)
                i += chunk
        chunk //= 2

    print(f'MINIMAL-pass done n={len(sup)} bounds='
          f'{bounds_for(M, sup)} ({total[0]} solves, '
          f'{n_timeouts[0]} timeouts, '
          f'{round(time.time() - t00, 1)}s)', flush=True)
    print('support =', sorted(sup), flush=True)
    snapshot(sup, 'minimal')

    # criticality certificate (drops any residual redundancy)
    crit = []
    done = set()
    for u in sorted(sup):
        if u in done:
            continue
        trial = [x for x in sup if x != u]
        ok, verdict, el = unsat(trial)
        if ok:
            crit.append((u, 'RED'))
            sup = trial
        else:
            crit.append((u, 'NEC' if verdict == 'SAT' else 'TO'))
        done.add(u)
        snapshot(sup, 'criticality', {'crit_done': len(crit)})
    n_nec = sum(1 for _, s in crit if s == 'NEC')
    n_red = sum(1 for _, s in crit if s == 'RED')
    n_to = sum(1 for _, s in crit if s == 'TO')
    print(f'criticality: {n_nec} necessary, {n_red} redundant-dropped, '
          f'{n_to} timeout-undecided', flush=True)

    # independent re-verify: Glucose42 pinned + Cadical unpinned
    v1, e1 = solve_budget_support(M, sup, v, pin=pin, solver=Glucose42)
    print(f'Glucose42 re-verify (pin={pin}): {v1} [{e1}s]', flush=True)
    v2, e2 = ('SKIP', 0)
    if pin:
        v2, e2 = solve_sub(dict(M=M, support=sorted(sup), v=v,
                                pin=False), budget * 4)
        print(f'Cadical UNPINNED re-verify: {v2} [{e2}s]', flush=True)

    anat = anchor_anatomy(sup, M)
    bnds = bounds_for(M, sup)
    for k, name in enumerate(('B0', 'B1', 'B2')):
        anat[name]['bound'] = bnds[k]
        a = anat[name]
        print(f'{name} n={a["n"]} bound={a["bound"]} '
              f'bot_off={a["bot_offsets"]} top_off={a["top_offsets"]} '
              f'mod4={a["parities_mod4"]}', flush=True)

    rec = {'tag': f'e171MUS {tag}', 'M': M, 'v': v, 'pin': pin,
           'n_support': len(sup), 'support': sorted(sup),
           'bounds': list(bnds),
           'criticality': crit,
           'n_necessary': n_nec, 'n_redundant': n_red,
           'n_timeout_undecided': n_to,
           'glucose_reverify': v1, 'unpinned_reverify': v2,
           'anatomy': anat, 'solves': total[0],
           'timeouts': n_timeouts[0],
           'elapsed': round(time.time() - t00, 1)}
    with open(fpath, 'w') as f:
        json.dump(rec, f, indent=1)
    print(f'FINAL n={len(sup)} written to {fpath}', flush=True)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--M', type=int, required=True)
    ap.add_argument('--v', type=int, required=True)
    ap.add_argument('--budget', type=float, default=1800.0)
    ap.add_argument('--chunk', type=int, default=32)
    ap.add_argument('--no-pin', action='store_true')
    ap.add_argument('--seed-json', type=str, default=None)
    args = ap.parse_args()
    os.makedirs(DATA, exist_ok=True)
    run(args.M, args.v, args.budget, args.chunk, not args.no_pin,
        args.seed_json)
