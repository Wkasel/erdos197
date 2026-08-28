"""a8_dich_indep: referee-independent verifier for notes/57 (DICH).

Written from the notes/57 text alone; no code shared with
experiments/e153_dich_lemmas.py or audit/a7_night2/a7_alpha_f.py.

Parts:
  A  Lemma FI brute check at M in {144, 176} (176: untouched scale;
     pure arithmetic, no catalogue needed) + A2 pair mass.
  B  Catalogue shape + F0 purity at all scales with a catalogue.
  C  H1 interval-intersection claim, exhaustively: for every
     (z_odd, z_even) with both offsets <= M-1, I(z_o) n I(z_e) != 0.
     (Pure arithmetic; run at 48..176.)
  D  alpha_c (shallow alive clique), bottom-singleton self-service,
     f_c, and the K* formula at every catalogue scale; compare with
     published values where they exist, else PREDICT (144, 160).
  E  F3 load-bearing half at 144/160: exact SAT scan — no
     admissible defector set of either class has minimum offset
     > M-1.  (Tiny SAT instances; sequential.)

Run: .venv/bin/python audit/a8_referee1/a8_dich_indep.py
Log: data/a8_dich_indep.log (caller tee).
"""
import json
import os
import sys
from itertools import combinations

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
DATA = os.path.join(BASE, 'data')

PUB = {  # published (alpha_E, alpha_O, f_O, f_E, K*) — notes/57 SS0.2/SS3
    48: (2, 2, 9, 9, 26), 64: (3, 2, 9, 8, 35), 80: (2, 2, 9, 9, 42),
    96: (2, 2, 8, 8, 51), 112: (3, 3, 8, 8, 60), 128: (3, 3, 8, 8, 68),
}


def blocks(M):
    return (list(range(M + 1, 2 * M + 1)),
            list(range(3 * M - 15, 4 * M + 1)),
            list(range(4 * M + 1, 6 * M + 16)))


def I_of(M, z):
    """Forced interval for a class-c defector z, full-class ownership."""
    c = z % 2
    lo, hi = 3 * M - 15, 4 * M
    out = []
    for u in range(M + 1, 2 * M + 1):
        if u % 2 != c:
            continue
        v = (u + z) // 2
        if lo <= v <= hi:
            out.append(v)
    return sorted(out)


def partA(M):
    m = M // 2
    bad = 0
    for z in range(4 * M + 1, 6 * M + 16):
        s = z - 4 * M
        c = z % 2
        iv = I_of(M, z)
        # consecutive integers
        assert iv == list(range(iv[0], iv[-1] + 1)), (M, z)
        ell = len(iv)
        ncl = sum(1 for v in iv if v % 2 == c)
        anch = iv[0] == 3 * M - 15
        assert anch == (s <= M - 31), (M, z, 'anchor')
        if s <= M - 31:
            assert ell == (s + 31) // 2 + (1 if c == 0 else 0), (M, z, ell)
        elif s <= 2 * M:
            assert ell == m, (M, z, ell)
        else:
            assert ell >= m - 8, (M, z, ell)
        assert ell >= 16 and ncl >= 8, (M, z, ell, ncl)
        if ncl == 8:
            assert (c == 1 and s in (1, 2 * M + 15)) or (c == 0 and s == 2), \
                (M, z, 'n=8 elsewhere')
    # A2: every 2-element same-class defector set has class mass >= 9
    for c in (0, 1):
        zs = [z for z in range(4 * M + 1, 6 * M + 16) if z % 2 == c]
        ivs = {z: set(I_of(M, z)) for z in zs}
        for z1, z2 in combinations(zs, 2):
            F = ivs[z1] | ivs[z2]
            assert sum(1 for v in F if v % 2 == c) >= 9, (M, c, z1, z2)
    print(f'A : M={M}: FI formulas + A2 pair mass OK (0 exceptions)',
          flush=True)


