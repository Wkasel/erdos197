"""e121 — FRONT N6: the ledger measurements (notes/46).

Machine-attack the two candidate infinite-accounting statements L1 / L2 on
concrete everywhere-split colorings by MEASURING price sequences and their
cross-scale coupling, plus the finite price curves p(k) that L2 needs.

Parts (arg --part, default all):
  A  counting: per-block prices, endpoint occupancy, pair supply, cross-
     scale completion flux (incl. donation->donation), window cleanness,
     orbit-light closure scan.  Colorings: gc3 (Geneson-complement lam=3),
     gc3e/gc3i (two-sided salted, endpoint vs interior plants), rnd1/rnd2
     (iid balanced), dyadic (Case-1 control).  Horizon 2^14.
  B  price curves: min-donation p(k) for k forced in-team attacker pairs
     at M = 64, 128 (crown/low pairs and chain pairs), e118-faithful
     2-colored encoding, COMPLETE transitivity, ITotalizer budgets.
  C  counterfactual rung probes on actual traces (majority trace of B(t)
     under all its own live chain pairs from B(t-1)), t = 10 (11 if time);
     plus the N5 density sweep: random sub-block at density d under 8
     chain pairs, M = 1024.

Outputs: data/e121_A.json, e121_B.json, e121_C.json (+ stdout log).
"""
import argparse
import json
import os
import sys
import time

import numpy as np

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, 'experiments'))
DATA = os.path.join(REPO, 'data')

H = 2 ** 14          # horizon
TMIN, TMAX = 4, 13   # blocks B(t) = (2^t, 2^{t+1}] fully inside horizon
W_EP = 16            # endpoint zone width


# ------------------------------------------------------------- colorings

def coloring_gc3():
    from h1_complement import Membership
    mem = Membership(H, lam=3, r=4)
    arr = np.zeros(H + 1, dtype=bool)
    for v in range(1, H + 1):
        arr[v] = mem.in_W(v)          # True = team A = W material
    return arr


def coloring_dyadic():
    arr = np.zeros(H + 1, dtype=bool)
    for v in range(2, H + 1):
        t = (v - 1).bit_length() - 1
        arr[v] = (t % 2 == 0)
    arr[1] = True
    return arr


def coloring_rnd(seed):
    rng = np.random.default_rng(seed)
    arr = rng.random(H + 1) < 0.5
    arr[0] = False
    return arr


def salt(base, endpoint=True):
    """Two-sided salting: enforce per-team presence >= f(t) = max(3, t-6)
    in every block t >= 6 by flipping values of the surplus team, placed
    on endpoint zones (endpoint=True) or spread through the interior."""
    arr = base.copy()
    for t in range(6, TMAX + 1):
        M = 2 ** t
        block = np.arange(M + 1, 2 * M + 1)
        f = max(3, t - 6)
        protected = set()                 # values flipped in this block
        for team in (True, False):
            have = int(np.sum(arr[block] == team))
            need = f - have
            if need <= 0:
                continue
            donors = block[(arr[block] != team)
                           & ~np.isin(block, list(protected))]
            if endpoint:
                # alternate bottom-up / top-down among donor values
                bot = [v for v in donors if v <= M + max(W_EP, need)]
                top = [v for v in donors if v >= 2 * M - max(W_EP, need)]
                picks = []
                i = j = 0
                while len(picks) < need and (i < len(bot) or j < len(top)):
                    if i < len(bot):
                        picks.append(bot[i]); i += 1
                    if len(picks) < need and j < len(top):
                        picks.append(top[-1 - j]); j += 1
                # fallback: nearest-to-edges donors
                k = 0
                while len(picks) < need and k < len(donors):
                    if donors[k] not in picks:
                        picks.append(int(donors[k]))
                    k += 1
            else:
                idx = np.linspace(0, len(donors) - 1, need).round().astype(int)
                picks = [int(donors[i]) for i in np.unique(idx)]
                k = 0
                while len(picks) < need and k < len(donors):
                    if donors[k] not in picks:
                        picks.append(int(donors[k]))
                    k += 1
            for v in picks[:need]:
                arr[v] = team
                protected.add(int(v))
    return arr