def partC(M):
    zo = [z for z in range(4 * M + 1, 6 * M + 16)
          if z % 2 == 1 and z - 4 * M <= M - 1]
    ze = [z for z in range(4 * M + 1, 6 * M + 16)
          if z % 2 == 0 and z - 4 * M <= M - 1]
    ivo = {z: set(I_of(M, z)) for z in zo}
    ive = {z: set(I_of(M, z)) for z in ze}
    nmin = None
    for a in zo:
        for b in ze:
            k = len(ivo[a] & ive[b])
            assert k >= 1, (M, a - 4 * M, b - 4 * M, 'H1 intersection FAILS')
            nmin = k if nmin is None else min(nmin, k)
    print(f'C : M={M}: H1 intersection exhaustive over '
          f'{len(zo)}x{len(ze)} minima pairs (s<=M-1): min overlap {nmin}',
          flush=True)


def load_cat(M):
    with open(os.path.join(DATA, f'e146_catalogue_M{M}.json')) as f:
        return json.load(f)


def fan_tables(M, cat):
    """Return (dead_pure per class, attacker->list of pure supports,
    purity counts)."""
    P0, P1, P2 = blocks(M)
    s0, s1, s2 = set(P0), set(P1), set(P2)
    dead_pure = {0: set(), 1: set()}
    pure_supps = {}
    all_supps = {}
    nsp = npure = 0
    for p in cat:
        if p['blk'] != 2:
            continue
        S = p['S']
        att = sorted(v for v in S if v in s1)
        supp = sorted(v for v in S if v in s2)
        assert len(att) == 2 and len(att) + len(supp) == len(S), (M, p)
        assert not any(v in s0 for v in S), (M, p, 'P0 value in pattern')
        assert supp, (M, p, 'empty support')
        key = tuple(att)
        all_supps.setdefault(key, []).append(supp)
        if att[0] % 2 == att[1] % 2:
            nsp += 1
            c = att[0] % 2
            if all(v % 2 == c for v in supp):
                npure += 1
                dead_pure[c].add(frozenset(att))
                pure_supps.setdefault(key, []).append(supp)
    return dead_pure, pure_supps, all_supps, nsp, npure


def max_no_dead(verts, dead):
    """Max subset of verts with no dead pair (exact DFS, small)."""
    verts = sorted(verts, reverse=True)
    best = [0]

    def rec(chosen, rest):
        if len(chosen) > best[0]:
            best[0] = len(chosen)
            best.append(list(chosen))
        while rest:
            v = rest.pop()
            if len(chosen) + len(rest) + 1 <= best[0]:
                return
            if all(frozenset((v, w)) not in dead for w in chosen):
                rec(chosen + [v], list(rest))

    rec([], list(verts))
    wit = best[-1] if len(best) > 1 else []
    return best[0], sorted(wit)


def self_serves(M, D, dead_pure, pure_supps):
    """Is defector set D (same class) pure-self-serving?"""
    c = next(iter(D)) % 2
    F = set()
    for z in D:
        F |= set(I_of(M, z))
    Fc = sorted(v for v in F if v % 2 == c)
    for pair in combinations(Fc, 2):
        if frozenset(pair) not in dead_pure[c]:
            continue
        for supp in pure_supps.get(tuple(sorted(pair)), []):
            if not set(supp) & D:
                return False, (pair, supp)
    return True, None