def build_colorings():
    gc3 = coloring_gc3()
    return {
        'gc3': gc3,
        'gc3e': salt(gc3, endpoint=True),
        'gc3i': salt(gc3, endpoint=False),
        'rnd1': coloring_rnd(1),
        'rnd2': coloring_rnd(2),
        'dyadic': coloring_dyadic(),
    }


# ------------------------------------------------------------- part A

def team_vals(arr, team, lo, hi):
    v = np.arange(lo + 1, hi + 1)
    return v[arr[v] == team]


def closure_scan(arr, team):
    """Doubling-closure from seeds team ∩ [2^9, 2^10) with reflectors
    team ∩ [1, 64]: does any chain reach the top half (censored) ?"""
    refl = [int(v) for v in np.nonzero(arr[1:65] == team)[0] + 1]
    seeds = team_vals(arr, team, 2 ** 9 - 1, 2 ** 10 - 1)
    seen = set(int(v) for v in seeds)
    frontier = list(seen)
    censored = 0
    while frontier:
        nxt = []
        for u in frontier:
            for f in refl:
                w = 2 * u - f
                if w <= u or w > H or not (arr[w] == team):
                    continue
                if w not in seen:
                    seen.add(w)
                    nxt.append(w)
                    if w > H // 2:
                        censored += 1
        frontier = nxt
    return {'reflectors': len(refl), 'seeds': len(seeds),
            'closure': len(seen), 'censored_tophalf': censored}