def partBD(M):
    m = M // 2
    P0, P1, P2 = blocks(M)
    cat = load_cat(M)
    dead_pure, pure_supps, all_supps, nsp, npure = fan_tables(M, cat)
    print(f'B : M={M}: {sum(1 for p in cat if p["blk"]==2)} blk-2 '
          f'patterns, shape OK; same-parity {nsp}, pure {npure} '
          f'{"(F0 TOTAL)" if nsp == npure else "(F0 FAILS!)"}', flush=True)
    assert nsp == npure, (M, 'F0 purity violated')
    res = {}
    for c, nm in ((0, 'E'), (1, 'O')):
        verts = [v for v in P1 if v % 2 == c and v >= 3 * M + 1]
        a, wit = max_no_dead(verts, dead_pure[c])
        res['alpha_' + nm] = a
        print(f'D : M={M}: alpha_{nm} = {a}  witness offs '
              f'{[v - 4 * M for v in wit]}', flush=True)
    for c, nm in ((1, 'O'), (0, 'E')):
        z0 = 4 * M + (1 if c else 2)
        ok, why = self_serves(M, {z0}, dead_pure, pure_supps)
        res['f_' + nm] = 8 if ok else 9
        if ok:
            print(f'D : M={M}: bottom {nm} singleton SELF-SERVES => '
                  f'f_{nm} = 8', flush=True)
        else:
            pair, supp = why
            print(f'D : M={M}: bottom {nm} singleton fails at pair offs '
                  f'({pair[0]-4*M},{pair[1]-4*M}) pure supp offs '
                  f'{[v-4*M for v in supp][:6]} => f_{nm} = 9', flush=True)
    kst = m + 9 + max(res['alpha_E'] - res['f_O'],
                      res['alpha_O'] - res['f_E'])
    if M in PUB:
        aE, aO, fO, fE, K = PUB[M]
        ok = (res['alpha_E'], res['alpha_O'], res['f_O'], res['f_E'],
              kst) == (aE, aO, fO, fE, K)
        print(f'D : M={M}: K* formula = {kst} vs published {K}  '
              f'[{"MATCH" if ok else "MISMATCH!"}]', flush=True)
        assert ok, (M, res, kst)
    else:
        print(f'D : M={M}: *** PREDICTION K*({M}) = {kst} ***  '
              f'(alpha_E={res["alpha_E"]}, alpha_O={res["alpha_O"]}, '
              f'f_O={res["f_O"]}, f_E={res["f_E"]})', flush=True)
    return dead_pure, pure_supps, kst


def partE(M, dead_pure, pure_supps):
    """F3 load-bearing half: no admissible defector set with minimum
    offset > M-1 (exact SAT per candidate minimum)."""
    from pysat.solvers import Cadical195
    P0, P1, P2 = blocks(M)
    Iv = {z: set(I_of(M, z)) for z in P2}
    for c, nm in ((1, 'O'), (0, 'E')):
        bad = []
        mins = [z for z in P2 if z % 2 == c and z - 4 * M > M - 1]
        for z0 in mins:
            zs = [z for z in P2 if z % 2 == c and z >= z0]
            dv = {z: i + 1 for i, z in enumerate(zs)}
            nv = len(zs)
            cls = [[dv[z0]]]
            ys = [y for y in P1 if y % 2 == c]
            yv = {}
            for y in ys:
                nv += 1
                yv[y] = nv
                owners = [dv[z] for z in zs if y in Iv[z]]
                for o in owners:
                    cls.append([-o, nv])
                cls.append([-nv] + owners)
            for pair in combinations(ys, 2):
                if frozenset(pair) not in dead_pure[c]:
                    continue
                for supp in pure_supps.get(tuple(sorted(pair)), []):
                    cls.append([-yv[pair[0]], -yv[pair[1]]]
                               + [dv[z] for z in supp if z in dv])
            with Cadical195(bootstrap_with=cls) as s:
                if s.solve():
                    bad.append(z0 - 4 * M)
        if bad:
            print(f'E : M={M}: {nm}: ADMISSIBLE MINIMA ABOVE M-1: {bad} '
                  f'— F3 load-bearing half FAILS', flush=True)
            sys.exit(1)
        print(f'E : M={M}: {nm}: no admissible minimum > M-1 '
              f'({len(mins)} candidates scanned)  OK', flush=True)


def main():
    for M in (144, 176):
        partA(M)
    for M in (48, 64, 80, 96, 112, 128, 144, 160, 176):
        partC(M)
    keep = {}
    for M in (48, 64, 80, 96, 112, 128, 144, 160):
        keep[M] = partBD(M)
    for M in (144, 160):
        dead_pure, pure_supps, _ = keep[M]
        partE(M, dead_pure, pure_supps)
    print('a8_dich_indep: ALL PARTS DONE', flush=True)


if __name__ == '__main__':
    main()