def part_A(colorings):
    out = {}
    for name, arr in colorings.items():
        t0 = time.time()
        rec = {'blocks': {}, 'flux': {}, 'windows': {}, 'closure': {}}
        for t in range(TMIN, TMAX + 1):
            M = 2 ** t
            block = np.arange(M + 1, 2 * M + 1)
            isA = arr[block]
            nA, nB = int(isA.sum()), int((~isA).sum())
            minority = 'A' if nA <= nB else 'B'
            mvals = block[isA == (minority == 'A')]
            ep_bot = int(np.sum(mvals <= M + W_EP))
            ep_top = int(np.sum(mvals >= 2 * M - W_EP + 1))
            # pair supply and switches
            pair = {}
            for team, lab in ((True, 'A'), (False, 'B')):
                tv = arr[block] == team
                g1 = int(np.sum(tv[:-1] & tv[1:]))
                g2 = int(np.sum(tv[:-2] & tv[2:]))
                pair[lab] = {'gap1': g1, 'gap2': g2}
            switches = int(np.sum(isA[:-1] != isA[1:]))
            rec['blocks'][t] = {
                'nA': nA, 'nB': nB, 'minority': minority, 'P': min(nA, nB),
                'minority_ep_bot': ep_bot, 'minority_ep_top': ep_top,
                'minority_interior': len(mvals) - ep_bot - ep_top,
                'pairs': pair, 'switches': switches,
            }
        for t in range(TMIN, TMAX):
            M = 2 ** t          # source block (M, 2M], target (2M, 4M]
            tgt = np.arange(2 * M + 1, 4 * M + 1)
            fx = {}
            for team, lab in ((True, 'A'), (False, 'B')):
                src = team_vals(arr, team, M, 2 * M)
                tv = arr[tgt] == team
                mass = 0
                for x in src:
                    z = 2 * tgt - int(x)
                    ok = z <= 4 * M
                    mass += int(np.sum(tv[ok] & (arr[z[ok]] == team)))
                # donation->donation flux: source x minority at t,
                # completion z minority at t+1
                min_t = rec['blocks'][t]['minority']
                min_t1 = rec['blocks'][t + 1]['minority']
                dd = 0
                if (lab == min_t) and (lab == min_t1):
                    dd = mass   # whole team IS the minority on both scales
                # live chain pairs: gap-1 pairs of team in (M,2M] with
                # >= 3 surviving attack completions into (2M,4M]
                live = 0; units = 0
                tvsrc = arr[np.arange(M + 1, 2 * M + 1)] == team
                xs = np.arange(M + 1, 2 * M)[tvsrc[:-1] & tvsrc[1:]]
                for x in xs:
                    j = np.arange(1, int(x) // 2 + 1)
                    y = 2 * M + j
                    z = 4 * M + 2 * j - int(x)
                    ok = (y <= 4 * M) & (z <= 4 * M) & (z > 2 * M)
                    u = int(np.sum((arr[y[ok]] == team) & (arr[z[ok]] == team)))
                    units += u
                    if u >= 3:
                        live += 1
                fx[lab] = {'chain_mass': mass, 'dd_flux': dd,
                           'live_pairs': live, 'attack_units': units,
                           'gap1_pairs': int(len(xs))}
            rec['flux'][t] = fx
        # window cleanness
        for team, lab in ((True, 'A'), (False, 'B')):
            pref = np.concatenate([[0], np.cumsum(arr[1:] == team)])
            a = np.arange(16, H // 2 + 1)
            cnt = pref[2 * a] - pref[a]
            co = a - cnt
            dens = cnt / a
            big = a >= 512
            rec['windows'][lab] = {
                'clean_C0': int(np.sum(co == 0)),
                'clean_C8': int(np.sum(co <= 8)),
                'clean_C32': int(np.sum(co <= 32)),
                'max_dens_a_ge_512': float(dens[big].max()),
                'argmax_a': int(a[big][dens[big].argmax()]),
            }
        rec['closure']['A'] = closure_scan(arr, True)
        rec['closure']['B'] = closure_scan(arr, False)
        rec['secs'] = round(time.time() - t0, 1)
        out[name] = rec
        print(f"[A] {name}: done in {rec['secs']}s", flush=True)
    return out


# ------------------------------------------------------------- part B

def price_curve(M, pairs, maxb=24, label=''):
    """e118-faithful 2-colored gadget on (M, 2M] with the given attacker
    pairs FORCED into team A; minimize donations (# block values = B).
    COMPLETE transitivity per team.  Returns list of records per k."""
    from pysat.card import ITotalizer
    from pysat.solvers import Cadical195
    V = list(range(M + 1, 2 * M + 1))
    n = len(V)
    idx = {v: i for i, v in enumerate(V)}
    results = []
    for k in range(1, len(pairs) + 1):
        atk = [x for p in pairs[:k] for x in p]
        var = 0
        col = {}
        for v in V + atk:
            var += 1
            col[v] = var
        ov = {'A': {}, 'B': {}}
        for T in ('A', 'B'):
            for i in range(n):
                for j in range(i + 1, n):
                    var += 1
                    ov[T][(i, j)] = var

        def o(T, u, w):
            i, j = idx[u], idx[w]
            return ov[T][(i, j)] if i < j else -ov[T][(j, i)]

        def notT(T, v):
            return -col[v] if T == 'A' else col[v]

        cl = []
        for y in V:                       # gated in-block AP triples
            d = 1
            while y + d <= 2 * M:
                x, z = y - d, y + d
                d += 1
                if x > M:
                    for T in ('A', 'B'):
                        g = [notT(T, x), notT(T, y), notT(T, z)]
                        cl.append(g + [-o(T, x, y), -o(T, y, z)])
                        cl.append(g + [-o(T, z, y), -o(T, y, x)])
        natk = 0
        for x in atk:                     # attacks (attackers forced A)
            for j in range(1, x // 2 + 1):
                y, z = M + j, 2 * M + 2 * j - x
                if M < z <= 2 * M and M < y <= 2 * M:
                    cl.append([notT('A', y), notT('A', z), o('A', z, y)])
                    natk += 1
        for T in ('A', 'B'):              # complete transitivity
            for i in range(n):
                for j in range(i + 1, n):
                    oij = ov[T][(i, j)]
                    for kk in range(j + 1, n):
                        ojk = ov[T][(j, kk)]
                        oik = ov[T][(i, kk)]
                        cl.append([-oij, -ojk, oik])
                        cl.append([oij, ojk, -oik])
        cl += [[col[x]] for x in atk]     # attackers in team A
        don = [-col[v] for v in V]
        sol = Cadical195(bootstrap_with=cl)
        tot = ITotalizer(lits=don, ubound=min(maxb, len(don)), top_id=var)
        sol.append_formula(tot.cnf.clauses)
        t0 = time.time()
        p = None
        witness = None
        for b in range(0, maxb + 1):
            assum = [-tot.rhs[b]] if b < len(tot.rhs) else []
            if sol.solve(assumptions=assum):
                model = set(l for l in sol.get_model() if l > 0)
                witness = sorted(v for v in V if col[v] not in model)
                p = b
                break
        secs = round(time.time() - t0, 1)
        supp = None
        if witness is not None:
            supp = {
                'bot': [v for v in witness if v <= M + W_EP],
                'top': [v for v in witness if v >= 2 * M - W_EP + 1],
                'interior': [v for v in witness
                             if M + W_EP < v < 2 * M - W_EP + 1],
            }
        rec = {'M': M, 'label': label, 'k': k, 'pairs': pairs[:k],
               'attacks': natk, 'p': p, 'witness': witness,
               'support': supp, 'secs': secs}
        results.append(rec)
        print(f"[B] M={M} {label} k={k}: p={p} ({secs}s) "
              f"support={supp if p is not None and p <= 12 else '...'}",
              flush=True)
        sol.delete()
        tot.delete()
        if p is None:
            break                          # price exceeds budget; stop set
    return results


def part_B():
    out = []
    out += price_curve(64, [(15, 16), (31, 32), (23, 24), (47, 48),
                            (55, 56)], label='low')
    out += price_curve(64, [(33, 34), (41, 42), (49, 50), (57, 58),
                            (37, 38), (45, 46)], label='chain')
    out += price_curve(128, [(15, 16), (31, 32), (63, 64), (23, 24),
                             (47, 48)], label='low')
    out += price_curve(128, [(65, 66), (81, 82), (97, 98), (113, 114),
                             (73, 74), (89, 90)], label='chain')
    return out


# ------------------------------------------------------------- part C

def probe(S, units, tag, max_secs=900):
    """Order gadget on value set S (inside (M, 2M]) with unit precedences
    `units` = list of (z, y) meaning z BEFORE y; in-S AP triples
    non-monotone; lazy transitivity (UNSAT conclusive; SAT verified)."""
    from pysat.solvers import Cadical195
    S = sorted(S)
    n = len(S)
    idx = {v: i for i, v in enumerate(S)}
    inS = set(S)
    var = {}
    c = 0
    for i in range(n):
        for j in range(i + 1, n):
            c += 1
            var[(i, j)] = c

    def o(u, w):
        i, j = idx[u], idx[w]
        return var[(i, j)] if i < j else -var[(j, i)]

    cl = [[o(z, y)] for (z, y) in units]
    ntr = 0
    lo, hi = S[0], S[-1]
    for y in S:
        d = 1
        while y + d <= hi:
            x, z = y - d, y + d
            d += 1
            if x >= lo and x in inS and z in inS:
                cl.append([-o(x, y), -o(y, z)])
                cl.append([-o(z, y), -o(y, x)])
                ntr += 1
    sol = Cadical195(bootstrap_with=cl)
    t0 = time.time()
    rounds = 0
    verdict = 'TIMEOUT'
    while time.time() - t0 < max_secs:
        if not sol.solve():
            verdict = 'UNSAT'
            break
        model = set(l for l in sol.get_model() if l > 0)
        Bm = np.zeros((n, n), dtype=bool)
        for (i, j), lit in var.items():
            if lit in model:
                Bm[i, j] = True
            else:
                Bm[j, i] = True
        R2 = (Bm.astype(np.uint8) @ Bm.astype(np.uint8)) > 0
        miss = R2 & ~Bm & ~np.eye(n, dtype=bool) & Bm.T
        ii, jj = np.nonzero(miss)
        if len(ii) == 0:
            verdict = 'SAT'
            break
        new = []

        def lit_of(p, q):
            return var[(p, q)] if p < q else -var[(q, p)]
        for i, j in zip(ii[:30000], jj[:30000]):
            kk = int(np.nonzero(Bm[i] & Bm[:, j])[0][0])
            new.append([-lit_of(i, kk), -lit_of(kk, j), lit_of(i, j)])
        sol.append_formula(new)
        rounds += 1
    secs = round(time.time() - t0, 1)
    print(f"[C] {tag}: n={n} units={len(cl) - 2 * ntr} triples={ntr} "
          f"-> {verdict} ({secs}s, {rounds} rounds)", flush=True)
    sol.delete()
    return {'tag': tag, 'n': n, 'units': len(units), 'triples': ntr,
            'verdict': verdict, 'secs': secs, 'rounds': rounds}


def trace_probe(arr, name, t):
    """Majority trace of B(t) attacked by ALL its own gap-1 pairs from
    B(t-1) (chain geometry)."""
    M = 2 ** t
    block = np.arange(M + 1, 2 * M + 1)
    isA = arr[block]
    team = bool(isA.sum() >= (len(block) - isA.sum()))
    S = [int(v) for v in block[isA == team]]
    inS = set(S)
    prev = np.arange(M // 2 + 1, M + 1)
    tv = arr[prev] == team
    xs = [int(x) for x in prev[:-1][tv[:-1] & tv[1:]]]
    units = set()
    for x0 in xs:
        for x in (x0, x0 + 1):
            for j in range(1, x // 2 + 1):
                y, z = M + j, 2 * M + 2 * j - x
                if y in inS and z in inS and M < z <= 2 * M:
                    units.add((z, y))
    return probe(S, sorted(units),
                 f"{name} t={t} maj={'A' if team else 'B'} "
                 f"pairs={len(xs)}")


def density_probe(M, d, seed, npairs=8):
    rng = np.random.default_rng(seed)
    block = list(range(M + 1, 2 * M + 1))
    S = [v for v in block if rng.random() < d]
    inS = set(S)
    xs = [M // 2 + 1 + i * (M // 2 - 2) // max(1, npairs - 1)
          for i in range(npairs)]
    units = set()
    for x0 in xs:
        for x in (x0, x0 + 1):
            for j in range(1, x // 2 + 1):
                y, z = M + j, 2 * M + 2 * j - x
                if y in inS and z in inS and M < z <= 2 * M:
                    units.add((z, y))
    return probe(S, sorted(units), f"dens M={M} d={d} seed={seed}")


def part_C(colorings):
    out = []
    for name in ('gc3e', 'gc3i', 'rnd1'):
        out.append(trace_probe(colorings[name], name, 10))
    for d in (1.0, 0.9, 0.8, 0.7, 0.6, 0.5):
        out.append(density_probe(1024, d, seed=11))
    # second seed on the interesting shoulder
    for d in (0.9, 0.8, 0.7):
        out.append(density_probe(1024, d, seed=12))
    for name in ('gc3e', 'rnd1'):
        out.append(trace_probe(colorings[name], name, 11))
    return out


# ------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--part', default='ABC')
    args = ap.parse_args()
    colorings = None
    if 'A' in args.part or 'C' in args.part:
        colorings = build_colorings()
    if 'A' in args.part:
        res = part_A(colorings)
        json.dump(res, open(os.path.join(DATA, 'e121_A.json'), 'w'),
                  indent=1)
        print('[A] written data/e121_A.json', flush=True)
    if 'B' in args.part:
        res = part_B()
        json.dump(res, open(os.path.join(DATA, 'e121_B.json'), 'w'),
                  indent=1)
        print('[B] written data/e121_B.json', flush=True)
    if 'C' in args.part:
        res = part_C(colorings)
        json.dump(res, open(os.path.join(DATA, 'e121_C.json'), 'w'),
                  indent=1)
        print('[C] written data/e121_C.json', flush=True)


if __name__ == '__main__':
    main()
